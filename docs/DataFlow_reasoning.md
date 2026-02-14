# DataFlow -- Reasoning Log

## Analysis

### Repository Structure
- `README.md`: Comprehensive docs in Chinese and English. Data preparation system for LLMs with CLI interface and optional WebUI.
- `Dockerfile`: Uses `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04` base image. Installs Python, pip, and the package with vLLM extra.
- `pyproject.toml`: Package name `open-dataflow`, Python >= 3.10. Dependencies include torch, transformers, datasets, gradio, fastapi, uvicorn.
- `requirements.txt`: 88 dependencies including numpy<2.0, torch, transformers, vllm.
- `dataflow/cli.py`: Typer-based CLI with commands for text2model, pdf2model, eval, chat, webui, init.
- `dataflow/cli_funcs/cli_webui.py`: WebUI launcher that downloads a separate executable from GitHub releases at runtime.

### Key Finding: GPU Required
The Dockerfile uses NVIDIA CUDA base image. The core functionality (vLLM inference, transformers model training) requires GPU acceleration. CPU would technically work for some operations but with severe performance degradation.

### Pre-built Image Available
Docker Hub has `molyheci/dataflow:cu124` maintained by the original developers. The docker-compose.yml and README both reference this image.

## Decision

### Use Pre-built Image
The original developers maintain `molyheci/dataflow:cu124` on Docker Hub. Using this aligns with architectural fidelity. Building from source would require a GPU host for testing, which we don't have.

### Mark as GPU-Only
Neither the laptop nor the desktop have NVIDIA GPUs. We cannot pull the image (it's ~15GB and CUDA-specific), build it, or test it. Documenting the pull command and CLI usage from the README is the best we can do.

### No Custom Dockerfile
The provided Dockerfile is production-ready and uses the NVIDIA CUDA base image. No modifications needed. No point building a CPU-only variant since the core functionality requires GPU.

## Other Options

### CPU-Only Build
Could strip vLLM and use python:3.10-slim base. Rejected because:
- Core inference pipeline requires GPU
- Would fundamentally change the app's behavior
- Violates architectural fidelity

### Testing on Cloud GPU
Could spin up a cloud GPU instance for testing. Rejected because:
- Outside the scope of this deployment project
- Cost and complexity not justified

## Test Details

All tests marked NOT TESTED because GPU is required. The pre-built image and CLI commands are documented from the README and source code analysis.

## Gotchas

1. **WebUI downloads at runtime**: The webui command downloads a separate executable from GitHub. Container needs internet access.
2. **NVIDIA Container Toolkit required**: Host must have nvidia-docker or NVIDIA Container Toolkit installed.
3. **Large image**: CUDA base images are typically 5-10GB.
4. **Optional MySQL**: The text2sql pipeline can connect to MySQL via pymysql, but it's not required for basic usage.
