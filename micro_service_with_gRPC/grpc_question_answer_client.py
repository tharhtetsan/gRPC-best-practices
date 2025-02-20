import grpc
import question_answer.question_answer_pb2 as pb2
import question_answer.question_answer_pb2_grpc as pb2_grpc

# Connect to the gRPC server at localhost:50052
channel = grpc.insecure_channel("localhost:50052")
stub = pb2_grpc.QuestionAnswerServiceStub(channel)

# Define the request
request = pb2.QARequest(
    context="Albert Einstein was a German-born theoretical physicist who developed the theory of relativity. He was born in 1879 in Germany and later moved to the United States.",
    question="Who developed the theory of relativity?"
)

# Send the request
response = stub.Predict(request)

# Print the response
print(f"Answer: {response.answer}")
print(f"Score: {response.score}")
print(f"Start: {response.start}, End: {response.end}")
