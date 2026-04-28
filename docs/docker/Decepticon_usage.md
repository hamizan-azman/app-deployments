# Decepticon. Usage Documentation

## Overview
Autonomous offensive security platform powered by LLM agents. Decepticon runs penetration testing tasks using a multi-agent pipeline backed by LangGraph, routes all LLM calls through a LiteLLM proxy, executes offensive tools in an isolated Kali Linux sandbox container, and exposes an interactive CLI. No custom Docker image is built for this deployment. All images are pulled from the upstream GHCR registry.

## Quick Start
```bash
cd dockerfiles/Decepticon

# Copy and fill in environment variables
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY or OPENAI_API_KEY, LITELLM_MASTER_KEY,
# LITELLM_SALT_KEY, POSTGRES_PASSWORD, and DECEPTICON_HOME

docker compose up -d
```

Start the interactive CLI in a separate terminal after the stack is healthy:
```bash
docker compose run --rm cli
```

## Services and Ports
| Service | Host Port | Description |
|---|---|---|
| langgraph | 2024 | LangGraph agent API server |
| litellm | 4000 | LiteLLM LLM proxy gateway (localhost-bound) |
| postgres | 5432 | PostgreSQL for LiteLLM usage tracking (localhost-bound) |
| sandbox | none | Isolated Kali Linux container for tool execution |
| cli | none | Interactive terminal UI (run-once, not a daemon) |
| c2-sliver | none | Sliver C2 server (optional, activated via COMPOSE_PROFILES) |

LiteLLM and PostgreSQL ports are bound to `127.0.0.1` only and are not accessible from external hosts.

## Networks
| Network | Services | Purpose |
|---|---|---|
| decepticon-net | langgraph, litellm, postgres | Internal agent and proxy communication |
| sandbox-net | sandbox, c2-sliver | Isolated offensive tool execution network |

The `sandbox` container has no access to `litellm`, `postgres`, or `langgraph`. LangGraph reaches the sandbox through the Docker socket (`/var/run/docker.sock`) using `docker exec`, not via the network.

## Environment Variables
Set these in `.env` before running compose.

| Variable | Required | Default | Description |
|---|---|---|---|
| ANTHROPIC_API_KEY | Conditional | None | Required if using Anthropic models |
| OPENAI_API_KEY | Conditional | None | Required if using OpenAI models |
| GOOGLE_API_KEY | No | None | Optional Google API key |
| LITELLM_MASTER_KEY | Yes | None | Master key for the LiteLLM proxy. Change from the default. |
| LITELLM_SALT_KEY | Yes | None | Salt key for LiteLLM. Change from the default. |
| POSTGRES_PASSWORD | Yes | None | PostgreSQL password. Change from the default. |
| DECEPTICON_MODEL_PROFILE | No | eco | Model profile: eco (mixed), max (Opus everywhere), test (Haiku only) |
| DECEPTICON_HOME | Yes | ~/.decepticon | Absolute path to Decepticon home directory. Do not use tilde. |
| COMPOSE_PROFILES | No | None | Set to `c2-sliver` to activate the Sliver C2 container |
| LANGGRAPH_PORT | No | 2024 | Override the LangGraph API port |
| LITELLM_PORT | No | 4000 | Override the LiteLLM proxy port |
| POSTGRES_PORT | No | 5432 | Override the PostgreSQL port |
| LANGSMITH_TRACING | No | None | Set to `true` to enable LangSmith tracing |
| LANGSMITH_API_KEY | No | None | LangSmith API key |
| DECEPTICON_DEBUG | No | None | Set to `true` to enable debug logging |

At least one of ANTHROPIC_API_KEY or OPENAI_API_KEY must be set.

## QC Test
No custom build is required. All images are pulled from GHCR on first `docker compose up`. Verify the stack is healthy:

```bash
docker compose ps
```

All services except `cli` should show status `running` or `healthy`.

Verify the LangGraph API is reachable:
```bash
curl http://localhost:2024/ok
```

## Optional: Activate Sliver C2
To start the Sliver command-and-control server alongside the main stack, set in `.env`:
```
COMPOSE_PROFILES=c2-sliver
```
Then run `docker compose up -d` again.

## Notes
- No custom Docker image is built. All images are from `ghcr.io/purpleailab/`.
- The Docker socket (`/var/run/docker.sock`) is mounted read-only into the `langgraph` container. This is required for the agent to reach the sandbox via `docker exec`. It is an intentional design choice by the upstream developers.
- The `sandbox` container runs with `NET_RAW`, `NET_ADMIN`, and `NET_BIND_SERVICE` capabilities, which allow offensive network operations. This container is isolated on `sandbox-net` and has no path to the host network by default.
- The sandbox workspace is persisted at `${DECEPTICON_HOME}/workspace` on the host.
- LITELLM_MASTER_KEY and LITELLM_SALT_KEY must both be changed from the example defaults before deployment.
- DECEPTICON_HOME must be an absolute path. Docker Compose does not expand the tilde character.

## Changes from Original
- No Dockerfile modifications. Our contribution is the compose file and `.env.example` stored in `dockerfiles/Decepticon/` for reproducibility.
- The compose file references upstream GHCR images tagged at `${DECEPTICON_VERSION:-latest}` and the fixed LiteLLM version `main-v1.82.3-stable.patch.2`.
