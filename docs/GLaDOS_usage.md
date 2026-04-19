# GLaDOS. Local Install Guide

## Overview
GLaDOS is a fully local voice assistant modelled on the GLaDOS character from the Portal video game. It runs a local speech-to-text model, sends the transcript to a local LLM (via Ollama or a similar OpenAI-compatible endpoint), and speaks the reply through a local text-to-speech model trained on GLaDOS's voice.

## Why Not Dockerized
The entire value of the project is live voice I/O. It requires.

- A working microphone device exposed to the process (PortAudio, `sounddevice` capture).
- A working speaker or audio-output device (`sounddevice` playback).
- Low-latency access to both, since the user experience is round-trip conversational.

Docker does not expose host audio devices by default. `--device /dev/snd` works on some Linux hosts but is unreliable on Docker Desktop. The WSL2 and Windows host audio stack drops or gates the device. Running the app without audio capture removes its only entry point. There is no CLI mode and no text-only fallback.

GPU is also strongly recommended for usable latency (the TTS model is the heavy part), which adds a second portability blocker for arbitrary Docker hosts.

## Requirements
- OS. Linux or Windows 10/11. macOS supported but not the primary test platform
- Python 3.11 (project uses `uv` for env management)
- `uv` (https://docs.astral.sh/uv/getting-started/installation/)
- A working microphone and speaker on the host
- NVIDIA GPU with 6 GB VRAM or more (strongly recommended. CPU-only is technically possible but slow)
- A local LLM endpoint. Ollama, llama-cpp-server, LM Studio, or any OpenAI-compatible server

## Installation

```bash
git clone https://github.com/dnhkng/GLaDOS.git
cd GLaDOS

uv sync
```

`uv sync` installs the pinned Python toolchain and all dependencies into `.venv`.

Make sure an LLM backend is running on the machine or LAN. For Ollama.

```bash
ollama pull llama3.1
ollama serve   # default port 11434
```

Edit `config/glados_config.yaml` if the LLM endpoint is not on `http://localhost:11434/v1`.

## Usage

```bash
uv run glados start
```

The assistant initialises, loads the voice-activity-detection model, the Whisper-based STT, the local LLM client, and the GLaDOS TTS model. Speak into the microphone. The agent replies through the speaker. `Ctrl+C` to stop.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| LLM_BASE_URL | No | http://localhost:11434/v1 | OpenAI-compatible LLM endpoint |
| LLM_MODEL    | No | llama3.1                  | Model name passed to the backend |

## Notes
- First start downloads the GLaDOS TTS weights (about 1 GB) into `./models`.
- Expect startup latency of 30 to 60 seconds on first run while models are cached.
- For non-interactive benchmarking, a text-only driver would have to be written from scratch. It is not part of the project.
- GitHub. https://github.com/dnhkng/GLaDOS
