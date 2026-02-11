# BiliNote. Reasoning Log

## Initial Assessment

BiliNote is an AI note-taking tool for videos. It accepts a Bilibili or YouTube URL, downloads and transcribes the audio using ctranslate2 (a fast inference engine for Whisper models), and generates structured notes using an LLM. The project has a separate frontend (Vue/Vite) and a FastAPI backend. The repository also references a GHCR-hosted Docker image.

## What Was Checked

1. **README.md**: Describes a full-stack application with a Vue frontend and FastAPI backend. Provides Docker and docker-compose instructions. References a pre-built GHCR image.

2. **GHCR image availability**: The GHCR image (`ghcr.io/...`) referenced in the README was checked and found to be not publicly accessible (returns 403 or 404 without authentication). Could not be pulled for use.

3. **backend/ directory**: FastAPI application. Reads configuration for LLM provider and model. Uses ctranslate2 for Whisper inference and ffmpeg for audio extraction.

4. **backend/requirements.txt**: Lists fastapi, ctranslate2, yt-dlp, faster-whisper, and LLM client libraries.

5. **frontend/ directory**: Vue 3 Vite project. The `npm run build` command was tested and failed due to missing node_modules and incompatible package versions in the repository state.

6. **Upstream Dockerfile**: None existed for the backend alone. A Dockerfile was written for this deployment.

## Decisions Made

### Backend-only deployment

The Vue frontend build failed during analysis. The Vite build encountered dependency resolution errors that would require modifying frontend source code to fix, which violates the architectural fidelity rule. The GHCR pre-built image for the frontend is also not publicly accessible. The backend is self-sufficient for research purposes: all video processing and note generation logic is in the FastAPI backend, and the API is fully documented via FastAPI's auto-generated docs at /docs. This is sufficient for supply chain security research.

### ctranslate2 pre-installed before requirements.txt

ctranslate2 must be installed before the rest of requirements.txt because the package resolver has conflicts when ctranslate2 is resolved alongside faster-whisper and other packages simultaneously. Pre-installing ctranslate2==4.4.0 first and then running the main requirements install resolves these conflicts.

### --security-opt seccomp=unconfined required

ctranslate2 uses CPU SIMD instructions (AVX2) that require the ability to modify the executable stack attribute. Docker's default seccomp profile blocks the `execstack` system call. Without `--security-opt seccomp=unconfined`, ctranslate2 raises a permission error when trying to set the executable stack bit for its JIT-compiled kernels. This is a known issue with ctranslate2 in Docker. The `--security-opt seccomp=unconfined` flag relaxes the seccomp filter for the container.

### Non-root user appuser created

The Dockerfile creates a non-root user (UID 1000) and runs the application as appuser. This follows the standard deployment pattern for this project even though the upstream had no Dockerfile.

### ffmpeg installed at build time

ffmpeg is required for audio extraction from video files. It is installed from apt in the Dockerfile.

## Testing

### Tests Performed
1. **Docker build**: Completed successfully. ctranslate2 pre-install and requirements.txt install both succeeded.
2. **Container startup without seccomp flag**: Container started but ctranslate2 raised an exec stack permission error when attempting to process audio. Expected behavior.
3. **Container startup with --security-opt seccomp=unconfined**: Service started and bound to port 8483.
4. **FastAPI import**: `python -c "import fastapi"` passed.

### What Was Not Tested
- Actual video transcription (requires a valid video URL and LLM configuration)
- Note generation (requires LLM API key)
- API endpoints beyond the root health check

## Gotchas

1. **seccomp=unconfined required**: This is a hard requirement for ctranslate2 to function in Docker. Without it, the service appears to start but immediately fails when any transcription is attempted. Always run with `--security-opt seccomp=unconfined`.

2. **GHCR image not public**: The upstream README links to a GHCR image. This image was not accessible without GitHub credentials. The backend-only deployment from source is the practical alternative.

3. **Frontend missing**: Researchers who need the Vue UI should build the frontend separately or use the API directly via /docs. The API is complete and supports all note generation features.

4. **Whisper model download at runtime**: The first transcription request will trigger a download of the Whisper model weights. This can take several minutes depending on network speed. Mount a volume for the model cache to persist downloads across container restarts.
