# NarratoAI. Usage Documentation

## Overview
NarratoAI is an AI-powered automated video narration tool. Provides script writing, automated video editing, voice-over (TTS), and subtitle generation via a Streamlit web UI. Uses LLMs (via LiteLLM) for video understanding and narration script generation.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/narratoai

# Or build from source
docker build -t narratoai apps/NarratoAI/

docker run -d --name narratoai \
  -p 9000:8501 \
  hoomzoom/narratoai
```

LLM API key is configured through the web UI settings panel (not via environment variables). Open `http://localhost:9000`, go to Settings, and enter your API key and model name. Supports OpenAI, DeepSeek, Gemini, Qwen, Claude, and 100+ other providers via LiteLLM.

## Base URL
http://localhost:9000

## Core Features
- AI video narration script generation (via LLM vision + text models)
- Automated video editing and clip assembly
- Multiple TTS engines: Edge TTS, Azure Speech, Tencent TTS, Qwen TTS, SoulVoice, IndexTTS2
- Subtitle generation and overlay
- Short drama commentary mode
- Multi-language UI (Chinese, English, Japanese)
- Supports 100+ LLM providers via LiteLLM (OpenAI, DeepSeek, Gemini, Qwen, Claude, etc.)

## Web Interface
This is a Streamlit web application. All interaction happens through the browser UI. There is no REST API. users interact via the Streamlit interface to upload videos, configure LLM/TTS settings, generate scripts, and produce narrated videos.

## Endpoints

### GET /
- **Description:** Main Streamlit web UI
- **Request:** `curl http://localhost:9000/`
- **Response:** HTML page (200 OK)
- **Tested:** Yes

### GET /_stcore/health
- **Description:** Streamlit health check
- **Request:** `curl http://localhost:9000/_stcore/health`
- **Response:** `ok`
- **Tested:** Yes

### GET /_stcore/allowed-message-origins
- **Description:** Streamlit CORS/message origins config
- **Request:** `curl http://localhost:9000/_stcore/allowed-message-origins`
- **Response:** XML with allowed origins
- **Tested:** Yes

### WebSocket /_stcore/stream
- **Description:** Streamlit WebSocket for real-time UI communication
- **Response:** Requires WebSocket upgrade (not accessible via HTTP)
- **Tested:** Yes (correctly rejects non-WebSocket requests)

### Video Generation (via UI)
- **Description:** Upload video, configure LLM/TTS, generate narrated video
- **Requires:** Valid LLM API key configured in config.toml or UI
- **Tested:** Partial. LLM connection confirmed (OpenAI API reached, rate-limited on low-tier key)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PYTHONUNBUFFERED | No | 1 | Unbuffered Python output |
| TZ | No | Asia/Shanghai | Timezone |

## Configuration
LLM and TTS settings are configured via `config.toml` (copied from `config.example.toml` on first run) or through the web UI settings panel.

Key config sections:
- `[app]`. LLM provider, model, API keys (vision + text models)
- `[azure]`. Azure TTS credentials
- `[tencent]`. Tencent TTS credentials
- `[ui]`. TTS engine selection, voice settings
- `[proxy]`. HTTP/HTTPS proxy
- `[frames]`. Video frame extraction interval

To persist config, mount a volume: `-v ./config.toml:/NarratoAI/config.toml`

## Notes
- The Dockerfile was modified to use default PyPI instead of Chinese mirror (pypi.tuna.tsinghua.edu.cn).
- The entrypoint script attempts `pip install --user` at startup (fails harmlessly in venv, deps are already installed).
- Internal port is 8501 (Streamlit default). Map to any host port.
- Requires ffmpeg and ImageMagick (both included in the Docker image).
- For persistent storage of generated videos, mount: `-v ./storage:/NarratoAI/storage`

## Changes from Original
**Category: Dependencies only.** Source code untouched.

- Chinese pip mirror (`pypi.tuna.tsinghua.edu.cn`) replaced with default PyPI. Same packages, different download source.

## V2 Dependency Changes (Minimum Version Pinning)
- `openai==1.77.0` → `openai==1.75.0` (litellm 1.70.0 requires openai<1.76.0)
