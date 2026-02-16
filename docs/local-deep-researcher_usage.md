# Local Deep Researcher -- Usage Documentation

## Overview
LangGraph-based research assistant that uses local LLMs via Ollama to conduct iterative web research. Searches the web using DuckDuckGo (no API key needed), summarizes findings, and generates research reports.

## Quick Start
```bash
docker pull hoomzoom/local-deep-researcher
docker run -d -p 2024:2024 -e OLLAMA_BASE_URL=http://host.docker.internal:11434/ hoomzoom/local-deep-researcher
```

API docs at http://localhost:2024/docs. Studio UI at the URL shown in container logs.

## Base URL
http://localhost:2024

## Core Features
- Iterative web research using local LLMs (Ollama)
- DuckDuckGo web search (no API key required)
- LangGraph dev server with full REST API
- Thread-based conversation management
- Configurable research depth and search parameters

## API Endpoints

### API Documentation
- **URL:** `/docs`
- **Method:** GET
- **Description:** OpenAPI documentation for the LangGraph API.
- **Request:** `curl http://localhost:2024/docs`
- **Tested:** Yes (200)

### Server Info
- **URL:** `/info`
- **Method:** GET
- **Description:** Server version and configuration.
- **Request:** `curl http://localhost:2024/info`
- **Response:** `{"version": "0.7.37", ...}`
- **Tested:** Yes (200)

### Search Assistants
- **URL:** `/assistants/search`
- **Method:** POST
- **Description:** List available research assistants.
- **Request:** `curl -X POST http://localhost:2024/assistants/search -H "Content-Type: application/json" -d '{}'`
- **Response:** List of assistants including `ollama_deep_researcher`.
- **Tested:** Yes (200)

### Create Thread
- **URL:** `/threads`
- **Method:** POST
- **Description:** Create a new research thread.
- **Request:** `curl -X POST http://localhost:2024/threads -H "Content-Type: application/json" -d '{}'`
- **Response:** `{"thread_id": "...", ...}`
- **Tested:** Yes (200)

### Run Research
- **URL:** `/threads/{thread_id}/runs`
- **Method:** POST
- **Description:** Start a research run on a thread. Requires a running Ollama instance with a model loaded.
- **Tested:** No (requires running Ollama instance)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OLLAMA_BASE_URL | Yes | http://localhost:11434/ | Ollama server URL |
| SEARCH_API | No | duckduckgo | Search provider (duckduckgo, tavily, perplexity) |
| TAVILY_API_KEY | No | None | Tavily API key (if using tavily search) |

## Notes
- Requires a running Ollama instance accessible from the container. Use `http://host.docker.internal:11434/` to connect to Ollama on the Docker host.
- DuckDuckGo search is the default and requires no API key.
- The LangGraph dev server is designed for development and testing, not production. Startup logs warn about using LangSmith Deployment for production.
- Uses `uvx` to bootstrap the LangGraph runtime at container startup, which downloads packages on first run. First startup is slow.
- The container runs as root.

## Changes from Original
No changes from original. The Dockerfile is used as provided by the developer.
