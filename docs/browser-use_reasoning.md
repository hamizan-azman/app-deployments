# browser-use. Deployment Reasoning

## App Type
CLI tool and Python library. No web UI. Entry point is the `browser-use` binary installed by uv into `/app/.venv/bin/`.

## Decision: Deploy
browser-use runs headlessly in Docker. Chromium is installed from Debian apt packages with a `--no-sandbox` headless mode suitable for containers. The upstream repo includes an official Dockerfile. We use it with minimal changes.

## Dockerfile Approach
Used the upstream Dockerfile as the base. The upstream file was written by the browser-use maintainers and is purpose-built for this app. Following the architectural fidelity rule, the structure was preserved exactly. Only one category of change was made: the removal of `--mount=type=cache` BuildKit cache mount directives.

### Why remove cache mounts
BuildKit cache mounts (`--mount=type=cache`) are unreliable on Windows Docker Desktop with WSL2. They can silently fail or cause build errors depending on the BuildKit version and WSL2 storage backend. Removing them does not change the build output. Packages are still installed in full. The only difference is that apt and uv caches are not persisted between builds, which means slightly longer rebuild times on a clean build. For a supply chain research deployment where reproducibility matters more than build speed, this is the correct tradeoff.

## User and Permissions
The upstream Dockerfile creates a `browseruse` system user with UID 911 and GID 911. The user is added to the `audio` and `video` groups, which is standard for browser automation containers that may need audio/video access. The container switches to this user before the entry point. All `/data` and home directory paths are chowned to this user during build.

## Chromium Install Strategy
Chromium is installed from Debian apt packages rather than via `playwright install chromium`. This avoids downloading a separate browser binary at build time and keeps the image self-contained. The binary is symlinked to two locations for compatibility with different Playwright detection paths. Several font packages are installed alongside Chromium to prevent rendering issues on pages that use non-Latin scripts.

## Port Rationale
Port 9242 is the browser-use internal port declared in the upstream Dockerfile. Port 9222 is the Chrome DevTools Protocol port, useful for external automation clients or debugging. Neither port is required for CLI operation. They are exposed for completeness and in case the app is used in a mode that starts an HTTP control interface.

## Volume Rationale
`/data` is declared as a Docker volume for persistent browser profiles. The default profile lives at `/data/profiles/default`. This allows browser state (cookies, session storage, cached auth) to persist across container runs, which is useful for tasks that require authenticated sessions.

## uv Package Manager
The upstream project uses `uv` for dependency management. `uv` is copied from the official `ghcr.io/astral-sh/uv:latest` image. Dependencies are installed in two phases: first `uv sync --no-install-project` to pre-install all sub-dependencies before copying source, then `uv sync --locked` after copying source to install the `browser-use` package itself. The `--locked` flag enforces the `uv.lock` file exactly, providing full reproducibility without additional pinning on our side.

## Healthcheck
The upstream Dockerfile contains a commented-out healthcheck that probes `http://localhost:8000/health/`. This was never activated because browser-use does not start an HTTP server by default when run as a CLI. We preserved the commented state. QC was validated by running `browser-use --help` inside the container, which exits 0 and prints usage.

## What Each QC Test Validates
- `browser-use --help` exits 0: confirms the venv is set up correctly, the entry point resolves, and Playwright and browser-use packages import without errors at startup.

## API Key Testing
Actual browser task execution requires a valid LLM provider API key. This was not tested in the QC phase. Infrastructure (entry point, imports, help output) was confirmed working. Task execution would require a live key and an actual browser task string.

## Build Notes
- Base image: `python:3.12-slim`
- `python:3.12-slim` uses Debian bookworm in the current slim tags, which is compatible with the Playwright/Chromium apt packages used here.
- The `--platform linux/amd64` flag was used during build as required by the project standard for cross-platform compatibility.
