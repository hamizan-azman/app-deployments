# BruteForceAI. Usage Documentation

## Overview
CLI tool that uses AI to perform intelligent login brute force attacks and analyze authentication endpoints. Supports local LLMs via Ollama or cloud inference via Groq. Uses Playwright with Chromium for browser-based interaction with login forms.

## Quick Start
```bash
docker pull hoomzoom/bruteforceai
docker run --rm hoomzoom/bruteforceai --help
```

## No Port Exposed
This is a CLI-only tool. No web interface, no HTTP server, no exposed port.

## Subcommands

### analyze
Analyze a login page and profile its authentication mechanism before attacking.
```bash
docker run --rm hoomzoom/bruteforceai analyze --url http://target.com/login
```

### attack
Run an AI-assisted brute force attack against a login endpoint.
```bash
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -e GROQ_API_KEY=<your-key> \
  hoomzoom/bruteforceai attack \
    --url http://target.com/login \
    --username admin \
    --wordlist /path/to/wordlist.txt \
    --llm-api-key <your-key>
```

### clean-db
Clear the local SQLite database of stored results.
```bash
docker run --rm -v bruteforceai-data:/app/db hoomzoom/bruteforceai clean-db
```

### check-updates
Check for upstream updates to the tool.
```bash
docker run --rm hoomzoom/bruteforceai check-updates
```

## LLM Backend Options

### Option A: Groq (cloud, no local GPU needed)
Pass your Groq API key via `--llm-api-key` or as an environment variable.
```bash
docker run --rm \
  -e GROQ_API_KEY=<your-key> \
  hoomzoom/bruteforceai attack --llm-api-key <your-key> ...
```

### Option B: Ollama (local, no API key needed)
Run Ollama on the host and point the container at it.
```bash
# Start Ollama on host first, then:
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  hoomzoom/bruteforceai attack \
    --ollama-host http://host.docker.internal:11434 \
    ...
```

## Health Check
```bash
docker run --rm hoomzoom/bruteforceai --help
# or
docker run --rm hoomzoom/bruteforceai python -c "import playwright"
```
Both pass. No HTTP endpoint to test.

## QC Test Result
Playwright import: PASS

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GROQ_API_KEY | No | None | Groq API key for cloud LLM inference |

API key can also be passed directly via `--llm-api-key` CLI flag.

## Notes
- The container does not run a server. Use `docker run --rm` for one-off invocations.
- Chromium is pre-installed by the Playwright base image. `playwright install chromium` is run at build time for the non-root user layer.
- SQLite is used internally for storing results. It is part of the Python standard library and does not need to be pip-installed.
- For attacks against services running on the host machine, use `--add-host=host.docker.internal:host-gateway` and address the target as `http://host.docker.internal:<port>`.
- API key features (LLM calls) are NOT TESTED in automated QC. Infrastructure (browser, imports) is confirmed working.

## Changes from Original
- `sqlite3` removed from `requirements.txt`. It is a Python standard library module and cannot be installed via pip. The original requirements file listed it incorrectly. Removing it fixes the build with no functional change.
- Build context uses the repo root (`apps/BruteForceAI/`) with the pinned requirements file copied from `dockerfiles/BruteForceAI/requirements.txt` before the app source is copied in.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=` specifiers changed to `==` exact versions). All minimum versions resolved successfully with no bumps needed, except `sqlite3` which was removed entirely (not a pip package).
