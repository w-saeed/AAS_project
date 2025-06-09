# Use official Python base image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y docker.io

# Set working directory inside container
WORKDIR /app

# Copy your code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run your app
CMD ["python", "main.py"]
