# TaskMatrix (Visual ChatGPT) -- Usage Documentation

## Status: SKIP (not compatible with Docker)

## Reason
- Heavy GPU requirements: 3-15GB GPU memory per foundation model
- Designed for multi-GPU setup (4x Tesla V100 32GB for full features)
- No complete Dockerfile for main application
- Downloads many large models at runtime (ControlNet, Stable Diffusion, BLIP)
- No CPU fallback for visual foundation models

## What It Does
Connects ChatGPT with visual foundation models to enable sending/receiving images during chat. Supports image generation, editing, visual QA through multiple AI models. Gradio web interface on port 7861.

## Original Repo
https://github.com/chenfei-wu/TaskMatrix

## Manual Build Steps

Since Docker cannot practically host the required multi-GPU model stack, build and run natively:

```bash
# Requires: Python 3.8, conda, NVIDIA GPU (16GB+ VRAM for multiple models)
# OpenAI API key required

# 1. Clone
git clone https://github.com/chenfei-wu/TaskMatrix.git
cd TaskMatrix

# 2. Create environment
conda create -n visgpt python=3.8
conda activate visgpt

# 3. Install dependencies
pip install -r requirements.txt
pip install git+https://github.com/IDEA-Research/GroundingDINO.git
pip install git+https://github.com/facebookresearch/segment-anything.git

# 4. Set API key
export OPENAI_API_KEY=your-key-here       # Linux/Mac
set OPENAI_API_KEY=your-key-here          # Windows

# 5. Run (adjust --load based on available GPU memory)
# Full features (requires ~60GB+ GPU memory across multiple GPUs):
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0"

# Minimal CPU mode (very slow):
python visual_chatgpt.py --load "ImageCaptioning_cpu,Text2Image_cpu"
```

Access Gradio UI at `http://localhost:7861`.

## Core Features
- Image generation from text
- Image editing (style transfer, object removal, etc.)
- Visual question answering
- Image captioning
- Supports 20+ visual foundation models

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for ChatGPT |
