# Devika -- Reasoning Log

## Initial Assessment

Devika is an open-source AI software engineer by stitionai. The repo has an existing Docker setup with two Dockerfiles (devika.dockerfile for the Flask-SocketIO backend, app.dockerfile for the Svelte frontend) and a docker-compose.yaml that ties them together with an Ollama service for local LLMs. The project is abandoned (last commit mid-2024) so dependency compatibility issues were expected.

## What Was Checked

1. **docker-compose.yaml (original)**: Three services. The backend builds from devika.dockerfile, the frontend from app.dockerfile, and Ollama pulls the official image. The backend depends on Ollama via a healthcheck. The frontend's VITE_API_BASE_URL is set to `http://localhost:1337` as a build arg. Services communicate over a shared Docker network.

2. **devika.dockerfile (original)**: Based on debian:12. Installs Python 3, installs `uv` via a curl script that downloads the installer, creates a venv, installs requirements.txt, installs Playwright with Chromium, copies source code, and runs `python3 -m devika`. The file also copies `config.toml` which does not exist in the repo (it is gitignored).

3. **app.dockerfile (original)**: Based on debian:12. Installs Node.js 20 via nodesource, copies UI source, runs npm install and installs bun. Also copies `config.toml` which doesn't exist. Runs the Svelte dev server via `npx bun run dev -- --host`.

4. **sample.config.toml**: Contains sections for storage paths, API keys (all placeholder values), API endpoints (Bing, Google, Ollama at localhost:11434, LM Studio, OpenAI), logging settings, and inference timeout.

5. **src/config.py**: The Config class constructor checks if config.toml exists, and if not, copies sample.config.toml to config.toml. This means the backend auto-creates its config on first run, so baking config.toml into the image is unnecessary.

6. **devika.py**: Flask-SocketIO application with 16 REST endpoints and 2 WebSocket events. The main interaction happens via the `user-message` socket event. The app loads tiktoken encoding and a BERT keyword extractor at startup.

7. **src/apis/project.py**: Blueprint with 5 project management endpoints (get files, create, delete, download zip, download PDF).

## Decisions Made

### Fixed uv installation method
The original Dockerfile installs uv with `curl -LsSf https://astral.sh/uv/install.sh | sh` and then references it at `$HOME/.cargo/bin/uv`. Newer versions of the uv installer place the binary at `~/.local/bin/uv` instead. Rather than guessing the current install path, we switched to `pip install uv --break-system-packages`, which puts uv on the system PATH reliably. This is simpler and avoids breakage from installer path changes.

### Removed config.toml COPY from both Dockerfiles
The original Dockerfiles both have `COPY config.toml ...`, but config.toml is listed in .gitignore and does not exist in the repo. The build fails at this step. For the backend, since config.py auto-creates config.toml from sample.config.toml at runtime, we removed the COPY entirely. For the frontend, the UI code reads config.toml for the API base URL, so we changed the COPY to use sample.config.toml as the source: `COPY sample.config.toml /home/nonroot/client/config.toml`.

### Added cairo system dependencies
The requirements.txt includes xhtml2pdf, which depends on pycairo. Building pycairo from source requires libcairo2-dev, pkg-config, and python3-dev. The original Dockerfile omits these, causing the build to fail with a meson build error for cairo. We added these three packages to the apt-get install line.

### Removed duplicate uv venv call
The original Dockerfile calls `uv venv` twice (once in the main setup and once later). The second call is redundant. We removed it.

### Kept the Svelte dev server as the frontend entrypoint
The original app.dockerfile runs `npx bun run dev -- --host`, which starts Vite's development server with hot reload. While a production build (`bun run build` + a static file server) would be more appropriate for deployment, the original developer designed the compose stack this way. Following architectural fidelity, we kept it as is.

### Rewrote docker-compose.yml for pre-built images
The original docker-compose.yaml builds from source using the Dockerfiles in the repo root. Our version uses the pre-built `hoomzoom/devika-backend` and `hoomzoom/devika-frontend` images from Docker Hub. We also added a health check for the Ollama service and a named volume for backend database persistence. The network and service structure remain the same.

### Ollama endpoint configuration
The sample.config.toml sets the Ollama endpoint to `http://127.0.0.1:11434`. When running in Docker Compose, the backend container needs to reach Ollama at the Docker service name instead. The config file created at runtime uses the sample defaults. Users who want to use Ollama with the compose setup need to update the Ollama endpoint in the UI settings to `http://ollama-service:11434`.

## Testing

### Tests Performed
1. **GET /api/status**: Returns 200 with `{"status":"server is running!"}`. Basic health check. Pass.
2. **GET /api/data**: Returns 200 with models list (Claude, Google, Groq, Mistral, Ollama, OpenAI providers), empty projects array, and search engines list. Pass.
3. **GET /api/settings**: Returns 200 with full config.toml contents as JSON. Pass.
4. **POST /api/settings**: Returns 200 with `{"message":"Settings updated"}`. Pass.
5. **GET /api/logs**: Returns 200 with log content. Pass.
6. **POST /api/messages**: Returns 200 with `{"messages":[]}` for non-existent project. Pass.
7. **POST /api/is-agent-active**: Returns 200 with `{"is_active":false}`. Pass.
8. **POST /api/get-agent-state**: Returns 200 with `{"state":null}`. Pass.
9. **POST /api/calculate-tokens**: Returns 200 with correct token count. Pass.
10. **GET /api/token-usage**: Returns 200 with `{"token_usage":0}`. Pass.
11. **GET /api/get-project-files**: Returns 200 with file list. Pass.
12. **POST /api/create-project**: Returns 200, creates project directory. Pass.
13. **POST /api/delete-project**: Returns 200, removes project. Pass.
14. **GET /api/get-browser-session**: Returns 200 with `{"session":null}`. Pass.
15. **GET /api/get-terminal-session**: Returns 200 with `{"terminal_state":null}`. Pass.
16. **POST /api/run-code**: Returns 200 with `{"message":"Code execution started"}`. The endpoint is a stub in the source code. Pass.

### What Was Not Tested
- WebSocket `user-message` event (requires valid LLM API key)
- WebSocket `socket_connect` event (requires Socket.IO client)
- GET /api/download-project and /api/download-project-pdf (require project with generated files)
- GET /api/get-browser-snapshot (requires active agent session with screenshots)
- Frontend Svelte application (tested via compose only)
- Ollama integration (requires pulling a model into the Ollama container)

## Build Issues Encountered

### uv path change (exit code 127)
The first build attempt failed with `/root/.cargo/bin/uv: not found`. The uv project changed its default install location from `~/.cargo/bin/` to `~/.local/bin/` in a newer release. Since the installer script is fetched at build time, the Dockerfile's hardcoded path broke. Switching to `pip install uv` resolved this permanently.

### Missing config.toml (COPY failure)
Both Dockerfiles try to COPY config.toml, which is gitignored and absent from the repo. This is a bug in the original Dockerfiles. The developer presumably had a local config.toml when they built the images. Fixed by removing the backend COPY (auto-created at runtime) and changing the frontend COPY to use sample.config.toml.

### pycairo build failure (missing cairo dev headers)
The xhtml2pdf package requires pycairo, which compiles against libcairo2. The original Dockerfile does not install the cairo development headers. This is another oversight in the original Dockerfiles. Added libcairo2-dev, pkg-config, and python3-dev to the apt-get install.

### TLS handshake timeout
One build attempt failed pulling the debian:12 base image due to a TLS handshake timeout. This was a transient network issue, resolved by retrying.

### Long build time
The backend build takes approximately 37 minutes due to the large requirements.txt (includes PyTorch dependencies for the BERT model), Playwright browser installation, and a lengthy `chown -R` on the entire working directory. This is expected for an image of this complexity.

## Gotchas

1. **No API key required at startup**: Unlike TaskWeaver, devika starts without any API keys configured. Keys are entered through the web UI settings page after startup. DuckDuckGo search works without any API key.

2. **BERT model download on first run**: The backend loads a KeyBERT model on startup. This happens inside the container and takes a few seconds. The model is cached in the container's filesystem.

3. **Frontend dev server**: The frontend runs Vite's dev server, not a production build. This means it hot-reloads on file changes, which is unnecessary in a Docker deployment but is how the original developer set things up.

4. **Ollama endpoint mismatch**: The auto-created config.toml sets Ollama to localhost:11434, but in docker-compose it needs to be ollama-service:11434. Users need to update this in the UI settings if they want to use local models.

5. **Database persistence**: The backend stores project data in an SQLite database at `/home/nonroot/devika/db/`. The docker-compose.yml maps this to a named volume so data persists across container restarts.

6. **Code execution**: The `/api/run-code` endpoint is a stub (returns a success message but does nothing). Actual code execution happens through the agent's internal code generation pipeline, which writes files to the project directory and may run commands via subprocess.

7. **Browser automation**: Playwright with Chromium is installed in the backend image for web research capabilities. This adds significant image size but is core to devika's functionality.
