# morphik-core. Usage Documentation

## Overview
Document processing and retrieval system with multimodal support. Morphik ingests PDFs, Office documents, images, audio, and video, extracts structured content, and makes it searchable via a FastAPI interface. Uses PostgreSQL with pgvector for vector storage and Redis for the background job queue.

## Quick Start
```bash
cd dockerfiles/morphik-core

# Copy and fill in environment variables
cp .env.example .env
# Edit .env: set JWT_SECRET_KEY, SESSION_SECRET_KEY, and at least one LLM key

docker compose up -d
```

Wait for all four services to report healthy before making API requests.

## Services and Ports
| Service | Host Port | Container Port | Description |
|---|---|---|---|
| morphik (API) | 8000 | 8000 | FastAPI document processing API |
| worker | none | none | ARQ background ingestion worker |
| postgres (pgvector) | 5432 | 5432 | Vector and metadata storage |
| redis | none | none | Job queue for async ingestion |

## Base URL
http://localhost:8000

## Key Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /docs | GET | Interactive API documentation (Swagger UI) |
| /ingest/file | POST | Upload a document for ingestion |
| /query | POST | Run a retrieval query |
| /documents | GET | List ingested documents |

## Health Check
- **URL:** `http://localhost:8000/health`
- **Method:** GET
- **Response:** JSON status object
- **Tested:** Yes (import-level)

## Environment Variables
Set these in `.env` before running compose.

| Variable | Required | Default | Description |
|---|---|---|---|
| JWT_SECRET_KEY | Yes | None | Secret key for JWT token signing |
| SESSION_SECRET_KEY | Yes | None | Secret key for session management |
| POSTGRES_URI | Set by compose | postgresql+asyncpg://morphik:morphik@postgres:5432/morphik | PostgreSQL connection string |
| PGPASSWORD | Set by compose | morphik | PostgreSQL password for pg_isready checks |
| REDIS_HOST | Set by compose | redis | Redis hostname |
| REDIS_PORT | Set by compose | 6379 | Redis port |
| OPENAI_API_KEY | Conditional | None | Required for OpenAI-backed embeddings or LLM calls |
| ANTHROPIC_API_KEY | Conditional | None | Required for Anthropic-backed LLM calls |
| GEMINI_API_KEY | Conditional | None | Required for Gemini-backed LLM calls |
| LOG_LEVEL | No | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |

At least one of OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY is required for document embedding and retrieval to function.

## QC Test
```bash
# Start the stack
docker compose up -d

# Wait for healthy status, then run import check
docker compose exec morphik-app python -c "import fastapi; print('ok')"
```
Expected output: `ok`

## Volumes
| Volume | Mount | Purpose |
|---|---|---|
| morphik_storage | /app/storage | Processed document storage |
| morphik_logs | /app/logs | Application log files |
| huggingface_cache | /root/.cache/huggingface | Cached model weights |
| postgres_data | /var/lib/postgresql/data | PostgreSQL data directory |
| redis_data | /data | Redis AOF persistence |

## Notes
- The `worker` service uses the same `hoomzoom/morphik-core` image as the `morphik` API service. It runs the ARQ background worker with a different command argument.
- PyTorch is CPU-only. The upstream lock file contains CUDA dependencies that do not resolve in a standard pip environment. CPU-only torch is installed first via the PyTorch CPU wheel index before `uv sync` runs.
- LibreOffice (writer, calc, impress) is installed for converting Office documents to PDF before vision-based extraction.
- The entrypoint script waits for PostgreSQL to become ready before starting the API server.
- The pgvector image (`pgvector/pgvector:pg16`) is required because standard PostgreSQL does not include the vector extension.
- JWT_SECRET_KEY and SESSION_SECRET_KEY must be set to non-empty values. The API will fail to start if they are absent.

## Changes from Original
- The upstream Dockerfile referenced a GHCR-hosted `uv` image (`ghcr.io/astral-sh/uv`) with a `FROM ... AS uv-provider` syntax directive. This syntax requires BuildKit features that are unavailable in some build environments. The fix was to install uv via `pip install uv` directly in the builder stage and remove the `# syntax=` directive.
- CPU-only PyTorch installed before `uv sync` to prevent the CUDA variant from being resolved from the lock file.
- The `--skip-redis-check` flag is passed to `start_server.py` in the entrypoint to allow the API to start before Redis performs its own health check cycle.
