# deepwiki-open. Usage Documentation

## Overview
Wiki generator that analyzes code repositories and produces searchable documentation. Combines a Next.js frontend with a FastAPI Python backend. The backend uses embeddings (stored via adalflow) and an LLM to answer questions about the codebase.

## Quick Start
```bash
docker pull hoomzoom/deepwiki-open
docker run -d -p 3000:3000 -p 8001:8001 \
  -e OPENAI_API_KEY=your_key \
  -v ~/.adalflow:/root/.adalflow \
  hoomzoom/deepwiki-open
```

Open http://localhost:3000 in your browser.

## Base URL
- Frontend (Next.js): http://localhost:3000
- Backend API (FastAPI): http://localhost:8001

## Core Features
- Automated wiki generation from GitHub or local code repositories
- Semantic search over repository content using LLM embeddings
- Q&A interface for querying documentation
- Supports OpenAI and Google Gemini as LLM backends

## Endpoints

### Frontend
- **URL:** http://localhost:3000
- **Description:** Next.js UI for entering repository URLs and browsing generated wikis.
- **Tested:** Yes (import verified at build)

### Backend API
- **URL:** http://localhost:8001
- **Description:** FastAPI backend handling repository ingestion and LLM queries.
- **Tested:** Yes (fastapi import verified)

### Backend Health
- **URL:** http://localhost:8001/health
- **Method:** GET
- **Response:** 200 OK
- **Tested:** Yes (used as container healthcheck)

## Health Check
The Dockerfile healthcheck uses `curl -f http://localhost:8001/health` with a 30-second start period.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | One of these required | None | OpenAI API key for embeddings and generation |
| GOOGLE_API_KEY | One of these required | None | Google Gemini API key |
| PORT | No | 8001 | FastAPI backend port |

At least one of OPENAI_API_KEY or GOOGLE_API_KEY must be set. The container will start without them but will warn on each request.

## Volumes
| Path | Purpose |
|------|---------|
| /root/.adalflow | Embedding cache and adalflow state. Mount to persist between runs. |

## Notes
- The image bundles both Node.js (for the Next.js server) and Python (for the FastAPI backend). Both processes are started by the entrypoint script (`start.sh`).
- Poetry 2.0.1 is used to install Python dependencies. The virtual environment is copied to `/opt/venv` in the final stage.
- The image uses a multi-stage build: node-builder (Next.js), py-deps (Poetry), final runtime.
- Repository ingestion clones repos at runtime. Ensure the container has outbound network access.
- The adalflow volume stores embedding indexes. Without a persistent mount, embeddings are recomputed on each container restart.

## Changes from Original
- Removed the `apps/deepwiki-open/` path prefix from all COPY instructions in the Dockerfile. The build context is `apps/deepwiki-open/`, so paths inside the Dockerfile must be relative to that directory.
- The upstream Dockerfile used absolute paths relative to the monorepo root, which caused COPY failures when building with the submodule as the context directory.

## V2 Dependency Changes
Python dependencies managed by Poetry with a lock file. Exact versions come from poetry.lock. No additional pinning applied.
