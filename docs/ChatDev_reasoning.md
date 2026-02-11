# ChatDev. Deployment Reasoning

## App Type
FastAPI backend (multi-agent software development system, DevAll v2.0). Backend-only deployment. Port 6400.

## Deployment Decision
Deploy. The upstream repo ships a Python FastAPI server (server_main.py) with a uv-managed lockfile, making it straightforward to containerize. The frontend is a separate Node.js application with no Dockerfile provided and is outside scope for this deployment.

## Build Approach
Multi-stage build with uv.

The app requires libcairo2-dev and build-essential at compile time (for cairosvg and related drawing packages) but only libcairo2 at runtime. A multi-stage build avoids shipping compilers and dev headers in the final image.

Stage 1 (builder): installs pkg-config, build-essential, python3-dev, libcairo2-dev, then installs uv and runs `uv sync --frozen` to create a virtualenv at /opt/venv.

Stage 2 (runtime): installs only curl and libcairo2, copies the built virtualenv from the builder stage, copies application code, drops privileges to appuser (UID 1000), and runs server_main.py on port 6400.

The virtualenv is placed at /opt/venv (controlled by UV_PROJECT_ENVIRONMENT) rather than inside /app so it is not hidden by any bind-mount of the working directory.

## Dependency Management
uv with --frozen flag. The upstream lockfile (uv.lock) pins all transitive dependencies exactly. No manual version pinning pass was needed because the lockfile already provides full reproducibility. This satisfies the V2 pinning requirement.

## API Key Handling
ChatDev requires API_KEY and BASE_URL at runtime to call the LLM provider. These are passed as environment variables and are never baked into the image. The server starts and serves /docs without valid credentials, but agent pipeline calls will fail. For QC purposes, testing /docs (infrastructure check) is sufficient without a live key.

## Port
6400. This is the port declared in server_main.py and confirmed in the CMD. No conflict with standard ports used by other apps in this project.

## Healthcheck
`curl -f http://localhost:6400/docs`. FastAPI always serves /docs when the server is up, regardless of API key configuration. This makes it a reliable liveness indicator.

## System Dependencies
- Builder stage: pkg-config, build-essential, python3-dev, libcairo2-dev (compile-time only).
- Runtime stage: curl (for healthcheck), libcairo2 (runtime shared library for cairosvg).

## Non-Root User
useradd creates appuser at UID 1000. chown transfers ownership of /app before switching. Standard practice for all deployments in this project.

## What Was Not Deployed
The ChatDev frontend is a Node.js web application that communicates with this backend. It has no Dockerfile and requires separate Node.js tooling to build and run. It is excluded from this deployment per the backend-only scope decision. Researchers interacting with the backend can use the /docs Swagger UI directly or build the frontend locally following upstream instructions.

## QC Result
Pass. Container started cleanly. GET /docs returned 200. Healthcheck passed within the start-period window.
