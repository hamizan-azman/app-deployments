# GPT Academic -- Usage Documentation

## Overview
GPT Academic (GPT 学术优化) is a Gradio-based web UI for interacting with LLMs. Designed for academic workflows: paper reading, translation, code analysis, polishing, LaTeX editing. Supports OpenAI, Azure, Zhipu GLM, Qwen, DeepSeek, Claude, and other models. Plugin system for extended functionality.

## Quick Start
```bash
docker pull hoomzoom/gpt_academic

docker run -d --name gpt_academic \
  -p 12345:12345 \
  -e WEB_PORT=12345 \
  -e API_KEY="sk-your-openai-key" \
  -e USE_PROXY="False" \
  -e AUTO_OPEN_BROWSER="False" \
  -e LLM_MODEL="gpt-3.5-turbo" \
  hoomzoom/gpt_academic
```

## Base URL
http://localhost:12345

## Core Features
- Multi-LLM chat (OpenAI, Azure, GLM, Qwen, DeepSeek, Claude, Gemini)
- Paper reading, translation, and polishing
- Code analysis and comment generation
- LaTeX paper translation (requires `_with_latex` image variant)
- Plugin system with hot-reload
- File upload and processing
- Text-to-speech (Edge TTS)
- Dark/light theme toggle

## Web Interface
This is a Gradio web application. All interaction happens through the browser UI at the base URL. There is no traditional REST API for chat -- users interact via the Gradio interface.

### Gradio Infrastructure Endpoints

#### GET /
- **Description:** Main Gradio web UI
- **Request:** `curl http://localhost:12345/`
- **Response:** HTML page (200 OK, ~206KB)
- **Tested:** Yes

#### GET /config
- **Description:** Gradio app configuration (component tree, layout)
- **Request:** `curl http://localhost:12345/config`
- **Response:** JSON with Gradio version, components, layout
- **Tested:** Yes

#### GET /info
- **Description:** Gradio API info with named/unnamed endpoints
- **Request:** `curl http://localhost:12345/info`
- **Response:** JSON listing all Gradio API endpoints
- **Tested:** Yes

#### GET /queue/status
- **Description:** Gradio queue status
- **Request:** `curl http://localhost:12345/queue/status`
- **Response:** `{"msg":"estimation","rank":null,"queue_size":0,...}`
- **Tested:** Yes

#### GET /startup-events
- **Description:** Triggers Gradio startup events
- **Request:** `curl http://localhost:12345/startup-events`
- **Response:** 200 OK
- **Tested:** Yes

#### GET /file={path}
- **Description:** File access (with security blocking for sensitive files)
- **Response:** Returns file content or 403 for blocked paths (config.py, __pycache__, docker-compose.yml, Dockerfile)
- **Tested:** Yes (config.py correctly blocked)

### Chat Functionality
- **Method:** Gradio WebSocket-based interaction via the browser UI
- **Requires:** Valid API_KEY for the chosen LLM provider
- **Tested:** Yes (via internal predict_no_ui_long_connection with gpt-4.1-mini, correct response received)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_KEY | Yes | (none) | LLM API key (OpenAI, Azure, etc.). Supports comma-separated multiple keys |
| WEB_PORT | No | -1 (random) | Web server port |
| LLM_MODEL | No | gpt-3.5-turbo-16k | Default LLM model |
| AVAIL_LLM_MODELS | No | (see config.py) | JSON list of available models |
| USE_PROXY | No | False | Enable proxy for API calls |
| proxies | No | None | Proxy config dict (e.g. socks5h://localhost:10880) |
| AUTO_OPEN_BROWSER | No | True | Auto-open browser on start |
| DARK_MODE | No | True | Enable dark theme |
| THEME | No | Default | UI theme |
| DEFAULT_WORKER_NUM | No | 8 | Max concurrent LLM requests |
| CONCURRENT_COUNT | No | 100 | Gradio thread concurrency |
| AUTHENTICATION | No | [] | User auth list: [("user","pass")] |
| DASHSCOPE_API_KEY | No | (none) | Alibaba Qwen API key |
| DEEPSEEK_API_KEY | No | (none) | DeepSeek API key |
| ZHIPUAI_API_KEY | No | (none) | Zhipu GLM API key |
| ANTHROPIC_API_KEY | No | (none) | Claude API key |
| GEMINI_API_KEY | No | (none) | Google Gemini API key |
| ENABLE_AUDIO | No | False | Enable voice input |
| TTS_TYPE | No | EDGE_TTS | Text-to-speech backend |

## Docker Image Variants
| Image | Description |
|-------|-------------|
| `gpt_academic_nolocal:master` | Online models only (smallest) |
| `gpt_academic_with_latex:master` | Online models + LaTeX support |
| `gpt_academic_chatglm_moss:master` | Online + local models (ChatGLM, MOSS) |
| `gpt_academic_with_all_capacity:master` | Full: CUDA + LaTeX + local models |

## Notes
- API_KEY must be valid for the chosen LLM provider. The app validates key format on startup.
- The app uses a custom Gradio 3.32.15 (vendored whl). Do not upgrade Gradio.
- WEB_PORT must match the host port mapping in `docker run -p`.
- The app binds to 0.0.0.0 internally, so port mapping works on all platforms.
- File security: config.py, __pycache__, docker-compose.yml, Dockerfile are blocked from `/file=` access.
- For multi-model setups, set AVAIL_LLM_MODELS as a JSON list string.

## Changes from Original
None. Uses the developer's own GHCR image (ghcr.io/binary-husky/gpt_academic_nolocal:master). Configuration via environment variables only.
