# Integuru -- Usage Documentation

## Overview
AI agent that reverse-engineers platform internal APIs by analyzing browser network traffic (HAR files). Uses LLM to identify API endpoints, extract dynamic parameters, build dependency graphs, and generate reusable Python code.

## Quick Start

```bash
docker pull hoomzoom/integuru
```

### Run CLI
```bash
docker run --rm -e OPENAI_API_KEY=sk-... \
  -v ./network_requests.har:/app/network_requests.har \
  -v ./cookies.json:/app/cookies.json \
  hoomzoom/integuru --prompt "download utility bills" --model gpt-4o
```

## HAR File Capture (Manual Step)

HAR capture must be done on a local machine with a browser, not inside Docker:

```bash
# On your local machine (not in Docker):
pip install playwright
playwright install chromium
python create_har.py
```

This opens a Chromium browser. Log into the target platform, perform the action you want to reverse-engineer, then press Enter. Saves `network_requests.har` and `cookies.json`.

## CLI Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| --prompt | Yes | None | Description of the action to reverse-engineer |
| --model | No | gpt-4o | OpenAI model (gpt-4o, o1-mini, o1) |
| --har | No | network_requests.har | Path to HAR file |
| --cookies | No | cookies.json | Path to cookies file |

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key |

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | CLI --help | PASS |
| 2 | Python import (integuru module) | PASS |
| 3 | Playwright chromium installed | PASS |
| 4 | Full HAR analysis | NOT TESTED (requires HAR file + API key) |

## Notes
- HAR capture (`create_har.py`) requires a GUI browser and cannot run in Docker.
- The tool works best with o1-mini or o1 models for code generation accuracy.
- Output includes a dependency graph visualization and generated Python code.
- Playwright + Chromium are installed in the image for potential headless browser operations within the agent.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied via Poetry. Added `poetry lock` step to Dockerfile to regenerate lock file after pinning. No dependency bumps were needed.
