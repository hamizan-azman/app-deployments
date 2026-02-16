# GPT Researcher -- Usage Documentation

## Overview
FastAPI web application that conducts autonomous online research on any topic. Uses LLMs to plan research queries, scrapes web content with Chromium and Firefox, and generates comprehensive research reports.

## Quick Start
```bash
docker pull hoomzoom/gpt-researcher
docker run -d -p 8000:8000 -e OPENAI_API_KEY=your-key -e TAVILY_API_KEY=your-key hoomzoom/gpt-researcher
```

Open http://localhost:8000 in your browser for the web UI, or http://localhost:8000/docs for the API documentation.

## Base URL
http://localhost:8000

## Core Features
- Autonomous web research on any topic
- Multiple report types (research, detailed, resource, outline)
- Web scraping with Chromium and Firefox (bundled in image)
- WebSocket streaming for real-time research progress
- Multi-agent research mode
- File upload for source documents
- Chat with research reports

## API Endpoints

### Frontend
- **URL:** `/`
- **Method:** GET
- **Description:** Serves the built-in web research interface.
- **Tested:** Yes

### Swagger Docs
- **URL:** `/docs`
- **Method:** GET
- **Description:** Interactive API documentation.
- **Tested:** Yes

### List Reports
- **URL:** `/api/reports`
- **Method:** GET
- **Description:** Get all research reports.
- **Request:** `curl http://localhost:8000/api/reports`
- **Response:** `{"reports": []}`
- **Tested:** Yes

### Create Report
- **URL:** `/api/reports`
- **Method:** POST
- **Description:** Create or update a research report.
- **Request:** `curl -X POST http://localhost:8000/api/reports -H "Content-Type: application/json" -d '{"task": "research topic"}'`
- **Tested:** No (requires valid API key)

### Get Report
- **URL:** `/api/reports/{research_id}`
- **Method:** GET
- **Description:** Get a specific report by ID.
- **Tested:** No

### Generate Report (Legacy)
- **URL:** `/report/`
- **Method:** POST
- **Description:** Generate a research report (legacy endpoint).
- **Tested:** No (requires valid API key)

### List Files
- **URL:** `/files/`
- **Method:** GET
- **Description:** List uploaded source files.
- **Request:** `curl http://localhost:8000/files/`
- **Response:** `{"files": []}`
- **Tested:** Yes

### Upload File
- **URL:** `/upload/`
- **Method:** POST
- **Description:** Upload a source document for research.
- **Request:** `curl -X POST http://localhost:8000/upload/ -F "file=@document.pdf"`
- **Tested:** No

### Chat
- **URL:** `/api/chat`
- **Method:** POST
- **Description:** Chat endpoint for conversational research.
- **Tested:** No (requires valid API key)

### Multi-Agent Research
- **URL:** `/api/multi_agents`
- **Method:** POST
- **Description:** Run multi-agent collaborative research.
- **Tested:** No (requires valid API key)

### WebSocket
- **URL:** `ws://localhost:8000/ws`
- **Description:** WebSocket endpoint for real-time research streaming.
- **Tested:** No (requires valid API key)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for LLM calls |
| TAVILY_API_KEY | Yes | None | Tavily API key for web search |
| HOST | No | 0.0.0.0 | Server bind address |
| PORT | No | 8000 | Server port |
| WORKERS | No | 1 | Number of uvicorn workers |

## Notes
- The image is large (~1.5 GB) because it bundles Chromium, Firefox, and their drivers for web scraping.
- The container runs as non-root user `gpt-researcher`.
- Reports and outputs are stored in `/usr/src/app/outputs/` inside the container. Mount a volume to persist them.
- Both OPENAI_API_KEY and TAVILY_API_KEY are needed for full functionality. The app starts without them but research will fail.
- The web UI at `/` provides a user-friendly interface for conducting research.

## Changes from Original
- Changed CMD from shell form (`CMD uvicorn ...`) to exec form (`CMD ["uvicorn", ...]`) to handle signals properly. No functional change.
