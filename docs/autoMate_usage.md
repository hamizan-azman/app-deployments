# autoMate -- Local Install Guide

## Overview
autoMate is an AI-powered RPA tool built on OmniParser that takes natural language task descriptions and automates desktop UI interactions by capturing the screen, interpreting it with a vision model, and simulating mouse/keyboard actions.

## Why Not Dockerized
autoMate captures and controls the live desktop display. It uses `pyautogui` and `pynput` to simulate input and reads the screen via OmniParser's OCR pipeline. Docker containers have no display server or input device access, and there is no headless mode.

## Requirements
- OS: Windows 10/11 (primary; macOS reported to work with caveats)
- Python 3.12
- Conda (miniconda or anaconda)
- NVIDIA GPU with 4GB+ VRAM strongly recommended (OmniParser's OCR pipeline is GPU-intensive; CPU fallback is very slow)
- OpenAI API key (gpt-4o or later; requires multimodal + structured output support)

## Installation

```bash
# Clone the repo
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate

# Create and activate environment
conda create -n automate python=3.12 -y
conda activate automate

# Run the project install script (installs deps and downloads OmniParser weights)
python install.py
```

If you have a CUDA GPU, replace the default torch with a CUDA-enabled build after running install.py. Check your CUDA version first with `nvidia-smi`, then:

```bash
# Example for CUDA 12.4:
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## Usage

```bash
conda activate automate
python main.py
```

Open `http://localhost:7888` in a browser. Enter your OpenAI API key in Settings, then describe a task in natural language and click Run.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OpenAI API key | Yes (via UI) | None | Entered through the Gradio web UI settings page |

## Notes
- The Gradio web UI at port 7888 handles configuration and task input only. The actual automation runs on the host desktop -- keep the desktop visible and unlocked while tasks run.
- Only OpenAI models with multimodal + structured output are supported: gpt-4o, gpt-4o-2024-08-06, gpt-4o-2024-11-20, o1.
- `install.py` downloads OmniParser model weights. Requires several GB of free disk space and a stable internet connection.
- On CPU-only machines, each automation step will be significantly slower due to OmniParser's OCR overhead.
- GitHub: https://github.com/yuruotong1/autoMate
