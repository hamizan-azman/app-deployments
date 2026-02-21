# django-ai-assistant -- Usage Documentation

## Overview
Django app integrating LangChain/LangGraph AI assistants with a web UI. Includes example assistants for weather, movies, issue tracking, RAG, and tour guide. React frontend with Mantine UI.

## Quick Start

```bash
docker pull hoomzoom/django-ai-assistant
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... hoomzoom/django-ai-assistant
```

## Base URL
- Web UI: `http://localhost:8000`
- Admin: `http://localhost:8000/admin/` (admin/admin)

## Core Features
- Multiple AI assistants (weather, movies, RAG, tour guide, issue tracker)
- Thread-based conversation management
- Tool calling support (web search, weather API, etc.)
- React frontend with Mantine components
- HTMX fallback for non-JS browsers

## API Endpoints

### List Assistants
- **URL:** `/ai-assistant/assistants/`
- **Method:** GET
- **Request:** `curl -b sessionid=... http://localhost:8000/ai-assistant/assistants/`
- **Tested:** Yes

### List Threads
- **URL:** `/ai-assistant/threads/`
- **Method:** GET
- **Request:** `curl -b sessionid=... http://localhost:8000/ai-assistant/threads/`
- **Tested:** Yes

### Create Thread
- **URL:** `/ai-assistant/threads/`
- **Method:** POST
- **Request:** `curl -X POST -b sessionid=... -H "Content-Type: application/json" -d '{"name":"test","assistant_id":"weather_assistant"}' http://localhost:8000/ai-assistant/threads/`
- **Tested:** Yes

### Send Message
- **URL:** `/ai-assistant/threads/{id}/messages/`
- **Method:** POST
- **Request:** `curl -X POST -b sessionid=... -H "Content-Type: application/json" -d '{"content":"Hello"}' http://localhost:8000/ai-assistant/threads/1/messages/`
- **Tested:** No (requires OPENAI_API_KEY)

### Delete Thread
- **URL:** `/ai-assistant/threads/{id}/`
- **Method:** DELETE
- **Tested:** Yes

## Authentication
All API endpoints require Django session authentication. Log in via admin panel or use session cookie.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for AI assistants |
| WEATHER_API_KEY | No | None | weatherapi.com key for weather assistant |
| BRAVE_SEARCH_API_KEY | No | None | Brave Search for RAG assistant |
| JINA_API_KEY | No | None | Jina for web scraping in RAG |

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | Server startup (runserver) | PASS |
| 2 | Admin panel loads | PASS |
| 3 | Frontend React app loads | PASS |
| 4 | List assistants API | PASS |
| 5 | Create/delete thread | PASS |
| 6 | Send message (LLM call) | NOT TESTED (requires API key) |

## V2 Dependency Changes (Minimum Version Pinning)
- `openai ^1.48.0` bumped to `openai==1.109.1` (langchain-openai==1.1.7 requires openai>=1.109.1)
- Removed `init_command` and `transaction_mode` from Django sqlite3 settings (Django 5.1+ features, incompatible with Django 4.2)
- Dockerfile changed from `python:3.12-slim` to `python:3.11-slim` for compatibility
- Added `poetry lock` step in Dockerfile to regenerate lock file after pinning

## Notes
- Default superuser: admin/admin (created during build).
- SQLite database (created at build time with migrations).
- Frontend is pre-built with webpack (production mode).
- Debug mode is on by default (ALLOWED_HOSTS accepts all).
