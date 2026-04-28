# MoneyPrinterTurbo. Usage Documentation

## Overview
Streamlit web UI and FastAPI backend for automated short video generation. Combines LLM script writing, Pexels stock footage, ImageMagick text rendering, and FFmpeg video assembly into a single pipeline.

## Quick Start
```bash
docker pull hoomzoom/moneyprinterturbo
docker run -d -p 8501:8501 -p 8080:8080 hoomzoom/moneyprinterturbo
```

Open http://localhost:8501 in your browser. Note: the app will start but cannot generate videos until a config.toml file with API keys is provided.

## Base URL
- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8080

## Core Features
- LLM-driven video script generation
- Automated stock footage sourcing from Pexels API
- Text overlay and subtitle rendering via ImageMagick
- Video assembly with FFmpeg
- Streamlit web UI for job configuration and monitoring
- FastAPI endpoint for programmatic access

## Endpoints

### Streamlit UI
- **URL:** http://localhost:8501
- **Description:** Main web interface for configuring and launching video generation jobs.
- **Tested:** Yes (import verified, full startup requires config.toml)

### FastAPI Docs
- **URL:** http://localhost:8080/docs
- **Description:** FastAPI interactive documentation for programmatic access.
- **Tested:** Not tested (requires valid config.toml for service startup)

## Health Check
The Dockerfile healthcheck runs `python -c "import streamlit"` with a 60-second start period. This verifies the Python environment, not full app readiness.

## Configuration
The app requires a `config.toml` file. Copy the example from the repo and edit it:

```bash
# Copy example config from the container
docker cp <container_id>:/MoneyPrinterTurbo/config.example.toml ./config.toml
# Edit config.toml with your API keys, then mount it
docker run -d -p 8501:8501 -p 8080:8080 \
  -v $(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \
  hoomzoom/moneyprinterturbo
```

## Environment Variables
The app uses config.toml rather than environment variables for most settings. Key config.toml entries:

| Config Key | Description |
|------------|-------------|
| llm.provider | LLM provider (openai, moonshot, etc.) |
| llm.api_key | API key for the chosen LLM |
| llm.model | Model name to use |
| pexels.api_keys | List of Pexels API keys for stock footage |

## Volumes
| Path | Purpose |
|------|---------|
| /MoneyPrinterTurbo/config.toml | Required config file with API keys |
| /MoneyPrinterTurbo/storage | Generated video output files |

## Notes
- The container runs without a non-root user (upstream Dockerfile sets 777 permissions on the workdir).
- ImageMagick is installed from apt and the security policy (`/etc/ImageMagick-6/policy.xml`) is patched at build time to allow the `@*` path pattern that moviepy uses for text rendering.
- FFmpeg is required for video assembly and is installed at build time.
- The app will start without config.toml but all generation features will fail with a config error.

## Changes from Original
- Removed Chinese PyPI mirror (`-i https://mirrors.aliyun.com/pypi/simple/`) from the pip install command.
- Removed Aliyun apt mirror configuration from the apt-get commands.

## V2 Dependency Changes
Minimum version pinning applied to requirements.txt. All minimum versions resolved successfully without bumps.
