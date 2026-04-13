# openclaw. Usage Documentation

## Overview
OpenClaw is a self-hosted AI coding assistant gateway and CLI. It provides a local server that proxies AI requests to Claude and other LLM providers, with a web UI for agent management and a CLI client. The compose deployment runs two containers from the same image: a gateway (HTTP server on port 18789) and a CLI agent.

## Quick Start
```bash
cd dockerfiles/openclaw
cp .env.example .env
# Edit .env with your CLAUDE_AI_SESSION_KEY or API credentials
mkdir -p ~/.openclaw/config ~/.openclaw/workspace
OPENCLAW_CONFIG_DIR=~/.openclaw/config OPENCLAW_WORKSPACE_DIR=~/.openclaw/workspace docker compose up -d
```

Gateway: http://localhost:18789

## Service Architecture

| Service | Image | Port | Role |
|---------|-------|------|------|
| openclaw-gateway | hoomzoom/openclaw | 18789, 18790 | HTTP gateway and web UI |
| openclaw-cli | hoomzoom/openclaw | (shared with gateway) | CLI agent, network via gateway |

The CLI container shares the gateway's network namespace (`network_mode: "service:openclaw-gateway"`), so it accesses the gateway at `localhost:18789`.

## Health Check
- **URL:** http://localhost:18789/healthz
- **Method:** GET
- **Response:** HTTP 200 (ok)
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| CLAUDE_AI_SESSION_KEY | Conditional | None | Session key for Claude.ai (web session auth) |
| CLAUDE_WEB_SESSION_KEY | Conditional | None | Alternative session key variable |
| CLAUDE_WEB_COOKIE | Conditional | None | Full cookie string for Claude.ai auth |
| OPENCLAW_GATEWAY_TOKEN | No | None | Token for securing the gateway |
| OPENCLAW_GATEWAY_PORT | No | 18789 | Host port for the gateway |
| OPENCLAW_BRIDGE_PORT | No | 18790 | Host port for the bridge |
| OPENCLAW_CONFIG_DIR | Yes | None | Host path for OpenClaw config directory |
| OPENCLAW_WORKSPACE_DIR | Yes | None | Host path for workspace directory |
| OPENCLAW_TZ | No | UTC | Timezone for the container |
| OPENCLAW_ALLOW_INSECURE_PRIVATE_WS | No | None | Allow insecure WebSocket connections |

OPENCLAW_CONFIG_DIR and OPENCLAW_WORKSPACE_DIR must be set to valid host directories. They are mounted as volumes.

## Volume Mounts
The compose file requires two volume mounts:
- `OPENCLAW_CONFIG_DIR` mounted at `/home/node/.openclaw`
- `OPENCLAW_WORKSPACE_DIR` mounted at `/home/node/.openclaw/workspace`

Create these directories before starting:
```bash
mkdir -p ~/.openclaw/config ~/.openclaw/workspace
```

## Gateway Modes
The gateway starts with `--allow-unconfigured` by default, which allows it to start without a valid session key. A session key is required to actually use any AI features.

## Notes
- The image is built from a 4-stage Dockerfile using pnpm and Bun.
- SHA256 pins were removed from the base image to avoid Docker credential helper issues on Windows.
- The CLI container has `cap_drop: [NET_RAW, NET_ADMIN]` and `no-new-privileges` for security hardening.
- The container runs as non-root user `node` (UID 1000, built into the node:24-bookworm image).
- AI features are NOT TESTED in CI (require Claude.ai session credentials).

## Changes from Original
SHA256 pins removed from base image references in the Dockerfile to avoid credential helper failures on Windows Docker Desktop during remote builds. No functional changes.
