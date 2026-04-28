# BiliNote. Usage Documentation

## Overview
FastAPI backend for AI-powered video note generation. Accepts Bilibili or YouTube video URLs, transcribes the audio, and generates structured notes using an LLM. Deployed as backend-only (frontend not included in this image).

## Quick Start
```bash
docker pull hoomzoom/bilinote
docker run -d -p 8483:8483 \
  --security-opt seccomp=unconfined \
  hoomzoom/bilinote
```

API documentation is available at http://localhost:8483/docs.

## Base URL
http://localhost:8483

## Core Features
- Video transcription from Bilibili and YouTube URLs
- AI note generation from transcribed content
- FastAPI REST API for programmatic access
- ctranslate2 for fast local transcription (Whisper models)
- ffmpeg for audio extraction

## Endpoints

### API Documentation
- **URL:** http://localhost:8483/docs
- **Description:** FastAPI interactive documentation with all available endpoints.
- **Tested:** Not tested (ctranslate2 exec stack issue, see Notes)

### Health
- **URL:** http://localhost:8483/
- **Description:** Root endpoint, returns service status.
- **Tested:** Conditional (see Notes)

## Health Check
The Dockerfile healthcheck uses `curl -f http://localhost:8483/` with a 15-second start period.

## Environment Variables
The app reads LLM configuration from environment variables or a config file. Refer to the upstream README for the full list. At minimum, an LLM API key is needed for note generation.

## Notes
- ctranslate2 requires the `seccomp=unconfined` security option to execute properly in Docker. Without it, ctranslate2 raises an exec stack permission error on startup. Run with `--security-opt seccomp=unconfined`.
- QC result: conditional pass. The ctranslate2 exec stack issue prevents a clean healthcheck without the seccomp flag. With `--security-opt seccomp=unconfined`, the service starts normally.
- The container runs as non-root user `appuser` (UID 1000).
- The frontend was not included in this deployment. The upstream frontend Vite build failed during analysis, and the GHCR image for the frontend is not publicly accessible. The backend-only deployment preserves the original architecture (FastAPI handles all logic).
- ffmpeg is required for audio extraction and is installed at build time.
- ctranslate2 is pinned to 4.4.0 and installed before the rest of requirements.txt to avoid resolver conflicts.

## Changes from Original
- Backend-only deployment. The upstream project has a separate frontend. This image runs only the FastAPI backend.
- ctranslate2==4.4.0 is pre-installed before requirements.txt to stabilize dependency resolution.

## V2 Dependency Changes
Minimum version pinning applied to backend/requirements.txt. ctranslate2 pinned separately at 4.4.0.
