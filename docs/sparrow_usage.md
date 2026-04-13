# sparrow. Usage Documentation

## Overview
FastAPI service that extracts structured data from documents (PDFs, images, tables) using LLMs. Deployed as the LLM component only (`sparrow-ml/llm`). Supports multiple inference backends including LlamaIndex, Hugging Face, and local models via MLX. Exposes a REST API for document parsing.

## Quick Start
```bash
docker pull hoomzoom/sparrow
docker run -d -p 7860:7860 hoomzoom/sparrow
```

Open http://localhost:7860/docs for the interactive API documentation.

## Base URL
http://localhost:7860

## Core Features
- Extract structured data from PDFs and images using LLM inference
- Multiple backend support (LlamaIndex, MLX, Hugging Face)
- REST API with FastAPI and automatic OpenAPI docs
- Configurable model selection via request parameters
- Requires poppler-utils for PDF rendering

## Endpoints

### API Documentation
- **URL:** http://localhost:7860/docs
- **Method:** GET
- **Description:** Interactive Swagger UI with all endpoint definitions and request schemas.
- **Tested:** Yes

### Alternative Docs
- **URL:** http://localhost:7860/redoc
- **Method:** GET
- **Description:** ReDoc-style API documentation.
- **Tested:** Yes (page loads)

### Inference (primary endpoint)
- **URL:** http://localhost:7860/api-inference/sparrow-data
- **Method:** POST
- **Description:** Submit a document and extraction query. Returns structured JSON.
- **Tested:** No (requires model configuration and input file)

## Health Check
- **URL:** http://localhost:7860/docs
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Conditional | None | Required when using OpenAI backend |
| ANTHROPIC_API_KEY | Conditional | None | Required when using Anthropic backend |
| HUGGINGFACE_TOKEN | Conditional | None | Required for gated Hugging Face models |

No API key is required to start the container. Keys are only needed when calling inference endpoints with cloud-backed models.

## Notes
- Deployed from the `sparrow-ml/llm` subdirectory of the upstream monorepo. The broader Sparrow project includes additional components (UI, data pipeline) that are not included in this image.
- poppler-utils is installed as a system dependency for PDF-to-image conversion.
- The container runs as non-root user `user` (UID 1000).
- Local model inference (MLX, Hugging Face) requires mounting model weights or downloading at runtime.

## Changes from Original
The upstream repo is a monorepo. This Dockerfile targets only the `sparrow-ml/llm` component, which is the LLM inference API. No other components are included.

## V2 Dependency Changes (Minimum Version Pinning)
Dependencies installed from `requirements_sparrow_parse.txt` via pip. Exact versions resolved at build time.
