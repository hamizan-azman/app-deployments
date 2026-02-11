# Open-LLM-VTuber. Reasoning Log

## Initial Assessment

Open-LLM-VTuber is an AI companion application with a Live2D animated avatar. It runs a WebSocket/FastAPI server that a browser frontend connects to. The frontend renders the Live2D model and streams audio. The backend handles ASR (speech recognition), LLM inference, and TTS (speech synthesis). All components are configured via a single conf.yaml file. The project uses uv for Python dependency management.

## What Was Checked

1. **README.md**: Describes local setup with uv and a Docker deployment path. Shows volume mounts for conf/ and models/ directories. Emphasizes that conf.yaml is required.

2. **pyproject.toml**: Python 3.10 required (pinned). Uses uv. Depends on fastapi, uvicorn, openai-whisper, various TTS libraries, and live2d-py.

3. **uv.lock**: Frozen lock file. Covers all runtime dependencies.

4. **conf.yaml.example**: Comprehensive configuration file covering LLM backend, ASR engine, TTS engine, Live2D model paths, character configuration, and audio settings.

5. **run_server.py**: Application entry point. Reads conf.yaml and starts the FastAPI/WebSocket server on port 12393.

6. **Upstream Dockerfile**: None. A Dockerfile was written for this deployment based on the README instructions and project structure.

## Decisions Made

### Python 3.10 required

The project's pyproject.toml specifies `requires-python = ">=3.10,<3.11"` (effectively requiring 3.10). Several audio and Live2D libraries in the dependency tree have compiled C extensions built for Python 3.10. Using 3.11 or later causes import failures at runtime. The base image is `python:3.10-slim`.

### conf.yaml mandatory with startup script enforcement

The application cannot start without conf.yaml. Rather than letting the app fail with an uninformative Python traceback, the startup script checks for the conf.yaml at /app/conf/conf.yaml and exits with a clear error message if it is absent. This makes the failure mode obvious to researchers mounting the wrong path.

The startup script also handles symlinks for optional directories (live2d-models, characters, avatars, backgrounds, model_dict.json). This mirrors the pattern used in the upstream README's Docker instructions.

### uv for dependency management

The project uses uv natively. The Dockerfile installs uv from the official astral.sh image (`COPY --from=ghcr.io/astral-sh/uv:latest`), runs `uv sync --frozen --no-dev` to install runtime dependencies from the lock file, and then installs the project package itself with `uv pip install --no-deps .`. The `--no-deps` flag avoids re-resolving transitive dependencies that were already installed by `uv sync`.

### RUN --mount=type=cache for uv

The uv sync step uses a build cache mount (`--mount=type=cache,target=/root/.cache/uv`) to speed up rebuilds. On cache misses (first build or cache cleared), the full dependency tree is downloaded. On cache hits, only changed packages are re-fetched.

### ffmpeg installed from apt

The application uses audio processing libraries that require ffmpeg at runtime (for audio format conversion and voice activity detection). It is installed from apt alongside curl and git.

### /app/conf and /app/models as VOLUME declarations

Both directories are declared as Docker volumes. /app/conf must be mounted by the user (conf.yaml is required). /app/models is where local model weights are downloaded at runtime (Whisper models, etc.). Declaring them as volumes ensures they are not accidentally included in image layers.

### Port 12393

The upstream hardcodes port 12393 in run_server.py. The Dockerfile exposes this port and the healthcheck targets it.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. uv sync resolved all dependencies from the frozen lock file. Project installed with uv pip install.
2. **FastAPI import**: `python -c "import fastapi"` passed.
3. **Container startup without conf volume**: Container exited immediately with "ERROR: conf.yaml is required" message from the startup script. Expected behavior.
4. **Startup script logic**: Verified the symlink creation logic for all optional conf directories.

### What Was Not Tested
- Full application startup with conf.yaml (requires a configured LLM backend)
- Live2D rendering (requires browser frontend connection)
- ASR/TTS pipeline (requires audio input and configured speech engines)
- WebSocket streaming

## Gotchas

1. **conf.yaml is a hard requirement**: The container will not start without it. This is by design. The startup script exits 1 immediately if the file is absent. Mount the conf directory before starting the container.

2. **Python 3.10 constraint**: The `requires-python` constraint is strict. Attempting to build with python:3.11-slim will cause pip to fail resolving packages that do not publish wheels for Python 3.11.

3. **Model downloads at first run**: ASR models (Whisper), TTS models, and any other configured local models are downloaded at runtime on first use. This can add several minutes to the first request. Mount /app/models to persist downloads across container restarts.

4. **Live2D model files**: If custom Live2D models are used, they must be placed in a `live2d-models/` subdirectory within the mounted /app/conf directory. The startup script creates the symlink automatically if the directory exists.

5. **uv cache mount scope**: The `--mount=type=cache` in RUN instructions is only available with BuildKit. If DOCKER_BUILDKIT=0 is used (required for some Windows Docker Desktop builds), the cache mount is silently ignored and the full dependency download occurs on every build.
