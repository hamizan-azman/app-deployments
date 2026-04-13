# kotaemon. Usage Documentation

## Overview
Gradio-based document QA platform for interacting with documents using RAG. Deployed in lite variant (no full model download at build time). Supports multiple LLM providers including OpenAI, Anthropic, Azure OpenAI, and local models via Ollama. Document ingestion, citation-backed answers, and multi-user support.

## Quick Start
```bash
docker pull hoomzoom/kotaemon
docker run -d -p 7860:7860 \
  -e OPENAI_API_KEY=your_key \
  hoomzoom/kotaemon
```

Open http://localhost:7860 in your browser.

## Base URL
http://localhost:7860

## Core Features
- Document upload and indexing (PDF, DOCX, HTML, and more)
- Citation-backed question answering
- Multi-user authentication
- Multiple LLM and embedding provider support
- Graphical UI built with Gradio

## Health Check
- **URL:** http://localhost:7860/
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Conditional | None | OpenAI API key |
| ANTHROPIC_API_KEY | Conditional | None | Anthropic API key |
| AZURE_OPENAI_API_KEY | Conditional | None | Azure OpenAI API key |
| AZURE_OPENAI_ENDPOINT | Conditional | None | Azure OpenAI endpoint URL |
| OLLAMA_HOST | No | None | Ollama server URL for local models |
| GRADIO_SERVER_NAME | No | 0.0.0.0 | Gradio bind address |
| GRADIO_SERVER_PORT | No | 7860 | Gradio port |

At least one LLM provider is required for QA features. The app starts without any keys but cannot answer questions.

## Persistent Data
To persist uploaded documents and conversation history across container restarts:
```bash
docker run -d -p 7860:7860 \
  -e OPENAI_API_KEY=your_key \
  -v kotaemon_data:/app/ktem_app_data \
  hoomzoom/kotaemon
```

## Notes
- Built using the lite variant of kotaemon. The full variant downloads large embedding models at build time. The lite variant downloads them at first use, keeping the image smaller.
- Built with `uv sync --frozen` for reproducible dependency resolution.
- graphrag is installed only on amd64 (not ARM) due to upstream compatibility constraints.
- The pdfservices-sdk is installed from a forked repository that allows unfrozen requirements.
- The container runs as non-root user `appuser` (UID 1000).
- Startup takes up to 60 seconds as Gradio initializes and PDF.js is loaded.
- LLM QA features are NOT TESTED in CI.

## Changes from Original
The upstream Dockerfile uses multi-stage build targeting the `lite` stage. We use the same approach. Windows line endings in `launch.sh` are fixed with `sed -i 's/\r$//'` to prevent script execution errors inside the Linux container.

## V2 Dependency Changes (Minimum Version Pinning)
Dependencies managed via `uv sync --frozen` from a locked `uv.lock` file. Versions are pinned in the lock file by the upstream project.
