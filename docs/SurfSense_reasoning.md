# SurfSense. Reasoning Log

## Initial Assessment

SurfSense is a full-stack research assistant with eight interdependent services. The upstream project publishes pre-built images on GHCR (`ghcr.io/modsetter/surfsense-backend` and `ghcr.io/modsetter/surfsense-web`). No custom build is required for the main services.

## What Was Checked

1. **README.md**: Describes self-hosted deployment using Docker Compose. References GHCR images. Lists required environment variables for LLM providers, database, and search.

2. **Upstream docker-compose.yml**: The base for our compose file. Defines all eight services with healthchecks, dependencies, and named volumes.

3. **Service roles**: Backend handles API and database migrations on first start. celery_worker and celery_beat handle async tasks (document ingestion, background indexing). zero-cache provides real-time sync between backend database and frontend.

4. **SearXNG version**: Upstream compose used `latest` for SearXNG. Pinned to `2026.3.13-3c1f68c59` to prevent silent breakage from upstream changes.

## Decisions Made

### Used upstream GHCR images
The upstream maintainer publishes official images. Using them preserves the authentic deployment configuration for supply chain research. No custom images are built for the backend or frontend.

### Pinned third-party images
SearXNG and Zero Cache used `latest` tags in the upstream compose file. We pin to specific versions (`2026.3.13-3c1f68c59` and `0.26.2` respectively) for reproducibility.

### Kept all eight services
The architectural fidelity rule prohibits merging services or removing components. All eight services are included as defined upstream.

### Long backend healthcheck start_period
The backend runs database migrations via Alembic on first startup. On a fresh volume this can take 2 to 3 minutes. The start_period of 200s prevents healthcheck failures during migration.

## Testing

### Tests Performed
1. **Docker Compose up**: All services start in dependency order. No startup failures. Pass.
2. **Backend health** (`curl http://localhost:8929/health`): Returns 200. Pass.
3. **Zero Cache keepalive** (`curl http://localhost:5929/keepalive`): Returns 200. Pass.
4. **Frontend** (http://localhost:3929): Next.js page loads. Pass.

### What Was Not Tested
- Document ingestion and indexing (requires LLM API key)
- Web search via SearXNG integration
- Celery task execution

## Gotchas

1. **backend start_period 200s**: First run is slow due to Alembic migrations. The healthcheck must be patient or compose will report the backend as unhealthy before it has finished initializing.

2. **Zero Cache and database sync**: The zero-cache service requires the backend to be healthy before it can start, because it connects to the same PostgreSQL database to set up its replication state.

3. **Environment file required**: The backend and worker use `env_file: .env`. If `.env` does not exist, Docker Compose will still start but the backend will fail at runtime when environment variables are missing. Copy `.env.example` to `.env` before running.

4. **Volume names**: Named volumes (`surfsense-postgres`, etc.) are scoped to the compose project name `surfsense`. Running a second instance will share data unless volumes are renamed.
