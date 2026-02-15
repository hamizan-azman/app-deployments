# AgentGPT -- Usage Documentation

## Overview
Autonomous AI agent platform. Users define goals, the system breaks them into tasks, selects tools (search, code, image gen), executes them, and returns results. Next.js frontend + FastAPI backend + MySQL.

## Quick Start

### Option 1: Pull from Docker Hub (recommended)
```bash
docker pull hoomzoom/agentgpt-frontend
docker pull hoomzoom/agentgpt-platform
# MySQL uses stock image: mysql:8.0
```
You still need the repo's `docker-compose.yml` and `.env` file to run. Clone the repo, then:
```bash
cd apps/AgentGPT
cp .env.example next/.env
```
Open `next/.env` in a text editor and replace `changeme` with your actual OpenAI API key:
```
REWORKD_PLATFORM_OPENAI_API_KEY=sk-proj-your-key-here
```
Then start all services:
```bash
docker compose up -d
```

### Option 2: Build from source
```bash
cd apps/AgentGPT
cp .env.example next/.env
# Edit next/.env as described above
docker compose build
docker compose up -d
```

## Architecture
| Service | Port | Image |
|---------|------|-------|
| frontend | 3000 | agentgpt-frontend (Next.js 13) |
| platform | 8000 | agentgpt-platform (FastAPI/uvicorn) |
| agentgpt_db | 3307 (mapped 3308) | mysql:8.0 |

## Base URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/api/docs

## Core Features
- Goal-driven autonomous agents
- Task decomposition and execution
- Tool selection (search, code, image generation, SID)
- Streaming responses
- OAuth integration (Google, GitHub, Discord)
- Organization/team support

## API Endpoints

### Health Check
- **URL:** `/api/monitoring/health`
- **Method:** GET
- **Request:** `curl http://localhost:8000/api/monitoring/health`
- **Response:** `null` (200 OK)
- **Tested:** Yes -- PASS

### Error Check
- **URL:** `/api/monitoring/error`
- **Method:** GET
- **Description:** Intentionally throws an error (for logging verification)
- **Request:** `curl http://localhost:8000/api/monitoring/error`
- **Response:** 500 Internal Server Error (expected)
- **Tested:** Yes -- PASS

### Swagger Docs
- **URL:** `/api/docs`
- **Method:** GET
- **Request:** `curl http://localhost:8000/api/docs`
- **Response:** 200 OK, Swagger UI
- **Tested:** Yes -- PASS

### OpenAPI Spec
- **URL:** `/api/openapi.json`
- **Method:** GET
- **Request:** `curl http://localhost:8000/api/openapi.json`
- **Response:** 200 OK, full OpenAPI 3.0 schema
- **Tested:** Yes -- PASS

### Get Tools
- **URL:** `/api/agent/tools`
- **Method:** GET
- **Request:** `curl http://localhost:8000/api/agent/tools`
- **Response:** `{"tools":[{"name":"image",...},{"name":"code",...},{"name":"sid",...}]}`
- **Tested:** Yes -- PASS

### Extract Metadata
- **URL:** `/api/metadata?url=<url>`
- **Method:** GET
- **Request:** `curl "http://localhost:8000/api/metadata?url=https://example.com"`
- **Response:** `{"title":null,"hostname":"example.com","favicon":"https://example.com/favicon.ico"}`
- **Tested:** Yes -- PASS

### Start Agent (auth required)
- **URL:** `/api/agent/start`
- **Method:** POST
- **Headers:** `Authorization: Bearer <token>`
- **Body:** `{"goal": "Create a business plan", "modelSettings": {"customModelName": "gpt-3.5-turbo"}}`
- **Response:** `{"run_id": "...", "newTasks": ["task1", "task2"]}`
- **Tested:** Auth enforcement verified (403 without token)

### Analyze Task (auth required)
- **URL:** `/api/agent/analyze`
- **Method:** POST
- **Body:** `{"goal": "...", "run_id": "...", "task": "...", "tool_names": ["search", "code"]}`

### Execute Task (auth required)
- **URL:** `/api/agent/execute`
- **Method:** POST
- **Body:** `{"goal": "...", "run_id": "...", "task": "...", "analysis": {"reasoning": "...", "action": "code", "arg": ""}}`
- **Response:** Streaming

### Create Tasks (auth required)
- **URL:** `/api/agent/create`
- **Method:** POST

### Summarize (auth required)
- **URL:** `/api/agent/summarize`
- **Method:** POST

### Chat (auth required)
- **URL:** `/api/agent/chat`
- **Method:** POST

### Get Models (auth required)
- **URL:** `/api/models`
- **Method:** GET
- **Models:** gpt-3.5-turbo (4k), gpt-3.5-turbo-16k (16k), gpt-4 (8k)

### Frontend
- **URL:** `http://localhost:3000`
- **Method:** GET (browser)
- **Tested:** Yes -- PASS (200 OK)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| REWORKD_PLATFORM_OPENAI_API_KEY | Yes | changeme | OpenAI API key |
| NEXTAUTH_SECRET | Yes | changeme | NextAuth session secret |
| REWORKD_PLATFORM_FF_MOCK_MODE_ENABLED | No | false | Enable mock agent mode (no API key needed) |
| REWORKD_PLATFORM_SERP_API_KEY | No | changeme | SerpAPI key for web search tool |
| REWORKD_PLATFORM_REPLICATE_API_KEY | No | changeme | Replicate key for image generation |
| GOOGLE_CLIENT_ID / SECRET | No | -- | Google OAuth |
| GITHUB_CLIENT_ID / SECRET | No | -- | GitHub OAuth |
| DISCORD_CLIENT_ID / SECRET | No | -- | Discord OAuth |

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Frontend GET / | PASS |
| 2 | Health GET /api/monitoring/health | PASS |
| 3 | Swagger GET /api/docs | PASS |
| 4 | OpenAPI GET /api/openapi.json | PASS |
| 5 | Tools GET /api/agent/tools | PASS |
| 6 | Metadata GET /api/metadata | PASS |
| 7 | Agent start POST /api/agent/start | PASS (403 auth enforced) |
| 8 | Models GET /api/models | PASS (403 auth enforced) |
| 9 | Error GET /api/monitoring/error | PASS (500 intentional) |

9/9 tests passed. Agent execution endpoints require OpenAI API key + auth token.

## Notes
- Development mode: frontend runs `npm run dev`, platform has hot reload enabled
- Auth uses NextAuth with Prisma adapter. In dev mode, sign-in is simplified
- Database auto-migrates on first frontend start via Prisma
- The `mock_mode` setting lets you test without an OpenAI key (returns fake agent responses)
