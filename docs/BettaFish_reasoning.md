# BettaFish -- Reasoning Log

## Initial Analysis

### Repository Structure
- `README.md`: Multi-agent opinion analysis platform targeting Chinese social media.
- `Dockerfile`: python:3.11-slim, installs system deps (Playwright, WeasyPrint, ffmpeg), uses `uv` for fast pip install, installs Playwright chromium. Exposes ports 5000, 8501-8503.
- `docker-compose.yml`: Uses pre-built image `ghcr.io/666ghj/bettafish:latest`. PostgreSQL 15 sidecar.
- `.env.example`: Shows 6 LLM API keys, 3 search API keys, 8 database params.
- `app.py`: Flask + SocketIO orchestrator (~2274 lines). Routes for status, config, start/stop engines, search, forum.
- `requirements.txt`: 91 packages including Flask, Streamlit, FastAPI, torch (CPU), Playwright, OpenAI SDK.

## Decisions

### Use Pre-built Image
The docker-compose.yml already references `ghcr.io/666ghj/bettafish:latest`. This is the developer's official image. Building from source would require downloading Playwright chromium and 91 pip packages -- the pre-built image includes everything.

### Docker Compose for PostgreSQL
BettaFish requires PostgreSQL for storing crawled data. The docker-compose.yml already configures this with sensible defaults (user/pass: bettafish, port 5444 on host mapping to 5432 internally).

### Infrastructure Testing Only
Without LLM API keys (Kimi, Gemini, DeepSeek, Qwen) and search API keys (Tavily/Anspire/Bocha), the agents cannot start. The Flask orchestrator and API endpoints work without keys, so I tested those.

## Test Details

### Test 1: Docker Compose Up
Pulled ghcr.io/666ghj/bettafish:latest (4.6GB) and postgres:15. Both containers started successfully.

### Test 2: Flask UI
`GET http://localhost:5000` returned 200 OK. The web UI loads with the full HTML interface.

### Test 3: API Status
`GET /api/status` returns JSON showing all 4 engines (forum, insight, media, query) in "stopped" state. This confirms the orchestrator is running and can manage engine lifecycle.

### Test 4: API Config
`GET /api/config` returns the full .env configuration as JSON. Confirmed database settings, API key placeholders, and search tool settings are all loaded correctly.

## Issues and Workarounds

1. **Image is 4.6GB**: Includes Playwright chromium, torch, and all Python dependencies.
2. **Multiple API keys needed**: 6 LLM providers + 1 search provider minimum.
3. **Chinese-focused**: UI and social media crawling targets Chinese platforms.
4. **Database auto-init**: Tables are created automatically on first app startup.
5. **Port 5444 for PostgreSQL**: External PostgreSQL port is 5444 (not standard 5432) to avoid conflicts.
