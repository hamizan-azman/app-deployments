# skyvern. Usage Documentation

## Overview
Autonomous browser automation platform driven by LLM vision. Skyvern uses Playwright and computer vision to navigate websites and complete tasks described in plain language. The deployment consists of three containers: the Skyvern API backend (FastAPI), the React frontend UI, and PostgreSQL.

## Quick Start
```bash
cd dockerfiles/skyvern
# Copy and fill in environment variables
cp .env.example .env   # set at least one LLM provider block in docker-compose.yml

docker compose up -d
```

Edit `docker-compose.yml` and uncomment one LLM provider block (OpenAI, Anthropic, Gemini, Azure, Bedrock, Ollama, or OpenRouter) before starting.

## Services and Ports
| Service | Host Port | Container Port | Description |
|---|---|---|---|
| skyvern (API) | 8000 | 8000 | FastAPI backend and agent runner |
| skyvern-ui | 8080 | 8080 | React frontend |
| skyvern-ui (artifacts) | 9090 | 9090 | Artifact serving sidecar |
| VNC | 6080 | 6080 | noVNC web viewer for live browser observation |
| PostgreSQL | internal | 5432 | Persistent task and run storage |

Open http://localhost:8080 for the UI. Open http://localhost:6080 for the VNC viewer to watch browser sessions live.

## Base URLs
- API: http://localhost:8000/api/v1
- UI: http://localhost:8080
- VNC: http://localhost:6080

## Key Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /api/v1/health | GET | API health check |
| /api/v1/tasks | POST | Submit a new automation task |
| /api/v1/tasks/{task_id} | GET | Poll task status and results |
| /api/v1/workflows | GET | List saved workflows |
| /api/v1/browser_sessions | GET | List active browser sessions |

## Health Check
- **URL:** `http://localhost:8000/api/v1/health`
- **Method:** GET
- **Response:** JSON status object
- **Tested:** Yes (import-level; full endpoint requires LLM key)

## Environment Variables
Set these in the `environment` block of the `skyvern` service in `docker-compose.yml`.

| Variable | Required | Description |
|---|---|---|
| DATABASE_STRING | Yes | PostgreSQL connection string (set by compose) |
| BROWSER_TYPE | Yes | Browser to use. `chromium-headful` for VNC-observable sessions |
| LLM_KEY | Yes | Identifier for the active LLM model (e.g. OPENAI_GPT4O) |
| ENABLE_OPENAI | Conditional | Set `true` when using OpenAI |
| OPENAI_API_KEY | Conditional | Required when ENABLE_OPENAI=true |
| ENABLE_ANTHROPIC | Conditional | Set `true` when using Anthropic |
| ANTHROPIC_API_KEY | Conditional | Required when ENABLE_ANTHROPIC=true |
| ENABLE_GEMINI | Conditional | Set `true` when using Gemini |
| GEMINI_API_KEY | Conditional | Required when ENABLE_GEMINI=true |
| ENABLE_AZURE | Conditional | Set `true` when using Azure OpenAI |
| AZURE_DEPLOYMENT | Conditional | Azure deployment name |
| AZURE_API_KEY | Conditional | Azure OpenAI API key |
| AZURE_API_BASE | Conditional | Azure OpenAI endpoint URL |
| AZURE_API_VERSION | Conditional | Azure API version string |
| ENABLE_BEDROCK | Conditional | Set `true` when using AWS Bedrock |
| AWS_REGION | Conditional | AWS region for Bedrock |
| AWS_ACCESS_KEY_ID | Conditional | AWS access key |
| AWS_SECRET_ACCESS_KEY | Conditional | AWS secret key |
| ENABLE_OLLAMA | Conditional | Set `true` when using local Ollama |
| OLLAMA_SERVER_URL | Conditional | Ollama server URL |
| OLLAMA_MODEL | Conditional | Model name (e.g. qwen2.5:7b-instruct) |
| ENABLE_OPENROUTER | Conditional | Set `true` when using OpenRouter |
| OPENROUTER_API_KEY | Conditional | OpenRouter API key |
| OPENROUTER_MODEL | Conditional | OpenRouter model identifier |
| ENABLE_CODE_BLOCK | No | Enable code execution in agents. Defaults to true in compose |
| VITE_SKYVERN_API_KEY | No | UI API key. Set this after first login via the UI settings page |

## QC Test
```bash
# Start the stack
docker compose up -d

# Wait for API to be healthy then run import check
docker compose exec skyvern python -c "import skyvern; print('ok')"
```
Expected output: `ok`

## Volumes (compose)
| Volume | Mount | Purpose |
|---|---|---|
| ./artifacts | /data/artifacts | Saved screenshots and artifacts |
| ./videos | /data/videos | Recorded browser session videos |
| ./har | /data/har | HAR network captures |
| ./log | /data/log | Application logs |

## Notes
- A valid LLM key is required for any task to run. Without one the API starts but all task submissions fail.
- The VNC viewer at port 6080 shows the live Chromium browser session. No VNC password is set by default.
- The UI API key (`VITE_SKYVERN_API_KEY`) is generated after first startup. Retrieve it from the UI settings page and set it in the compose environment.
- PostgreSQL data persists in the `postgres-data` named volume.
- The Bitwarden CLI is installed in the image for credential vault integration (optional feature).
- The image is built on `python:3.11-slim-bookworm`. The bookworm base is used explicitly because Playwright requires libraries that are not available in the trixie-based slim image.

## Changes from Original
- `xdpyinfo` package replaced with `x11-utils` in the Dockerfile. The upstream Dockerfile referenced `xdpyinfo` directly but this is a binary provided by the `x11-utils` package, not a package name itself. This caused an apt install failure.
- Windows line ending strip added for `entrypoint-skyvern.sh` (`sed -i 's/\r$//'`).
- Compose file updated to reference `hoomzoom/skyvern` and `hoomzoom/skyvern-ui` images.
