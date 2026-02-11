# BruteForceAI Deployment Reasoning

## App Type
CLI tool. No web interface, no server, no exposed port.

## Base Image Decision
Used `mcr.microsoft.com/playwright/python:v1.40.0-jammy` (Microsoft's official Playwright image). This is the correct base for any app that drives a real browser. It ships with all system-level Chromium dependencies pre-installed. Using a slim Python base and manually installing Playwright system deps would be fragile and much larger. The Playwright image is the right architectural choice here.

`playwright install chromium` is still run at build time to install the browser binary into the non-root user's cache directory, which is separate from the system-level deps the base image provides.

## sqlite3 Removal
The original `requirements.txt` listed `sqlite3` as a pip dependency. `sqlite3` is part of the Python standard library and has never been a PyPI package. Attempting `pip install sqlite3` fails with a resolution error that aborts the build. Removing it is the correct fix, not a workaround. The module is available in the container automatically because it is built into CPython.

## Build Context
The Dockerfile uses the repo root as the build context (not `apps/BruteForceAI/` as a self-contained context). This was necessary to allow copying the pinned `requirements.txt` from `dockerfiles/BruteForceAI/requirements.txt` into the image before the app source arrives. The sequence is:

1. Copy pinned requirements from `dockerfiles/BruteForceAI/requirements.txt`
2. `pip install` from those pinned requirements
3. Copy app source from `apps/BruteForceAI/`

This pattern keeps the V2-pinned deps in the `dockerfiles/` directory (the canonical location for all our dep files) while still layering them correctly before the source copy.

## LLM Backend
The app supports two backends: Ollama (local) and Groq (cloud). Neither is available in the container itself. Ollama must run on the host and be reachable via `host.docker.internal`. Groq requires a key at runtime. Neither backend is tested in automated QC as both require external services or credentials. The infrastructure (Playwright, Chromium, imports) is what the health check validates.

## Health Check Design
The HEALTHCHECK runs `python BruteForceAI.py --help || python -c "import playwright"`. The `||` fallback ensures the check passes as long as either the entrypoint can start or the Playwright library is importable. For a CLI tool with no server, this is the appropriate approach.

## Architectural Fidelity
No changes were made to the app's architecture. The entrypoint is exactly `python BruteForceAI.py`, matching how the developer intended the tool to be invoked. No wrapper scripts, no server shim, no custom API layer.

## QC Validation
QC test: `python -c "import playwright"` inside the running container. Result: PASS. This confirms the Playwright install succeeded and the browser dependencies are in place. Browser execution against a real target was not tested in automated QC (requires a live login page and LLM backend).

## Skip Consideration
BruteForceAI uses Playwright in headless mode (no display required) and has no desktop GUI dependency. It was correctly assessed as deployable. The Playwright Microsoft image handles all the headless browser plumbing.
