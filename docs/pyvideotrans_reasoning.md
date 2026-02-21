# pyvideotrans. Reasoning Log

## Initial Assessment

pyvideotrans by jianchang512 is a video translation/dubbing tool. Primarily a desktop GUI app (PySide6/Qt6) with a CLI mode for headless operation. Python 3.10 only. ~250 pinned dependencies including PyTorch, multiple ASR engines (faster-whisper, FunASR, OpenAI Whisper), TTS providers, and translation APIs. Very heavy build.

## What Was Checked

1. **pyproject.toml**: Python >=3.10,<3.11 (strict). 250+ dependencies pinned to exact versions. Uses uv for package management with custom PyTorch indexes (CUDA 12.8 for Linux/Windows, CPU for macOS). faster-whisper installed from GitHub master branch.

2. **cli.py**: CLI entry point. Supports 4 task types: stt (speech-to-text), tts (text-to-speech), sts (subtitle translation), vtv (full video translation). Uses argparse. Imports from videotrans package.

3. **videotrans/configure/config.py**: Defines paths for temp files, output, models, FFmpeg binary. HuggingFace and ModelScope cache directories set to `ROOT_DIR/models/`.

4. **uv.lock**: Lock file present for reproducible builds with uv.

## Decisions Made

### Base image: python:3.10-slim
Strict Python 3.10 requirement. No flexibility.

### CPU-only PyTorch
Used PyTorch CPU wheels instead of CUDA. The CUDA variant adds 2-4GB to the image and requires NVIDIA runtime on the host. For research/testing, CPU is sufficient. Users needing GPU can rebuild with CUDA wheels.

### uv for dependency management
The project uses uv-specific features (custom indexes, source overrides). Using uv directly is more reliable than trying to convert to pip.

### FFmpeg via apt
Installed ffmpeg from Debian packages rather than downloading a binary. The apt version is sufficient for the operations used.

### Volume mounts for models and output
ASR/TTS models are downloaded on first use and can be gigabytes. Mounting /app/models as a volume avoids re-downloading on each container run. Output is written to /app/output.

## Build Challenges

### Complex dependency resolution
250+ packages with exact version pins, custom PyTorch indexes, and a GitHub-sourced package (faster-whisper). The uv tool handles this better than pip since the pyproject.toml uses uv-specific configuration.

### Large image size
PyTorch alone is ~800MB. With all the ML libraries (transformers, librosa, scipy, etc.), the image will be 3-5GB minimum. No way around this given the tool's requirements.

### Alibaba Cloud SDKs
The dependency list includes multiple Alibaba Cloud SDK packages for Chinese cloud translation services. These add bulk but are part of the original developer's design.

## Testing Plan

1. CLI --help: Validates entry point works
2. FFmpeg available: Validates system dependency
3. Module imports: Validates Python packages installed correctly
4. STT task with tiny model: Validates full pipeline (requires model download on first run)

## Gotchas

1. **First run downloads models**: Whisper models are not included in the image. First STT/VTV run will download the specified model (tiny=40MB, large-v3=2.9GB). Mount /app/models to cache.

2. **Python 3.10 only**: Strict version requirement. 3.11+ will break.

3. **azure-cognitiveservices-speech**: This package is listed without a version pin and may have platform-specific build issues on Linux.

4. **GPU acceleration**: The Docker image uses CPU PyTorch. For real video translation workloads, GPU is practically required for reasonable processing times.

5. **Chinese-centric defaults**: The tool was primarily designed for Chinese video translation. Default language settings and some UI text are in Chinese.
