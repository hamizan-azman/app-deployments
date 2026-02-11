# deepwiki-open. Reasoning Log

## Initial Assessment

deepwiki-open generates wiki-style documentation from code repositories. It clones a repository, indexes it using embeddings, and lets users ask questions about the codebase through a chat interface. The architecture is a Next.js frontend (port 3000) backed by a FastAPI Python API (port 8001). The Python backend uses Poetry for dependency management and the adalflow library for embedding storage.

## What Was Checked

1. **README.md**: Describes both local and Docker deployment. Lists environment variables (OPENAI_API_KEY, GOOGLE_API_KEY). Shows docker-compose usage with volume mounts for the adalflow cache.

2. **Upstream Dockerfile**: A four-stage multi-stage build. Stage 1 (node_deps) installs npm dependencies. Stage 2 (node_builder) builds the Next.js application. Stage 3 (py_deps) installs Python dependencies via Poetry. Stage 4 is the final runtime image combining both.

3. **api/ directory**: FastAPI application. Uses Poetry for dependency management (pyproject.toml + poetry.lock). Provides repository ingestion and Q&A endpoints.

4. **src/ directory**: Next.js frontend source.

5. **COPY path analysis**: The upstream Dockerfile used paths like `COPY apps/deepwiki-open/package.json ...` and `COPY apps/deepwiki-open/src/ ./src/`. These paths assume the Docker build context is the root of a monorepo. Our build context is `apps/deepwiki-open/`, making these paths invalid.

## Decisions Made

### Used the existing Dockerfile with COPY path fix

The upstream Dockerfile is well-structured and covers all the complexity of combining a Node.js and Python application in one image. The only issue was the COPY paths.

### Fixed COPY paths throughout the Dockerfile

The upstream Dockerfile was written assuming a monorepo build context at the repository root. All COPY instructions had the `apps/deepwiki-open/` prefix. Since we build with `apps/deepwiki-open/` as the context directory, all paths inside the Dockerfile must be relative to that directory. The fix was removing the `apps/deepwiki-open/` prefix from every COPY instruction.

For example:
- `COPY apps/deepwiki-open/package.json package-lock.json ./` became `COPY package.json package-lock.json ./`
- `COPY apps/deepwiki-open/src/ ./src/` became `COPY src/ ./src/`
- `COPY apps/deepwiki-open/api/pyproject.toml .` became `COPY api/pyproject.toml .`

Without this fix, Docker would look for `apps/deepwiki-open/package.json` relative to the build context directory, which would resolve to `apps/deepwiki-open/apps/deepwiki-open/package.json`. All COPY instructions would fail with "file not found."

### Kept Poetry 2.0.1 pin

The py_deps stage explicitly installs poetry==2.0.1. This is important because Poetry 2.x changed several API behaviors compared to Poetry 1.x. The lock file was generated with Poetry 2.0.1 and the install options (--only main, --no-interaction) are compatible with this version.

### Kept nodejs installation in final stage

The final runtime stage installs Node.js 20 from NodeSource to run the Next.js standalone server. This is necessary because Next.js's standalone build still requires Node.js at runtime (for the server.js process). The standalone build is lighter than a full Next.js project but is not a static export.

### Kept the embedded start.sh generation

The Dockerfile generates a startup script inline using `echo`. This script loads an optional .env file, warns if API keys are missing, starts the FastAPI backend in the background, starts the Next.js server, and waits for either process to exit. This design is correct for a single-container two-process deployment.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. All four stages completed. Next.js standalone build succeeded. Poetry install succeeded.
2. **FastAPI import**: `python -c "import fastapi"` passed.
3. **Container startup**: Both processes started. FastAPI bound to 8001, Next.js bound to 3000.
4. **Health check**: `curl http://localhost:8001/health` returned 200.

### What Was Not Tested
- Repository ingestion (requires a GitHub URL and a valid API key)
- Q&A interface (requires ingested repository and LLM API key)
- Google Gemini backend (tested only with OpenAI key environment)

## Gotchas

1. **COPY path prefix issue**: As described above, this is the main non-obvious fix. The symptom is that the Docker build succeeds (COPY from a stage does not error if the source is empty) but the final image is missing files, causing runtime failures.

2. **adalflow volume**: The adalflow library creates embedding indexes on first run and stores them in ~/.adalflow (which resolves to /root/.adalflow in the container). Without a persistent volume mount, these indexes are rebuilt on every container restart, adding significant startup time for large repositories.

3. **API key warning is not a failure**: The start.sh script warns if API keys are missing but does not exit. The container will start without API keys. All LLM-dependent operations will fail with 401 errors at request time.

4. **NODE_OPTIONS max-old-space-size**: The node_builder stage sets `NODE_OPTIONS="--max-old-space-size=4096"` to prevent the Node.js build process from running out of memory during Next.js compilation. This is a build-time setting and does not affect the runtime image.
