# SlideDeck AI. Usage Documentation

## Overview
SlideDeck AI is a Streamlit app and CLI that generates PowerPoint slide decks from a topic using LLMs, and optionally enriches slides with images.

## Quick Start
```
# Pull from Docker Hub (recommended)
docker pull hoomzoom/slidedeckai

# Or build from source
docker build -t slidedeckai .

docker run --rm -p 8501:8501 \
  -e OPENAI_API_KEY=your-api-key \
  -e PEXEL_API_KEY=your-pexels-key \
  hoomzoom/slidedeckai
```

## Base URL
http://localhost:8501

## Core Features
- Generate PPTX slide decks from a topic
- Streamlit UI for interactive generation
- Optional image search via Pexels

## API Endpoints

### Streamlit UI
- **Command:** `streamlit run app.py`
- **Method:** UI
- **Description:** Launches the web interface.
- **Request:** `streamlit run app.py --server.port 8501 --server.address 0.0.0.0`
- **Response:** Streamlit web app.
- **Tested:** Yes (UI loads)

### List Supported Models
- **Command:** `slidedeckai --list-models`
- **Method:** CLI
- **Description:** Prints supported model keys grouped by provider.
- **Request:** `slidedeckai --list-models`
- **Response:** List of supported models.
- **Tested:** Yes

### Generate Slide Deck
- **Command:** `slidedeckai generate --model <model> --topic <topic>`
- **Method:** CLI
- **Description:** Generates a PPTX deck from a topic.
- **Request:** `slidedeckai generate --model '[oa]gpt-4.1-mini' --topic 'Make a slide deck on AI' --api-key 'your-openai-key'`
- **Response:** Path to generated PPTX.
- **Tested:** Yes (LLM call succeeds, PPTX generation fails due to Git LFS template issue)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | No | None | OpenAI key for `[oa]` models. |
| `AZURE_OPENAI_API_KEY` | No | None | Azure OpenAI key for `[az]` models. |
| `GOOGLE_API_KEY` | No | None | Google Gemini key for `[gg]` models. |
| `ANTHROPIC_API_KEY` | No | None | Anthropic key for `[an]` models. |
| `COHERE_API_KEY` | No | None | Cohere key for `[co]` models. |
| `OPENROUTER_API_KEY` | No | None | OpenRouter key for `[or]` models. |
| `SAMBANOVA_API_KEY` | No | None | SambaNova key for `[sn]` models. |
| `TOGETHER_API_KEY` | No | None | Together AI key for `[to]` models. |
| `PEXEL_API_KEY` | No | None | Pexels key for image search. |
| `RUN_IN_OFFLINE_MODE` | No | False | Use Ollama offline mode when `True`. |

## Notes
- The `slidedeckai launch` command is disabled in the current CLI. Use `streamlit run app.py` for the UI.
- This repo uses Git LFS for PPTX templates. Run `git lfs pull` before building if templates are LFS pointers.
- `slidedeckai --list-models` triggers a Hugging Face model load on first run.

## Changes from Original
None. Dockerfile written from scratch but source code and dependencies are untouched.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed - all minimum versions resolved successfully.
