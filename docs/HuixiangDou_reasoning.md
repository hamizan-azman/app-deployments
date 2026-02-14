# HuixiangDou -- Reasoning Log

## Overview

### Repository Structure
- `README.md`: Professional knowledge assistant for group chat. Three-stage pipeline. Supports CPU-only, 2GB GPU, 10GB GPU configs.
- No Dockerfile in repo root (uses pre-built image).
- Pre-built Docker image: `tpoisonooo/huixiangdou:20240814` on Docker Hub.
- Web UI on port 7860 (Gradio), API on port 23333.
- Supports multiple LLM providers: kimi, deepseek, stepfun, siliconcloud, vllm.

## Decision

### Use Pre-built Image
The original developers provide `tpoisonooo/huixiangdou:20240814`. Building from source would require complex setup of knowledge base tools, embedding models, and retrieval infrastructure. The pre-built image includes everything.

### Mark as PULL-ONLY
The image requires manual configuration after first run (setting up LLM API keys, creating knowledge bases). Without hands-on setup, automated testing is not feasible. Documenting the pull command and basic usage is appropriate.

## Why Not Full Testing
- Requires manual knowledge base creation (upload documents, set positive/negative examples)
- LLM API configuration is interactive (edit config files inside container)
- The setup process is documented in README but requires human judgment
- Pre-built image is trusted (maintained by original developers, active project)

## Gotchas
1. Image is from August 2024. May not include latest features.
2. Manual configuration required inside container for LLM API keys.
3. Knowledge base must be created before the chat feature works.
4. CPU-only mode works but inference is slow.
