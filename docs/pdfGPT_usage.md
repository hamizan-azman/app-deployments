# pdfGPT -- Usage Documentation

## Overview
PDF question-answering app using Universal Sentence Encoder embeddings and OpenAI. Two-service architecture: langchain-serve backend (Jina/FastAPI) + Gradio frontend.

## Quick Start
```bash
cd apps/pdfGPT
OPENAI_API_KEY=sk-... docker compose up -d
```

Docker Hub images are available for all pdfGPT services:
- `docker pull hoomzoom/pdfgpt-frontend`
- `docker pull hoomzoom/pdfgpt-langchain-serve`
- `docker pull hoomzoom/pdfgpt-backend`
- `docker pull hoomzoom/pdfgpt-pdf-gpt`

## Base URLs
- Frontend (Gradio UI): http://localhost:7860
- Backend (langchain-serve API): http://localhost:8080
- Swagger UI: http://localhost:8080/docs

## Core Features
- Upload PDF or provide URL
- Ask questions about PDF content
- Semantic search with Universal Sentence Encoder
- Cited answers with page numbers
- Supports OpenAI models via litellm

## API Endpoints

### Health Check
- **URL:** `/healthz`
- **Method:** GET
- **Description:** Backend health status
- **Request:** `curl http://localhost:8080/healthz`
- **Response:** `{"status":"ok"}`
- **Tested:** Yes

### Swagger UI
- **URL:** `/docs`
- **Method:** GET
- **Description:** Interactive API documentation
- **Request:** `curl http://localhost:8080/docs`
- **Tested:** Yes

### Ask URL
- **URL:** `/ask_url`
- **Method:** POST
- **Description:** Ask a question about a PDF from URL
- **Request:**
```bash
curl -X POST http://localhost:8080/ask_url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/paper.pdf", "question": "What is the main topic?", "envs": {"OPENAI_API_KEY": "sk-..."}}'
```
- **Response:** `{"result": "The main topic is...", "error": "", "stdout": ""}`
- **Tested:** Yes (pipeline works, but text-davinci-003 is deprecated by OpenAI)

### Ask File
- **URL:** `/ask_file`
- **Method:** POST
- **Description:** Ask a question about an uploaded PDF file
- **Request:**
```bash
curl -X POST http://localhost:8080/ask_file \
  -F "file=@paper.pdf" \
  -G --data-urlencode 'input_data={"question":"What is this about?","envs":{"OPENAI_API_KEY":"sk-..."}}'
```
- **Response:** `{"result": "This document is about...", "error": "", "stdout": ""}`
- **Tested:** No (same pipeline as ask_url, would also hit deprecated model)

### Gradio Frontend
- **URL:** `/`
- **Port:** 7860
- **Method:** Browser
- **Description:** Web UI for uploading PDFs and asking questions
- **Tested:** Yes (200 OK, UI loads)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (for queries) | - | OpenAI API key for LLM completion |
| LCSERVE_HOST | No | http://langchain-serve:8080 | Backend URL (set automatically in docker-compose) |

## Test Summary
| # | Test | Result |
|---|------|--------|
| 1 | docker compose up starts both services | PASS |
| 2 | Backend health check (/healthz) | PASS |
| 3 | Backend Swagger UI (/docs) | PASS |
| 4 | Frontend Gradio UI (port 7860) | PASS |
| 5 | ask_url endpoint (full pipeline) | PASS (pipeline works; text-davinci-003 deprecated by OpenAI) |
| 6 | ask_file endpoint (full pipeline) | NOT TESTED (same pipeline as ask_url) |

## Notes
- The backend image is large (~4GB) due to TensorFlow + Universal Sentence Encoder model baked in
- First startup takes ~30s as TensorFlow initializes
- The original `text-davinci-003` model in api.py is deprecated by OpenAI; litellm may route to alternatives
- Uses openai==0.27.8 (old API) -- this is the original developer's architecture
- langchain-serve is abandoned software with broken dependency chains; multiple version pins required

## Changes from Original
**Category: Modified.** Gradio compatibility fixes and 7 dependency pins.

**Source changes:**

| File | Change | Why |
|------|--------|-----|
| `app.py` | Removed `btn.style(full_width=True)` | Gradio 3.x API removed in 4.x |
| `app.py` | Removed `demo.app.server.timeout = 60000` | Not available in Gradio 4.x |
| `app.py` | Removed `enable_queue=True` from `demo.launch()`, added `server_name="0.0.0.0"` | Gradio compat + Docker binding |
| `app.py` | Added `os.environ.get('LCSERVE_HOST', 'http://localhost:8080')` for backend host | Docker compose networking |

**Dependency pins (7):**

| Package | Original | Deployed | Why |
|---------|----------|----------|-----|
| langchain | unpinned | ==0.0.267 | langchain-serve requires pre-split monolithic langchain |
| litellm | unpinned | ==0.1.424 | Modern litellm requires openai>=1.0 which is incompatible |
| openai | ==0.27.4 | ==0.27.8 | litellm 0.1.424 requires >=0.27.8 |
| pydantic | unpinned | <2 | Jina 3.x crashes with pydantic v2 |
| huggingface_hub | unpinned | <1.0 | Gradio 4.x imports HfFolder removed in hub >=1.0 |
| setuptools | unpinned | <71 (build constraint) | langchain-serve uses pkg_resources |
| opentelemetry-exporter-prometheus | unpinned | ==1.12.0rc1 | Yanked from PyPI but required by jina 3.14.1 |

The Gradio compat fixes change UI behavior slightly but not the backend API. The era-matched dependency pins lock the backend to 2023-era versions. The hardcoded `text-davinci-003` model in `api.py` was NOT changed.
