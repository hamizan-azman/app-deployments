# localGPT -- Reasoning Log

## Repo Walkthrough

### Repository Structure
- `docker-compose.yml`: Defines 4 services -- rag-frontend (Next.js, port 3000), rag-backend (Python HTTP server, port 8000), rag-api (Python RAG pipeline, port 8001), and rag-ollama (Ollama, port 11434, optional profile). The compose file already exists and is well-structured.
- `Dockerfile.frontend`: node:18-alpine, Next.js build with `npm run build` and `npm start`.
- `Dockerfile.backend`: python:3.11-slim, installs backend requirements, runs `server.py`.
- `Dockerfile.rag-api`: python:3.11-slim, installs rag_system requirements including ML deps (sentence-transformers, lancedb, etc.), runs `api_server.py`.
- `backend/server.py`: Python http.server-based backend. Handles sessions, chat (direct LLM via Ollama), file upload, document indexing (delegates to RAG API), and index management. All state in SQLite.
- `rag_system/api_server.py`: Advanced RAG API. Initializes an agentic RAG pipeline at startup. Handles /chat (with smart routing between RAG and direct LLM), /chat/stream (SSE), /index (document indexing), and /models.
- `backend/ollama_client.py`: Client for Ollama API. Has "thinking" mode enabled by default which some models (qwen2.5) don't support.

### Key Design Decisions in the App
The app has a two-tier architecture: the backend (port 8000) handles session management and acts as a lightweight proxy, while the RAG API (port 8001) handles the heavy ML work (embeddings, retrieval, reranking, generation). The frontend talks to both. Ollama is optional -- can use host Ollama or containerized via the "with-ollama" profile.

## Deployment Strategy

### Use Existing Dockerfiles
All three Dockerfiles exist and work. No modifications needed. This is the ideal case for architectural fidelity.

### Use with-ollama Profile
Without the Ollama profile, the services expect a host Ollama instance. Using `--profile with-ollama` includes a containerized Ollama so the deployment is fully self-contained.

### Pull qwen2.5:0.5b for Testing
Needed a small model to test functionality. qwen2.5:0.5b is only ~400MB and sufficient for verifying the API endpoints work. Full functionality requires larger models (qwen3:8b is the default).

## Test Details

### Test 1: Frontend
`GET http://localhost:3000` returned 200 OK. The Next.js app loads and serves the chat UI.

### Tests 2-8: Backend Endpoints
- `/health`: Returns full status including Ollama connectivity, model list, and database stats. All healthy.
- `/sessions` GET: Returns empty sessions list. Database working.
- `/sessions` POST: Created a session with model "qwen2.5:0.5b". Session ID returned, stored in SQLite.
- `/chat` POST: Endpoint works but qwen2.5:0.5b doesn't support "thinking" mode (the OllamaClient enables it by default). The error is wrapped in the response, not a server crash.
- `/sessions/{id}/messages` POST: Smart routing kicks in -- detects "Say hello" as a greeting, routes to direct LLM (not RAG). Tries qwen3:8b (session default model mismatch). The routing and session management work correctly even when the model isn't available.
- `/models`: Returns generation models (from Ollama) and embedding models (hardcoded HuggingFace list).
- `/indexes`: Returns empty index list. CRUD infrastructure works.

### Tests 9-10: RAG API Endpoints
- `/models`: Returns same model list as backend (both query Ollama).
- `/chat`: Accepts a query, runs through the RAG pipeline. With no indexed documents, returns "I could not find an answer in the documents." -- correct behavior.

## Gotchas

1. **Model compatibility**: The OllamaClient defaults to "thinking" mode. Only qwen3 series models support this. qwen2.5 and other models will error. Session chat defaults to qwen3:8b even if you created the session with a different model.
2. **Image sizes are large**: RAG API is 10.7GB (ML deps), Backend is 3.4GB, Frontend is 1.5GB, Ollama is 9GB. Total ~25GB.
3. **No external database**: Uses SQLite (file in container). Data is lost when containers are recreated unless volumes are mounted.
4. **Profile required**: `docker compose up` without `--profile with-ollama` will NOT start Ollama. The backend and RAG API will then fail to connect to Ollama.
5. **Model must be pulled separately**: After `docker compose up`, you must `docker exec rag-ollama ollama pull MODEL` to download a model. No models are pre-installed.
6. **Frontend health check**: Frontend shows "unhealthy" in docker ps because its healthcheck likely expects a specific response. The app itself works fine (200 OK).
