# DeepGit. Usage Documentation

## Overview
Gradio web application for deep GitHub repository search using LLM agents. Given a natural language query, the app uses a multi-step agent pipeline to search, rank, and summarize relevant repositories. Uses Groq as the inference backend and the GitHub API for repository data.

## Quick Start
```bash
docker pull hoomzoom/deepgit
docker run -d -p 7860:7860 \
  -e GITHUB_API_KEY=<your_github_token> \
  -e GROQ_API_KEY=<your_groq_key> \
  hoomzoom/deepgit
```

Open http://localhost:7860 in your browser.

## Base URL
http://localhost:7860

## Core Features
- Natural language GitHub repository search powered by LLM agents
- Multi-step retrieval pipeline that goes beyond simple keyword matching
- Semantic re-ranking using sentence-transformers embeddings
- Summarisation of search results with source repository links

## Endpoints

### Main UI
- **URL:** http://localhost:7860
- **Description:** Gradio interface where you enter a search query and receive ranked, summarised repository results.
- **Tested:** Yes (page loads, search requires valid API keys)

## Health Check
- **URL:** `/gradio_api/info`
- **Method:** GET
- **Response:** JSON with Gradio app metadata
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GITHUB_API_KEY | Yes | None | GitHub personal access token for repository search API |
| GROQ_API_KEY | Yes | None | Groq API key for LLM inference |
| GRADIO_SERVER_NAME | Set in image | 0.0.0.0 | Bind address for the Gradio server |

## Notes
- Both GITHUB_API_KEY and GROQ_API_KEY are required. The search pipeline will not function without them.
- Sentence-transformers models are downloaded from Hugging Face on first startup. Expect a delay of 30 to 60 seconds on the initial run while models download.
- Subsequent startups use the cached models and are faster.
- The container runs as non-root user `appuser` (UID 1000).
- No persistent storage is required, but model downloads are lost when the container is removed. Use a volume mount at `/home/appuser/.cache` to persist the model cache across restarts.
- GRADIO_SERVER_NAME is set to `0.0.0.0` in the image. This is required because Gradio defaults to binding on `127.0.0.1`, which makes the port unreachable from outside the container.

## Changes from Original
- Added `ENV GRADIO_SERVER_NAME=0.0.0.0` to the Dockerfile. The upstream app does not set this, so Gradio binds to 127.0.0.1 and the container port is not reachable from the host.
- Build context is the repo root (not the app subdirectory) because the Dockerfile copies pinned requirements from `dockerfiles/DeepGit/requirements.txt` before copying the app source from `apps/DeepGit/`.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). Pinned requirements are in `dockerfiles/DeepGit/requirements.txt`. See `v2_pinned_versions.md` for the full change log.
