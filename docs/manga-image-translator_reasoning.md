# manga-image-translator. Reasoning Log

## Investigation

### Docker Image vs Building from Source
The repo has a Dockerfile, but there is also a pre-built image `zyddnys/manga-image-translator:main` on Docker Hub. The image is ~10GB and contains the full ML pipeline (text detection, OCR, translation, inpainting, rendering models). Building from source would require downloading all the same models during build, plus compiling dependencies. Using the pre-built image saves significant time and matches what users of the tool actually run.

### Server Architecture (server/main.py)
Read `server/main.py` to understand the API surface. The server is a FastAPI app with:
- Translation endpoints in three response formats (JSON, image PNG, custom bytes)
- Each format available via JSON body or multipart form upload
- Streaming variants for all endpoints (progress tracking)
- Batch translation endpoints
- Result storage and retrieval
- Web UI (index.html) and manual page
- Internal API endpoints for translator instance registration

The server spawns a translator subprocess on port 5004 (port + 1) when `--start-instance` is passed. This subprocess registers back to the main server via `/register` using a nonce for authentication.

### Request Model (server/request_extraction.py)
Read `request_extraction.py` to understand how images are accepted:
- `TranslateRequest.image` accepts `bytes|str`. can be a URL (fetched via requests.get), base64-encoded data URI, or raw bytes from multipart upload
- `Config` object controls translator, target language, and model selection
- Queue-based processing: requests are added to a task queue and wait for a translator instance to process them

### Docker Run Command
The entrypoint needed to be overridden because the default image entrypoint runs the CLI tool, not the web server. The correct command:
```
docker run -p 5003:5003 --ipc=host --entrypoint python zyddnys/manga-image-translator:main server/main.py --verbose --start-instance --host=0.0.0.0 --port=5003
```

Key flags:
- `--entrypoint python`: Override default entrypoint to run the server instead of CLI
- `server/main.py`: The web server module
- `--start-instance`: Tells the server to spawn a translator subprocess
- `--host=0.0.0.0`: Bind to all interfaces (required for Docker networking)
- `--port=5003`: API server port
- `--ipc=host`: Shared memory for large image processing
- `--verbose`: Detailed logging (helpful for debugging model downloads)

### Port Selection
Used port 5003 on the host to avoid conflicts with other deployments. The server internally uses 5003 for the API and 5004 for the translator instance.

## Decisions Made

### Using Pre-built Image
Decided to use `zyddnys/manga-image-translator:main` instead of building from source:
- Image already has all Python deps, CUDA, and base models
- Building from source would require a complex multi-stage Dockerfile with model downloads
- The pre-built image IS what the developer publishes and maintains
- Architectural fidelity: this is the official deployment method

### No Dockerfile Created
Since we use `docker pull`, no custom Dockerfile is needed. The run command fully documents how to start the service. This is the same pattern as omniparse.

### Model Download on First Request
The sugoi translator models (~622MB) are not included in the Docker image. They download on the first translation request. This means:
- First request takes several minutes (download + extraction + loading)
- Subsequent requests are fast (models cached in container filesystem)
- If the container is removed, models must re-download
- I waited for the download to complete before testing, confirmed via docker logs showing "sugoi-models.zip" download progress

### Default Translator (sugoi)
The default translator for Japanese-to-English is "sugoi", which is an offline neural translation model. This is ideal for our deployment because:
- No API keys needed
- Works completely offline
- Good quality for manga dialogue
- Other translators (GPT-4, DeepL) are available but require API keys

## Testing

### Test 1: Web UI (GET /)
Validates the web frontend loads. This is the primary user-facing interface. A 75KB HTML response confirms the full frontend assets are served.

### Test 2: OpenAPI Docs (GET /docs)
FastAPI auto-generates Swagger docs. Confirms the API schema is accessible and the server framework is working correctly.

### Test 3: Queue Size (POST /queue-size)
Simple API test that exercises the queue system. Returns 0 when idle. Confirms the internal task queue is initialized.

### Test 4: Results List (GET /results/list)
Tests the result storage system. Returns empty list on fresh container. Confirms the result directory is created and accessible.

### Test 5: Translate via JSON (POST /translate/json)
The core test. Sends a real manga image URL and waits for full translation pipeline:
1. Server fetches the image from URL
2. Text detection model finds 14 text regions
3. OCR reads Japanese text from each region
4. Sugoi translator converts Japanese to English
5. Inpainter removes original text
6. Renderer places English text

Result: 200 OK, 386KB JSON response containing all 14 translated regions with coordinates, original Japanese, English translation, and base64-encoded background patches. Sample translation: "Hey, what do you think of Sakamoto?"

This test proves the ENTIRE ML pipeline works end-to-end on CPU.

### Test 6: Manual Page (GET /manual)
Validates the help/manual page loads. 6.9KB HTML response.

### Tests Not Run
- Streaming endpoints: Would require custom client to parse the binary streaming protocol (1 byte status + 4 byte size + N bytes data). The underlying translation pipeline is the same as the tested /translate/json.
- Form upload endpoints: Share the same pipeline, just different input method (multipart vs JSON body).
- Batch endpoints: Share the same pipeline, just process multiple images.
- Image/bytes response formats: Same translation, different serialization.
- Delete/clear results: Destructive operations, not needed for validation.

## Pitfalls

### First Request Timeout
The first translation request triggers model downloads. The sugoi translator models are ~622MB and take several minutes to download and extract. If you set a short timeout (e.g. 30s), the request will fail. Use at least 600s timeout for the first request, or wait for logs to confirm models are loaded before sending requests.

### MSYS_NO_PATHCONV on Windows Git Bash
When running docker commands from Git Bash on Windows, paths like `/app` get mangled to `C:/Program Files/Git/app`. Must prefix with `MSYS_NO_PATHCONV=1`. This affected the `--entrypoint python` path resolution.

### PowerShell for Testing
Git Bash curl can timeout on localhost Docker ports even when the container is listening. PowerShell's Invoke-WebRequest works reliably. All tests were run via PowerShell scripts.

### Container Size
The pulled image is ~10GB. With model downloads at runtime, the container uses additional space. Ensure sufficient disk space.

### Internal Port 5004
The translator instance runs on port 5004 inside the container. This port does not need to be exposed to the host. Only port 5003 (the API server) needs mapping.

### CPU vs GPU
The translation works on CPU but is slow (30-60 seconds per image depending on text density). For production use, pass `--gpus all` to docker run and use the NVIDIA runtime. The image is CUDA-capable.
