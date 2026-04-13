# Verba. Usage Documentation

## Overview
The Golden RAGtriever: an open-source Retrieval-Augmented Generation (RAG) application built on Weaviate. Provides a web interface for document ingestion, chunking, vector search, and LLM-powered question answering. Deployed as a FastAPI application that connects to an external Weaviate instance.

## Quick Start
```bash
docker pull hoomzoom/verba
docker run -d -p 8000:8000 \
  -e WEAVIATE_URL_VERBA=http://your-weaviate:8080 \
  -e OPENAI_API_KEY=your_key \
  hoomzoom/verba
```

Open http://localhost:8000 in your browser.

## Base URL
http://localhost:8000

## Core Features
- Document ingestion with multiple chunking strategies
- Vector search over ingested documents
- LLM-powered question answering with source attribution
- Multiple LLM provider support (OpenAI, Cohere, HuggingFace, Ollama)
- Built-in web UI for all operations

## Health Check
- **URL:** http://localhost:8000/api/health
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Pages
- **Home:** http://localhost:8000 - Main RAG interface
- **API docs:** http://localhost:8000/docs - FastAPI Swagger UI

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| WEAVIATE_URL_VERBA | Yes | None | URL of Weaviate instance |
| WEAVIATE_API_KEY | Conditional | None | API key for Weaviate Cloud |
| OPENAI_API_KEY | Conditional | None | OpenAI key for embeddings and chat |
| COHERE_API_KEY | Conditional | None | Cohere API key |
| ANTHROPIC_API_KEY | Conditional | None | Anthropic API key |
| HF_TOKEN | Conditional | None | Hugging Face token |
| OLLAMA_URL | No | None | URL of Ollama instance for local models |

At least one LLM provider key and a Weaviate URL are required for functional use.

## Running with Local Weaviate

To run Verba with a local Weaviate instance, use Docker Compose:

```yaml
services:
  weaviate:
    image: semitechnologies/weaviate:1.24.1
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
      DEFAULT_VECTORIZER_MODULE: none
      ENABLE_MODULES: ""
      CLUSTER_HOSTNAME: node1

  verba:
    image: hoomzoom/verba
    ports:
      - "8000:8000"
    environment:
      WEAVIATE_URL_VERBA: http://weaviate:8080
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - weaviate
```

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- Verba requires an external Weaviate instance. It does not bundle Weaviate.
- RAG features (ingestion, search, QA) are NOT TESTED in CI as they require Weaviate and an LLM API key.
- The Verba package is installed via `pip install '.'` from the repo root.

## Changes from Original
The upstream Dockerfile uses `python:3.11-slim`. We use the same base. `wget` is installed as a system dependency (required by the upstream Dockerfile for health probe purposes). SHA256 pins are not present in the upstream Dockerfile so no changes were needed there.

## V2 Dependency Changes (Minimum Version Pinning)
Package installed via `pip install '.'` from pyproject.toml. Exact versions resolved by pip at build time.
