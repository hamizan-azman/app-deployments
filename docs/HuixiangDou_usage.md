# HuixiangDou -- Usage Documentation

## Overview
Knowledge assistant powered by LLM. RAG pipeline for document Q&A with Gradio WebUI and FastAPI. Supports web search, code search, multimodal queries. CPU-only deployment with remote LLM APIs.

## Quick Start
```bash
docker pull hoomzoom/huixiangdou
docker run -d -p 7860:7860 hoomzoom/huixiangdou
```
Access WebUI at `http://localhost:7860`.

The UI loads without an API key, but queries require one. To configure your LLM API key, mount a custom `config-cpu.ini`:
```bash
# 1. Copy the default config out of the container
docker run --rm hoomzoom/huixiangdou cat config-cpu.ini > config-cpu.ini

# 2. Edit config-cpu.ini -- find the [web_search] and [llm] sections and set:
#    remote_api_key = "sk-your-api-key"
#    remote_type = "openai"  (or "kimi", "deepseek", "siliconcloud", etc.)

# 3. Run with your config mounted
docker run -d -p 7860:7860 -v ./config-cpu.ini:/app/config-cpu.ini hoomzoom/huixiangdou
```

## Base URL
http://localhost:7860 (Gradio WebUI)

## Core Features
- Document Q&A via RAG pipeline
- Web search integration (DuckDuckGo or Serper)
- Code search over repositories
- Multimodal queries (text + image)
- Parallel and serial pipeline modes
- FastAPI REST API (port 23333)

## Gradio WebUI
The default entry point. Provides:
- Text input for questions
- Optional image upload for multimodal queries
- Language toggle (English/Chinese)
- Web search toggle
- Code search toggle
- Pipeline type selection (chat_with_repo / chat_in_group)

## FastAPI API Server
Alternative entry point for programmatic access:
```bash
docker run -d -p 23333:23333 hoomzoom/huixiangdou \
  python -m huixiangdou.api_server --config_path config-cpu.ini --port 23333
```

### POST /huixiangdou_inference
- **Method:** POST
- **Description:** Single-shot Q&A inference
- **Request:** `curl -X POST http://localhost:23333/huixiangdou_inference -H "Content-Type: application/json" -d '{"text": "How to install HuixiangDou?"}'`
- **Response:** JSON with response text and references

### POST /huixiangdou_stream
- **Method:** POST
- **Description:** Streaming Q&A inference (server-sent events)
- **Request:** `curl -X POST http://localhost:23333/huixiangdou_stream -H "Content-Type: application/json" -d '{"text": "How to install HuixiangDou?"}'`
- **Response:** Streaming text/event-stream

### GET / (Swagger docs)
- **URL:** `/`
- **Method:** GET
- **Description:** FastAPI auto-generated Swagger documentation

## Configuration
The app uses `config-cpu.ini` by default (remote embeddings + remote LLM). To use a custom config:
```bash
docker run -d -p 7860:7860 -v /path/to/config.ini:/app/config.ini hoomzoom/huixiangdou \
  python -m huixiangdou.gradio_ui --config_path config.ini
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (via config.ini) remote_api_key | Yes | None | LLM API key (OpenAI, Kimi, DeepSeek, SiliconCloud, etc.) |
| (via config.ini) remote_type | Yes | siliconcloud | LLM provider type |
| (via config.ini) serper_x_api_key | No | None | Serper web search API key |

## Building Feature Store
Before the app can answer questions about your documents, build a feature store:
```bash
docker run -it -v /path/to/docs:/app/repodir hoomzoom/huixiangdou \
  python -m huixiangdou.services.store --config_path config-cpu.ini
```

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Docker build | PASS |
| 2 | Gradio WebUI GET / | PASS (200, 17KB) |
| 3 | Gradio /info endpoint | PASS (200) |
| 4 | Gradio /config endpoint | PASS (200, 11KB) |
| 5 | Package import (huixiangdou) | PASS |
| 6 | Pipeline imports (Serial + Parallel) | PASS |
| 7 | FeatureStore import | PASS |

7/7 tests passed.

## Notes
- LLM API key required for actual inference. Without it, the UI loads but queries fail.
- `config-cpu.ini` uses SiliconCloud API for embeddings/reranking (no local models needed).
- Default `config.ini` uses local embedding models (requires download on first run).
- Feature store must be built before the app can answer questions about specific documents.
- The pre-built image from the original developers (`tpoisonooo/huixiangdou:20240814`) is broken. This custom build fixes all issues.
- Web search requires either DuckDuckGo (free, default) or Serper (needs API key).
