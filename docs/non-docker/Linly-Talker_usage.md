# Linly-Talker -- Local Install Guide

**Deployment**: GPU server. NVIDIA GPU 8+ GB VRAM.

## Overview
Linly-Talker is a digital human video synthesis system. It takes text or audio input and generates a talking-head video of a virtual character with synchronized lip movements. The interface is a Gradio web UI. The synthesis pipeline relies on several GPU-accelerated models including SadTalker, MuseTalk, and Wav2Lip.

## Why Not Dockerized
Linly-Talker requires an NVIDIA GPU with CUDA for all of its core synthesis models. The pipeline combines multiple deep learning components (lip sync, face generation, TTS) that require significant VRAM and are not designed to run on CPU. Containerising the full GPU-accelerated pipeline requires NVIDIA Container Toolkit and direct GPU passthrough, which is not reliably supported in the Docker Desktop on Windows environment used for this research.

## Requirements
- OS: Linux (recommended) or Windows with CUDA support
- NVIDIA GPU with at least 8GB VRAM (16GB+ recommended for higher quality modes)
- CUDA 11.8 or 12.x
- Python 3.10
- conda (recommended for environment isolation)
- ffmpeg installed and on PATH

## Installation

```bash
git clone https://github.com/Kedreamix/Linly-Talker.git
cd Linly-Talker

# Create conda environment
conda create -n linly python=3.10 -y
conda activate linly

# Install PyTorch with CUDA (adjust cu118 or cu121 to match your CUDA version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install project dependencies
pip install -r requirements.txt
```

Install ffmpeg if not already available:
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: download from https://ffmpeg.org/download.html and add to PATH

Download pretrained model weights by following the instructions in the repository's README. Weights are hosted on Hugging Face and Baidu Pan.

## Usage

```bash
conda activate linly
python app.py
```

The Gradio UI will launch and print a local URL (default `http://localhost:7860`). Open it in a browser, upload or select a character image, provide text input or an audio file, and generate the talking-head video.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Optional | None | Required only if using the GPT-based conversational mode |
| `LINLY_API_KEY` | Optional | None | Required if using the Linly-LLM cloud backend for response generation |

## Notes
- The core video synthesis pipeline works without any API keys. LLM-powered conversational modes require a key for the chosen backend.
- Model weight downloads are several GB in total. Ensure stable internet and sufficient disk space before starting.
- On Windows, run inside WSL2 with CUDA support for the most reliable experience.
- GitHub: https://github.com/Kedreamix/Linly-Talker
