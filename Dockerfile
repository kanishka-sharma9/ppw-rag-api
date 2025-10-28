# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn[standard]

# Copy application code
COPY . .

# Create embeddings and logs directories
RUN mkdir -p embeddings logs

# Expose port for FastAPI
EXPOSE 8000

# Default command runs the API server
# To run indexing, override with: docker run <image> python indexing.py
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
