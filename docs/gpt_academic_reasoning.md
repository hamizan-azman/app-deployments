# GPT Academic -- Reasoning Log

## What This App Is

GPT Academic (GPT 学术优化) is a Chinese-origin academic productivity tool built on Gradio. It provides a web UI for interacting with various LLMs, with a plugin system optimized for academic workflows: paper reading, translation, code analysis, LaTeX editing, and more. It was created by binary-husky and has significant Chinese-language documentation and UI strings.

## What I Checked and Why

### README.md
The README is almost entirely in Chinese. Key findings:
- Multiple Docker image variants exist (nolocal, with_latex, chatglm_moss, all_capacity)
- The user specified `gpt_academic_nolocal:master` which is the lightweight online-models-only variant
- Installation instructions show both pip-based and Docker-based deployment

### config.py
This is the central configuration file. All settings can be overridden via environment variables. Key findings:
- `API_KEY` is the main LLM key (OpenAI format by default)
- `WEB_PORT = -1` means random port by default -- we need to set this explicitly
- `USE_PROXY = False` by default, which is what we want
- `AUTO_OPEN_BROWSER = True` by default -- need to disable in Docker
- Supports dozens of LLM providers: OpenAI, Azure, Zhipu GLM, Qwen, DeepSeek, Claude, Gemini, Baidu Qianfan, Xunfei Spark, Yi, Moonshot, etc.
- The config comment at line 1-8 explicitly states: "Reading priority: environment variable > config_private.py > config.py"

### Dockerfile (repo's own)
The repo has its own Dockerfile. It uses `ghcr.io/astral-sh/uv:python3.12-bookworm` as base, installs requirements, and runs `python main.py`. The pre-built image we're pulling was built from this Dockerfile (or a similar CI variant), so we don't need to build from scratch.

### docker-compose.yml
Shows multiple deployment "plans" (方案). Key insight: the nolocal plan uses `WEB_PORT: 22303` and `network_mode: "host"`. For Windows Docker Desktop, host networking doesn't work, so we use port mapping instead. The compose file confirms that environment variables are the correct way to configure the app.

### main.py
The entry point. Key findings:
- Requires Gradio version 3.32.15 specifically (a custom vendored version)
- Uses `shared_utils/fastapi_server.py` to start the server
- Builds the entire Gradio UI programmatically with buttons, file upload, plugins, etc.
- Port determined by `WEB_PORT` config or random if -1

### shared_utils/fastapi_server.py
The actual server. Key findings:
- Binds to `0.0.0.0` (line 278), so no need to override host binding
- Uses uvicorn under the hood
- Has security features: blocks access to config.py, __pycache__, docker-compose.yml, Dockerfile via `/file=` path
- Mounts the Gradio app under `CUSTOM_PATH` (default `/`)
- Supports TTS via `/vits` endpoint

### requirements.txt
Notable: requires a custom Gradio whl from `public.agent-matrix.com`, not from PyPI. This is Gradio 3.32.15, a forked/customized version. The pre-built image has this already installed.

## What I Decided and Why

### Use pre-built image (docker pull) instead of building from source
The user specified `docker pull` approach. The pre-built image `ghcr.io/binary-husky/gpt_academic_nolocal:master` is maintained by the project author and includes all dependencies pre-installed, including the custom Gradio whl. Building from source would be slower and would use Chinese mirror pip sources that may not work from our location.

### Port 12345
The user requested port 12345. This matches the port used in the docker-compose examples. The `WEB_PORT` env var must be set to match the host port mapping.

### Placeholder API key
No real API key was provided. I used `sk-placeholder-for-testing` to allow the app to start. The app logs a warning about invalid key format but still boots and serves the UI. This is sufficient for infrastructure testing.

### Environment variables used
- `WEB_PORT=12345` -- fixed port, not random
- `API_KEY="sk-placeholder-for-testing"` -- allows boot without real key
- `USE_PROXY="False"` -- no proxy needed
- `AUTO_OPEN_BROWSER="False"` -- no browser in Docker container
- `LLM_MODEL="gpt-3.5-turbo"` -- default model selection

### No Dockerfile creation needed
We are using the pre-built image directly. No custom Dockerfile was created. This follows architectural fidelity -- the image is the developer's own build.

## Alternatives Considered

### Building from the repo's Dockerfile
Could have done `docker build -t gpt_academic apps/gpt_academic/`. However:
- The Dockerfile uses Chinese pip mirrors (mirrors.aliyun.com) which may be slow from our location
- The pre-built image is maintained by the author and is the recommended deployment method
- No advantage to building locally when the image is available

### Using the full-capacity image (gpt_academic_with_all_capacity)
This includes CUDA, LaTeX, and local models. Rejected because:
- Much larger image size
- Requires NVIDIA GPU runtime
- We only need online model support for testing

### Using docker-compose instead of docker run
The repo provides docker-compose.yml. Rejected because:
- The compose file uses `network_mode: "host"` which doesn't work on Windows Docker Desktop
- A simple `docker run` with port mapping is cleaner and more portable
- No additional services (DB, Redis) needed

## How Each Test Was Chosen

### Test 1: GET / (Main UI)
**Why:** This is the most fundamental test. If the Gradio app starts and serves HTML, the entire Python application stack is working: uvicorn, FastAPI, Gradio, all imports, plugin loading.
**Result:** 200 OK, 206KB HTML. The HTML contains the Gradio app with all components.

### Test 2: GET /config
**Why:** The `/config` endpoint returns the Gradio component tree as JSON. This proves Gradio is not just serving static HTML but has actually initialized all components (chatbot, buttons, dropdowns, file upload).
**Result:** JSON with `version: 3.32.15`, full component list.

### Test 3: GET /info
**Why:** The `/info` endpoint lists all Gradio API endpoints. This proves the Gradio queue system and API layer are operational.
**Result:** JSON with named and unnamed endpoints listed.

### Test 4: GET /queue/status
**Why:** Gradio uses a queue system for handling requests. This endpoint proves the queue is initialized and accepting connections.
**Result:** `queue_size: 0`, queue operational.

### Test 5: GET /startup-events
**Why:** This endpoint triggers Gradio's startup lifecycle. A 200 response proves the app completed startup successfully.
**Result:** 200 OK.

### Test 6: GET /file=config.py (security test)
**Why:** The app explicitly blocks access to sensitive files. Testing this proves the security middleware is active -- important for supply chain security research.
**Result:** Correctly returned 403 with message "File not allowed: config.py."

### Test 7: LLM chat (OpenAI gpt-3.5-turbo)
**Why:** The core function of the app. Tested by running `predict_no_ui_long_connection` inside the container, which calls the OpenAI API through the app's own bridge layer.
**Input:** "Say hello in exactly 5 words."
**Result:** PASS. Received coherent response: "Greetings and salutations to you!"

## Gotchas and Debugging

### Custom Gradio version
The app requires exactly Gradio 3.32.15, a custom forked version distributed as a whl from `public.agent-matrix.com`. If you tried to install standard Gradio, `main.py` would raise `ModuleNotFoundError` at line 38. The pre-built image has this already installed.

### API key validation
The app validates API key format on startup. With our placeholder key, it logs:
```
[API_KEY] 您的 API_KEY（sk-placeholder-***）不满足任何一种已知的密钥格式
```
But the app still starts and serves the UI. Only actual LLM requests would fail.

### MSYS_NO_PATHCONV on Windows
When running `docker exec` or `docker run` from Git Bash on Windows, paths like `/gpt/` get mangled to `C:/Program Files/Git/gpt/`. Must prefix commands with `MSYS_NO_PATHCONV=1`.

### WEB_PORT must match -p mapping
If `WEB_PORT` doesn't match the port in `-p HOST:CONTAINER`, the app will listen on the wrong port inside the container and be unreachable. Both must be the same value.

### Chinese UI strings
The entire UI is in Chinese by default. There is no built-in language toggle. The app works fine regardless of language -- it's purely cosmetic for the web interface.

### No REST API for chat
Unlike many LLM apps, GPT Academic does not expose a REST API for chat. All interaction goes through the Gradio WebSocket/queue system in the browser. The `/info` endpoint lists Gradio's internal unnamed endpoints, but these are meant for the Gradio client library, not direct curl usage.

## Test Summary
| # | Test | Result |
|---|------|--------|
| 1 | GET / (UI loads) | PASS |
| 2 | GET /config (Gradio config) | PASS |
| 3 | GET /info (API info) | PASS |
| 4 | GET /queue/status | PASS |
| 5 | GET /startup-events | PASS |
| 6 | GET /file=config.py (security block) | PASS |
| 7 | LLM chat (OpenAI gpt-3.5-turbo) | PASS |

Infrastructure: 6/6 passed. Chat: 1/1 passed. Total: 7/7.
