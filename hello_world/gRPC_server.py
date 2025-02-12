import grpc
from concurrent import futures
import books_pb2
import books_pb2_grpc


class BookService(books_pb2_grpc.BookServiceServicer):
    def __init__(self):
        self.books = [
            books_pb2.Book(id=1, title="1984", author="George Orwell"),
            books_pb2.Book(id=2, title="Brave New World", author="Aldous Huxley"),
        ]

    def GetBooks(self, request, context):
        return books_pb2.BookList(books=self.books)

    def GetBookById(self, request, context):
        book = next((b for b in self.books if b.id == request.id), None)
        return book if book else books_pb2.Book(id=0, title="", author="")

    def AddBook(self, request, context):
        self.books.append(request)
        return request
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()