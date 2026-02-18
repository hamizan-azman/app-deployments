# TaskMatrix (Visual ChatGPT) -- Local Install Guide

## Overview
TaskMatrix connects ChatGPT with Visual Foundation Models (image generation, editing, segmentation, visual QA, depth estimation, and more) to enable image-processing tasks during chat. It provides a Gradio web UI on port 7861.

## Why Not Dockerized
TaskMatrix loads multiple large vision models simultaneously. The full model set requires approximately 60-70 GB of VRAM across multiple GPUs. Even a minimal subset of models requires at least 6-8 GB of VRAM. Docker on this machine (RTX 3070, 8 GB VRAM) cannot reliably host the required GPU model stack, and some vision models require CUDA compilation steps (GroundingDINO, segment-anything) that make containerization impractical.

## Requirements
- OS: Linux or Windows with WSL2 (macOS not supported for CUDA models)
- Python 3.8
- Conda
- NVIDIA GPU: 8 GB+ VRAM minimum for a small subset of models; 16 GB+ for practical use; 60 GB+ for full model set
- OpenAI API key
- CUDA 11.6+ with matching PyTorch build

## Installation

```bash
# Clone the repo
git clone https://github.com/moymix/TaskMatrix.git
cd TaskMatrix

# Create and activate environment
conda create -n visgpt python=3.8 -y
conda activate visgpt

# Install base dependencies
pip install -r requirements.txt

# Install GroundingDINO (requires CUDA build tools)
pip install git+https://github.com/IDEA-Research/GroundingDINO.git

# Install Segment Anything
pip install git+https://github.com/facebookresearch/segment-anything.git

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here       # Linux/macOS
# set OPENAI_API_KEY=your-key-here        # Windows CMD
```

## Usage

Launch with the `--load` argument to select which models to load and on which device. Format: `ModelName_device:index` (e.g., `cuda:0`, `cpu`).

```bash
# Minimal load -- 2 models, approximately 4-6 GB VRAM
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0"

# Small GPU (8GB) -- image captioning + basic generation
python visual_chatgpt.py --load "ImageCaptioning_cuda:0,Text2Image_cuda:0,Image2Canny_cuda:0,CannyText2Image_cuda:0"

# CPU-only fallback (very slow, for code inspection only)
python visual_chatgpt.py --load "ImageCaptioning_cpu,Text2Image_cpu"
```

Open the Gradio UI at `http://localhost:7861`.

### Available models for --load
ImageCaptioning, Text2Image, ImageEditing, VisualQuestionAnswering, Image2Canny, CannyText2Image, Image2Depth, DepthText2Image, Image2Hed, HedText2Image, Image2Scribble, ScribbleText2Image, Image2Pose, PoseText2Image, Image2Seg, SegText2Image, Image2Normal, NormalText2Image, InstructPix2Pix, Segmenting, Text2Box

### Approximate VRAM per model
- Image2Canny, Image2Depth, Image2Hed: ~0 MB (OpenCV-based, no GPU)
- ImageCaptioning: ~1,200 MB
- Text2Image (Stable Diffusion): ~3,700 MB
- ImageEditing (InstructPix2Pix): ~4,000 MB
- Segmenting (SAM): ~2,400 MB

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for the ChatGPT backbone |

## Notes
- RTX 3070 (8 GB) can run a small subset of models. Avoid loading ImageEditing, VisualQuestionAnswering, and InstructPix2Pix simultaneously.
- Models are downloaded from HuggingFace on first use. Expect several GB of downloads per model.
- GitHub: https://github.com/moymix/TaskMatrix (mirror of https://github.com/microsoft/TaskMatrix)
