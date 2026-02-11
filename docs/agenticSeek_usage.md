# agenticSeek. Usage Documentation

## Overview
AI-powered assistant with multiple specialized agents (casual chat, coding, file management, web browsing, planning). Uses OpenAI API with SearxNG for web search, Selenium/Chrome for browser automation, and Redis for task queue. React frontend provides chat interface.

## Quick Start
```bash
# Clone repo (needed for docker-compose.yml and config files)
git clone https://github.com/Fosowl/agenticSeek
cd agenticSeek

# Create .env. replace YOUR_OPENAI_KEY with your actual OpenAI API key
cat > .env <<EOF
SEARXNG_SECRET_KEY=supersecretkey123
SEARXNG_BASE_URL=http://searxng:8080
REDIS_BASE_URL=redis://redis:6379/0
BACKEND_PORT=7777
OPENAI_API_KEY=YOUR_OPENAI_KEY
EOF

# Edit config.ini: set provider to openai, model to gpt-4o-mini, is_local=False
# See config.ini section below

# Build and run all 4 services
docker compose --profile full up --build -d
```

## Docker Pull (pre-built)
```bash
docker pull hoomzoom/agenticseek-backend:latest
docker pull hoomzoom/agenticseek-frontend:latest
```

## Architecture
| Service | Image | Port | Description |
|---------|-------|------|-------------|
| Backend | agenticseek-backend | 7777 | FastAPI + Selenium + Chrome |
| Frontend | agenticseek-frontend | 3000 | React chat UI |
| SearxNG | searxng/searxng:latest | 8080 | Web search engine |
| Redis | valkey/valkey:8-alpine | (internal) | Celery task broker |

## Base URL
- Backend: http://localhost:7777
- Frontend: http://localhost:3000
- SearxNG: http://localhost:8080

## Core Features
- Multi-agent system: Jarvis (casual), Coder, File Agent, Browser, Planner
- Web search via SearxNG
- Browser automation via headless Chrome/Selenium
- Code execution
- File management
- Automatic agent routing based on query type

## API Endpoints

### Health Check
- **URL:** `/health`
- **Method:** GET
- **Description:** Check if backend is running
- **Request:** `curl http://localhost:7777/health`
- **Response:** `{"status":"healthy","version":"0.1.0"}`
- **Tested:** Yes

### Is Active
- **URL:** `/is_active`
- **Method:** GET
- **Description:** Check if an agent is currently processing
- **Request:** `curl http://localhost:7777/is_active`
- **Response:** `{"is_active":true}`
- **Tested:** Yes

### Submit Query
- **URL:** `/query`
- **Method:** POST
- **Description:** Send a query to the agent system. Routes to appropriate agent automatically.
- **Request:** `curl -X POST http://localhost:7777/query -H "Content-Type: application/json" -d '{"query": "What is 2+2?"}'`
- **Response:**
```json
{
  "done": "true",
  "answer": "2 + 2 equals 4!",
  "reasoning": "",
  "agent_name": "Jarvis",
  "success": "True",
  "blocks": {},
  "status": "Ready",
  "uid": "uuid-string"
}
```
- **Tested:** Yes

### Latest Answer
- **URL:** `/latest_answer`
- **Method:** GET
- **Description:** Get the most recent agent response
- **Request:** `curl http://localhost:7777/latest_answer`
- **Response:** Same schema as /query response
- **Tested:** Yes

### Screenshot
- **URL:** `/screenshot`
- **Method:** GET
- **Description:** Get latest browser screenshot (from Browser agent)
- **Request:** `curl http://localhost:7777/screenshot`
- **Response:** PNG image file, or 404 if no screenshot available
- **Tested:** Yes (returns 404 when no screenshot exists, 200 after browser activity)

### Stop
- **URL:** `/stop`
- **Method:** GET
- **Description:** Stop the currently running agent task
- **Request:** `curl http://localhost:7777/stop`
- **Response:** `{"status": "stopped"}`
- **Tested:** Yes (returns 500 when no agent is active, which is expected)

## config.ini
```ini
[MAIN]
is_local = False
provider_name = openai
provider_model = gpt-4o-mini
provider_server_address = api.openai.com
agent_name = Jarvis
recover_last_session = False
save_session = False
speak = False
listen = False
jarvis_personality = False
languages = en
[BROWSER]
headless_browser = True
stealth_mode = False
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | OpenAI API key |
| SEARXNG_BASE_URL | No | http://searxng:8080 | SearxNG instance URL |
| SEARXNG_SECRET_KEY | No | - | SearxNG secret key |
| REDIS_BASE_URL | No | redis://redis:6379/0 | Redis connection URL |
| BACKEND_PORT | No | 7777 | Backend API port |
| DEEPSEEK_API_KEY | No | - | DeepSeek API key (alternative provider) |
| OPENROUTER_API_KEY | No | - | OpenRouter API key (alternative provider) |
| TOGETHER_API_KEY | No | - | Together API key (alternative provider) |
| GOOGLE_API_KEY | No | - | Google API key (alternative provider) |
| ANTHROPIC_API_KEY | No | - | Anthropic API key (alternative provider) |
| HUGGINGFACE_API_KEY | No | - | HuggingFace API key (alternative provider) |

## Notes
- Backend takes 2-3 minutes to start (loads zero-shot classification pipeline and LLM router model on CPU)
- Default config uses ollama. must change to openai in config.ini for Docker deployment
- The /query endpoint blocks until the agent finishes (can be 10-60+ seconds for complex queries)
- Only one query can be processed at a time (returns 429 if busy)
- Browser agent runs headless Chrome inside the container
- Backend image is ~15.8GB due to PyTorch, Chrome, and ML models
- Frontend image is ~2.1GB (Node.js + React)

## V2 Dependency Changes (Minimum Version Pinning)
- `playsound3>=1.0.0` bumped to `playsound3==3.0.0` (1.0.0 doesn't exist on PyPI. 2.0.0 requires pygobject/Cairo system deps)
- `together>=1.5.0` bumped to `together==1.5.2` (1.5.0 doesn't exist on PyPI)
- `tqdm>=4` bumped to `tqdm==4.66.2` (together 1.5.2 requires tqdm>=4.66.2)

## Changes from Original
**Category: Modified.** Configuration file changed.

| File | Change | Why |
|------|--------|-----|
| `config.ini` | `is_local = True` changed to `is_local = False` | Docker deployment uses remote API, not local Ollama |
| `config.ini` | `provider_name = ollama` changed to `provider_name = openai` | Same reason |
| `config.ini` | `provider_model = deepseek-r1:14b` changed to `provider_model = gpt-4o-mini` | Use available model |
| `config.ini` | `provider_server_address = 127.0.0.1:11434` changed to `provider_server_address = api.openai.com` | Point to OpenAI API |

Config-only changes selecting LLM provider. All application code unchanged.
