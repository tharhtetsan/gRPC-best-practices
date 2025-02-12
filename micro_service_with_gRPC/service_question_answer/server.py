import grpc
from concurrent import futures
import question_answer.question_answer_pb2 as pb2
import question_answer.question_answer_pb2_grpc as pb2_grpc

from transformers import pipeline

# Load a QA pipeline with TensorFlow (distilbert variant)
qa_pipeline = pipeline(
    task="question-answering",
    model="distilbert-base-cased-distilled-squad",
    framework="tf"
)



class QuestionAnswerService(pb2_grpc.QuestionAnswerServiceServicer):
    def Predict(self, request, context):
        # request has 'context' and 'question'
        inputs = {
            "context": request.context,
            "question": request.question
        }
        result = qa_pipeline(inputs)  
        # result example: {'score': 0.97, 'start': 12, 'end': 20, 'answer': 'some answer'}

        response = pb2.QAResponse(
            answer=result["answer"],
            score=float(result["score"]),
            start=int(result["start"]),
            end=int(result["end"]),
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb2_grpc.add_QuestionAnswerServiceServicer_to_server(
        QuestionAnswerService(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Question Answering Service running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()