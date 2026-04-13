# onyx. Usage Documentation

## Overview
Enterprise-grade AI knowledge management and search platform (formerly Danswer). Indexes documents from connected sources and provides LLM-powered search and chat. Heavy compose stack with 11 services including Vespa vector search, OpenSearch, PostgreSQL, Redis, nginx, two model servers, MinIO object store, and a code interpreter.

## Quick Start
```bash
cd dockerfiles/onyx
cp .env.example .env
# Edit .env with required credentials
# Set vm.max_map_count before starting (required by OpenSearch)
wsl -d docker-desktop sysctl -w vm.max_map_count=262144
docker compose --profile s3-filestore up -d
```

Web UI: http://localhost:3000 (also http://localhost:80)

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| api_server | onyxdotapp/onyx-backend | internal (8080) | FastAPI application server |
| background | onyxdotapp/onyx-backend | internal | Supervisor managing indexing workers |
| web_server | onyxdotapp/onyx-web-server | internal | Next.js frontend |
| inference_model_server | onyxdotapp/onyx-model-server | internal (9000) | Embedding model inference |
| indexing_model_server | onyxdotapp/onyx-model-server | internal (9000) | Embedding model for indexing |
| relational_db | postgres:15.2-alpine | internal | PostgreSQL (max 250 connections) |
| index | vespaengine/vespa:8.609.39 | internal | Vespa vector search engine |
| opensearch | opensearchproject/opensearch:3.4.0 | internal | OpenSearch full-text search |
| nginx | nginx:1.25.5-alpine | 80, 3000 | Reverse proxy and static serving |
| cache | redis:7.4-alpine | internal | Redis session and task cache |
| minio | minio/minio | internal (9000/9001) | S3-compatible object store (s3-filestore profile) |
| code-interpreter | onyxdotapp/code-interpreter | internal | Sandboxed code execution |

## Startup
Full startup takes 5 to 10 minutes on first run due to database migrations and model downloads.

```bash
# With MinIO object storage
docker compose --profile s3-filestore up -d

# Without MinIO (uses PostgreSQL file storage)
docker compose up -d
```

## Health Checks
- **API server**: `curl http://localhost:3000/api/health` (proxied through nginx)
- **Inference model server**: port 9000 (internal only)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| AUTH_TYPE | No | basic | Authentication type |
| POSTGRES_USER | No | postgres | Database username |
| POSTGRES_PASSWORD | No | password | Database password |
| FILE_STORE_BACKEND | No | s3 | Storage backend (s3 or postgres) |
| OPENSEARCH_ADMIN_PASSWORD | No | StrongPassword123! | OpenSearch admin password |
| IMAGE_TAG | No | latest | Tag for all Onyx images |
| HOST_PORT | No | 3000 | Main UI host port |
| OPENAI_API_KEY | No | None | OpenAI API key |
| ANTHROPIC_API_KEY | No | None | Anthropic API key |
| MINIO_ROOT_USER | No | minioadmin | MinIO admin username |
| MINIO_ROOT_PASSWORD | No | minioadmin | MinIO admin password |

## System Requirement: vm.max_map_count
OpenSearch requires a higher virtual memory map limit than the default. Run this command before starting the stack:
```bash
wsl -d docker-desktop sysctl -w vm.max_map_count=262144
```
Without this, OpenSearch will fail to start with a bootstrap check error.

## Persistent Volumes
onyx-db, onyx-vespa, onyx-minio, onyx-model-cache-hf, onyx-indexing-model-cache-hf, onyx-api-server-logs, onyx-background-logs, onyx-inference-model-server-logs, onyx-indexing-model-server-logs, onyx-file-system, onyx-opensearch-data

## Notes
- Uses official upstream images from Docker Hub (`onyxdotapp/`). No custom builds required.
- nginx templates are mounted read-only from `apps/onyx/deployment/data/nginx`. The app submodule must be present for nginx to start.
- The code-interpreter runs as root and mounts the Docker socket for DinD code execution.
- LLM connector features are NOT TESTED in CI.

## Changes from Original
The `mcp_server`, `certbot`, and `computer` services are omitted (optional services not needed for research deployment). The MinIO image was pinned to `RELEASE.2025-07-23T15-54-02Z-cpuv1` for reproducibility.
