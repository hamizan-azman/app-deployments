# browser-use. Usage Documentation

## Overview
CLI tool and Python library for AI-driven browser automation using Playwright and Chromium. Lets LLM agents control a browser to perform tasks on the web. Supports OpenAI, Anthropic, and other LLM providers via environment variables.

## Quick Start
```bash
docker pull hoomzoom/browser-use
docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY hoomzoom/browser-use --help
```

## Entry Point
The container entry point is the `browser-use` CLI. All usage goes through CLI arguments passed after the image name.

## Core Features
- AI-driven browser automation using Playwright and Chromium
- LLM-orchestrated web task execution (form filling, navigation, data extraction)
- Chromium bundled from apt packages, no Playwright browser download needed
- Persistent browser profiles via /data volume
- Chrome DevTools Protocol accessible on port 9222

## CLI Usage

### Help
```bash
docker run --rm hoomzoom/browser-use --help
```

### Run a browser task
```bash
docker run --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  hoomzoom/browser-use <task-or-args>
```

### With persistent profile volume
```bash
docker run --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v browser-use-data:/data \
  hoomzoom/browser-use <task-or-args>
```

### With Chrome DevTools Protocol exposed
```bash
docker run --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -p 9242:9242 \
  -p 9222:9222 \
  -v browser-use-data:/data \
  hoomzoom/browser-use <task-or-args>
```

## Ports
| Port | Purpose |
|------|---------|
| 9242 | browser-use internal port |
| 9222 | Chrome DevTools Protocol (CDP) |

Neither port is required for basic CLI usage. Expose 9222 if you need to connect external DevTools or automation clients to the running Chromium instance.

## Volumes
| Path | Purpose |
|------|---------|
| /data | Persistent browser profiles. Default profile at /data/profiles/default. |

Mount a named volume to preserve browser state across runs.

## Health Check
QC test: `browser-use --help` exits 0.

There is no HTTP health endpoint. The upstream Dockerfile includes a commented-out HTTP health check that was never activated.

- **Tested:** Yes (`--help` prints usage and exits 0)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Conditional | None | OpenAI API key |
| ANTHROPIC_API_KEY | Conditional | None | Anthropic API key |
| IN_DOCKER | Set by image | True | Signals to app that it is running in Docker |
| TZ | Set by image | UTC | Timezone |
| LANG | Set by image | C.UTF-8 | Locale |

At least one LLM provider API key is required for actual browser task execution. Without a key the CLI starts and prints help but cannot run tasks.

## Notes
- The container runs as non-root user `browseruse` (UID 911, GID 911).
- Chromium is installed from Debian apt packages, not via Playwright's browser download. The binary is symlinked to `/usr/bin/chromium-browser` and `/app/chromium-browser`.
- Dependencies are managed with `uv` and installed into a venv at `/app/.venv`.
- API key features (actual task execution) are NOT TESTED. Infrastructure only (help output, import, startup) was tested.
- The upstream healthcheck was commented out in the original Dockerfile. No HTTP server is started by default.

## Changes from Original
- Removed `--mount=type=cache` BuildKit cache directives. These are unreliable on Windows/WSL2 Docker Desktop. Build output is functionally identical.
- All other structure preserved exactly: user setup (UID 911), chromium apt install, uv venv approach, exposed ports, volume declaration, and entrypoint.

## V2 Dependency Changes (Minimum Version Pinning)
Dependency pinning is managed by the upstream `uv.lock` file. The lock file is copied into the image and `uv sync --locked` is used during build, which enforces exact versions. No additional pinning was applied. The upstream lock file already provides full reproducibility.
