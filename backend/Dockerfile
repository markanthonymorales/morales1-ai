# backend/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ../requirements.txt .
RUN pip install python-multipart --no-cache-dir -r requirements.txt

# Copy backend source code
COPY ../backend/app ./app

# Copy frontend static files
COPY ../frontend ./frontend

# Set working directory for the app
WORKDIR /app/app

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
