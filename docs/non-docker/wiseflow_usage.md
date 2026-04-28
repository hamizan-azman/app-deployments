# wiseflow. Local Install Guide

**Deployment**: Workstation with full (non-headless) Chrome or Chromium installed.

## Overview
wiseflow is a web-monitoring and information-extraction agent. It periodically crawls a user-defined list of sources (social feeds, forums, news sites, research pages), passes fetched content through an LLM for filtering and summarisation, and writes the results into a local database. The crawler is Chrome-based.

## Why Not Dockerized
The crawler depends on a real, non-headless Chrome/Chromium instance with a visible profile and JavaScript execution parity to a normal browser. The upstream README states that headless Chrome and most containerised browser setups fail on a large fraction of target sites (captcha walls, bot-detection redirects, sites that block `HeadlessChrome` in the UA). The repo ships no Dockerfile and the maintainers do not support Docker. Running it in a container would either degrade crawl coverage below usable levels, or require a full X server plus undetected-chromedriver stack that defeats the point of the research benchmark.

## Requirements
- OS. Windows 10/11, macOS, or Linux with a desktop environment
- Python 3.10 or newer
- Google Chrome or Chromium (full, non-headless build) installed on the host
- About 4 GB RAM free (peaks during crawl cycles)
- OpenAI-compatible LLM endpoint. OpenAI, DeepSeek, or a local OpenAI-compatible server such as vLLM or Ollama

## Installation

```bash
git clone https://github.com/TeamWiseFlow/wiseflow.git
cd wiseflow/core

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in `LLM_API_KEY`, `LLM_API_BASE`, `PRIMARY_MODEL`, and `PB_API_BASE` (PocketBase URL, default `http://127.0.0.1:8090`).

Start the bundled PocketBase backend.

```bash
cd pb
./pocketbase serve
```

## Usage

In a second terminal.

```bash
cd wiseflow/core
source .venv/bin/activate
python run_task.py
```

Point your browser at `http://127.0.0.1:8090/_/` to configure the source list, focus points, and schedule. The agent iterates through the configured sources at the configured interval.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| LLM_API_KEY | Yes | None | API key for the LLM backend |
| LLM_API_BASE | Yes | None | Base URL of the OpenAI-compatible LLM |
| PRIMARY_MODEL | Yes | None | Model name (e.g. `gpt-4o-mini`, `deepseek-chat`) |
| PB_API_BASE | Yes | http://127.0.0.1:8090 | PocketBase URL |
| PROJECT_DIR | No | `./work_dir` | Where crawler state and logs are written |

## Notes
- The project is designed to run next to a desktop Chrome install. Forcing it onto headless Chrome yields capture failures on roughly half the common source types the benchmark list uses.
- PocketBase is bundled as the storage layer. No external database is required.
- Upstream restructure caught 27 April 2026. The repo no longer has a `core/` subdirectory. The current top-level layout is a TypeScript / Node project (`package.json`, `pnpm-lock.yaml`) with directories `addons/`, `awada/`, `crews/`, `skills/`, `config-templates/`, plus an `openclaw.version` file. The Python + PocketBase + Chromium install path described above belongs to an earlier version of the project and no longer matches HEAD. The install steps in this doc need a full rewrite against the current upstream before the app can be re-deployed.
- GitHub. https://github.com/TeamWiseFlow/wiseflow
