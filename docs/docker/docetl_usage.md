# docetl. Usage Documentation

## Overview
Document ETL pipeline tool with a FastAPI backend and Next.js frontend. Processes large document collections using LLM-powered operations such as extraction, transformation, and summarization. Configured via a YAML pipeline definition.

## Quick Start
```bash
docker pull hoomzoom/docetl
docker run -d -p 3000:3000 -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data:/docetl-data \
  hoomzoom/docetl
```

Open http://localhost:3000 in your browser.

## Base URL
- Frontend (Next.js): http://localhost:3000
- Backend API (FastAPI): http://localhost:8000

## Core Features
- LLM-powered document extraction, transformation, and aggregation
- YAML-based pipeline configuration
- Next.js UI for building and monitoring pipelines
- FastAPI backend for executing pipeline operations
- Pluggable output format support

## Endpoints

### Frontend
- **URL:** http://localhost:3000
- **Description:** Next.js interface for designing and running ETL pipelines.
- **Tested:** Yes (import verified at build)

### Backend API
- **URL:** http://localhost:8000
- **Description:** FastAPI backend handling pipeline execution and document processing.
- **Tested:** Yes (fastapi import verified)

### Backend Health
- **URL:** http://localhost:8000/health
- **Method:** GET
- **Response:** 200 OK
- **Tested:** Yes (used as container healthcheck)

### Backend Docs
- **URL:** http://localhost:8000/docs
- **Description:** FastAPI interactive API documentation.
- **Tested:** Not tested separately

## Health Check
The Dockerfile healthcheck uses `curl -f http://localhost:8000/health` with a 40-second start period.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for LLM operations |
| DOCETL_HOME_DIR | No | /docetl-data | Directory for pipeline data and outputs |

## Volumes
| Path | Purpose |
|------|---------|
| /docetl-data | Input documents, output files, and pipeline state. Declared as a VOLUME in the Dockerfile. |

## Notes
- The image bundles Node.js 20 and Python 3.11. Both the FastAPI server and Next.js server start from a single CMD.
- Python dependencies are managed by uv. The virtual environment is built in the python-builder stage and copied to the final image.
- The `nobody` user owns `/docetl-data` with 777 permissions. Mount the volume as a named Docker volume or a host path.
- An empty `.env` file is created at build time so the app does not fail if no `.env` is mounted.
- libgl1 and libglib2.0-0 are installed for OpenCV support (used by some document processing operations).

## Changes from Original
No changes to the upstream Dockerfile structure. The Dockerfile was written for this deployment following the upstream docker-compose.yml as reference.

## V2 Dependency Changes
Python dependencies managed by uv with a lock file generated from pyproject.toml. Node dependencies pinned by package-lock.json. No additional pinning applied.
