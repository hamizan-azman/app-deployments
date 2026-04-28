# Aider. Usage Documentation

## Overview
CLI AI pair programming tool that runs inside your terminal. It lets you edit code in a local git repository using a conversational interface backed by an LLM. Supports OpenAI, Anthropic, DeepSeek, and other providers.

## Quick Start
```bash
docker pull hoomzoom/aider
docker run --rm -it \
  -v $(pwd):/app \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  hoomzoom/aider
```

Your current directory is mounted into the container at `/app`. Aider operates on the files there and commits changes via git.

## Browser Mode (Optional)
Aider can serve a browser UI on port 8501 with `--browser`.

```bash
docker run --rm -it \
  -v $(pwd):/app \
  -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  hoomzoom/aider --browser
```

Open http://localhost:8501 in your browser.

## Common Commands

### Ask about a file
```bash
docker run --rm -it \
  -v $(pwd):/app \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  hoomzoom/aider --message "Explain what main.py does" main.py
```

### Use Anthropic Claude instead of OpenAI
```bash
docker run --rm -it \
  -v $(pwd):/app \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  hoomzoom/aider --model claude-3-5-sonnet-20241022
```

### Use DeepSeek
```bash
docker run --rm -it \
  -v $(pwd):/app \
  -e DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY \
  hoomzoom/aider --model deepseek/deepseek-chat
```

### Run help only
```bash
docker run --rm hoomzoom/aider --help
```

## Volume Mount
The volume mount is required for aider to function. Without it, there are no files to edit.

| Host path | Container path | Purpose |
|-----------|---------------|---------|
| `$(pwd)` | `/app` | Your code repository |

The container's working directory is `/app`. Aider reads and writes files here, and creates git commits in the mounted repo.

Note: Use `MSYS_NO_PATHCONV=1` before `docker run` in Git Bash on Windows to prevent path mangling.

## Health Check
The Dockerfile healthcheck runs `aider --help` every 30 seconds. This validates that the CLI is installed and executable. No HTTP endpoint is exposed.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | One required | None | OpenAI API key |
| ANTHROPIC_API_KEY | One required | None | Anthropic API key |
| DEEPSEEK_API_KEY | One required | None | DeepSeek API key |

At least one API key must be provided. Which key to supply depends on which model you pass via `--model`.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- Aider creates a `.aider` cache directory. With `HOME=/app`, this lands in your mounted project directory.
- No port is exposed by default. Port 8501 is only used in `--browser` mode.
- API features are NOT TESTED in this deployment. Infrastructure (CLI startup, `--help`) is confirmed working.
- The mounted repo must be a valid git repository for aider to commit changes. Run `git init` first if needed.

## Changes from Original
- Installed from PyPI (`aider-chat`) instead of from source. The upstream source install uses setuptools-scm for version detection, which fails inside a git submodule environment (the `apps/aider` submodule has no tags). PyPI install is the recommended install path in the official aider docs and behaves identically at runtime.
- Base image is `python:3.12-slim-bookworm` (Debian bookworm). Not `python:3.12-slim` (Debian trixie) to avoid dependency breakage patterns seen on other apps.
- A virtual environment at `/venv` is used to isolate the aider install from the system Python.
- `git config --system safe.directory /app` is set so git operations on the mounted volume work correctly without ownership warnings.

## V2 Dependency Changes (Minimum Version Pinning)
Pinning not applied. Aider is installed as a single package (`aider-chat`) with no explicit version pin. PyPI resolves the latest stable release. The package manages its own transitive dependency tree internally. Pinning individual transitive deps is not feasible here.
