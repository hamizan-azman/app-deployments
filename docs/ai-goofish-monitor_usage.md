# ai-goofish-monitor. Usage Documentation

## Overview
FastAPI backend with a Vue frontend for monitoring second-hand product listings on Xianyu (Goofish). Uses Playwright to scrape listings and a vision-capable LLM to extract and analyze price data. The backend serves both the API and the prebuilt Vue static files.

## Quick Start
```bash
docker pull hoomzoom/ai-goofish-monitor
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e OPENAI_BASE_URL=https://api.openai.com/v1 \
  -e OPENAI_MODEL_NAME=gpt-4o \
  hoomzoom/ai-goofish-monitor
```

Open http://localhost:8000 in your browser.

## Base URL
http://localhost:8000

## Core Features
- Automated Xianyu listing scraper using Playwright with Chromium
- LLM vision analysis for extracting product and price details from listing screenshots
- Vue frontend served from the same FastAPI process
- Price history tracking with JSONL storage

## Endpoints

### Web UI
- **URL:** http://localhost:8000
- **Description:** Vue frontend for configuring monitors and viewing results.
- **Tested:** Yes (import verified)

### API (FastAPI)
- **URL:** http://localhost:8000/docs
- **Description:** FastAPI auto-generated interactive API documentation.
- **Tested:** Not tested (requires browser session for Xianyu login)

## Health Check
The Dockerfile uses `curl -f http://localhost:8000/` as the healthcheck with a 60-second start period. The FastAPI process must fully start and Playwright must initialize before the healthcheck passes.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | API key for the vision LLM |
| OPENAI_BASE_URL | Yes | None | Base URL for the OpenAI-compatible API |
| OPENAI_MODEL_NAME | Yes | None | Model name to use, must support vision (e.g. gpt-4o) |

## Volumes
| Path | Purpose |
|------|---------|
| /app/data | Scraped listing data |
| /app/state | Browser session state (Xianyu login cookies) |
| /app/logs | Application logs |
| /app/images | Downloaded listing images |
| /app/jsonl | Raw JSONL records |
| /app/price_history | Price history per product |

To persist login state across restarts, mount /app/state to a host directory.

## Notes
- A Xianyu account session is required for the scraper to work. Log in through the UI on first run and save the session state.
- The container runs as root (upstream requirement for Playwright browser management).
- Playwright Chromium is installed inside the image. No external browser is needed.
- Timezone is set to Asia/Shanghai (upstream default). No functional impact for non-CN deployments.
- tini is used as the init process.

## Changes from Original
- Removed Chinese PyPI mirror (`-i https://pypi.tuna.tsinghua.edu.cn/simple`) from the pip install command to use the default PyPI index.
- Fixed the COPY path for the Vue build output. The upstream Dockerfile copied from `/web-ui/dist` but the Node build stage outputs to `/dist` (Vite default). Changed to `COPY --from=frontend-builder /dist /app/dist`.

## V2 Dependency Changes
Minimum version pinning applied to requirements-runtime.txt. All minimum versions resolved successfully without bumps.
