Public REST API + Internal gRPC Microservices
In a real-world scenario, you may want to expose a public-facing REST API while using gRPC for internal microservices communication.

Use Case: Bookstore API
A Public REST API allows external clients (browsers, mobile apps) to interact with the system.
Internal gRPC-based Microservices handle high-performance data exchange.





#### Generate gRPC code
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bookstore.proto

```