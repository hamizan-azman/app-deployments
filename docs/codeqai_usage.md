# codeqai -- Usage Documentation

## Overview
CLI + Streamlit app for semantic code search and GPT-powered chat over codebases. Indexes git repos into FAISS vector stores using embeddings (OpenAI or local sentence-transformers), then enables similarity search and conversational Q&A. Also exports finetuning datasets from code.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/codeqai

# Or build from source
docker build -t codeqai apps/codeqai/

docker run -p 8501:8501 -e OPENAI_API_KEY=your-key hoomzoom/codeqai
```

First run indexes the bundled sample project (~10s). Then Streamlit launches on port 8501.

## Base URL
http://localhost:8501

## Core Features
- Semantic search across codebase methods and functions
- GPT-powered chat (ask questions about the code)
- Vector store sync with latest git changes
- Finetuning dataset export (Alpaca, conversational, instruction formats)
- Supports 11 languages: Python, JS, TS, Java, Rust, Go, C, C++, C#, Kotlin, Ruby

## Streamlit UI

### Search Mode
- Select "Search" in sidebar
- Enter a query (e.g. "how are embeddings created")
- Returns matching code snippets with file paths and method names

### Chat Mode
- Select "Chat" in sidebar
- Ask questions about the codebase in natural language
- Uses OpenAI GPT for responses with retrieval-augmented generation
- Clear Chat button resets conversation history

### Sync
- Click "Sync with current git checkout" in sidebar
- Updates vector store to match latest code changes

## CLI Commands (inside container)

### Semantic Search
```bash
docker exec -it codeqai codeqai search
```
Interactive CLI search. Requires TTY (`-it` flag).

### Chat
```bash
docker exec -it codeqai codeqai chat
```
Interactive CLI chat. Requires TTY.

### Sync Vector Store
```bash
docker exec codeqai codeqai sync
```

### Export Dataset
```bash
docker exec codeqai codeqai dataset --format conversational
docker exec codeqai codeqai dataset --format alpaca
docker exec codeqai codeqai dataset --distillation doc
```

### Reconfigure
```bash
docker exec -it codeqai codeqai configure
```
Interactive config wizard. Requires TTY.

## Streamlit Endpoints

### Main UI
- **URL:** `/`
- **Method:** GET
- **Tested:** Yes -- 200 OK, Streamlit app renders

### Health Check
- **URL:** `/_stcore/health`
- **Method:** GET
- **Response:** `ok`
- **Tested:** Yes -- 200 OK

### Host Config
- **URL:** `/_stcore/host-config`
- **Method:** GET
- **Response:** JSON with allowed origins and settings
- **Tested:** Yes -- 200 OK

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for embeddings and chat |
| ANTHROPIC_API_KEY | No | None | Required if using Anthropic chat models |
| OPENAI_API_TYPE | No | None | Set to "azure" for Azure OpenAI |
| AZURE_OPENAI_ENDPOINT | No | None | Azure OpenAI endpoint URL |
| OPENAI_API_VERSION | No | None | Azure OpenAI API version |

## Notes
- Config pre-set for OpenAI embeddings (text-embedding-ada-002) + OpenAI chat (gpt-4o-mini).
- To change models, edit `/root/.config/codeqai/config.yaml` inside the container.
- The bundled sample project is codeqai's own source code (32 Python files).
- To index a different repo: mount it as a volume at `/app/sample-project` (must be a git repo).
- FAISS index stored at `/root/.cache/codeqai/`. Delete to re-index.
- Image is large (~5GB) due to torch + sentence-transformers pulled by langchain-huggingface.
- Python >=3.9,<3.12 required. Image uses 3.11.
