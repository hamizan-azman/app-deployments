# khoj. Usage Documentation

## Overview
AI second-brain assistant with a web interface for chat, document search, and automation. Self-hostable compose deployment using the upstream GHCR image. Includes PostgreSQL with pgvector, SearXNG for web search, and a Terrarium sandbox for code execution.

## Quick Start
```bash
cd dockerfiles/khoj
cp .env.example .env
# Edit .env with credentials and API keys
docker compose up -d
```

Open http://localhost:42110 in your browser.

## Base URL
http://localhost:42110

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| database | pgvector/pgvector:pg15 | internal | PostgreSQL with vector search |
| sandbox | ghcr.io/khoj-ai/terrarium | internal | Code execution sandbox |
| search | searxng/searxng | internal | Self-hosted web search |
| server | ghcr.io/khoj-ai/khoj | 42110 | Main Khoj application |

## Health Check
- **URL:** http://localhost:42110/api/health
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| POSTGRES_USER | No | postgres | Database username |
| POSTGRES_PASSWORD | No | postgres | Database password (change in production) |
| POSTGRES_DB | No | postgres | Database name |
| KHOJ_DJANGO_SECRET_KEY | No | change-me-in-production | Django secret key |
| KHOJ_ADMIN_EMAIL | No | admin@example.com | Admin account email |
| KHOJ_ADMIN_PASSWORD | No | change-me-in-production | Admin account password |
| KHOJ_PORT | No | 42110 | Host port for the Khoj server |
| OPENAI_API_KEY | No | None | OpenAI API key for cloud models |
| GEMINI_API_KEY | No | None | Google Gemini API key |
| ANTHROPIC_API_KEY | No | None | Anthropic API key |
| KHOJ_TELEMETRY_DISABLE | No | unset | Set to True to disable telemetry |

All defaults allow the server to start without any credentials. Change KHOJ_DJANGO_SECRET_KEY and KHOJ_ADMIN_PASSWORD before exposing to a network.

## Persistent Volumes
| Volume | Purpose |
|--------|---------|
| khoj-config | Khoj configuration files |
| khoj-db | PostgreSQL data |
| khoj-models | Cached sentence transformer and Hugging Face models |
| khoj-search | SearXNG configuration |

## Stopping and Cleanup
```bash
# Stop services
docker compose down

# Stop and remove volumes (destroys all data)
docker compose down -v
```

## Notes
- Uses upstream GHCR images directly. No custom build required.
- The server runs in anonymous mode (`--anonymous-mode`) allowing access without user login.
- The optional VNC desktop service (khoj-ai/khoj-computer) is not included. It requires a desktop GUI and cannot run headlessly.
- SearXNG requires a `settings.yml` placed in the `khoj-search` volume for web search to function. See upstream docs at https://docs.khoj.dev/.
- LLM API features are NOT TESTED in CI.

## Changes from Original
The optional `computer` service (VNC desktop) was removed. It requires desktop GUI access which is incompatible with headless Docker. All other services are unchanged from the upstream compose configuration.
