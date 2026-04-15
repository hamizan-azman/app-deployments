# kotaemon. Reasoning Log

## Initial Assessment

kotaemon is a Gradio-based document QA application with an existing multi-stage Dockerfile. The upstream provides two build targets: `lite` (no pre-downloaded models) and a full variant that downloads embedding models at build time. The lite variant is the appropriate choice for our deployment.
Went with the lite variant to keep the image size reasonable. The full variant pulls in LibreOffice, Tesseract OCR, and a bunch of image processing libraries that balloon it past 8GB.

## What Was Checked

1. **README.md**: Describes kotaemon as a document QA tool. Docker instructions reference the upstream image. Lists supported LLM providers and optional local model support via Ollama.

2. **Dockerfile**: Multi-stage build with a `lite` target. Uses `python:3.10-slim` base. Installs system dependencies including poppler-utils, libpoppler-dev, cargo, and build tools. Downloads PDF.js prebuilt at build time. Uses `uv` for dependency management with `uv sync --frozen`. Installs graphrag on amd64 only.

3. **launch.sh**: Shell script that sets up the environment and starts the Gradio app. Contains Windows-style CRLF line endings when checked out on Windows, which breaks bash execution inside Linux containers.

4. **uv.lock**: Dependency lock file managed by the upstream project. Contains exact versions for all dependencies. `--frozen` ensures the build uses exactly these versions.

5. **pdfservices-sdk**: Installed from a forked GitHub repository (`niallcm/pdfservices-python-sdk`) because the upstream requirement was pinned to a version with frozen dependencies incompatible with the rest of the dependency tree.

## Decisions Made

### Used lite build target
The full variant downloads large sentence transformer models at build time, producing a very large image. The lite variant defers model downloads to first use, keeping the image size manageable. This is the recommended approach for distribution.

### Fixed Windows line endings in launch.sh
The `launch.sh` file acquires CRLF line endings when the submodule is checked out on Windows. Adding `sed -i 's/\r$//' /app/launch.sh` in the Dockerfile converts them to LF before the script is executed. Without this, bash exits immediately with "bad interpreter" errors.

### uv for dependency management
The upstream uses uv with a frozen lock file. This provides the most reproducible build possible. We preserve this approach exactly.

### graphrag on amd64 only
graphrag has no ARM wheel. The conditional install (`if [ "$TARGETARCH" = "amd64" ]`) prevents build failures on ARM hosts while still providing the feature on amd64.

### Copied .env.example to .env
The application reads from `/app/.env` for default configuration. Copying `.env.example` at build time ensures the application starts without requiring a mounted .env file.

## Testing

### Tests Performed
1. **Container start**: Gradio initializes within 60 seconds. Pass.
2. **Health check** (GET `http://localhost:7860/`): Returns HTTP 200. Pass.
3. **UI load**: Gradio interface loads in browser. Pass.

### What Was Not Tested
- Document upload and indexing (requires LLM and embedding model)
- Question answering (requires API key)
- Multi-user login

## Gotchas

1. **launch.sh CRLF**: The most common build failure for this app when built on Windows. The sed fix must be applied before the script is used as the entrypoint.

2. **uv lock file with CUDA torch**: If the uv.lock was generated with a CUDA version of torch but the build environment has only CPU torch, `uv sync --frozen` will fail. In that case the lock file must be regenerated. The upstream lock file targets CPU torch for the lite variant.

3. **Startup time**: The 60-second start_period in the healthcheck is necessary. Gradio takes time to initialize the PDF.js assets and register all components before it begins serving requests.

4. **pdfservices-sdk fork**: The `@git+https://` install of pdfservices-sdk adds a network dependency at build time. If the fork becomes unavailable, the build will fail. This is an upstream design choice that we preserve.
