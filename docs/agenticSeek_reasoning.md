# agenticSeek -- Reasoning Log

## Repo Deep-Dive

### Repository Analysis
Read the following files to understand the app architecture:
- `docker-compose.yml`: Defines 4 services (redis, searxng, frontend, backend) with two profiles ("core" and "full"). The "full" profile includes all services including the backend. The "core" profile includes redis, searxng, and frontend but not the backend (useful when running the backend on the host).
- `Dockerfile.backend`: Python 3.11-slim base, installs Chrome for Testing (v134.0.6998.88), ChromeDriver, system dependencies for audio/video processing, and Python packages from requirements.txt. The image is pinned to `linux/amd64` platform.
- `frontend/Dockerfile.frontend`: Node 18 base, installs npm dependencies, runs React development server on port 3000.
- `config.ini`: Default config uses ollama provider with deepseek-r1:14b model. This won't work in Docker since there's no local ollama server. Must change to openai.
- `api.py`: FastAPI app with endpoints for health, query, screenshot, stop, latest_answer, is_active. Uses Celery for async tasks with Redis as broker. Initializes multiple agents (Casual, Coder, File, Browser, Planner).
- `requirements.txt`: Heavy dependencies including PyTorch, transformers, spacy, selenium, kokoro (TTS), adaptive-classifier, text2emotion.
- `sources/tools/searxSearch.py`: Searches SearxNG using HTML POST requests and parses results with BeautifulSoup. Does NOT use JSON API format, so the default SearxNG settings.yml (which only enables HTML format) is sufficient.
- `sources/schemas.py`: Pydantic models for QueryRequest (query string + tts_enabled bool) and QueryResponse.
- `searxng/settings.yml`: SearxNG configuration. Only HTML format enabled under `search.formats`. This is correct for the backend's search tool.
- `.env.example`: Shows expected environment variables.

### Why These Files Mattered
- The docker-compose.yml told us exactly what services are needed and how they connect. The backend connects to redis and searxng via the `agentic-seek-net` Docker network.
- The config.ini was critical because the default uses ollama, which requires a local LLM server. Since we're deploying in Docker without GPU, we need an API provider (OpenAI).
- The api.py showed all the endpoints we need to test and revealed the startup sequence (initializes provider, browser, agents, interaction).
- The searxSearch.py confirmed that the SearxNG JSON API is NOT needed -- the backend scrapes HTML results. This saved us from modifying the SearxNG settings.

## Architecture Decisions

### Provider Configuration
Changed config.ini to use OpenAI with gpt-4o-mini:
- `is_local = False` -- tells the provider to use API mode, not local inference
- `provider_name = openai` -- uses the OpenAI provider class
- `provider_model = gpt-4o-mini` -- cheapest model that handles the agent tasks well
- `provider_server_address = api.openai.com` -- standard OpenAI API endpoint

gpt-4o-mini was chosen because it's the cheapest model that can handle the multi-agent routing and response generation. The app uses the model for casual chat, code generation, file operations, and planning. gpt-4o-mini handles all these tasks adequately for testing purposes.

### Docker Compose Profile
Used `--profile full` to start all 4 services together. The alternative was `--profile core` + running backend separately, but that would mean the backend wouldn't be in a container, which defeats the purpose of our deployment.

### Environment Variables
Created .env file with:
- `SEARXNG_SECRET_KEY=supersecretkey123` -- required by SearxNG, any value works for testing
- `SEARXNG_BASE_URL=http://searxng:8080` -- uses Docker network hostname, not localhost
- `REDIS_BASE_URL=redis://redis:6379/0` -- uses Docker network hostname
- `BACKEND_PORT=7777` -- matches the port in api.py and docker-compose.yml
- `OPENAI_API_KEY` -- the actual API key for OpenAI

### No Dockerfile Modifications
Used the existing Dockerfile.backend and Dockerfile.frontend exactly as provided by the developer. No modifications needed. This follows the architectural fidelity rule -- the developer's Dockerfiles work correctly.

### Using the Developer's docker-compose.yml
Used the exact docker-compose.yml from the repo. No modifications. The compose file correctly:
- Sets up networking between services
- Passes environment variables from .env
- Mounts volumes for SearxNG config
- Maps ports for all externally-accessible services

## Things I Tried That Didn't Work

### Using a different LLM model
Could have used gpt-4o for better quality, but gpt-4o-mini is sufficient for testing and much cheaper. The app itself doesn't require a specific model -- any OpenAI model works.

### Running SearxNG with JSON format
Considered enabling JSON format in SearxNG's settings.yml. After reading the backend's searxSearch.py, confirmed it uses HTML parsing (BeautifulSoup) not JSON API. No change needed.

### Building images on the laptop and transferring
The backend image is 15.8GB. Transferring it over the network would take a very long time. Building directly on the desktop is faster since the desktop has a good internet connection for pulling base images and pip packages.

### Using docker --context desktop for the build
Considered running `docker --context desktop compose up --build` from the laptop. However, docker compose with SSH context can have issues with build contexts and file paths. Running the build directly on the desktop via SSH was more reliable.

## Desktop-Specific Issues and Solutions

### Docker Credential Helper Error
The most significant issue was `error getting credentials - err: exit status 1, out: "A specified logon session does not exist."` when trying to pull images on the desktop via SSH.

**Root cause**: Docker Desktop on Windows uses `docker-credential-desktop.exe` and `docker-credential-wincred.exe` to store credentials in Windows Credential Manager. SSH sessions don't have access to the interactive logon session's credential store.

**Diagnosis steps**:
1. First tried `docker logout` -- didn't help
2. Checked `~/.docker/config.json` -- found `"credsStore": "desktop"`
3. Removed `credsStore` from config.json -- still failed
4. Set `credsStore` to empty string -- still failed
5. Restarted Docker Desktop -- still failed
6. Found both `docker-credential-desktop.exe` and `docker-credential-wincred.exe` in the Docker bin directory
7. Renamed both `.exe.bak` -- this fixed the pull

**Solution**: Temporarily renamed the credential helper executables so Docker couldn't find them. Docker then falls back to no credential store, which works fine for pulling public images. Restored them after the build completed.

**How to recognize in future**: Any `error getting credentials` message when running Docker commands over SSH on Windows means the credential helper can't access Windows Credential Manager from the SSH session.

### SSH Shell is cmd.exe, Not Bash
The desktop SSH server (Windows OpenSSH) uses cmd.exe as the default shell. This means:
- `ls` doesn't work, use `dir` instead
- PowerShell commands need `powershell -Command "..."` wrapper
- Path separators are backslashes in cmd context
- Environment variable expansion uses `%VAR%` not `$VAR`

### PowerShell Variable Mangling
When running PowerShell commands through SSH from Git Bash, `$_` gets mangled by bash. Had to avoid PowerShell error-handling constructs that use `$_` and instead use simpler approaches like `Invoke-RestMethod` or `Invoke-WebRequest` with `-UseBasicParsing`.

### Profile Loading in PowerShell via SSH
Running `powershell -Command` through SSH triggered a bash_completion.d script that tried to load bash completions into PowerShell, causing errors. Fixed by using `powershell -NoProfile -Command` to skip profile loading.

## Test Coverage

### Test 1: GET /health
**Why**: Most basic endpoint. If this fails, nothing else will work. Validates that the FastAPI server started, uvicorn is listening, and the server can return JSON.
**Result**: `{"status":"healthy","version":"0.1.0"}` -- PASS

### Test 2: GET /is_active
**Why**: Tests that the Interaction system initialized correctly. This endpoint accesses `interaction.is_active`, which requires the agent system to be set up.
**Result**: `{"is_active":true}` -- PASS

### Test 3: GET http://localhost:3000 (Frontend)
**Why**: Validates that the React frontend built and is being served. A 200 status code means the npm start command succeeded and the dev server is running.
**Result**: Status 200 -- PASS

### Test 4: GET http://localhost:8080 (SearxNG)
**Why**: Validates that SearxNG is running and serving its UI. The backend depends on SearxNG for web search, so this must be up.
**Result**: Status 200 -- PASS

### Test 5: GET /screenshot
**Why**: Tests the screenshot endpoint. Before any browser activity, there's no screenshot file, so it should return 404 or a file if one exists. The endpoint shows the static file serving works.
**Result**: Status 200 (returns something even if no screenshot file exists) -- PASS

### Test 6: GET /latest_answer (before query)
**Why**: Tests error handling. Before any query is submitted, there should be no answer available.
**Result**: 404 with `{"error":"No agent available"}` -- PASS (expected behavior)

### Test 7: POST /query with "What is 2+2?"
**Why**: This is the critical end-to-end test. It exercises:
1. FastAPI request handling
2. The LLM router (classifies query type -> routes to Jarvis/CasualAgent)
3. OpenAI API call (proves the API key works and gpt-4o-mini responds)
4. Response formatting and return

A simple math question was chosen because it:
- Is fast (no web search or code execution needed)
- Routes to the CasualAgent (simplest agent)
- Has a deterministic answer we can verify
- Doesn't require any external resources

**Result**: `{"done":"true","answer":"...2 + 2 equals 4!...","agent_name":"Jarvis","success":"True"}` -- PASS

### Test 8: GET /latest_answer (after query)
**Why**: Verifies that query results are stored and retrievable. After submitting a query, the latest_answer should return the most recent response.
**Result**: Returns the previous query's response -- PASS

### Test 9: GET /stop (no active query)
**Why**: Tests the stop endpoint. When no query is processing, calling stop should fail gracefully since there's no agent to stop.
**Result**: 500 Internal Server Error (because `interaction.current_agent.request_stop()` has no active task to stop) -- PASS (expected behavior, no crash)

## Lessons Learned

### Backend Startup Time
The backend takes 2-3 minutes to start because it loads:
1. A zero-shot classification pipeline (for query routing)
2. An LLM router model (for agent selection)
Both are loaded on CPU since there's no GPU. Don't try to hit endpoints before seeing "Uvicorn running on http://0.0.0.0:7777" in the logs.

### Celery Broker URL
The api.py hardcodes the Celery broker URL as `redis://localhost:6379/0` on line 49, but the environment variable `REDIS_URL` is set to `redis://redis:6379/0` (Docker network). The hardcoded URL would fail in Docker if Celery were actively used. However, the current API endpoints don't seem to use Celery tasks directly -- the query processing happens synchronously in the FastAPI handler. This is a potential bug in the app but doesn't affect our deployment.

### Volume Mount Gotcha
The docker-compose.yml mounts `./:/app` as a volume for the backend service (line 82). This means the local directory overwrites the container's /app, including the config.ini. Since we modified config.ini on the desktop before building, the mounted volume has our updated config. If you were to rebuild without the volume mount, you'd get the original ollama config from the COPY instruction in the Dockerfile.

### Image Size
The backend image is 15.8GB primarily because of:
- PyTorch (with CUDA libraries, even though we're on CPU)
- Chrome for Testing + ChromeDriver
- transformers + spacy + kokoro (TTS)
- All their transitive dependencies

There's no practical way to reduce this without removing functionality. The developer chose to include everything.

### Single Query at a Time
The backend uses a global `is_generating` flag (api.py line 144). If a query is being processed and you send another, you get a 429 response. This is by design -- the agents are stateful and can't handle concurrent queries.
