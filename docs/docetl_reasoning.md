# docetl. Reasoning Log

## Initial Assessment

docetl is a document ETL pipeline framework. Users define pipelines in YAML that chain LLM operations (extract, map, reduce, filter) over document collections. The application has a Next.js frontend for pipeline design, a FastAPI backend for execution, and uses Python's uv for dependency management. The project ships with a docker-compose.yml for development.

## What Was Checked

1. **README.md**: Describes both pip install and Docker deployment. The Docker setup uses a pre-built image from GHCR or a local build. Lists OPENAI_API_KEY as required.

2. **docker-compose.yml**: Single service using the upstream image. Mounts a data volume and passes environment variables. Exposes ports 3000 and 8000.

3. **pyproject.toml**: Defines the Python package with uv as the build tool. Includes fastapi, openai, and document processing libraries.

4. **server/ directory**: FastAPI application. Main entry point is server/app/main.py.

5. **website/ directory**: Next.js frontend. Standard Next.js project structure with package.json and npm build.

6. **Dockerfile construction**: No upstream Dockerfile for standalone deployment was found. One was written following the docker-compose.yml as the specification.

## Decisions Made

### Written Dockerfile based on docker-compose.yml specification

The upstream docker-compose.yml is the canonical deployment specification. The Dockerfile implements the same environment: Python 3.11, uv for Python deps, Node 20 for the frontend, DOCETL_HOME_DIR=/docetl-data, and ports 3000 and 8000.

### Three-stage build: python-builder, node-builder, runtime

The build is split into three stages to keep the final image clean. The python-builder stage installs uv and resolves the full dependency tree. The node-builder stage compiles the Next.js application. The runtime stage copies only the built artifacts from both stages plus the runtime system packages.

### uv for Python dependency management

The project uses uv natively (pyproject.toml with uv sync). The python-builder stage installs uv via the official installer script and runs `uv sync --all-extras` to install all optional dependency groups. The virtual environment is then copied to the runtime stage.

### Next.js website served alongside the FastAPI process

The CMD starts both processes: `python3 server/app/main.py` in the background and `cd website && npm run start` in the foreground. This matches the docker-compose service design where both UI and API are expected from a single container.

### /docetl-data as a VOLUME

The DOCETL_HOME_DIR environment variable points to /docetl-data. This directory is used for pipeline inputs, outputs, and intermediate state. Declaring it as a VOLUME ensures Docker manages it separately from the container filesystem, preventing data loss on container replacement.

### libgl1 and libglib2.0-0 installed

These libraries are required by OpenCV, which is a transitive dependency of some document processing packages. Without them, importing certain document processing modules fails with a library not found error.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. uv sync resolved all dependencies. Next.js build completed. Runtime stage assembled correctly.
2. **FastAPI import**: `python -c "import fastapi"` passed.
3. **Container startup**: Both FastAPI and Next.js processes started. FastAPI bound to 8000, Next.js bound to 3000.
4. **Health check**: `curl http://localhost:8000/health` returned 200.

### What Was Not Tested
- Pipeline execution (requires a YAML pipeline definition and OPENAI_API_KEY)
- Frontend pipeline builder (requires running container with API key)
- Document processing with local files

## Gotchas

1. **uv installer via curl pipe**: The python-builder stage installs uv using `curl -LsSf https://astral.sh/uv/install.sh | sh`. This is an upstream pattern but is a supply chain risk. The install script is fetched at build time over TLS. The install path is `/root/.local/bin/uv`.

2. **DOCETL_HOME_DIR must be writable**: The nobody user owns /docetl-data. If the volume is mounted from a host path that the nobody user cannot write to, the app will fail with permission errors. Use `chmod 777` on the host path or use a named Docker volume.

3. **npm run start vs npm run build**: The node-builder stage runs `npm run build` to compile the Next.js app. The runtime stage runs `npm run start` which requires the compiled output to be present. The `COPY --from=node-builder /app/website ./website` instruction copies the entire website directory including the .next build artifacts.

4. **Empty .env file**: A `touch .env` instruction creates an empty .env file so the application does not fail if it tries to read environment variables from .env. The actual OPENAI_API_KEY should be passed as a docker run -e flag, not written to .env.
