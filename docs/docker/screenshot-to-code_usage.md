# screenshot-to-code. Usage Documentation

## Overview
Two-container application that converts screenshots, mockups, and Figma designs into working HTML/CSS/JavaScript code. The backend is a FastAPI service that calls LLM vision APIs. The frontend is a Vite/React development server. Supports GPT-4o, Claude 3.5 Sonnet, and other vision-capable models.

## Quick Start
```bash
cd dockerfiles/screenshot-to-code
docker compose up -d
```

Frontend UI: http://localhost:5173
Backend API: http://localhost:7001

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| backend | hoomzoom/screenshot-to-code-backend | 7001 | FastAPI with LLM vision API integration |
| frontend | hoomzoom/screenshot-to-code-frontend | 5173 | Vite/React web UI |

## Health Checks
- **Backend:** http://localhost:7001/docs returns 200
- **Frontend:** http://localhost:5173 returns HTTP response (not 5xx)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Conditional | None | Required for GPT-4o and GPT-4 Vision |
| ANTHROPIC_API_KEY | Conditional | None | Required for Claude models |
| BACKEND_PORT | No | 7001 | Host port for backend |

Pass API keys in a `.env` file or as environment variables:
```bash
OPENAI_API_KEY=your_key docker compose up -d
```

## API Endpoints

### API Documentation
- **URL:** http://localhost:7001/docs
- **Method:** GET
- **Description:** FastAPI Swagger UI with all endpoint definitions.
- **Tested:** Yes

### Generate code (primary endpoint)
- **URL:** http://localhost:7001/generate-code
- **Method:** WebSocket
- **Description:** Accepts an image and returns generated HTML/CSS/JS code as a streaming WebSocket response.
- **Tested:** No (requires valid vision API key)

## Building Images
```bash
# Build backend
docker build --platform linux/amd64 \
  -t hoomzoom/screenshot-to-code-backend \
  apps/screenshot-to-code/backend \
  -f dockerfiles/screenshot-to-code/backend/Dockerfile

# Build frontend
docker build --platform linux/amd64 \
  -t hoomzoom/screenshot-to-code-frontend \
  apps/screenshot-to-code/frontend \
  -f dockerfiles/screenshot-to-code/frontend/Dockerfile
```

## Notes
- The frontend uses WebSocket to stream generated code from the backend. The WebSocket URL is configured at build time via `VITE_WS_BACKEND_URL`.
- The frontend depends on the backend being healthy before it starts.
- LLM code generation features are NOT TESTED in CI.
- The frontend runs the Vite dev server (`yarn dev`), which is appropriate for a research deployment.
- PUPPETEER_SKIP_DOWNLOAD=true is set in the frontend Dockerfile to prevent Puppeteer from downloading Chromium.

## Changes from Original
The upstream repo has no Dockerfile. Both Dockerfiles were written from scratch. Backend uses Poetry for dependency management. Frontend uses yarn with the Vite dev server. The frontend WebSocket URL is set to `ws://localhost:7001` by default, matching the backend's host port.

## V2 Dependency Changes (Minimum Version Pinning)
Backend: Poetry lock file used for exact version pinning. Frontend: yarn.lock provides exact Node dependency versions.
