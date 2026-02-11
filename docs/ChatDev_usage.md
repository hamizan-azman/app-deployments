# ChatDev. Usage Documentation

## Overview
FastAPI backend for ChatDev's multi-agent software development system (DevAll v2.0). A team of LLM-powered agents collaborates to build software from a single natural language description, covering design, coding, testing, and documentation stages. This deployment covers the backend only. The upstream frontend is a separate Node.js application and is not containerized here.

## Quick Start
```bash
docker pull hoomzoom/chatdev
docker run -d -p 6400:6400 \
  -e API_KEY=your_api_key_here \
  -e BASE_URL=https://api.openai.com/v1 \
  hoomzoom/chatdev
```

API docs available at http://localhost:6400/docs.

## Base URL
http://localhost:6400

## Core Features
- Multi-agent pipeline that produces complete software projects from a natural language prompt
- Supports OpenAI-compatible APIs and Google GenAI
- Agents cover product manager, designer, programmer, reviewer, and tester roles
- DevAll v2.0 pipeline with iterative refinement

## Endpoints

### API Documentation
- **URL:** http://localhost:6400/docs
- **Method:** GET
- **Description:** Interactive Swagger UI listing all available endpoints.
- **Tested:** Yes (returns 200)

### Health Check
- **URL:** http://localhost:6400/docs
- **Method:** GET
- **Response:** 200 OK
- **Tested:** Yes

All functional endpoints (project creation, agent task submission) require a valid API key and are not tested in this deployment.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_KEY | Yes | None | API key for the LLM provider (OpenAI or compatible) |
| BASE_URL | Yes | None | Base URL for the LLM API (e.g. https://api.openai.com/v1) |

Both variables must be set for the multi-agent pipeline to function. The container starts and the /docs endpoint is accessible without them, but all agent tasks will fail without valid credentials.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- Backend only. The ChatDev frontend (Node.js) is not included and must be run separately if a UI is needed.
- Multi-agent tasks are stateful and may take several minutes to complete depending on project complexity.
- No persistent storage is configured. Generated project files exist only for the duration of the request unless the app writes to a mounted volume.

## Changes from Original
- Added multi-stage build (builder + runtime) to separate compile-time system dependencies (libcairo2-dev, build-essential) from runtime dependencies (libcairo2 only), reducing final image size.
- Installed dependencies via uv with a frozen lockfile for reproducible builds.
- Added non-root user (appuser, UID 1000).
- Added HEALTHCHECK against /docs.
- No changes to application code or entrypoint logic.

## V2 Dependency Changes (Minimum Version Pinning)
Dependencies managed via uv with a frozen lockfile (uv.lock). Pinning is enforced by the lockfile at build time. No additional minimum version pinning pass was required.
