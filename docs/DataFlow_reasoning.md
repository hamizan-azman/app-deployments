# DataFlow -- Reasoning Log

## Analysis

### Repository Structure
DataFlow is a data preparation and training system by OpenDataLab. The repo has a CLI tool (`dataflow`) with subcommands for text-to-model training, PDF-to-model training, evaluation, chat, and a Gradio WebUI. The core value is its 100+ data processing operators (filters, evaluators, generators, refiners) that can be composed into pipelines.

### Pre-built Image
The developers maintain `molyheci/dataflow:cu124` on Docker Hub. This image is based on `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04` with Python 3.10.12, PyTorch 2.7.0+cu126, and vLLM 0.9.2 pre-installed. No reason to build from scratch.

## Decision

### Upgrading from PULL-ONLY to Deployed
Originally marked PULL-ONLY because "GPU required (CUDA 12.4)." Tested on a GTX 1650 (4GB VRAM) and it works fine for the WebUI and CLI. The data processing operators run mostly on CPU. Only training and inference via vLLM actually need GPU memory. For security research purposes, the app's full attack surface (Gradio WebUI, pipeline configuration, file upload/processing) is exercisable even without heavy GPU workloads.

### No Dockerfile Created
Used the pre-built image as-is. No modifications needed. The developers maintain it and it already includes all dependencies.

## Other Options

### Building from the Repo's Dockerfile
The repo has its own Dockerfile but it uses the Tsinghua University pip mirror (Chinese mirror), which is slower outside China. The pre-built image is already there on Docker Hub, so no benefit to rebuilding.

### CPU-Only
DataFlow doesn't have a CPU-only image. The CUDA base image runs fine even for non-GPU operations but is much larger than necessary if you only need the data processing operators. Not worth creating a custom CPU image for this project.

## Test Details

### Test 1: Docker Pull
Pulled `molyheci/dataflow:cu124` successfully. Image is large (multiple GB) due to CUDA + PyTorch + vLLM.

### Test 2: GPU Detection
Ran `nvidia-smi` inside the container with `--gpus all`. Detected GTX 1650 with 4GB VRAM and CUDA 13.1 driver (compatible with the 12.4 toolkit).

### Test 3: CLI Help
`dataflow --help` shows 7 subcommands: init, env, chat, eval, pdf2model, text2model, webui. The CLI requires a pseudo-TTY (`-t` flag) for commands that print formatted output (e.g., `dataflow -v`, `dataflow env`). Without it, `os.get_terminal_size()` throws `Inappropriate ioctl for device`.

### Test 4: Environment Info
`dataflow env` prints system info: Python 3.10.12, PyTorch 2.7.0+cu126, GPU type and memory, vLLM version. Confirms all dependencies are correctly installed and GPU is accessible.

### Test 5: WebUI
Started with `dataflow webui --host 0.0.0.0 --port 7862`. GET on port 7862 returns 200. The WebUI is a Gradio app with pipeline builder, operator selection, and configuration panels. Two benign warnings on startup about `vqa_extract_pipeline_mineru.py` (has 2 classes where 1 expected) and `rare_pipeline.py` (missing import).

### Test 6: Gradio API
GET `/gradio_api/info` returns a large JSON listing all available operators and their parameters. Over 100 operators across categories: general text, knowledge cleaning, code, math, rare, agentic RAG.

## Gotchas

1. **Port 7862, not 7860**: The WebUI defaults to port 7862 in operators mode, not the usual Gradio 7860.
2. **Binds to 127.0.0.1**: Must pass `--host 0.0.0.0` for Docker access. Without it, the WebUI only listens on localhost inside the container.
3. **TTY required for CLI**: `dataflow -v` and `dataflow env` crash without a terminal because they call `os.get_terminal_size()`. Use `docker run -t` (allocate pseudo-TTY) for these commands.
4. **Chinese text in WebUI**: Some UI labels are in Chinese. The WebUI has a language switcher (Chinese/English).
5. **vLLM memory**: Running actual model inference via vLLM will need more GPU memory than the GTX 1650's 4GB for most models. The WebUI and operators themselves are fine.
