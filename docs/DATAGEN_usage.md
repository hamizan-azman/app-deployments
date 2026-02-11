# DATAGEN. Usage Documentation

## Overview
CLI multi-agent data analysis pipeline built on LangChain and LangGraph. Accepts structured or unstructured data files, orchestrates a team of LLM-powered agents to analyze and reason over the data, and writes results to an output directory. Google Chrome and ChromeDriver are bundled for Selenium-based data collection tasks.

## Quick Start
```bash
docker pull hoomzoom/datagen
docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -v /path/to/your/data:/app/data \
  hoomzoom/datagen
```

## No Web Interface
This is a CLI tool. There are no HTTP endpoints and no browser UI. Interaction is through environment variables, mounted data volumes, and container logs.

## Running the Container

### With OpenAI
```bash
docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -v /path/to/your/data:/app/data \
  hoomzoom/datagen
```

### With Anthropic
```bash
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v /path/to/your/data:/app/data \
  hoomzoom/datagen
```

### With Google AI
```bash
docker run --rm \
  -e GOOGLE_API_KEY=your_key_here \
  -v /path/to/your/data:/app/data \
  hoomzoom/datagen
```

### Windows (Git Bash, prevent path mangling)
```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -e OPENAI_API_KEY=your_key_here \
  -v /path/to/your/data:/app/data \
  hoomzoom/datagen
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | One of these three is required | None | OpenAI API key |
| ANTHROPIC_API_KEY | One of these three is required | None | Anthropic Claude API key |
| GOOGLE_API_KEY | One of these three is required | None | Google AI API key |
| CHROMEDRIVER_PATH | No | /usr/local/bin/chromedriver | Path to ChromeDriver binary (pre-set in image) |
| WORKING_DIRECTORY | No | /app/data/ | Directory used for input and output files (pre-set in image) |

At least one LLM API key must be provided. The app will fail at runtime if no key is available.

## Volumes
| Mount point | Purpose |
|-------------|---------|
| `/app/data` | Input data files and analysis outputs. Mount a host directory here to pass in data and retrieve results. |

## Health Check
The container health check runs:
```bash
python -c "import langchain"
```
A healthy container exits 0. This confirms the Python environment is intact. It does not test LLM connectivity.

## QC Test Result
- Import test (`import langchain`): Pass
- LLM-dependent features: NOT TESTED (requires valid API key at test time)

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- Google Chrome and a matching ChromeDriver are bundled in the image for Selenium-based workflows.
- CHROMEDRIVER_PATH and WORKING_DIRECTORY are set as ENV defaults in the image. They can be overridden at runtime if needed.
- Place input files in the mounted `/app/data` directory before running. Output files are written to the same directory.
- The container exits after the pipeline completes. Use `--rm` to auto-remove it after each run.

## Changes from Original
- Added Google Chrome installation via official Google .deb package.
- Added ChromeDriver installation matched to the installed Chrome version using the Chrome for Testing API.
- Added non-root user `appuser` (UID 1000).
- Added HEALTHCHECK using `python -c "import langchain"`.
- Set ENV defaults for CHROMEDRIVER_PATH and WORKING_DIRECTORY to match the upstream `.env.example`.
- Created `/app/data` directory with correct ownership.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied. All `>=` specifiers converted to `==` exact versions. No dependency bumps were needed. All minimum versions resolved successfully.
