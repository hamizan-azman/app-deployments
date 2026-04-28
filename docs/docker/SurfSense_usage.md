# SurfSense. Usage Documentation

## Overview
AI-powered personal research assistant that indexes and searches across web content, documents, and connected sources. Full-stack compose application with a FastAPI backend, Next.js frontend, PostgreSQL with pgvector, Redis, SearXNG web search, Celery task queue, and a Zero Cache sync layer. Uses GHCR images from the upstream project.

## Quick Start
```bash
cd dockerfiles/SurfSense
cp .env.example .env
# Edit .env with your API keys and passwords
docker compose up -d
```

Frontend: http://localhost:3929
Backend API: http://localhost:8929
Zero Cache: http://localhost:5929

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| db | pgvector/pgvector:pg17 | internal | PostgreSQL with vector extension |
| redis | redis:8-alpine | internal | Celery broker and result backend |
| searxng | searxng/searxng:2026.3.13 | internal | Self-hosted web search |
| backend | ghcr.io/modsetter/surfsense-backend | 8929 | FastAPI API server |
| celery_worker | ghcr.io/modsetter/surfsense-backend | internal | Async task worker |
| celery_beat | ghcr.io/modsetter/surfsense-backend | internal | Periodic task scheduler |
| zero-cache | rocicorp/zero:0.26.2 | 5929 | Real-time sync cache |
| frontend | ghcr.io/modsetter/surfsense-web | 3929 | Next.js web UI |

## Startup Order
Services start in dependency order. The backend waits for db, redis, and searxng to be healthy. The frontend waits for both backend and zero-cache to be healthy. Full startup takes approximately 3 to 5 minutes.

## Health Checks
- **Backend**: `curl http://localhost:8929/health` returns 200
- **Zero Cache**: `curl http://localhost:5929/keepalive` returns 200
- **Frontend**: accessible at http://localhost:3929 once backend and zero-cache are healthy

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DB_USER | No | surfsense | PostgreSQL username |
| DB_PASSWORD | No | surfsense | PostgreSQL password (change in production) |
| DB_NAME | No | surfsense | PostgreSQL database name |
| SURFSENSE_VERSION | No | latest | GHCR image tag to pull |
| BACKEND_PORT | No | 8929 | Host port for backend API |
| FRONTEND_PORT | No | 3929 | Host port for Next.js frontend |
| ZERO_CACHE_PORT | No | 5929 | Host port for Zero Cache |
| SEARXNG_SECRET | No | surfsense-searxng-secret | SearXNG secret key |
| NEXT_FRONTEND_URL | No | http://localhost:3929 | Frontend URL for CORS |
| LLM_API_KEY | Conditional | None | API key for LLM provider (set in .env) |

Copy `.env.example` to `.env` and fill in LLM API keys and any passwords you want to change before first run.

## Persistent Volumes
| Volume | Purpose |
|--------|---------|
| surfsense-postgres | PostgreSQL data |
| surfsense-redis | Redis persistence |
| surfsense-shared-temp | Shared temp files between backend and worker |
| surfsense-zero-cache | Zero Cache sync state |

## Stopping and Cleanup
```bash
# Stop services
docker compose down

# Stop and remove volumes (destroys all data)
docker compose down -v
```

## Notes
- This deployment uses upstream GHCR images directly. No custom images are built.
- The zero-cache service uses `extra_hosts: host.docker.internal:host-gateway` for host network access.
- The backend has a long start_period (200s) in its healthcheck due to database migration on first run.
- LLM API features are NOT TESTED in CI.

## Changes from Original
Compose file adapted from upstream for research deployment. Version pinned for SearXNG (`2026.3.13-3c1f68c59`) and Zero Cache (`0.26.2`) to avoid breaking changes from `latest` tags.
