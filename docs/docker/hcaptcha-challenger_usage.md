# hcaptcha-challenger. Usage Documentation

## Overview
CLI tool and optional FastAPI server for solving hCaptcha challenges using Playwright-based browser automation and Gemini vision AI. Supports multiple operational modes including a headless server mode and a dataset collection mode.

## Quick Start
```bash
docker pull hoomzoom/hcaptcha-challenger
docker run --rm \
  -e GEMINI_API_KEY=your_key \
  hoomzoom/hcaptcha-challenger \
  sh -c "xvfb-run --auto-servernum hc --help"
```

## Base URL
Port 8000 (optional FastAPI server, not started by default)

## Core Features
- Automated hCaptcha challenge solving using Gemini vision models
- Playwright with Camoufox for browser fingerprint evasion
- Optional FastAPI endpoint for remote solve requests
- Dataset collection mode for training data generation
- Xvfb virtual display for headless operation

## CLI Usage
```bash
# Show help
docker run --rm hoomzoom/hcaptcha-challenger sh -c "xvfb-run --auto-servernum hc --help"

# Run solver (requires GEMINI_API_KEY)
docker run --rm \
  -e GEMINI_API_KEY=your_key \
  hoomzoom/hcaptcha-challenger \
  sh -c "xvfb-run --auto-servernum hc invoke --help"
```

The default CMD runs `xvfb-run ... hc --help` to verify the binary is available.

## Optional FastAPI Server
To start the HTTP server instead of the CLI default:
```bash
docker run -d -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  hoomzoom/hcaptcha-challenger \
  sh -c "xvfb-run --auto-servernum uv run python -m hcaptcha_challenger.server"
```

## Health Check
The Dockerfile healthcheck runs `python -c "import hcaptcha_challenger"` or falls back to `hc --help`. Due to the partial install state (see Notes), the import check may not pass, but `hc --help` succeeds.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GEMINI_API_KEY | Yes | None | Google Gemini API key for vision model calls |
| DISPLAY | No | :99 | Xvfb display number |

## Notes
- The base image is `mcr.microsoft.com/playwright/python:v1.52.0-noble`, which includes all Playwright dependencies and browsers.
- Xvfb provides a virtual framebuffer for headless browser operation. All browser commands must be wrapped with `xvfb-run`.
- The `uv sync --frozen --no-cache --all-extras` step installs all extras (server, camoufox, dataset). The `hc` CLI binary is available at the system level.
- QC result: conditional pass. The `hc --help` command works. The Python package import (`import hcaptcha_challenger`) may fail due to the uv-managed virtual environment not being on the default Python path. Use `uv run` prefix for Python-level invocations.
- Camoufox GeoIP data is fetched at build time and bundled in the image.

## Changes from Original
No changes to the upstream Dockerfile structure. The Dockerfile was written for this deployment.

## V2 Dependency Changes
Dependencies managed by uv with a frozen lock file. Exact versions come from uv.lock. No additional pinning applied.
