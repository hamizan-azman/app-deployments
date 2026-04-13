# screenshot-to-code. Reasoning Log

## Initial Assessment

screenshot-to-code converts UI screenshots to HTML/CSS code using vision LLMs. It is a two-container application: a Python FastAPI backend and a React/Vite frontend. The upstream repo has no Dockerfile, so both were written from scratch.

## What Was Checked

1. **README.md**: Documents running the app in development mode. Backend uses Poetry. Frontend uses yarn. The primary user-facing feature is drag-and-drop an image and receive generated code.

2. **backend/pyproject.toml**: Python backend with Poetry. FastAPI application. Main entry is `main:app` run via uvicorn on port 7001.

3. **frontend/package.json**: Node.js frontend with Vite and React. `yarn dev` starts the dev server. `yarn dev --host 0.0.0.0` enables external access.

4. **WebSocket architecture**: The primary code generation flow uses a WebSocket connection (`/generate-code`). The Vite dev server proxies WebSocket connections to the backend. `VITE_WS_BACKEND_URL` must be set to the backend WebSocket URL accessible from the browser.

5. **PUPPETEER_SKIP_DOWNLOAD**: Puppeteer is listed as a dependency but browser automation is not needed for core functionality. Setting `PUPPETEER_SKIP_DOWNLOAD=true` prevents the 200MB Chromium download at install time.

## Decisions Made

### Two separate containers with compose
The backend (Python/FastAPI) and frontend (Node/Vite) are fundamentally different runtimes. Keeping them separate follows the upstream architecture and the architectural fidelity rule. The compose file wires them together on a shared network.

### Backend: Poetry with python:3.12.3-slim-bullseye
The backend pyproject.toml specifies a Poetry project. Using `poetry install --only main` installs only production dependencies. `python:3.12.3-slim-bullseye` is used rather than a generic 3.12-slim to match the Python version tested upstream.

### Frontend: node:22-bullseye-slim with yarn dev
The frontend is served via `yarn dev --host 0.0.0.0`. This is the upstream development workflow. For a research deployment, the dev server is appropriate. Using node:22-bullseye-slim provides a recent Node.js LTS release.

### VITE_WS_BACKEND_URL=ws://localhost:7001
The WebSocket URL is set to `localhost:7001`, meaning the browser connects directly to the backend, not through the frontend container. This is the correct pattern for a dev server setup where the frontend serves the JS bundle but WebSocket traffic goes directly to the backend.

### Backend healthcheck on /docs
FastAPI /docs is served immediately on startup without requiring any model or API key initialization. It is the most reliable indicator that the backend is ready to accept connections.

## Testing

### Tests Performed
1. **Backend health** (GET `http://localhost:7001/docs`): Returns HTTP 200. Swagger UI loads. Pass.
2. **Frontend** (http://localhost:5173): Returns HTTP 200. React application loads. Pass.
3. **Compose startup**: Frontend waits for backend healthcheck before starting. Pass.

### What Was Not Tested
- Code generation (requires valid OpenAI or Anthropic vision API key)
- WebSocket streaming
- Figma import integration

## Gotchas

1. **VITE_WS_BACKEND_URL is set at build time**: The Vite dev server bundles the WebSocket URL into the JavaScript at build time (or applies it via environment at startup). If the backend is on a non-standard port or host, this must be changed before building the frontend image.

2. **Poetry virtualenvs.create false**: The Dockerfile sets `poetry config virtualenvs.create false` so packages install into the system Python environment rather than a virtualenv. This is necessary because there is no activation step in the Docker entrypoint.

3. **Non-root user in backend**: The non-root user is created after pip install to avoid permission issues. Files are chowned to appuser after copy.

4. **Frontend uses dev server**: `yarn dev` is appropriate for research but not production. The dev server has no gzip compression and no production optimizations. For a production deployment, `yarn build` and a static file server would be more appropriate.
