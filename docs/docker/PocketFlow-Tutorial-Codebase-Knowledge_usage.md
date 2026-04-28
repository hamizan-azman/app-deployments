# PocketFlow-Tutorial-Codebase-Knowledge. Usage Documentation

## Overview
CLI tool that crawls a GitHub repository or local directory and generates a structured tutorial explaining the codebase. Uses an LLM to identify core abstractions, trace relationships between them, and produce beginner-friendly documentation in Markdown or other formats.

## Quick Start
```bash
docker pull hoomzoom/pocketflow
docker run --rm -e GEMINI_API_KEY=<your_key> -v $(pwd)/output:/app/output hoomzoom/pocketflow --repo https://github.com/user/repo
```

Output files are written inside the container. Mount a volume to retrieve them on the host.

## Entry Point
```
python main.py [--repo <url>] [--dir <path>] [options]
```

## Core Features
- Crawl any public GitHub repository by URL
- Crawl a local directory via --dir
- Identify core abstractions and generate chapter-by-chapter tutorial docs
- Supports Gemini (default), OpenAI, and any OpenAI-compatible provider
- Optional GitHub token for private repositories

## Commands

### Analyse a public GitHub repo
```bash
docker run --rm \
  -e GEMINI_API_KEY=<your_key> \
  -v $(pwd)/output:/app/output \
  hoomzoom/pocketflow \
  --repo https://github.com/user/repo
```

### Analyse a local directory
```bash
docker run --rm \
  -e GEMINI_API_KEY=<your_key> \
  -v /path/to/code:/app/input:ro \
  -v $(pwd)/output:/app/output \
  hoomzoom/pocketflow \
  --dir /app/input
```

### Use an OpenAI provider instead of Gemini
```bash
docker run --rm \
  -e OPENAI_API_KEY=<your_key> \
  -v $(pwd)/output:/app/output \
  hoomzoom/pocketflow \
  --repo https://github.com/user/repo
```

### Access a private GitHub repository
```bash
docker run --rm \
  -e GEMINI_API_KEY=<your_key> \
  -e GITHUB_TOKEN=<your_token> \
  -v $(pwd)/output:/app/output \
  hoomzoom/pocketflow \
  --repo https://github.com/user/private-repo
```

## Health Check
No HTTP endpoint. The Dockerfile healthcheck runs:
```
python -c "import main"
```
This confirms the application module loads correctly.

## QC Test Result
- `python -c "import main"` passes inside the container.
- Running `docker run --rm hoomzoom/pocketflow` (no args) exits with a usage error, confirming the entrypoint is wired correctly and the --repo or --dir argument is required.
- Tested: Yes (module import check). Full generation NOT tested (requires live API key and network access).

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GEMINI_API_KEY | Yes (if using Gemini) | None | Google Gemini API key. Default LLM provider. |
| OPENAI_API_KEY | No | None | OpenAI or compatible provider API key. |
| GITHUB_TOKEN | No | None | GitHub personal access token for private repos. |

At least one LLM API key must be provided at runtime. Neither key is baked into the image.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- No port is exposed. This is a CLI batch tool with no web interface.
- Output is written inside the container at runtime. Mount a host volume to persist results.
- The upstream repository includes its own Dockerfile, which was used as the base for this deployment.
- On Windows with Git Bash, prefix docker run with `MSYS_NO_PATHCONV=1` to prevent path mangling on volume mounts.

## Changes from Original
- Added non-root user (`appuser`, UID 1000). The upstream Dockerfile ran as root.
- Added HEALTHCHECK using `python -c "import main"` to satisfy deployment standards. The original had no healthcheck.
- No changes to dependencies, entrypoint, or application logic.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=` specifiers changed to `==` exact versions). No dependency bumps were needed. All minimum versions resolved successfully on PyPI.
