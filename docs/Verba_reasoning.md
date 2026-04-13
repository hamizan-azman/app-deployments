# Verba. Reasoning Log

## Initial Assessment

Verba is a RAG application that wraps Weaviate with a user-friendly interface. The upstream repo includes a well-structured Dockerfile. The main deployment decision was whether to bundle Weaviate or require it as an external dependency. The upstream design requires external Weaviate, which we preserve.

## What Was Checked

1. **README.md**: Describes Verba as "The Golden RAGtriever." Documents deployment via Docker and docker-compose. Shows WEAVIATE_URL_VERBA as the primary required environment variable.

2. **Dockerfile**: Uses `python:3.11-slim`. Installs `wget` as a system dependency. Installs Verba via `pip install '.'`. Creates non-root user. Exposes port 8000. Healthcheck uses Python urllib against `/api/health`. CMD is `verba start --port 8000 --host 0.0.0.0`.

3. **pyproject.toml**: Verba is packaged as a Python package. The `verba` console script is the entry point. Multiple extras are available for different embedding providers.

4. **API structure**: FastAPI application. The `/api/health` endpoint returns 200 without requiring a database connection, making it a reliable healthcheck target.

## Decisions Made

### Used the existing Dockerfile as-is
The upstream Dockerfile is well-constructed. It uses the correct base image, creates a non-root user, and has a working healthcheck. No modifications were needed.

### Require external Weaviate
Verba is explicitly designed to connect to an external Weaviate instance. The architectural fidelity rule prohibits bundling Weaviate into the Verba container. A compose example is documented for researchers who want to run both together.

### Port 8000
The upstream default port. The FastAPI app binds to 0.0.0.0:8000.

### wget system dependency
The upstream Dockerfile installs wget. While the healthcheck uses Python urllib (not wget), wget may be used by other internal scripts or future healthcheck variants. Keeping it matches the upstream Dockerfile exactly.

## Testing

### Tests Performed
1. **Health check** (GET `http://localhost:8000/api/health`): Returns HTTP 200 even without a Weaviate connection. Pass.
2. **API docs** (GET `http://localhost:8000/docs`): Swagger UI loads. Pass.
3. **Main page** (GET `http://localhost:8000`): Returns HTTP 200. Application loads. Pass.

### What Was Not Tested
- Document ingestion (requires Weaviate instance and LLM API key)
- Vector search
- Question answering
- Weaviate Cloud connection (requires cloud credentials)

## Gotchas

1. **Weaviate required**: Without WEAVIATE_URL_VERBA, the application starts but all data operations fail. The health endpoint returns 200 regardless, so a healthy container does not imply Weaviate is connected.

2. **No bundled Weaviate**: Unlike some RAG apps that bundle their vector database, Verba deliberately externalizes Weaviate. This is intentional design, not a limitation.

3. **wget installed but not needed for healthcheck**: The upstream Dockerfile installs wget as a build dependency. The Python urllib approach in the healthcheck is sufficient and avoids curl/wget version issues.
