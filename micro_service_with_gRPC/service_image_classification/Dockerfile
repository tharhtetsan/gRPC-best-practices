FROM python:3.9-slim

WORKDIR /app

COPY service_image_classification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy classification stubs
COPY ./classification/ /app/classification



# Copy the server code
COPY service_image_classification/server.py .

EXPOSE 50051

CMD ["python", "server.py"]
