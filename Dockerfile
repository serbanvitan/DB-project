# Use the official Python image as a base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app to the working directory in the container
COPY src/ /app/

# Set environment variable for Google credentials (pointing to the copied file)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-file.json"

# Command to run the app
CMD ["python", "apigee_manager.py"]
