# Use a slim base image to reduce image size
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ .

# Expose the FastAPI port
EXPOSE 8000


#default command if no command is provided in docker run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]