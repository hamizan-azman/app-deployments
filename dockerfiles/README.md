# Dockerfiles and Compose Files

This directory contains all Dockerfiles, docker-compose files, and config templates needed to rebuild or run each deployed app. All pre-built images are on Docker Hub under `hoomzoom/`.

## Directory Structure

Each app has its own subdirectory containing:
- `Dockerfile` -- the Dockerfile used to build the image
- `docker-compose.yml` -- for multi-container apps (already configured to pull from `hoomzoom/`)
- `.env.example` -- environment variable template (where applicable)
- `config*.ini` -- config files (where applicable)
- `README.md` -- notes for apps without a custom Dockerfile

## Multi-Container Apps

These apps need `docker compose up -d` (not just `docker run`). Copy the compose file to a working directory, create the `.env` file, and run:

| App | Services | Compose File |
|-----|----------|-------------|
| AgentGPT | frontend + platform + MySQL | `AgentGPT/docker-compose.yml` |
| agenticSeek | backend + frontend + SearxNG + Redis | `agenticSeek/docker-compose.yml` |
| BettaFish | app + PostgreSQL | `BettaFish/docker-compose.yml` |
| localGPT | frontend + backend + rag-api + Ollama | `localGPT/docker-compose.yml` |
| pdfGPT | langchain-serve + pdf-gpt | `pdfGPT/docker-compose.yaml` |
| gpt_academic | single service (multiple scheme variants) | `gpt_academic/docker-compose.yml` |

## Single-Container Apps

These just need `docker pull hoomzoom/xxx` and `docker run`. See each app's usage doc in `docs/` for the exact run command.

## Source Code Changes

Some apps required source code modifications to work in Docker. These changes are baked into the Docker Hub images. The reasoning docs (`docs/*_reasoning.md`) document every change made. Key apps with source modifications:

- **HuixiangDou** -- patched gradio_ui.py (debug=False, health check fix) and gradio_client/utils.py (pydantic v2 compat)
- **pdfGPT** -- era-matched dependency pins for abandoned langchain-serve
- **gpt_academic** -- uses pre-built image, no source changes
- **agenticSeek** -- config.ini changes for OpenAI provider

If you need to understand exactly what differs from the original repo, read the corresponding reasoning doc.
