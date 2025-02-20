```bash
python -m grpc_tools.protoc \
    --proto_path=. \
    --python_out=. \
    --grpc_python_out=. \
    classification.proto


```

```bash
cd classification
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. classification.proto
cd ../question_answer
python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. question_answer.proto
cd ..

```