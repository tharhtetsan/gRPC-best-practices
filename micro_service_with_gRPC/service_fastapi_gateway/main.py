from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import uvicorn
import grpc

# Image classification stubs
import classification.classification_pb2 as class_pb2
import classification.classification_pb2_grpc as class_pb2_grpc

# Question answering stubs
import question_answer.question_answer_pb2 as qa_pb2
import question_answer.question_answer_pb2_grpc as qa_pb2_grpc

app = FastAPI(title="ML Gateway", version="1.0.0")

# ================
# 1) Image Classification Endpoint
# ================
@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    # Read the image bytes
    image_data = await file.read()

    # Connect to the Image Classification gRPC service
    with grpc.insecure_channel("service_image_classification:50051") as channel:
        stub = class_pb2_grpc.ImageClassificationServiceStub(channel)
        request = class_pb2.ImageRequest(image_data=image_data)
        response = stub.Predict(request)

    # Return the top predictions
    predictions = [
        {"class_name": p.class_name, "confidence": p.confidence}
        for p in response.predictions
    ]
    return {"predictions": predictions}


# ================
# 2) Question Answering Endpoint
# ================
class QARequest(BaseModel):
    context: str
    question: str

@app.post("/question-answer")
async def question_answer(payload: QARequest):
    # Connect to the QA gRPC service
    with grpc.insecure_channel("service_question_answer:50052") as channel:
        stub = qa_pb2_grpc.QuestionAnswerServiceStub(channel)
        request = qa_pb2.QARequest(
            context=payload.context,
            question=payload.question
        )
        response = stub.Predict(request)
    return {
        "answer": response.answer,
        "score": response.score,
        "start": response.start,
        "end": response.end
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Gateway. Use /docs for API docs."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
