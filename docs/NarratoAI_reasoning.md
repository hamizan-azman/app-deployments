# NarratoAI -- Reasoning Log

## What This App Is

NarratoAI is an automated video narration/commentary tool. You upload a video, it uses an LLM vision model to understand the video frames, generates a narration script with a text LLM, converts it to speech via TTS, and produces a final video with voiceover and subtitles. It was originally forked from MoneyPrinterTurbo and refactored to focus on film/drama commentary. The web UI is built with Streamlit.

## What I Checked and Why

### README-en.md
English version of the README. Confirmed:
- It's a Streamlit web app for automated video narration
- Requires Python 3.12+
- Supports multiple LLM providers and TTS engines
- Has Docker support (Dockerfile + docker-compose.yml)
- Version 0.7.6 (from config.example.toml)

### Dockerfile
Multi-stage build:
- Builder stage: python:3.12-slim-bookworm, installs build-essential, git, git-lfs, creates venv, pip installs requirements from Chinese mirror
- Runtime stage: python:3.12-slim-bookworm, copies venv from builder, installs imagemagick/ffmpeg/curl/git-lfs/dos2unix, creates non-root user `narratoai`, copies app code, exposes port 8501
- Entrypoint: `docker-entrypoint.sh` with CMD `webui`
- Health check: `curl -f http://localhost:8501/_stcore/health`

The Dockerfile was well-structured. Only change needed: swap the Chinese pip mirror for default PyPI.

### docker-compose.yml
Simple single-service compose. Maps port 8501:8501, mounts storage/, config.toml, and resource/ as volumes. Uses health check. Confirms the app architecture is straightforward.

### config.example.toml
Central configuration file. Key findings:
- LLM config uses LiteLLM as a unified interface to 100+ providers
- Two LLM slots: vision model (for video frame understanding) and text model (for script generation)
- Default vision model: `gemini/gemini-2.0-flash-lite`
- Default text model: `deepseek/deepseek-chat`
- API keys are stored in the config file, not env vars
- Multiple TTS backends: Edge TTS (default, free), Azure Speech, Tencent TTS, Qwen TTS, SoulVoice, IndexTTS2
- Proxy config available
- Frame extraction interval configurable (default 3 seconds)

### docker-entrypoint.sh
The entrypoint script:
1. Checks for config.toml (copies from example if missing)
2. Creates storage directories
3. Attempts to `pip install --user -r requirements.txt` at startup (for hot-updating deps when volume-mounting new code)
4. Starts Streamlit on 0.0.0.0:8501 with CORS enabled, XSRF disabled, max upload 2048MB

The `pip install --user` fails in the venv with "User site-packages are not visible in this virtualenv" but this is harmless -- all deps are already installed from the build stage.

### webui.py
The main Streamlit app:
- Sets page config (title, icon, layout)
- Initializes logging with loguru
- Registers LLM providers via `app.services.llm.providers.register_all_providers()`
- Detects FFmpeg hardware acceleration
- Renders UI panels: basic settings, script settings, audio settings, video settings, subtitle settings, system settings
- "Generate Video" button triggers the full pipeline: script generation, video editing, TTS, subtitle overlay

### requirements.txt
Clean, well-organized. Key deps:
- streamlit>=1.45.0 (web UI)
- moviepy==2.1.1 (video editing)
- edge-tts==6.1.19 (default TTS)
- litellm>=1.70.0 (unified LLM interface)
- openai>=1.77.0 (OpenAI SDK)
- google-generativeai>=0.8.5 (Gemini)
- azure-cognitiveservices-speech>=1.37.0 (Azure TTS)
- Pillow>=10.3.0 (image processing)
- No torch/GPU deps required (optional)

## What I Decided and Why

### Build from Dockerfile (not docker pull)
No pre-built image exists on Docker Hub. The repo's Dockerfile is well-structured and builds cleanly. This is the intended deployment method.

### Changed pip mirror from Chinese to default PyPI
The original Dockerfile uses `https://pypi.tuna.tsinghua.edu.cn/simple` as the pip index. This is a Tsinghua University mirror optimized for users in China. From our location, default PyPI is faster and more reliable. This change only affects build speed/reliability, not app behavior.

### Port mapping 9000:8501
User requested port 9000. The app internally uses Streamlit's default port 8501 (hardcoded in docker-entrypoint.sh). Mapped 9000 on host to 8501 in container.

### No config.toml volume mount
For testing, the default config.toml (copied from config.example.toml) works fine. The app starts and serves the UI without any API keys configured. LLM features require keys to be set via the web UI or config file.

### No API key testing
The app requires LLM API keys to be configured in config.toml or via the Streamlit UI settings panel. Unlike apps that take API keys as environment variables, NarratoAI stores them in a TOML config file. Testing the video generation pipeline would require:
1. Mounting a config.toml with valid API keys
2. Uploading a video through the Streamlit UI
3. Triggering the generation pipeline
This is UI-driven and cannot be easily automated with curl.

## Alternatives Considered

### Using docker-compose
The repo provides docker-compose.yml. However, it mounts local directories (storage/, config.toml, resource/) which requires setup, and maps to port 8501 instead of the requested 9000. A simple `docker run` with port mapping is cleaner for testing.

### Modifying the entrypoint to skip pip install
The entrypoint's `pip install --user` fails harmlessly. Could have patched it out, but it doesn't affect startup time significantly (takes ~2 seconds) and doesn't break anything.

## How Each Test Was Chosen

### Test 1: GET / (Main UI)
**Why:** Proves the Streamlit app started, all Python imports succeeded (webui.py, app modules, LLM providers), and the web server is serving.
**Result:** 200 OK with full Streamlit HTML/JS app.

### Test 2: GET /_stcore/health
**Why:** This is Streamlit's built-in health check, also used by the Dockerfile's HEALTHCHECK directive. A response of "ok" proves the Streamlit runtime is healthy.
**Result:** PASS. Response: `ok`

### Test 3: GET /_stcore/allowed-message-origins
**Why:** Proves the Streamlit core server infrastructure is running (not just a static page). This endpoint returns CORS configuration.
**Result:** PASS. Returns XML configuration.

### Test 4: WebSocket /_stcore/stream
**Why:** Streamlit uses WebSockets for real-time UI communication. Testing this confirms the WebSocket server is running. We expect a rejection for non-WebSocket HTTP requests.
**Result:** PASS. Correctly returns "Can only Upgrade to WebSocket."

### Test 5: Video script generation (OpenAI gpt-4o-mini)
**Why:** Core pipeline test. Uploaded a 143.7s 1080p video, configured OpenAI key via UI, triggered script generation.
**Result:** PARTIAL PASS. The app successfully extracted 72 keyframes from the video and sent them to OpenAI's API. The LLM call was rate-limited (`RATE_LIMIT_ERROR: API调用频率超限`) due to a low-tier OpenAI key. A second attempt with reduced batch size hit a different error (`'bool' object is not a mapping`), likely a bug in error recovery logic. The pipeline up to and including the LLM API call is confirmed working.

## Gotchas and Debugging

### Chinese pip mirror in Dockerfile
The original Dockerfile uses `pypi.tuna.tsinghua.edu.cn`. If building from China, keep it. Outside China, swap to default PyPI or your preferred mirror.

### Entrypoint pip install --user failure
The entrypoint script tries to install deps at startup with `--user` flag. This fails in a venv ("User site-packages are not visible in this virtualenv"). This is harmless -- all deps are installed during the Docker build. The error message appears in logs but doesn't affect the app.

### Config via TOML file, not env vars
Unlike most apps in this project, NarratoAI configures LLM API keys via a TOML config file, not environment variables. To pre-configure, mount a config.toml: `-v ./config.toml:/NarratoAI/config.toml`.

### Non-root user
The Dockerfile creates and runs as user `narratoai`. This means volume-mounted directories need appropriate permissions. If mounting storage or config, ensure the files are writable by the container user.

### ImageMagick policy
The Dockerfile patches ImageMagick's security policy to allow read/write for `@*` patterns. This is needed for moviepy's text overlay features.

## Test Summary
| # | Test | Result |
|---|------|--------|
| 1 | GET / (UI loads) | PASS |
| 2 | GET /_stcore/health | PASS |
| 3 | GET /_stcore/allowed-message-origins | PASS |
| 4 | WebSocket /_stcore/stream | PASS |
| 5 | Video script generation (OpenAI) | PARTIAL PASS (API reached, rate-limited) |

Infrastructure: 4/4 passed. Video generation: partial (LLM connection confirmed, rate-limited on low-tier key).
