# DeepBI. Usage Documentation

## Overview
AI-powered business intelligence platform for data analysis and visualization. Compose application with a Flask web server, Celery task workers, scheduler, AI API service, WebSocket server, Redis, PostgreSQL, and a mail dev server. Uses the `hoomzoom/deepbi` image for all application services.

## Quick Start
```bash
cd dockerfiles/DeepBI
cp .env.example .env
docker compose up -d
```

Web UI: http://localhost:8338
AI API: http://localhost:8340
WebSocket: http://localhost:8339
Mail UI (dev): http://localhost:1080

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| server | hoomzoom/deepbi | 8338 | Main Flask web server |
| server_ai_api | hoomzoom/deepbi | 8340 | AI inference API |
| server_socket | hoomzoom/deepbi | 8339 | WebSocket server |
| scheduler | hoomzoom/deepbi | internal | Celery beat scheduler |
| worker | hoomzoom/deepbi | internal | Celery task worker |
| redis | redis:3-alpine | internal | Celery broker and result backend |
| postgres | postgres:14-alpine | internal | Primary database |
| email | maildev/maildev | 1080 | Development SMTP mail catcher |

## Health Check
- **URL:** http://localhost:8338/
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DEEPBI_LOG_LEVEL | No | INFO | Application log level |
| DEEPBI_RATELIMIT_ENABLED | No | false | Enable API rate limiting |
| DEEPBI_MAIL_DEFAULT_SENDER | No | test@example.com | Default email sender |
| DEEPBI_MAIL_SERVER | No | email | SMTP server hostname |
| DEEPBI_ENFORCE_CSRF | No | true | Enable CSRF protection |
| DEEPBI_GUNICORN_TIMEOUT | No | 60 | Gunicorn worker timeout (seconds) |
| DEEPBI_WEB_WORKERS | No | 4 | Number of Gunicorn workers |
| DEEPBI_CELERY_WORKERS | No | 4 | Number of Celery workers |
| OPENAI_API_KEY | Conditional | None | Required for AI analysis features |

Place additional configuration in `.env`. The compose file loads it via `env_file: .env`.

## Mail Dev
DeepBI sends transactional email in some workflows. The `email` service is a development SMTP server (maildev). All outgoing emails are captured and visible at http://localhost:1080. No real email is sent.

## Stopping and Cleanup
```bash
# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Notes
- All application services (server, worker, scheduler, AI API, socket) use the same `hoomzoom/deepbi` image with different CMD arguments.
- Python 3.8.18 is used to match the upstream Dockerfile.
- The container runs as non-root user `deepbi` (UID 1000).
- AI analysis features are NOT TESTED in CI.
- The compose file version is `2.0` (legacy format, no Swarm features needed).

## Changes from Original
The upstream Dockerfile is used as-is with one fix: an importlib_resources compatibility patch for Python 3.8.18 (replaces `from importlib_resources import path` with `from importlib.resources import path` in the saml2 library). This fix is applied via sed in the Dockerfile.

## V2 Dependency Changes (Minimum Version Pinning)
Dependencies installed from `vrequment.txt` via pip. pip itself is pinned to version 20.2.4 as required by the upstream Dockerfile.
