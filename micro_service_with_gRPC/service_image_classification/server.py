import grpc
from concurrent import futures
import classification.classification_pb2 as pb2
import classification.classification_pb2_grpc as pb2_grpc
import tensorflow as tf
import numpy as np

# For demonstration, use MobileNetV2 pretrained on ImageNet
MODEL = tf.keras.applications.mobilenet_v2.MobileNetV2(weights="imagenet")


# Load ImageNet labels
class_labels_url = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
class_labels_path = tf.keras.utils.get_file("ImageNetLabels.txt", class_labels_url)
with open(class_labels_path, "r") as f:
    # The first label is 'background', so skip for direct indexing
    IMAGENET_LABELS = [line.strip() for line in f.readlines()][1:]


def preprocess_image(image_data: bytes):
    img = tf.image.decode_jpeg(image_data, channels=3)
    img = tf.image.resize(img, [224, 224])
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return np.expand_dims(img, axis=0)



class ImageClassificationService(pb2_grpc.ImageClassificationServiceServicer):
    def Predict(self, request, context):
        image_data = request.image_data
        input_tensor = preprocess_image(image_data)
        preds = MODEL.predict(input_tensor)
        top_indices = preds[0].argsort()[-5:][::-1]  # top 5 predictions

        response = pb2.ImageResponse()
        for idx in top_indices:
            prediction = pb2.Prediction(
                class_name=IMAGENET_LABELS[idx],
                confidence=float(preds[0][idx])
            )
            response.predictions.append(prediction)
        return response
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb2_grpc.add_ImageClassificationServiceServicer_to_server(
        ImageClassificationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Image Classification Service running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()