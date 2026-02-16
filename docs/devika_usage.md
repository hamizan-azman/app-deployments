# Devika -- Usage Documentation

## Overview
Devika is an AI software engineer that can understand high-level instructions, break them into steps, research relevant information, and write code. It uses a multi-agent architecture with planning, coding, and browser automation capabilities. The system consists of a Flask-SocketIO backend, a Svelte frontend, and an optional Ollama service for local LLMs.

## Quick Start

```bash
docker pull hoomzoom/devika-backend
docker pull hoomzoom/devika-frontend
```

Download the docker-compose.yml and .env.example from the `dockerfiles/devika/` directory, then:

```bash
docker compose up
```

This starts three services:
- Backend on port 1337
- Frontend on port 3000
- Ollama on port 11434

## Base URL
- Backend API: `http://localhost:1337`
- Frontend UI: `http://localhost:3000`

## Core Features
- AI-powered software engineering agent
- Multi-model support (OpenAI, Claude, Gemini, Mistral, Groq, Ollama)
- Web search (Bing, Google, DuckDuckGo)
- Browser automation via Playwright
- Project file management and code generation
- Token usage tracking

## API Endpoints

### Server Status
- **URL:** `/api/status`
- **Method:** GET
- **Description:** Health check endpoint.
- **Request:** `curl http://localhost:1337/api/status`
- **Response:** `{"status":"server is running!"}`
- **Tested:** Yes

### Get Data
- **URL:** `/api/data`
- **Method:** GET
- **Description:** Returns available models, projects, and search engines.
- **Request:** `curl http://localhost:1337/api/data`
- **Response:** `{"models":{...},"projects":[],"search_engines":["Bing","Google","DuckDuckGo"]}`
- **Tested:** Yes

### Get Settings
- **URL:** `/api/settings`
- **Method:** GET
- **Description:** Returns current configuration from config.toml.
- **Request:** `curl http://localhost:1337/api/settings`
- **Response:** `{"settings":{...}}`
- **Tested:** Yes

### Update Settings
- **URL:** `/api/settings`
- **Method:** POST
- **Description:** Updates configuration values.
- **Request:** `curl -X POST http://localhost:1337/api/settings -H "Content-Type: application/json" -d '{"API_KEYS": {"OPENAI": "sk-your-key"}}'`
- **Response:** `{"message":"Settings updated"}`
- **Tested:** Yes

### Get Logs
- **URL:** `/api/logs`
- **Method:** GET
- **Description:** Returns real-time server logs.
- **Request:** `curl http://localhost:1337/api/logs`
- **Response:** `{"logs":"..."}`
- **Tested:** Yes

### Get Messages
- **URL:** `/api/messages`
- **Method:** POST
- **Description:** Returns message history for a project.
- **Request:** `curl -X POST http://localhost:1337/api/messages -H "Content-Type: application/json" -d '{"project_name":"my-project"}'`
- **Response:** `{"messages":[...]}`
- **Tested:** Yes

### Check Agent Active
- **URL:** `/api/is-agent-active`
- **Method:** POST
- **Description:** Checks if the agent is currently running for a project.
- **Request:** `curl -X POST http://localhost:1337/api/is-agent-active -H "Content-Type: application/json" -d '{"project_name":"my-project"}'`
- **Response:** `{"is_active":false}`
- **Tested:** Yes

### Get Agent State
- **URL:** `/api/get-agent-state`
- **Method:** POST
- **Description:** Returns the latest agent state for a project.
- **Request:** `curl -X POST http://localhost:1337/api/get-agent-state -H "Content-Type: application/json" -d '{"project_name":"my-project"}'`
- **Response:** `{"state":null}`
- **Tested:** Yes

### Calculate Tokens
- **URL:** `/api/calculate-tokens`
- **Method:** POST
- **Description:** Counts tokens in a prompt using tiktoken.
- **Request:** `curl -X POST http://localhost:1337/api/calculate-tokens -H "Content-Type: application/json" -d '{"prompt":"Hello world"}'`
- **Response:** `{"token_usage":2}`
- **Tested:** Yes

### Get Token Usage
- **URL:** `/api/token-usage`
- **Method:** GET
- **Description:** Returns token usage for a project.
- **Request:** `curl "http://localhost:1337/api/token-usage?project_name=my-project"`
- **Response:** `{"token_usage":0}`
- **Tested:** Yes

### Get Project Files
- **URL:** `/api/get-project-files`
- **Method:** GET
- **Description:** Lists files in a project directory.
- **Request:** `curl "http://localhost:1337/api/get-project-files?project_name=my-project"`
- **Response:** `{"files":[...]}`
- **Tested:** Yes

### Create Project
- **URL:** `/api/create-project`
- **Method:** POST
- **Description:** Creates a new project.
- **Request:** `curl -X POST http://localhost:1337/api/create-project -H "Content-Type: application/json" -d '{"project_name":"my-project"}'`
- **Response:** `{"message":"Project created"}`
- **Tested:** Yes

### Delete Project
- **URL:** `/api/delete-project`
- **Method:** POST
- **Description:** Deletes a project.
- **Request:** `curl -X POST http://localhost:1337/api/delete-project -H "Content-Type: application/json" -d '{"project_name":"my-project"}'`
- **Response:** `{"message":"Project deleted"}`
- **Tested:** Yes

### Download Project
- **URL:** `/api/download-project`
- **Method:** GET
- **Description:** Downloads project files as a zip archive.
- **Request:** `curl "http://localhost:1337/api/download-project?project_name=my-project" -o project.zip`
- **Tested:** No (requires existing project with files)

### Download Project PDF
- **URL:** `/api/download-project-pdf`
- **Method:** GET
- **Description:** Downloads project files as a PDF document.
- **Request:** `curl "http://localhost:1337/api/download-project-pdf?project_name=my-project" -o project.pdf`
- **Tested:** No (requires existing project with files)

### Get Browser Snapshot
- **URL:** `/api/get-browser-snapshot`
- **Method:** GET
- **Description:** Downloads a browser screenshot taken during agent execution.
- **Request:** `curl "http://localhost:1337/api/get-browser-snapshot?snapshot_path=/path/to/snapshot.png" -o snapshot.png`
- **Tested:** No (requires active agent session)

### Get Browser Session
- **URL:** `/api/get-browser-session`
- **Method:** GET
- **Description:** Returns browser session data for a project.
- **Request:** `curl "http://localhost:1337/api/get-browser-session?project_name=my-project"`
- **Response:** `{"session":null}`
- **Tested:** Yes

### Get Terminal Session
- **URL:** `/api/get-terminal-session`
- **Method:** GET
- **Description:** Returns terminal session data for a project.
- **Request:** `curl "http://localhost:1337/api/get-terminal-session?project_name=my-project"`
- **Response:** `{"terminal_state":null}`
- **Tested:** Yes

### Run Code
- **URL:** `/api/run-code`
- **Method:** POST
- **Description:** Executes code in a project context (stub, not fully implemented in source).
- **Request:** `curl -X POST http://localhost:1337/api/run-code -H "Content-Type: application/json" -d '{"project_name":"my-project","code":"print(1)"}'`
- **Response:** `{"message":"Code execution started"}`
- **Tested:** Yes

### WebSocket: User Message
- **Event:** `user-message`
- **Description:** Sends a task to the AI agent via Socket.IO. This is the primary interaction method.
- **Payload:** `{"message":"build a todo app","base_model":"gpt-4","project_name":"my-project","search_engine":"duckduckgo"}`
- **Tested:** No (requires valid LLM API key)

## Environment Variables

API keys and settings are configured through the web UI settings page or by editing `config.toml` directly. The config file is auto-created from `sample.config.toml` on first run.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (via UI) | No | None | OpenAI, Claude, Gemini, Mistral, Groq API keys |
| (via UI) | No | None | Bing, Google Search API keys |
| (via UI) | No | DuckDuckGo | Search engine selection |

When using docker-compose, the Ollama endpoint is pre-configured to `http://ollama-service:11434`.

## Security Warning
Devika executes arbitrary code and commands inside the backend container via Playwright browser automation and code generation. Do not expose the backend to untrusted networks. The `/api/run-code` endpoint (currently a stub) is designed to execute arbitrary code.

## Notes
- The backend loads a BERT keyword extraction model on first startup, which takes a few seconds.
- DuckDuckGo search works without any API key. For Bing or Google search, configure keys in the UI.
- For local LLMs, Ollama is included in the compose file. Pull models with `docker exec <ollama-container> ollama pull <model>`.
- The frontend dev server runs via `bun` and hot-reloads. This is the original developer's setup.
- Project data is persisted in the `devika-backend-dbstore` Docker volume.

## Changes from Original
- **devika.dockerfile**: Replaced `uv` installation via curl script with `pip install uv` to avoid path issues with newer uv versions. Removed `COPY config.toml` (config.toml is gitignored and auto-created at runtime from sample.config.toml). Added `libcairo2-dev`, `pkg-config`, and `python3-dev` to apt dependencies for pycairo/xhtml2pdf support. Removed duplicate `uv venv` call.
- **app.dockerfile**: Changed `COPY config.toml` to `COPY sample.config.toml /home/nonroot/client/config.toml` since config.toml does not exist in the repo.
- **docker-compose.yml**: Rewrote to use pre-built `hoomzoom/` images instead of building from source. Added health checks for backend and Ollama services. Added named volume for backend database persistence.
