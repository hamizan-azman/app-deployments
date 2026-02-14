# localGPT -- Usage Documentation

## Overview
Local RAG (Retrieval-Augmented Generation) system with document indexing, chat, and session management. Next.js frontend, Python backend with session/index management, Python RAG API with agentic retrieval pipeline. Uses Ollama for local LLM inference.

## Quick Start
```bash
cd apps/localGPT
docker compose --profile with-ollama up --build -d
# Pull a model into Ollama
docker exec rag-ollama ollama pull qwen2.5:0.5b
```

## Docker Pull (pre-built)
```bash
docker pull hoomzoom/localgpt-frontend:latest
docker pull hoomzoom/localgpt-backend:latest
docker pull hoomzoom/localgpt-rag-api:latest
```

## Architecture
| Service | Image | Port | Description |
|---------|-------|------|-------------|
| rag-frontend | localgpt-frontend | 3000 | Next.js chat UI |
| rag-backend | localgpt-backend | 8000 | Session/index management, direct LLM chat |
| rag-api | localgpt-rag-api | 8001 | Agentic RAG pipeline, document indexing |
| rag-ollama | ollama/ollama | 11434 | Local LLM inference (optional profile) |

## Base URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- RAG API: http://localhost:8001
- Ollama: http://localhost:11434

## API Endpoints -- Backend (port 8000)

### Health Check
- **URL:** `/health`
- **Method:** GET
- **Response:** `{"status":"ok","ollama_running":true,"available_models":["qwen2.5:0.5b"],"database_stats":{...}}`
- **Tested:** Yes

### List Sessions
- **URL:** `/sessions`
- **Method:** GET
- **Response:** `{"sessions":[...],"total":0}`
- **Tested:** Yes

### Create Session
- **URL:** `/sessions`
- **Method:** POST
- **Request:** `curl -X POST http://localhost:8000/sessions -H "Content-Type: application/json" -d '{"model":"qwen2.5:0.5b"}'`
- **Response:** `{"session":{"id":"uuid","title":"New Chat",...},"session_id":"uuid"}`
- **Tested:** Yes

### Session Chat
- **URL:** `/sessions/{id}/messages`
- **Method:** POST
- **Request:** `curl -X POST http://localhost:8000/sessions/{id}/messages -H "Content-Type: application/json" -d '{"message":"hello"}'`
- **Response:** `{"response":"...","session":{...},"source_documents":[],"used_rag":false}`
- **Tested:** Yes (requires matching model pulled in Ollama)

### Legacy Chat
- **URL:** `/chat`
- **Method:** POST
- **Request:** `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"hello","model":"qwen2.5:0.5b"}'`
- **Tested:** Yes (model must support thinking mode, or use qwen3 series)

### Models
- **URL:** `/models`
- **Method:** GET
- **Response:** `{"generation_models":["qwen2.5:0.5b"],"embedding_models":["Qwen/Qwen3-Embedding-0.6B",...]}`
- **Tested:** Yes

### Indexes
- **URL:** `/indexes`
- **Method:** GET
- **Response:** `{"indexes":[],"total":0}`
- **Tested:** Yes

### File Upload
- **URL:** `/sessions/{id}/upload`
- **Method:** POST (multipart/form-data, field: "files")
- **Tested:** No

### Index Documents
- **URL:** `/sessions/{id}/index`
- **Method:** POST
- **Tested:** No

### Delete Session
- **URL:** `/sessions/{id}`
- **Method:** DELETE
- **Tested:** No

## API Endpoints -- RAG API (port 8001)

### Models
- **URL:** `/models`
- **Method:** GET
- **Response:** `{"generation_models":["qwen2.5:0.5b"],"embedding_models":[...]}`
- **Tested:** Yes

### Chat (RAG)
- **URL:** `/chat`
- **Method:** POST
- **Request:** `curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"query":"What is X?","model":"qwen2.5:0.5b"}'`
- **Response:** `{"answer":"...","source_documents":[...]}`
- **Tested:** Yes

### Chat Stream (SSE)
- **URL:** `/chat/stream`
- **Method:** POST
- **Description:** Server-Sent Events streaming for real-time chat
- **Tested:** No

### Index Documents
- **URL:** `/index`
- **Method:** POST
- **Request:** `curl -X POST http://localhost:8001/index -H "Content-Type: application/json" -d '{"file_paths":["/path/to/doc.pdf"]}'`
- **Tested:** No

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| RAG_CONFIG_MODE | No | default | RAG agent mode (default, fast, react) |
| OLLAMA_HOST | No | http://ollama:11434 | Ollama server URL |

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Frontend (port 3000) | PASS (200 OK) |
| 2 | Backend /health | PASS |
| 3 | Backend /sessions GET | PASS |
| 4 | Backend /sessions POST | PASS |
| 5 | Backend /chat POST | PASS (endpoint works, model-dependent) |
| 6 | Backend /sessions/{id}/messages POST | PASS (endpoint works, model-dependent) |
| 7 | Backend /models | PASS |
| 8 | Backend /indexes | PASS |
| 9 | RAG API /models | PASS |
| 10 | RAG API /chat | PASS |

## Notes
- Ollama runs in a Docker container (profile "with-ollama"). Pull models after startup: `docker exec rag-ollama ollama pull MODEL`.
- Default chat model is qwen3:8b. If only a smaller model is pulled (e.g. qwen2.5:0.5b), session chat will error with "model not found".
- The OllamaClient enables "thinking" mode by default. Models that don't support it (qwen2.5) return errors via chat. Use qwen3 series models for full compatibility.
- RAG API image is ~10.7GB (includes ML dependencies for embeddings, reranking, etc.).
- Backend image is ~3.4GB. Frontend image is ~1.5GB. Ollama is ~9GB.
- Database is SQLite (local file), no external DB needed.
- Document upload and indexing require Ollama models for embedding and enrichment.
