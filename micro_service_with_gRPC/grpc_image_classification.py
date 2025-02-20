import grpc
import classification.classification_pb2 as pb2
import classification.classification_pb2_grpc as pb2_grpc

# Load image as bytes
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

# Connect to the gRPC server at localhost:50051
channel = grpc.insecure_channel("localhost:50051")
stub = pb2_grpc.ImageClassificationServiceStub(channel)

# Read and send an image
image_path = "test_img.png" 
image_data = load_image(image_path)

# Create request
request = pb2.ImageRequest(image_data=image_data)

# Send request and receive response
response = stub.Predict(request)

# Print predictions
for prediction in response.predictions:
    print(f"Class: {prediction.class_name}, Confidence: {prediction.confidence:.4f}")
