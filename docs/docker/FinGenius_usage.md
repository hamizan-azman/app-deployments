# FinGenius. Usage Documentation

## Overview
CLI financial analysis tool that uses a multi-agent LLM system to research stocks and generate investment analysis reports. Accepts a stock code as input, runs a pipeline of specialized agents, and writes a Markdown report to the output directory. Supports OpenAI-compatible APIs, Anthropic, and Ollama as LLM backends.

## Quick Start
```bash
docker pull hoomzoom/fingenius

# Create a config file and output directory on the host
mkdir -p ./config ./report
cp /path/to/your/config.toml ./config/config.toml

docker run --rm \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd)/report:/app/report" \
  hoomzoom/fingenius AAPL
```

The report is written to `./report/` on the host after the run completes.

## Entry Point
```
python main.py <stock_code>
```

There is no web interface and no exposed port. The container runs to completion and exits.

## Configuration

FinGenius reads its LLM provider settings from `/app/config/config.toml` inside the container. Mount a `config.toml` from the host at that path before running.

### config.toml structure
```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.0

[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."
max_tokens = 4096
temperature = 0.0
```

For Anthropic or Ollama, set `base_url` and `model` to the appropriate values for each provider.

## Volume Mounts
| Mount | Purpose |
|-------|---------|
| `/app/config` | Directory containing `config.toml` with LLM provider settings |
| `/app/report` | Directory where the generated analysis report is written |

Both volumes should be mounted for the container to function correctly.

## Example Run Commands

### OpenAI provider
```bash
docker run --rm \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd)/report:/app/report" \
  hoomzoom/fingenius AAPL
```

### Passing API key via environment (modify config.toml to read from env if supported)
The recommended approach is to write the API key directly into `config.toml` before mounting. Do not store keys in the Dockerfile or image.

### Help flag
```bash
docker run --rm hoomzoom/fingenius --help
```

## Health Check
The container healthcheck runs `python main.py --help`. There is no HTTP endpoint. The check passes if the Python environment and entry point are intact.

## API Key Requirements
| Key | Required | Notes |
|-----|----------|-------|
| LLM provider key | Yes | Written into `config/config.toml` before mounting. Supports OpenAI, Anthropic, Ollama. |

Financial data (stock prices, fundamentals) is fetched via the `efinance` library using public APIs. No additional financial data API key is required.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- No port is exposed. This is a batch CLI tool, not a server.
- Output reports are written to `/app/report/` inside the container. Mount this directory to retrieve results.
- The `efinance` package downloads financial data to a cache directory inside the container. Permissions on that directory are set to world-writable at build time to allow the non-root user to write cache files.
- Stock codes follow the conventions expected by `efinance` (e.g., US tickers like `AAPL`, Chinese A-share codes like `600519`).

## Changes from Original
- No existing Dockerfile in the upstream repo. Dockerfile written from scratch following project patterns.
- Added non-root user `appuser` (UID 1000).
- Added `VOLUME` declarations for `/app/config` and `/app/report`.
- Applied `chmod a+rw` to the `efinance` package data directory to fix a permission error that prevented the non-root user from writing cache files at runtime.
- Added `HEALTHCHECK` using `python main.py --help`.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed. All minimum versions resolved without conflicts.
