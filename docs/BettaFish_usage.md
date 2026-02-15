# BettaFish -- Usage Documentation

## Overview
Multi-agent opinion analysis system. Performs sentiment analysis across social media platforms using specialized AI agents (Query, Media, Insight, Report). Flask web UI with Streamlit components and PostgreSQL backend.

## Quick Start
```bash
docker pull hoomzoom/bettafish
```

## Docker Compose
```bash
# 1. Copy example env and fill in your API keys
cp .env.example .env
```
Open `.env` in a text editor and set these values:
```
INSIGHT_ENGINE_API_KEY=sk-your-openai-key
MEDIA_ENGINE_API_KEY=sk-your-openai-key
QUERY_ENGINE_API_KEY=sk-your-openai-key
REPORT_ENGINE_API_KEY=sk-your-openai-key
TAVILY_API_KEY=your-tavily-key
```
All four engine keys can use the same OpenAI API key. TAVILY_API_KEY is for web search (optional).
```bash
# 2. Start services
docker compose up -d
```

## Base URLs
- Flask UI: http://localhost:5000
- Insight Engine: http://localhost:8501
- Media Engine: http://localhost:8502
- Query Engine: http://localhost:8503

## API Endpoints

### Status
- **URL:** `/api/status`
- **Method:** GET
- **Response:** `{"forum":{"status":"stopped"},"insight":{"status":"stopped","port":8501},...}`
- **Tested:** Yes

### Config
- **URL:** `/api/config`
- **Method:** GET
- **Response:** `{"config":{...all env vars...},"success":true}`
- **Tested:** Yes

### Start Engine
- **URL:** `/api/start/<app_name>`
- **Method:** GET
- **Description:** Start an engine (insight, media, query, forum)
- **Tested:** No (requires API keys)

### Stop Engine
- **URL:** `/api/stop/<app_name>`
- **Method:** GET
- **Tested:** No

### Search
- **URL:** `/api/search`
- **Method:** POST
- **Description:** Submit a search/analysis query
- **Tested:** No (requires API keys + search API)

### Forum
- **URL:** `/api/forum/*`
- **Method:** Various
- **Description:** Multi-agent forum collaboration endpoints
- **Tested:** No (requires API keys)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DB_HOST | Yes | db | Database hostname |
| DB_PORT | Yes | 5432 | Database port |
| DB_USER | Yes | bettafish | Database user |
| DB_PASSWORD | Yes | bettafish | Database password |
| DB_NAME | Yes | bettafish | Database name |
| DB_DIALECT | Yes | postgresql | Database type |
| INSIGHT_ENGINE_API_KEY | For insight | None | LLM API key for Insight Agent |
| MEDIA_ENGINE_API_KEY | For media | None | LLM API key for Media Agent |
| QUERY_ENGINE_API_KEY | For query | None | LLM API key for Query Agent |
| REPORT_ENGINE_API_KEY | For report | None | LLM API key for Report Agent |
| TAVILY_API_KEY | For search | None | Tavily search API key |

## Services
- `bettafish`: Main app (Flask + Streamlit)
- `db`: PostgreSQL 15

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Docker compose up | PASS |
| 2 | Flask UI (port 5000) | PASS (200 OK) |
| 3 | API /api/status | PASS |
| 4 | API /api/config | PASS |
| 5 | Engine start/search | NOT TESTED (requires API keys) |

## Notes
- Pre-built image from `hoomzoom/bettafish` (4.6GB).
- Requires multiple LLM API keys (Insight, Media, Query, Report agents).
- Requires at least one search API key (Tavily, Anspire, or Bocha).
- Database auto-initializes on first run.
- CPU-only (torch CPU version), no GPU needed.
- Chinese social media focused (Weibo, Bilibili, etc.).

## Changes from Original
None. Uses the developer's own pre-built image (ghcr.io/666ghj/bettafish:latest).
