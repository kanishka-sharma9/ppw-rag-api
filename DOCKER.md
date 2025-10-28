# Docker Deployment Guide

## Quick Start

### 1. Set up environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 2. Build the FAISS index (first time only)
```bash
docker-compose --profile setup run --rm indexing
```

### 3. Start the API service
```bash
docker-compose up -d api
```

The API will be available at `http://localhost:8000`

### 4. View API documentation
Open `http://localhost:8000/docs` in your browser to see the FastAPI Swagger UI.

## Available Services

### API Service (default)
```bash
# Start the API
docker-compose up -d api

# View logs
docker-compose logs -f api

# Stop the API
docker-compose down
```

### CLI Interface
```bash
# Run the CLI tool interactively
docker-compose --profile cli run --rm cli
```

### Rebuild Index
```bash
# Rebuild the FAISS index when templates change
docker-compose --profile setup run --rm indexing
```

## Building from Scratch

```bash
# Build the Docker image
docker-compose build

# Or build directly with Docker
docker build -t ppw-rag .
```

## Volume Mounts

- `./embeddings` - Shared between indexing and API services for FAISS index storage
- `./templates.py` - Mounted read-only in indexing service

## Troubleshooting

### Index not found error
Make sure you've run the indexing service first:
```bash
docker-compose --profile setup run --rm indexing
```

### API key errors
Check that your `.env` file exists and contains a valid `OPENAI_API_KEY`.

### Port conflicts
If port 8000 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Use 8080 instead
```

## Production Considerations

1. **API Keys**: Use Docker secrets or a proper secrets management system
2. **Scaling**: Use `docker-compose up --scale api=3` to run multiple API instances
3. **Reverse Proxy**: Put nginx or traefik in front of the API service
4. **Health Checks**: The API service includes health checks for monitoring
