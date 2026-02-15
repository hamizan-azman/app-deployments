# autoMate -- Usage Documentation

## Status: SKIP (not compatible with Docker)

## Reason
- Desktop RPA (Robotic Process Automation) tool
- Requires GUI/display for screen automation
- Useless in Docker (no desktop environment)
- Designed for Windows desktop with mouse/keyboard control

## What It Does
Desktop automation tool using LLMs to control mouse, keyboard, and screen interactions. Web UI on port 7888.

## Original Repo
https://github.com/yuruotong1/autoMate

## Manual Build Steps

Since Docker cannot provide a GUI environment, build and run natively:

```bash
# Requires: Python 3.12, conda, NVIDIA GPU (4GB+ VRAM recommended)

# 1. Clone
git clone https://github.com/yuruotong1/autoMate.git
cd autoMate

# 2. Create environment
conda create -n automate python==3.12
conda activate automate

# 3. Install dependencies and download model weights
python install.py

# 4. Run
python main.py
```

Access the web UI at `http://localhost:7888/`.

## Core Features
- Screen automation via LLM-driven mouse/keyboard control
- Supports OpenAI models (gpt-4o, o1, etc.)
- Web UI for task configuration

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (via UI) | Yes | None | LLM API key, configured through the web interface |
