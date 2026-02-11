# Open-LLM-VTuber. Usage Documentation

## Overview
AI VTuber assistant with a Live2D animated avatar, real-time speech synthesis, and LLM-powered conversation. Exposes a FastAPI/WebSocket server that a browser frontend connects to. Requires a user-provided configuration file at startup.

## Quick Start
```bash
docker pull hoomzoom/open-llm-vtuber

# Copy default config from the repo (required)
mkdir -p conf
cp apps/Open-LLM-VTuber/conf.yaml conf/conf.yaml
# Edit conf/conf.yaml with your LLM provider and model settings

docker run -d -p 12393:12393 \
  -v $(pwd)/conf:/app/conf \
  -v $(pwd)/models:/app/models \
  hoomzoom/open-llm-vtuber
```

Open http://localhost:12393 in your browser.

## Base URL
http://localhost:12393

## Core Features
- Live2D avatar rendering in browser
- Real-time speech synthesis and voice activity detection
- LLM-driven conversation (supports OpenAI-compatible backends and local models)
- WebSocket-based real-time audio/text streaming
- Configurable character personalities, voices, and Live2D models

## Endpoints

### Web UI
- **URL:** http://localhost:12393
- **Description:** Browser frontend with Live2D avatar and chat interface.
- **Tested:** Yes (fastapi import verified)

### WebSocket
- **URL:** ws://localhost:12393/ws
- **Description:** Real-time bidirectional audio and text streaming endpoint.
- **Tested:** Not tested (requires full audio stack)

## Health Check
The Dockerfile healthcheck uses `curl -f http://localhost:12393/` with a 60-second start period.

## Configuration
`conf.yaml` is required. The container startup script checks for `/app/conf/conf.yaml` and exits with an error if it is not found.

```bash
# The startup script symlinks mounted config files into the app directory:
# /app/conf/conf.yaml          -> /app/conf.yaml (required)
# /app/conf/model_dict.json    -> /app/model_dict.json (optional)
# /app/conf/live2d-models/     -> /app/live2d-models/ (optional)
# /app/conf/characters/        -> /app/characters/ (optional)
# /app/conf/avatars/           -> /app/avatars/ (optional)
# /app/conf/backgrounds/       -> /app/backgrounds/ (optional)
```

Key conf.yaml settings:

| Config Key | Description |
|------------|-------------|
| llm.provider | LLM provider (openai, ollama, etc.) |
| llm.model | Model name |
| llm.api_key | API key (if using a cloud provider) |
| tts.engine | Text-to-speech engine |
| asr.engine | Automatic speech recognition engine |

## Volumes
| Path | Purpose |
|------|---------|
| /app/conf | Required. Mount directory containing conf.yaml and optional extras. |
| /app/models | Optional. Download location for local model weights. |

## Notes
- The container will not start without a valid conf.yaml at /app/conf/conf.yaml. This is enforced by the startup script, which exits 1 if the file is absent.
- Python 3.10 is required (pinned by the upstream project for compatibility with the Live2D and audio libraries).
- uv is used for dependency management. The package is installed with `uv pip install --no-deps .` after `uv sync`.
- ffmpeg is installed for audio processing.
- The CONFIG_FILE environment variable is set to /app/conf/conf.yaml inside the container and does not need to be changed.
- Local model weights (if using Ollama or local ASR/TTS) are downloaded to /app/models at runtime. Mount this volume to persist downloads.

## Changes from Original
- The Dockerfile was written for this deployment. The upstream project provides a docker-compose.yml but no standalone Dockerfile.
- The startup script handles all required symlink creation and config validation before launching the server.

## V2 Dependency Changes
Python dependencies managed by uv with a frozen lock file from uv.lock. Exact versions come from the lock file. No additional pinning applied.
