# DataFlow -- Usage Documentation

## Overview
Data preparation and training system for LLMs. Provides CLI tools for text/PDF-to-SQL pipelines, reasoning enhancement, knowledge base cleaning, and agentic RAG. GPU required.

## Quick Start
```bash
docker pull molyheci/dataflow:cu124
docker run --gpus all -it molyheci/dataflow:cu124
```

## Requirements
- NVIDIA GPU with CUDA 12.4+ support
- NVIDIA Container Toolkit installed on host
- `--gpus all` flag required

## CLI Commands
```bash
# Inside container
dataflow -v                              # Check version
dataflow --help                          # Show all commands
dataflow init repo                       # Initialize a project
dataflow text2model init                 # Initialize text-to-QA pipeline
dataflow text2model train                # Train text-to-QA model
dataflow pdf2model init                  # Initialize PDF-to-QA pipeline
dataflow pdf2model train                 # Train PDF-to-QA model
dataflow eval init                       # Initialize evaluation
dataflow eval api                        # Run API-based evaluation
dataflow eval local                      # Run local evaluation
dataflow chat --model /path/to/model     # Chat with trained model
dataflow webui --host 0.0.0.0 --port 8000  # Launch WebUI
```

## WebUI
The WebUI is downloaded at runtime from GitHub releases. Launch with:
```bash
docker run --gpus all -it -p 8000:8000 molyheci/dataflow:cu124 \
  bash -c "dataflow webui --host 0.0.0.0 --port 8000"
```
Access at `http://localhost:8000`.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DF_API_KEY | No | None | API key for OpenAI-compatible operators |

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Docker pull | NOT TESTED (requires GPU) |
| 2 | CLI commands | NOT TESTED (requires GPU) |
| 3 | WebUI | NOT TESTED (requires GPU) |

## Notes
- GPU is non-negotiable. Uses NVIDIA CUDA 12.4.1 + vLLM for inference.
- Pre-built image maintained by original developers.
- CLI-only tool with optional WebUI (downloaded at runtime).
- No REST API endpoints exposed by default.
- Full pipeline testing requires GPU and optional API keys.
