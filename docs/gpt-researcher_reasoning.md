# gpt-researcher -- Reasoning Log

## Initial Assessment

GPT Researcher is a FastAPI application that performs autonomous web research using LLMs. It has a well-structured multi-stage Dockerfile that bundles Chromium and Firefox for web scraping. The image is large but necessary for the scraping functionality.

## What Was Checked

1. **README.md**: Describes autonomous research capabilities. Requires OPENAI_API_KEY and TAVILY_API_KEY. Has both a web UI and REST API. WebSocket support for streaming research progress.

2. **Dockerfile**: Three-stage build. Stage 1 installs browsers (Chromium, Firefox) and their drivers. Stage 2 installs Python dependencies. Stage 3 creates non-root user, copies app, sets up uvicorn server. Uses `python:3.12-slim-bookworm` (no SHA256 pin, so no credential issues).

3. **requirements.txt and multi_agents/requirements.txt**: Two requirement files. The main one has LangChain, OpenAI, and web scraping deps. The multi_agents one has additional deps for collaborative research.

4. **OpenAPI spec**: 14 endpoints covering reports CRUD, file management, chat, and multi-agent research.

5. **Application structure**: `main.py` is the FastAPI entry point. Backend in `backend/` directory. Multi-agent system in `multi_agents/`. Frontend served from built static files.

## Decisions Made

### Used the existing Dockerfile as-is (with one minor change)
The Dockerfile is well-constructed with proper multi-stage build. No modifications needed except converting the CMD from shell form to exec form.

### Changed CMD to exec form
The original `CMD uvicorn main:app --host ${HOST} --port ${PORT} --workers ${WORKERS}` uses shell form, which wraps the command in `/bin/sh -c`. This means signals (like SIGTERM for graceful shutdown) go to the shell, not uvicorn. Exec form (`CMD ["uvicorn", ...]`) passes signals directly. This is a best practice fix. Since we use exec form, we hardcode the default values instead of using env var substitution (which only works in shell form).

### Did not add a healthcheck
The original Dockerfile has no healthcheck. Since this is a FastAPI app, we could add one, but following architectural fidelity we keep it as the developer intended.

## Testing

### Tests Performed
1. **Root endpoint** (GET `/`): Returns HTTP 200, serves the web UI. Pass.
2. **Swagger docs** (GET `/docs`): Returns HTTP 200, interactive API docs. Pass.
3. **List reports** (GET `/api/reports`): Returns `{"reports": []}`. Pass.
4. **List files** (GET `/files/`): Returns `{"files": []}`. Pass.
5. **Startup logs**: Clean startup, shows "GPT Researcher API ready - local mode (no database persistence)". Pass.

### What Was Not Tested
- Actual research (requires OPENAI_API_KEY and TAVILY_API_KEY)
- WebSocket streaming
- File upload
- Multi-agent research
- Report generation

## Gotchas

1. **Large image size**: The image is ~1.5 GB due to bundled browsers. This is expected and necessary for the scraping functionality.

2. **Two API keys required**: Unlike the Streamlit apps where keys are optional, GPT Researcher needs both OPENAI_API_KEY and TAVILY_API_KEY for its core research functionality. The app starts without them but cannot perform research.

3. **No SHA256 pin**: Unlike attackgen and stride-gpt, this Dockerfile uses `python:3.12-slim-bookworm` without a SHA256 pin, so it builds fine with BuildKit.

4. **Output persistence**: Research outputs are stored in `/usr/src/app/outputs/`. Without a volume mount, these are lost when the container stops.
