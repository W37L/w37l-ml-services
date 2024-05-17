# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y gcc

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Expose the port FastAPI is running on
EXPOSE 8000

# Start the FastAPI server using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]