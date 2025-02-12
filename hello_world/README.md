### Generate gRPC code
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. books.proto
```

### Run gRPC server and client
```bash
pipenv run python gRPC_server.py
pipenv run python gRPC_client.py

```

### Test with Postman
1. Open Postman.
2. Click New Request → Select gRPC.
3. Enter the gRPC server address (localhost:50051).
4. Import Book.proto
5. Select methods and Invoke