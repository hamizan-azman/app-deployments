# HuixiangDou -- Usage Documentation

## Overview
Professional knowledge assistant based on LLM. Three-stage pipeline (preprocess, rejection, response) for group chat and real-time streaming chat with RAG capabilities. Supports CPU-only, 2GB GPU, and 10GB GPU configurations.

## Quick Start
```bash
docker pull tpoisonooo/huixiangdou:20240814
docker run -it -p 7860:7860 -p 23333:23333 tpoisonooo/huixiangdou:20240814
```

## Configuration
Requires LLM API configuration. Supports: kimi, deepseek, stepfun, siliconcloud, OpenAI-compatible APIs.

CPU-only mode (no local GPU needed):
```bash
docker run -it \
  -p 7860:7860 \
  -p 23333:23333 \
  -e LLM_API_KEY=your-key \
  tpoisonooo/huixiangdou:20240814
```

## Interfaces
- Web UI: http://localhost:7860 (Gradio)
- API: http://localhost:23333

## Features
- Group chat integration (WeChat, Feishu, Discord)
- Knowledge base creation from documents
- Hybrid retrieval (dense + sparse + knowledge graph)
- Image and text retrieval
- Real-time streaming chat
- Android app support

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| LLM_API_KEY | Yes | None | API key for LLM provider |

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Docker pull | NOT TESTED (large image, manual setup required) |
| 2 | Web UI | NOT TESTED |
| 3 | API | NOT TESTED |

## Notes
- Pre-built image maintained by original developers.
- Requires manual knowledge base setup after first run.
- CPU-only mode works but is slower.
- Web UI for creating knowledge bases, managing positive/negative examples, and testing chat.
- Full setup requires configuring LLM providers in config files inside the container.
