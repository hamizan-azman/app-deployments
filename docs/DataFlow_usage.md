# DataFlow -- Usage Documentation

## Overview
Data preparation and training system for LLMs. CLI + WebUI for text/PDF data pipelines, reasoning enhancement, knowledge base cleaning, and agentic RAG. Includes vLLM for inference. GPU required.

## Quick Start
```bash
docker pull hoomzoom/dataflow
docker run --gpus all -it -p 7862:7862 hoomzoom/dataflow \
  dataflow webui --host 0.0.0.0 --port 7862
```
Access WebUI at `http://localhost:7862`.

## Requirements
- NVIDIA GPU with CUDA 12.4+ support
- NVIDIA Container Toolkit installed on host
- `--gpus all` flag required
- Works on GTX 1650 (4GB VRAM) for WebUI and basic operations

## Base URL
http://localhost:7862 (WebUI)

## CLI Commands
```bash
# Must use -t flag for interactive commands (terminal size detection)
docker run --gpus all -t hoomzoom/dataflow dataflow --help
docker run --gpus all -t hoomzoom/dataflow dataflow env

# Inside an interactive container
docker run --gpus all -it hoomzoom/dataflow bash
dataflow -v                              # Check version (1.0.6)
dataflow init repo                       # Initialize a project
dataflow text2model init                 # Initialize text-to-QA pipeline
dataflow text2model train                # Train text-to-QA model
dataflow pdf2model init                  # Initialize PDF-to-QA pipeline
dataflow pdf2model train                 # Train PDF-to-QA model
dataflow eval init                       # Initialize evaluation
dataflow eval api                        # Run API-based evaluation
dataflow eval local                      # Run local evaluation
dataflow chat --model /path/to/model     # Chat with trained model
dataflow webui --host 0.0.0.0 --port 7862  # Launch WebUI
```

## WebUI Modes
```bash
# Default: operators mode (data processing pipeline builder)
dataflow webui --host 0.0.0.0 --port 7862

# Agent mode (FastAPI + uvicorn)
dataflow webui --ui_mode agent --host 0.0.0.0 --port 7862

# PDF/KB cleaning mode
dataflow webui --ui_mode pdf
```

## Environment
- DataFlow version: 1.0.6
- Python: 3.10.12
- PyTorch: 2.7.0+cu126
- vLLM: 0.9.2

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DF_API_KEY | No | None | API key for OpenAI-compatible operators |

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Docker pull | PASS |
| 2 | GPU detection (nvidia-smi) | PASS (GTX 1650, 4GB) |
| 3 | dataflow --help | PASS (7 subcommands) |
| 4 | dataflow env | PASS (shows full environment) |
| 5 | WebUI GET / | PASS (200 OK) |
| 6 | Gradio API /gradio_api/info | PASS (100+ operators listed) |

6/6 tests passed.

## Notes
- GPU is required for the CUDA image. Uses NVIDIA CUDA 12.4.1 + vLLM.
- CLI commands that print formatted output (dataflow -v, dataflow env) need a pseudo-TTY (-t flag) or they crash with `Inappropriate ioctl for device`.
- WebUI default port is 7862, not 7860. Pass --port explicitly if needed.
- WebUI binds to 127.0.0.1 by default. Must pass --host 0.0.0.0 for Docker access.
- Pre-built image maintained by original developers on Docker Hub.
- Two warnings on startup about pipeline analysis (vqa_extract, rare_pipeline) are benign.
