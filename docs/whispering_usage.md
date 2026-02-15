# whispering (Whispering Tiger) -- Usage Documentation

## Status: SKIP (not compatible with Docker)

## Reason
- Requires live audio device (microphone) -- crashes without one
- Windows-centric: PyAudioWPatch, pywin32, winsdk, triton-windows
- WebSocket-only interface (no HTTP API)
- ~185 direct dependencies, many from custom GitHub forks
- No deployment Dockerfile (only PyInstaller build Dockerfiles)
- Would require significant architectural changes to run in Docker headless

## What It Does
Speech transcription tool using Whisper models. Streams audio from microphone, transcribes in real-time via WebSocket, outputs to OSC. Supports Whisper, Seamless M4T, Speech T5, Phi-4, NeMo Canary models.

## Original Repo
https://github.com/Sharrnah/whispering

## Manual Build Steps

Since Docker cannot provide audio device access, build and run natively:

```bash
# Requires: Python 3.10, microphone/audio input device, FFmpeg in PATH
# GPU recommended (NVIDIA CUDA) for real-time transcription

# 1. Clone
git clone https://github.com/Sharrnah/whispering.git
cd whispering

# 2. Install dependencies
pip install -r requirements.txt -U

# For NVIDIA GPU support:
pip install -r requirements.nvidia.txt -U

# For AMD GPU support:
pip install -r requirements.amd.txt -U

# 3. List available audio devices
python audioWhisper.py --devices true

# 4. Run with a specific device
python audioWhisper.py --device_index <index> --model medium --task transcribe
```

## Core Features
- Real-time speech-to-text from microphone
- Multiple model backends (Whisper, Seamless M4T, Speech T5, NeMo Canary)
- WebSocket interface for streaming results
- OSC output for integration with other tools

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (none) | - | - | No env vars required. Configuration via CLI flags. |
