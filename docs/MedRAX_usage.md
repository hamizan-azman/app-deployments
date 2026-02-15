# MedRAX -- Usage Documentation

## Status: SKIP (not compatible with Docker)

## Reason
- Requires GPU for medical imaging model inference
- Multiple large models from HuggingFace (CheXagent, LLaVA-Med, MedSAM, Maira-2)
- No Dockerfile provided
- Specialized medical imaging pipeline requiring automatic model download
- GPU-only inference with torch, transformers, accelerate, bitsandbytes

## What It Does
Medical reasoning agent for chest X-ray interpretation using specialized AI tools and multimodal LLMs. Gradio web interface.

## Original Repo
https://github.com/bowang-lab/MedRAX

## Manual Build Steps

Since Docker cannot practically host the required GPU model stack, build and run natively:

```bash
# Requires: Python 3.10+, NVIDIA GPU with CUDA, OpenAI API key
# Models download automatically from HuggingFace on first run

# 1. Clone
git clone https://github.com/bowang-lab/MedRAX.git
cd MedRAX

# 2. Install
pip install -e .

# 3. Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# 4. Run
python main.py
```

Models are downloaded from HuggingFace on first launch (several GB). The Gradio web UI will start after models are loaded.

## Core Features
- Chest X-ray interpretation
- Medical image segmentation (MedSAM)
- Multi-tool agent pipeline (CheXagent, LLaVA-Med, Maira-2)
- Gradio web interface

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key (or compatible provider). Set in .env file |
| OPENAI_BASE_URL | No | OpenAI default | Override for local LLMs (e.g. http://localhost:11434/v1 for Ollama) |
