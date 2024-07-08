# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the default command to run when the container starts
CMD ["python", "api.py"]
