FROM python:3.9-slim

WORKDIR /app

COPY service_fastapi_gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy gRPC stubs for classification + QA
COPY ../classification /app/classification
COPY ../question_answer /app/question_answer

# Copy main.py (FastAPI gateway)
COPY service_fastapi_gateway/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
