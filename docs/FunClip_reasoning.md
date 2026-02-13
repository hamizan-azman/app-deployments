# FunClip -- Reasoning Log

## What I Checked and Why

### Repository Structure
Read `README.md`, `requirements.txt`, all Python files in `funclip/`. The README is the primary source for understanding how the app is meant to run. The requirements.txt tells us the dependency stack. The Python files reveal the actual architecture.

Key findings:
- `funclip/launch.py` is the entry point. It builds a Gradio web UI, loads FunASR models, and serves on port 7860.
- `funclip/videoclipper.py` is the core logic. It wraps FunASR for speech recognition and uses moviepy for video clipping.
- `funclip/llm/` contains three LLM integration modules: OpenAI API, Qwen API, and g4f (free GPT proxy).
- `funclip/utils/` has subtitle generation, timestamp processing, and a Gradio theme JSON.
- `font/STHeitiMedium.ttc` is a Chinese font for subtitle rendering, already included in the repo.
- No Dockerfile, no docker-compose.yml, no setup.py, no pyproject.toml.

### Import Structure in launch.py
The imports in launch.py are non-package relative: `from videoclipper import VideoClipper`. This works because Python adds the directory containing the executed script to sys.path. So when you run `python funclip/launch.py`, the `funclip/` directory is on sys.path and `videoclipper`, `llm.openai_api`, `utils.trans_utils`, `introduction` all resolve correctly. This means the working directory should be the project root, not `funclip/`.

### Server Binding
launch.py has a `--listen` flag that switches `server_name` from `127.0.0.1` to `0.0.0.0`. This is critical for Docker -- without `--listen`, the Gradio server only binds to localhost inside the container, making it unreachable from the host.

### Language Flag
The `-l` / `--lang` flag determines which FunASR model is loaded. Chinese (`zh`) uses SeACo-Paraformer with hotword support. English (`en`) uses a simpler Paraformer model. I chose `-l en` for the default CMD since the researchers are English-speaking. This can be changed by overriding the CMD.

## Dockerfile Decisions

### Base Image: python:3.10-slim
FunASR 1.3.1 requires Python 3.8+. Python 3.10 is a safe middle ground -- new enough for all deps, old enough to avoid compatibility issues. Slim variant keeps image size down while still having the build tools pip needs.

### System Dependencies
- `ffmpeg`: Required by moviepy for video processing. Without it, all video operations fail.
- `imagemagick`: Required for burning subtitles into video (the "Clip+Subtitles" feature). The README explicitly mentions this as a dependency.
- `libsndfile1`: Required by the `soundfile` Python package for reading/writing audio files.
- `git`: Required by some pip packages that install from git repos during dependency resolution.

### ImageMagick Policy Fix
ImageMagick ships with a restrictive security policy that blocks read/write operations. The README says to fix it with `sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml`. However, the current Debian Trixie ships ImageMagick 7, not 6, so the path is different. I used `find /etc -name policy.xml -exec sed ...` to handle any version, with `|| true` so the build doesn't fail if the file doesn't exist.

### Torch CPU Installation
The requirements.txt specifies `torch>=1.13` and `torchaudio`. By default, pip installs the CUDA-enabled version of PyTorch, which is ~2GB larger. Since Docker Desktop uses CPU (no GPU passthrough on Windows), I install torch from the CPU-only index first: `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu`. This saves significant image size. When pip later processes requirements.txt, it sees torch is already installed and skips it.

### No .dockerignore
The repo includes a `docs/images/` directory with screenshots, but it's small enough that I didn't bother creating a .dockerignore. The total repo is under 10MB excluding dependencies.

## Alternatives Considered and Rejected

### GPU-enabled Image
Could have used an nvidia/cuda base image, but Docker Desktop on this Windows machine doesn't support GPU passthrough. CPU inference works fine for FunASR models, just slower. If someone needs GPU, they can change the base image and torch install.

### Pre-downloading Models into the Image
FunASR models are downloaded from ModelScope at first startup (~1.2GB total: Paraformer ~823MB, VAD ~50MB, punctuation ~278MB, speaker model ~27MB). I could have added `RUN python -c "from funasr import AutoModel; AutoModel(...)"` to the Dockerfile to bake models into the image. I chose not to because:
1. It would make the Docker image 1.2GB larger
2. The models cache inside the running container
3. Users can mount a volume for persistence if needed
4. Keeping the image lean is better for our use case (we build many images)

### Using docker-compose
FunClip is self-contained -- no database, no Redis, no external services. A single `docker run` is sufficient. docker-compose would add complexity without benefit.

### Pinning Gradio Version
The requirements.txt has unpinned `gradio`. pip installed Gradio 6.5.1, which has some API differences from older versions (the `meta` field requirement for FileData, the `/gradio_api/` prefix instead of `/api/`). I let pip resolve the latest version because FunClip's code is straightforward Gradio usage (gr.Blocks, gr.Button.click, etc.) and works fine with 6.x.

## How Each Change Relates to the Repo's Behavior

### `--listen` Flag
Without this, `server_name='127.0.0.1'` and the Gradio server only accepts connections from inside the container. With `--listen`, it binds to `0.0.0.0` and the `-p 7860:7860` port mapping works.

### Torch CPU vs CUDA
The FunASR models run inference using PyTorch. CPU inference is slower but functionally identical. For a 3-second audio file, recognition takes about 2-3 seconds on CPU. This is acceptable for a testing/research deployment.

### ImageMagick Policy
If the policy isn't fixed, the "Clip+Subtitles" feature fails because moviepy calls ImageMagick's `convert` command, which is blocked by the default security policy. The basic "Clip" (without subtitles) still works because it only uses ffmpeg.

## How Each Test Was Chosen and What It Validated

### Test 1: Homepage GET /
**Why:** Confirms the Gradio web server started and serves the UI. If this fails, nothing else works.
**Result:** HTTP 200, 95KB HTML response. PASS.

### Test 2: /gradio_api/info
**Why:** Gradio 6.x exposes API metadata at this endpoint. Confirms all 7 function endpoints are registered.
**Result:** 7 endpoints listed (/mix_recog, /mix_recog_speaker, /mix_clip, /video_clip_addsub, /llm_inference, /AI_clip, /AI_clip_subti). PASS.

### Test 3: /mix_recog (ASR)
**Why:** This is the core feature -- speech recognition. Tests the entire FunASR pipeline: audio loading, VAD, Paraformer inference, punctuation, SRT generation.
**What I did:** Created a 3-second 440Hz sine wave with ffmpeg, uploaded it via the Gradio upload API, then called /mix_recog. A sine wave isn't speech, but FunASR still processes it and returns some output ("Mmhmmm mmhmm").
**Result:** Returns text and SRT subtitle. The ASR models loaded correctly, inference ran, output was properly formatted. PASS.

### Test 4: /mix_recog_speaker (ASR + Speaker Diarization)
**Why:** Tests the speaker diarization model (CAM++) in addition to ASR. Same audio file.
**Result:** Returns text with `spk0` speaker label. The speaker model loaded and ran correctly. PASS.

### Test 5: /mix_clip (Clipping)
**Why:** Tests the core clipping pipeline -- the main value of this app.
**Initial attempt:** Failed via Gradio JSON API because `gr.State` stores Python dicts with numpy arrays that can't round-trip through JSON (state comes back as `null`).
**Fix:** Tested by calling the Python functions directly inside the container, bypassing the Gradio API serialization layer. Downloaded the real example audio file from the README (a Chinese interview clip). Used the Chinese SeACo-Paraformer model for recognition, then clipped using a substring from the middle of the recognized text.
**Result:** ASR recognized the full interview. Text matching found 1 period at 95.72s-97.94s. Clipped 2.22 seconds of audio with correct SRT subtitles. PASS.

### Test 6: /llm_inference
**Why:** Tests the LLM integration end-to-end.
**What I did:** Passed the OPENAI_API_KEY env var into the container, then called /llm_inference with model `gpt-4-turbo`, a system prompt asking it to analyze SRT subtitles, and the SRT output from the ASR test. Note: the code routes `gpt-3.5-turbo` to moonshot.cn (not OpenAI!), and `deepseek` to deepseek.com. Only `gpt-4-turbo` and similar actually hit the OpenAI API (base_url stays None).
**Result:** GPT-4-turbo returned `1. [00:00:00,680-00:00:03,050] mmhmmm mmhmm,` -- a properly formatted timestamp + text clip suggestion. PASS.

## Gotchas and Debugging

### Gradio Log Output Invisible
After "Initializing VideoClipper", no more log output appeared from `docker logs`. The Gradio startup message ("Running on http://0.0.0.0:7860") was not captured in Docker's log driver. However, the port was listening and responding to HTTP requests. This might be a Gradio 6.x stdout buffering issue. Takeaway: always test the actual port, don't rely on log output.

### ImageMagick 6 vs 7
The README instructions reference `/etc/ImageMagick-6/policy.xml` but current Debian installs ImageMagick 7. The `find`-based approach handles both versions. This kind of path change is common when Linux distros bump major versions of packages.

### Gradio 6.x FileData Format
Gradio 6.x requires a `meta` field in file upload payloads: `{'path': '...', 'meta': {'_type': 'gradio.FileData'}}`. Without it, pydantic validation fails. Older Gradio versions accepted just `{'path': '...'}`. The API prefix also changed from `/api/` to `/gradio_api/`.

### gr.State Serialization
Gradio's `gr.State` component is designed for browser session state, not API usage. The state stores Python objects (dicts with numpy arrays) that can't be serialized to JSON. This means clip endpoints only work through the browser UI. This is the intended usage -- FunClip is a Gradio app, not a REST API.

### Model Download on First Start
FunASR models are downloaded from ModelScope on first container start. This takes 3-7 minutes depending on network speed. The container appears to hang during this time. To persist models across container restarts, mount a volume at `/root/.cache/modelscope`.
