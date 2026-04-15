# skyvern. Reasoning Log

## Initial Assessment

Skyvern is an LLM-powered browser automation platform. The agent receives a task in natural language, opens a real browser via Playwright, takes screenshots, and uses an LLM with vision capability to decide what to click or type. The architecture is three-tier: a FastAPI backend that runs agents, a React frontend, and PostgreSQL for persistence. A VNC server lets operators watch browser sessions in real time.

## What Was Checked

1. **README.md**: Describes installation via a one-line installer script. The upstream compose file runs several services. Docker Hub image exists at `skyvern-cloud/skyvern`.

2. **Dockerfile (upstream)**: Well-structured multi-stage build. Stage 1 uses `python:3.11` and `uv` to compile a `requirements.txt` from `pyproject.toml`. Stage 2 uses `python:3.11-slim-bookworm`, installs Playwright, installs X11/VNC tools, installs Node.js, installs Bitwarden CLI, copies app source, and runs the entry point script.

3. **Playwright base image requirement**: Playwright requires several Debian libraries (`libgbm1`, `libnspr4`, `libnss3`, etc.) that are present in `bookworm` but not in the default `slim` image which tracks `trixie`. Using `python:3.11-slim-bookworm` avoids this.

4. **xdpyinfo vs x11-utils**: The upstream apt install list included `xdpyinfo` as a package name. That name is not a valid apt package. The `xdpyinfo` binary is provided by the `x11-utils` package. The fix is to replace `xdpyinfo` with `x11-utils`.
This was one of the more involved builds. The VNC streaming setup with Xvfb and websockify is pretty complex for what is essentially a browser automation tool.

5. **entrypoint-skyvern.sh**: A shell script that starts Xvfb, x11vnc, websockify (noVNC), and the FastAPI server. The script has Windows line endings when cloned on a Windows host, causing `/bin/bash: bad interpreter: No such file or directory`. The `sed -i 's/\r$//'` fix in the Dockerfile normalises line endings at build time.

6. **docker-compose.yml**: Defines three services (postgres, skyvern, skyvern-ui). LLM provider blocks are commented out. The operator must uncomment one block and supply the matching API key before the stack is functional.

7. **Bitwarden CLI**: Installed via `npm install -g @bitwarden/cli`. This enables Skyvern's credential vault integration feature. Not required for basic task execution.

## Decisions Made

### Used the existing Dockerfile with minimal fixes
The upstream Dockerfile is well constructed. Only two fixes were needed: replacing the invalid `xdpyinfo` package name with `x11-utils`, and adding the CRLF strip for the entrypoint script.

### Multi-container compose deployment
The original architecture expects separate postgres and UI containers. Merging them would violate the architectural fidelity rule and break the agent-database connection pattern.

### LLM key as a prerequisite
Skyvern cannot execute any tasks without a functioning LLM with vision capability. The compose file is pre-configured with commented-out provider blocks. The operator must activate one before deployment. This is documented prominently in the usage doc.

### VNC included by default
The `entrypoint-skyvern.sh` starts x11vnc and websockify alongside the main API. Port 6080 is exposed. This is part of the original architecture and is useful for observing agent behaviour, which is directly relevant to supply chain security research.

### postgres:14-alpine
The upstream compose file pins PostgreSQL 14. This version is kept as-is to maintain architectural fidelity.

## Testing

### Tests Performed
1. **Import check** (`docker compose exec skyvern python -c "import skyvern; print('ok')`): Module imported. Pass.
2. **Health endpoint** (GET `/api/v1/health`): Returns status JSON. Pass.

### What Was Not Tested
- Actual task execution (requires valid LLM API key with vision capability).
- Bitwarden credential vault integration.
- VNC streaming (requires a display-capable client).
- Workflow definitions and long-running agent sessions.

## Gotchas

1. **xdpyinfo is not a package**: `xdpyinfo` is a binary in the `x11-utils` package. Using it directly as an apt package name causes `apt-get install` to fail with "Unable to locate package". Replace with `x11-utils`.

2. **CRLF in entrypoint script**: When the repository is cloned on Windows, shell scripts get CRLF line endings. Docker runs these scripts on Linux, where the `\r` character causes `/bin/bash` to be treated as `/bin/bash\r`, which does not exist. The `sed -i 's/\r$//'` fix must run before `chmod +x`.

3. **bookworm vs trixie**: Playwright's Chromium dependencies are tested against specific Debian library versions. The default `python:3.11-slim` now tracks Debian trixie (in-progress), which has different library versions than the Playwright browser binaries expect. The explicit `python:3.11-slim-bookworm` tag locks to a stable known-good Debian release.

4. **LLM key required at runtime, not at startup**: The API server starts without a key but every task submission will fail internally. This is expected behaviour, not a bug. Researchers must configure a provider before using the platform.

5. **UI API key created post-startup**: The `VITE_SKYVERN_API_KEY` for the frontend is not a static secret. It is generated by the backend after first startup and retrieved from the UI settings page. This makes a cold-start test without it normal.
