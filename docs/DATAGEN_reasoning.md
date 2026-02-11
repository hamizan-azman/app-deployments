# DATAGEN. Deployment Reasoning

## App Classification
- Type: CLI multi-agent pipeline (no web UI)
- Framework: LangChain, LangGraph
- Python version: 3.10
- Entry point: `python main.py`
- Ports: None

## Deployment Decision
Deployed as a CLI container. The app is a pipeline that runs to completion and exits, so no persistent server process or exposed port is needed. The `/app/data` volume handles all input and output. This matches the original developer's intended usage pattern.

## Dockerfile Decisions

### Base image
Used `python:3.10-slim`. The upstream project targets Python 3.10 and slim is sufficient for a non-GUI pipeline. No Playwright involved, so the trixie/bookworm concern does not apply here.

### Google Chrome and ChromeDriver
The app uses Selenium for data collection tasks, which requires a real browser binary and a matching driver. The upstream `.env.example` includes a `CHROMEDRIVER_PATH` field, confirming this is an expected dependency.

Chrome was installed via the official Google .deb package (`google-chrome-stable_current_amd64.deb`). ChromeDriver was then installed by querying the Chrome for Testing API to fetch the exact version matching the installed Chrome build. This keeps Chrome and ChromeDriver version-locked at build time.

Installing Chrome via the .deb package also pulls in all required system libraries (NSS, D-Bus, fonts, etc.) as package dependencies, which avoids the fragile manual `apt-get install` lists that commonly miss libraries and cause runtime crashes.

### Non-root user
Added `appuser` at UID 1000 following the project standard. The `/app/data` directory is created and chowned before switching users so the pipeline can write output files without permission errors.

### Environment variables
`CHROMEDRIVER_PATH` and `WORKING_DIRECTORY` are set as ENV defaults to match the upstream `.env.example`. This means the container works correctly out of the box without requiring the user to pass these variables manually.

### Health check
The container has no HTTP endpoint to probe, so the health check is an import test: `python -c "import langchain"`. This confirms the Python environment installed correctly and the core dependency is importable. It does not test LLM connectivity, which requires a live API key and is not appropriate for a passive health check.

### No EXPOSE
No port is exposed because this is a CLI tool with no server process. Omitting EXPOSE makes the container's purpose explicit.

## Build Notes
- The Chrome .deb install step is the longest step in the build due to the size of the Chrome package and its dependencies.
- The ChromeDriver download step requires outbound HTTPS access to `googlechromelabs.github.io` and `storage.googleapis.com` at build time. These are stable Google-hosted endpoints.
- The `--no-cache-dir` flag on pip install keeps the image smaller by not retaining the pip cache.

## V2 Pinning Notes
All `>=` specifiers in requirements.txt were converted to `==` exact versions. All minimum declared versions resolved without conflicts. No bumps or era-matching were needed.

## QC Testing
- Health check (import test): Pass
- LLM pipeline execution: NOT TESTED. Requires a valid LLM API key and input data file. Infrastructure is confirmed functional via the import test.

## What Each Test Validates
- `python -c "import langchain"`: Confirms Python 3.10 environment is intact, LangChain installed correctly, and the container starts without crashing. Sufficient for infrastructure-level QC on a CLI tool.
