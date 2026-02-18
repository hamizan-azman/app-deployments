# magentic-ui -- Reasoning Log

## What Was Checked
- PyPI package `magentic-ui` -- Microsoft's official package, installable via pip
- The app's architecture: it runs a FastAPI backend that spawns Docker containers for VNC browsing and Python code execution
- Initially marked as SKIP because it requires Docker-in-Docker, but user approved DinD approach

## Dockerfile Strategy
Used `python:3.12-slim` with `docker.io` installed for Docker CLI access. The app itself installs cleanly from PyPI. Key decisions:

- **docker.io package**: Needed so the container can communicate with the Docker daemon via the mounted socket
- **INSIDE_DOCKER=1 and RUN_WITHOUT_DOCKER=False**: Environment variables that tell magentic-ui it's running inside Docker and should use Docker for helper containers
- **`--upgrade-database`**: Ensures SQLite schema is up to date on startup

## Docker-in-Docker Approach
The container doesn't run its own Docker daemon. Instead, it mounts the host's Docker socket (`/var/run/docker.sock`), so when magentic-ui spawns helper containers (VNC browser, Python executor), they run as sibling containers on the host Docker.

This is the standard DinD pattern -- simpler than running dockerd inside the container, but requires the `-v /var/run/docker.sock:/var/run/docker.sock` mount.

## Testing
1. **Web UI (/)**: Returns 200, serves the React frontend
2. **Sessions API (/api/sessions?user_id=test)**: Returns 200 with empty session list, proves backend is functional
3. **First-run behavior**: On startup, the app pulls two helper images (VNC browser and Python executor). This takes 2-3 minutes but only happens once.

Chat functionality was not tested as it requires active OpenAI API calls and a full browsing session, but the infrastructure (web UI + API + database + Docker communication) all verified working.

## Gotchas
- Without Docker socket mount, the app exits immediately with "Docker is not running"
- First startup is slow due to helper image pulls
- The 422 on `/api/sessions` without `user_id` parameter is expected FastAPI validation behavior
