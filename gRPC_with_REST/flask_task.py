from flask import Flask, jsonify, request
import grpc
import bookstore_pb2
import bookstore_pb2_grpc

app = Flask(__name__)

def get_grpc_stub():
    """Connects to gRPC BookService"""
    channel = grpc.insecure_channel("localhost:50051")
    return bookstore_pb2_grpc.BookServiceStub(channel)

@app.route("/books", methods=["GET"])
def get_books():
    stub = get_grpc_stub()
    response = stub.GetBooks(bookstore_pb2.Empty())
    books = [{"id": b.id, "title": b.title, "author": b.author} for b in response.books]
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    stub = get_grpc_stub()
    response = stub.GetBookById(bookstore_pb2.BookRequest(id=book_id))
    if response.id == 0:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": response.id, "title": response.title, "author": response.author})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
