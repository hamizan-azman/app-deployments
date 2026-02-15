# RD-Agent -- Usage Documentation

## Overview
Microsoft's autonomous R&D framework that uses LLMs to automate data-driven research workflows: financial factor discovery, quantitative trading, Kaggle competition automation, and ML model extraction from papers.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/rd-agent

# Or build from source
docker build -t rd-agent ./RD-Agent

docker run --rm hoomzoom/rd-agent --help
```

## Base URL
http://localhost:19899 (Streamlit UI)

## Core Features
- Autonomous financial factor discovery and backtesting
- Quantitative model development
- Kaggle competition automation
- ML model extraction from research papers
- Streamlit web UI for log visualization
- Health check and diagnostics

## CLI Commands

### Show help
- **Command:** `rdagent --help`
- **Run:** `docker run --rm rd-agent --help`
- **Tested:** Yes

### Health check
- **Command:** `rdagent health_check`
- **Description:** Checks Docker availability, port status, and API key config
- **Run:**
```bash
# Full check (needs Docker socket + API key)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e CHAT_MODEL=gpt-4o \
  -e EMBEDDING_MODEL=text-embedding-3-small \
  rd-agent health_check

# Port check only
docker run --rm rd-agent health_check --no-check-env --no-check-docker
```
- **Tested:** Yes (port check passes; Docker/env checks require socket mount and API key)

### Collect system info
- **Command:** `rdagent collect_info`
- **Description:** Prints OS, Python version, and Docker status
- **Run:** `docker run --rm rd-agent collect_info`
- **Tested:** Yes (system info prints; Docker portion fails without socket mount)

### Streamlit UI
- **Command:** `rdagent ui --port 19899`
- **Description:** Web app to view log traces from executed workflows
- **Run:**
```bash
docker run -d -p 19899:19899 --name rd-agent-ui rd-agent ui --port 19899
```
- **Access:** http://localhost:19899
- **Tested:** Yes (HTTP 200, Streamlit loads)

### Financial factor discovery
- **Command:** `rdagent fin_factor`
- **Description:** Auto R&D evolving loop for fintech factors
- **Run:**
```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e CHAT_MODEL=gpt-4o \
  -e EMBEDDING_MODEL=text-embedding-3-small \
  rd-agent fin_factor
```
- **Tested:** No (requires API key + Docker socket + Qlib data)

### Financial model development
- **Command:** `rdagent fin_model`
- **Description:** Auto R&D evolving loop for fintech models
- **Run:** Same pattern as fin_factor, replace command with `fin_model`
- **Tested:** No (requires API key + Docker socket + Qlib data)

### Quantitative finance
- **Command:** `rdagent fin_quant`
- **Description:** Combined factor + model loop for quantitative trading
- **Run:** Same pattern as fin_factor, replace command with `fin_quant`
- **Tested:** No (requires API key + Docker socket + Qlib data)

### Factor extraction from reports
- **Command:** `rdagent fin_factor_report`
- **Description:** Extracts factors from finance reports, then implements them
- **Tested:** No (requires API key + report files)

### General model extraction
- **Command:** `rdagent general_model`
- **Description:** Extracts and implements models from research papers
- **Tested:** No (requires API key + paper files)

### Data science (Kaggle)
- **Command:** `rdagent data_science --competition <name>`
- **Description:** Automates Kaggle competition workflows
- **Run:**
```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e CHAT_MODEL=gpt-4o \
  -e EMBEDDING_MODEL=text-embedding-3-small \
  -e KAGGLE_USERNAME=$KAGGLE_USERNAME \
  -e KAGGLE_KEY=$KAGGLE_KEY \
  rd-agent data_science --competition titanic
```
- **Tested:** No (requires API key + Kaggle credentials)

### Grade summary
- **Command:** `rdagent grade_summary`
- **Description:** Generates test scores for log traces
- **Tested:** No (requires existing log data)

### Data science interactive UI
- **Command:** `rdagent ds_user_interact --port 19900`
- **Run:** `docker run -d -p 19900:19900 rd-agent ds_user_interact --port 19900`
- **Tested:** No

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for LLM calls |
| CHAT_MODEL | Yes | None | Chat model name (e.g., gpt-4o) |
| EMBEDDING_MODEL | Yes | None | Embedding model (e.g., text-embedding-3-small) |
| OPENAI_API_BASE | No | None | Custom API base URL |
| KAGGLE_USERNAME | No | None | Kaggle username (for data_science command) |
| KAGGLE_KEY | No | None | Kaggle API key |
| DEEPSEEK_API_KEY | No | None | Alternative: use DeepSeek instead of OpenAI |
| LITELLM_PROXY_API_KEY | No | None | Separate embedding API key |
| LITELLM_PROXY_API_BASE | No | None | Separate embedding API base |
| MAX_RETRY | No | 10 | Max LLM call retries |
| RETRY_WAIT_SECONDS | No | 20 | Wait between retries |
| USE_CHAT_CACHE | No | False | Enable chat response caching |
| USE_EMBEDDING_CACHE | No | False | Enable embedding caching |

## Docker Socket Mount
RD-Agent uses Docker internally to execute generated code. For full functionality, mount the host Docker socket:
```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e CHAT_MODEL=gpt-4o \
  -e EMBEDDING_MODEL=text-embedding-3-small \
  rd-agent <command>
```

## Test Summary
| Test | Result |
|------|--------|
| Docker build | PASS |
| rdagent --help | PASS |
| health_check (port check) | PASS |
| collect_info (system info) | PASS |
| Streamlit UI (port 19899) | PASS (HTTP 200) |
| fin_factor / fin_model / fin_quant | NOT TESTED (needs API key + Qlib) |
| data_science | NOT TESTED (needs API key + Kaggle) |
| general_model | NOT TESTED (needs API key + papers) |

## Notes
- No public Dockerfile existed in the repo. Dockerfile written from scratch.
- The internal `.devcontainer/Dockerfile` uses a private Azure Container Registry image and is not available for public use.
- RD-Agent requires Docker-in-Docker for scenario execution. Without Docker socket mount, only the CLI, health_check, and UI work.
- All R&D scenario commands (fin_*, data_science, general_model) require an LLM API key and Docker socket.
- Image is based on python:3.10-slim. Build takes ~2 minutes on first run.
- Official support is Linux only; the Docker container handles this on Windows/Mac.
