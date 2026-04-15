# morphik-core. Reasoning Log

## Initial Assessment

Morphik Core is a multimodal document processing and retrieval system. It ingests documents of many types (PDF, Word, Excel, PowerPoint, images, audio, video), extracts content using ColPali-style vision models and standard extractors, and stores embeddings in PostgreSQL with the pgvector extension. A FastAPI application serves retrieval queries. Background ingestion jobs run through an ARQ worker backed by Redis.

## What Was Checked

1. **README.md**: Describes Morphik as a document intelligence platform. Installation via the upstream Docker Compose file. Notes that a configuration TOML file controls model selection and API backend.

2. **Dockerfile (upstream)**: Multi-stage build. Stage 1 (builder) installs Rust (needed for a morphik-rust path dependency), installs uv, copies pyproject.toml and uv.lock, runs `uv sync`, and copies full source. Stage 2 (production) installs runtime system deps including LibreOffice, ffmpeg, poppler-utils, and copy the venv from the builder stage. The entrypoint script waits for PostgreSQL before starting the server.

3. **GHCR uv image reference**: The upstream Dockerfile included a `# syntax=docker/dockerfile:1.4` directive and a `FROM ghcr.io/astral-sh/uv AS uv-provider` stage. This syntax directive requires BuildKit's frontend feature, and the GHCR image pull fails when building in environments without authenticated GHCR access. The fix is to remove the syntax directive and install uv via pip in the builder stage.

4. **uv.lock CUDA conflict**: The upstream uv lock file was generated on a CUDA-capable machine and includes `torch` pinned to the CUDA variant. Running `uv sync` in a standard Docker build pulls the CUDA wheel (several GB, and can fail on pip-managed environments that do not have the CUDA runtime). Installing CPU-only torch first via `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu` before `uv sync` resolves this because the CPU torch is already satisfied when the lock file resolver runs.
The uv.lock was generated on a machine with a CUDA GPU so all the nvidia packages were baked in. Had to force CPU-only torch before running uv sync, otherwise it would try to download CUDA libraries that do not exist on the build machine.

5. **docker-compose.yml**: Four services: morphik (API), worker (ARQ), postgres (pgvector/pgvector:pg16), redis (redis:7-alpine). The API and worker share the same image with different CMD arguments. Both depend on postgres and redis being healthy before starting.

6. **morphik.docker.toml**: Default configuration file baked into the image. Can be overridden by mounting a custom `morphik.toml` at `/app/morphik.toml` at runtime.

7. **ARQ worker**: The worker service runs `arq core.workers.ingestion_worker.WorkerSettings`. It processes ingestion jobs queued by the API. Without the worker running, uploaded documents are queued but never processed.

## Decisions Made

### Removed GHCR uv image reference and syntax directive
The `# syntax=` directive activates BuildKit's Dockerfile frontend, which fetches an additional image from GHCR. In isolated or Windows-based Docker Desktop environments this causes authentication failures. Removing it and installing uv via pip is functionally equivalent and more portable.

### CPU-only PyTorch override
The research deployment does not require GPU acceleration. Installing CPU torch before the uv sync step prevents the multi-GB CUDA build from being pulled. This also keeps the image significantly smaller.

### Kept all four services as separate containers
The architectural fidelity rule prohibits merging services. The postgres, redis, API, and worker containers each serve a distinct role and the original developer designed them to run separately. Merging them would obscure the real attack surface for supply chain analysis.

### pgvector/pgvector:pg16 image
Standard PostgreSQL does not include the vector extension. The `pgvector/pgvector:pg16` image is required. This is the upstream choice and is kept as-is.

### entrypoint wait logic
The `docker-entrypoint.sh` baked into the image loops on `pg_isready` before starting the server. The `--skip-redis-check` argument is passed to `start_server.py` to defer the Redis connectivity check, allowing the server to start before Redis completes its own health cycle on slow machines.

## Testing

### Tests Performed
1. **Import check** (`python -c "import fastapi; print('ok')`): FastAPI imported successfully. Pass.
2. **Health endpoint** (GET `/health`): Returns status JSON after all four services are healthy. Pass.
3. **API docs** (GET `/docs`): Swagger UI loads. Pass.

### What Was Not Tested
- Document ingestion (requires a valid LLM API key for embedding generation).
- Retrieval queries (requires ingested documents).
- Office document conversion via LibreOffice.
- Audio and video ingestion via ffmpeg.

## Gotchas

1. **GHCR image pull for uv**: The upstream syntax directive and GHCR FROM line require authenticated access to GitHub Container Registry. On Windows Docker Desktop in an SSH or CI context this fails silently or with credential errors. Installing uv via pip avoids the external registry dependency entirely.

2. **CUDA lock file**: The uv lock file was created with CUDA torch pinned. A plain `uv sync` in a CPU-only Docker build will attempt to download CUDA wheels. Pre-installing CPU torch before uv sync prevents this.

3. **JWT and session keys are required at startup**: The API module loads configuration at import time and validates that JWT_SECRET_KEY and SESSION_SECRET_KEY are non-empty strings. Containers with empty values crash immediately on startup with a configuration validation error.

4. **Worker must run alongside API**: The API only enqueues ingestion jobs. If the ARQ worker is not running, uploaded documents sit in the Redis queue indefinitely and never appear in the document list. Both services must be started together.

5. **pgvector extension**: The standard postgres image does not have pgvector. Using `pgvector/pgvector:pg16` is mandatory. Substituting `postgres:16` will cause vector extension creation to fail at startup.
