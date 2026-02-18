# Integuru -- Reasoning Log

## Initial Assessment

Integuru is a CLI tool by Integuru-AI that reverse-engineers platform APIs by analyzing HAR (HTTP Archive) files captured from browser sessions. It uses LangGraph/LangChain with OpenAI to analyze network traffic patterns, identify API endpoints, and generate Python code to replicate browser actions programmatically.

## What Was Checked

1. **pyproject.toml**: Poetry-based project, Python 3.12 only (>=3.12,<3.13). 16 direct dependencies including langchain-openai, langgraph, playwright, click, networkx, matplotlib. Entry point is `integuru = "integuru.__main__:cli"`.

2. **integuru/__main__.py**: Click-based CLI. Takes --prompt, --model, --har, --cookies options. Loads HAR file and cookies, passes to the LangGraph agent for analysis.

3. **create_har.py**: Playwright script that opens a real Chromium browser (headless=False), records all network requests as HAR, waits for user to interact with the browser, then saves HAR + cookies. This requires a GUI display and cannot run in Docker.

4. **poetry.lock**: 330+ locked packages. Full dependency resolution available.

## Decisions Made

### Base image: python:3.12-slim
Required Python >=3.12,<3.13. Slim variant works since Playwright handles its own browser deps.

### Poetry with --only main --no-root
Used Poetry for dependency management since the project uses poetry.lock. The `--no-root` flag is needed because README.md is referenced in pyproject.toml but not copied at the dep install stage. `--only main` replaces the deprecated `--no-dev`.

### Playwright chromium installation
Added `playwright install --with-deps chromium` to install browser + system dependencies. While the main use case (HAR analysis) doesn't need a browser, the agent may use Playwright for verification steps.

### CLI entrypoint
Set ENTRYPOINT to `integuru` (the Click CLI). Users pass arguments directly.

## Build Issues

### Poetry --no-dev deprecated
First attempt used `--no-dev` which is removed in newer Poetry versions. Fixed to `--only main`.

### Missing README.md at install stage
Poetry tried to install the project package and failed because README.md wasn't copied yet. Fixed with `--no-root` to skip installing the current project, then copy source later.

## Testing Plan

1. CLI --help: Validates package installed and entry point works
2. Module import: Validates internal dependencies resolve
3. Playwright chromium: Validates browser is installed
4. Full run: Requires real HAR file + OpenAI API key

## Gotchas

1. **HAR capture is local-only**: The `create_har.py` script opens a real browser window for the user to interact with. This fundamentally cannot work in a headless Docker container. Users must capture HAR files on their local machine and mount them into the container.

2. **OpenAI API key mandatory**: Unlike some tools that can fall back to local models, Integuru requires OpenAI specifically (langchain-openai).

3. **Python 3.12 strict**: The pyproject.toml pins Python to >=3.12,<3.13. Using 3.11 or 3.13 would fail dependency resolution.
