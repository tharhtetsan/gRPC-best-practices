import grpc
import books_pb2
import books_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = books_pb2_grpc.BookServiceStub(channel)

    response = stub.GetBooks(books_pb2.Empty())
    for book in response.books:
        print(f"{book.id}: {book.title} by {book.author}")

if __name__ == "__main__":
    run()
