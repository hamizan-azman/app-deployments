# gpt-pilot. Usage Documentation

## Overview
CLI AI coding agent that builds full applications interactively from a user-provided prompt. The agent breaks the task into steps, writes code, runs tests, and asks clarifying questions throughout the process. Supports OpenAI, Anthropic, and Groq as LLM providers.

## Quick Start
```bash
docker pull hoomzoom/gpt-pilot
docker run -it --rm \
  -v gpt-pilot-data:/app/data \
  hoomzoom/gpt-pilot
```

The container is interactive. It will prompt for project details on startup.

## Base URL
None. This is a CLI tool with no HTTP interface.

## Usage

### Basic interactive run
```bash
docker run -it --rm \
  -v gpt-pilot-data:/app/data \
  hoomzoom/gpt-pilot
```

### Passing a config file with API credentials
Create a `config.json` file (see Environment Variables section for format), then mount it:

```bash
docker run -it --rm \
  -v gpt-pilot-data:/app/data \
  -v /path/to/config.json:/app/config.json:ro \
  hoomzoom/gpt-pilot
```

### Persisting project output
The agent writes generated code to `/app/data`. Mount a named volume or bind mount to keep the output after the container exits:

```bash
docker run -it --rm \
  -v $(pwd)/output:/app/data \
  hoomzoom/gpt-pilot
```

## API Key Configuration
API credentials are configured via `config.json`. The agent supports multiple providers. Example structure:

```json
{
  "llm": {
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o",
    "api_key": "sk-..."
  }
}
```

For Anthropic, set `base_url` to `https://api.anthropic.com` and choose a Claude model. For Groq, use the Groq API base URL.

API key features are NOT TESTED in QC (requires valid credentials and interactive session).

## Health Check
The container uses an import-based healthcheck:

```bash
python -c "from core.agents.orchestrator import Orchestrator"
```

This verifies the core package is importable without starting a project or touching the network.

**QC result:** Import passes. HEALTHCHECK returns healthy.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| None | | | All configuration is via config.json, not environment variables |

## Persistent Storage
| Path | Purpose |
|------|---------|
| `/app/data` | SQLite database and generated project files. Mount a volume to persist across runs. |

## Notes
- The container must be run with `-it` (interactive + TTY). gpt-pilot is a conversational CLI that requires stdin.
- The container runs as non-root user `pilot` (UID 1000).
- SQLite is used by default. No external database is required.
- Generated project code is written under `/app/data`. Use a named volume or bind mount to access it from the host.
- The upstream repository is `Pythagora-io/gpt-pilot`. The published image on Docker Hub is `hoomzoom/gpt-pilot`.

## Changes from Original
- The upstream Dockerfile builds a full code-server (VS Code in browser) image and requires a proprietary VSIX extension (`pythagora-vs-code.vsix`) that is not publicly distributed. That file is absent from the public repository, making the upstream Dockerfile unbuildable as-is.
- A custom slim Dockerfile was written that installs only the CLI core (`pythagora-core` v2.0.10) without code-server or the VSIX extension.
- System dependencies `git` and `build-essential` were added. `git` is needed because gpt-pilot shells out to git during project generation. `build-essential` is needed to compile C extensions (`tiktoken`, `greenlet`).
- A non-root user `pilot` (UID 1000) was added.
- An import-based HEALTHCHECK was added.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied to `requirements.txt`. All `>=` specifiers converted to `==` exact versions. No dependency bumps were needed. All minimum versions resolved successfully.
