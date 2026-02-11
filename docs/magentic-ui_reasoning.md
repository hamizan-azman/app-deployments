# magentic-ui. Reasoning Log

## What Was Checked
- PyPI package `magentic-ui`. Microsoft's official package, installable via pip
- The app's architecture: it runs a FastAPI backend that spawns Docker containers for VNC browsing and Python code execution
- Initially marked as SKIP because it requires Docker-in-Docker, but user approved DinD approach

## Dockerfile Strategy
Used `python:3.12-slim` with `docker.io` installed for Docker CLI access. The app itself installs cleanly from PyPI. Key decisions:

- **docker.io package**: Needed so the container can communicate with the Docker daemon via the mounted socket
- **INSIDE_DOCKER=1 and RUN_WITHOUT_DOCKER=False**: Environment variables that tell magentic-ui it's running inside Docker and should use Docker for helper containers
- **`--upgrade-database`**: Ensures SQLite schema is up to date on startup

## Docker-in-Docker Approach
The container doesn't run its own Docker daemon. Instead, it mounts the host's Docker socket (`/var/run/docker.sock`), so when magentic-ui spawns helper containers (VNC browser, Python executor), they run as sibling containers on the host Docker.

Two alternatives were considered:
1. **Full DinD (dockerd inside container)**: Would require `--privileged`, add complexity, and still need 2GB+ for the nested daemon. No benefit for research purposes.
2. **Disable Docker entirely (`RUN_WITHOUT_DOCKER=True`)**: Would make the app non-functional - the browser and code execution agents are the core feature.

Socket mounting is the standard pattern - simpler, no privilege escalation beyond socket access, and helper containers share the host's image cache.

## Helper Image Architecture
On first startup, magentic-ui pulls two images:
- **VNC browser container**: Runs a headless Chromium instance accessible via VNC, used by the browsing agent to navigate web pages
- **Python executor container**: Sandboxed Python environment where the coding agent runs generated code

These are sibling containers managed by the magentic-ui backend via the Docker API. They're created per-session and destroyed when the session ends.

## Testing
1. **Web UI (/)**: Returns 200, serves the React frontend
2. **Sessions API (/api/sessions?user_id=test)**: Returns 200 with empty session list, proves backend is functional
3. **First-run behavior**: On startup, the app pulls two helper images (VNC browser and Python executor). This takes 2-3 minutes but only happens once.

Chat functionality was not tested as it requires active OpenAI API calls and a full browsing session, but the infrastructure (web UI + API + database + Docker communication) all verified working.

## Gotchas
- Without Docker socket mount, the app exits immediately with "Docker is not running"
- First startup is slow due to helper image pulls
- The 422 on `/api/sessions` without `user_id` parameter is expected FastAPI validation behavior
