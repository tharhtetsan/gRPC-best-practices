FROM python:3.9-slim

WORKDIR /app

COPY service_question_answer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the question_answer stubs
COPY ../question_answer /app/question_answer

# Copy the server code
COPY service_question_answer/server.py .

EXPOSE 50052

CMD ["python", "server.py"]
