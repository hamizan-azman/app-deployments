# MedRAX -- Local Install Guide

## Overview
MedRAX is an AI agent for chest X-ray analysis that integrates multiple specialized medical imaging models (CheXagent, LLaVA-Med, MedSAM, Maira-2) with GPT-4o to perform detection, classification, segmentation, and report generation. It exposes a Gradio web interface.

## Why Not Dockerized
MedRAX loads multiple large vision-language models simultaneously. The official deployment configuration used an NVIDIA RTX 6000 (48 GB VRAM). Even with 8-bit quantization, the combined model stack requires well beyond the 8 GB available on the RTX 3070. The models are also downloaded dynamically from HuggingFace at first launch, making Docker image size unmanageable.

## Requirements
- OS: Linux or Windows with WSL2 (recommended); macOS (CPU only, very slow)
- Python 3.8+
- NVIDIA GPU: 12 GB+ VRAM minimum (for a subset of tools); 24 GB+ for full tool set; 48 GB for full official configuration
- CUDA 11.8+ and matching PyTorch
- OpenAI API key (GPT-4o used as the reasoning backbone)
- 50+ GB free disk space for model weights

## Installation

```bash
# Clone the repo
git clone https://github.com/bowang-lab/MedRAX.git
cd MedRAX

# Create and activate a virtual environment (Python 3.8+)
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install the package
pip install -e .

# Create .env with your API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

## Usage

Before running, open `main.py` and set `model_dir` to the directory where HuggingFace model weights should be stored:

```python
# In main.py, find and set:
model_dir = "/path/to/your/model/directory"
```

To reduce VRAM usage, comment out tool initializations for models you do not need (LlavaMedTool and Maira2Tool are the most resource-intensive).

Then launch:

```bash
python main.py
```

The Gradio web UI will start after models finish loading. First run downloads several GB of model weights from HuggingFace.

### Quickstart (minimal, for testing)

```bash
python quickstart.py
```

This loads a minimal subset of tools for basic chest X-ray analysis.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for GPT-4o reasoning backbone. Set in `.env`. |
| OPENAI_BASE_URL | No | OpenAI default | Override for OpenAI-compatible local LLMs (e.g., Ollama). |

## Notes
- RTX 3070 (8 GB) is insufficient for the full stack. You may be able to run a single tool (e.g., CheXagent only) with 8-bit quantization, but this is not a supported configuration.
- 8-bit quantization is enabled by default where supported (bitsandbytes). Disable it if you have abundant VRAM for better accuracy.
- Selective tool initialization: comment out tools in `main.py` to reduce memory footprint.
- GitHub: https://github.com/bowang-lab/MedRAX
