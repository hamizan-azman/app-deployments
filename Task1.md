# Task 1: Application Dockerization and Deployment

## Summary

Deployed 31 LLM-powered GitHub applications into Docker containers for supply chain security analysis. Each app was cloned, analyzed, containerized (Dockerfile written or pre-built image used), tested, and documented. Custom-built images are published to Docker Hub under `hoomzoom/`.

**Results:** 25 deployed, 5 skipped (incompatible with Docker), 1 pull-only (base env only).

---

## How to Use This

Each deployed app has a **usage doc** (`docs/<appname>_usage.md`) in the repo with:
- Exact `docker build` / `docker run` / `docker compose` commands
- All API endpoints or CLI commands
- curl/test examples
- Environment variables and configuration
- Test results (pass/fail per endpoint)

There is also a **reasoning doc** (`docs/<appname>_reasoning.md`) explaining why each deployment decision was made, what broke, and how it was fixed.

> **To access the docs:** They are all in the `docs/` folder of the [app-deployments repo](https://github.com/hamizan-azman/app-deployments). You can also find them attached below if I've uploaded them to this Lark doc.

---

## Deployed Apps (23)

### Web UI Apps

| # | App | What It Does | Interface | Docker Image | Needs API Key | Tests | Docs |
|---|-----|-------------|-----------|-------------|---------------|-------|------|
| 1 | pycorrector | Chinese text error correction (MacBERT) | Gradio | `hoomzoom/pycorrector` | No | 6/6 | [usage](docs/pycorrector_usage.md) |
| 2 | FunClip | Video/audio clipping with ASR + speaker diarization | Gradio | `hoomzoom/funclip` | No | 4/4 | [usage](docs/FunClip_usage.md) |
| 3 | omniparse | Parses PDFs, images, web pages into structured markdown | Gradio + FastAPI | `hoomzoom/omniparse` | No | 5/5 | [usage](docs/omniparse_usage.md) |
| 4 | manga-image-translator | Translates text in manga/comic images | Web UI + REST API | `hoomzoom/manga-image-translator` | No | 5/5 | [usage](docs/manga-image-translator_usage.md) |
| 5 | pdfGPT | PDF question-answering with embeddings + LLM | Gradio + langchain-serve | `hoomzoom/pdfgpt-*` (4 images) | Yes (OpenAI) | 4/4 infra | [usage](docs/pdfGPT_usage.md) |
| 6 | gpt_academic | Academic writing assistant, code interpreter, Latex | Gradio | `hoomzoom/gpt_academic` | Yes (OpenAI) | Infra only | [usage](docs/gpt_academic_usage.md) |
| 7 | NarratoAI | Automated video narration (script + TTS + subtitles) | Streamlit | `hoomzoom/narratoai` | Yes (LLM provider) | 5/5 | [usage](docs/NarratoAI_usage.md) |
| 8 | codeqai | Semantic code search + GPT chat over codebases | Streamlit + CLI | `hoomzoom/codeqai` | Yes (OpenAI) | 5/5 | [usage](docs/codeqai_usage.md) |
| 9 | slide-deck-ai | Generates PowerPoint decks from a topic | Streamlit | `hoomzoom/slidedeckai` | Yes (OpenAI) | Infra only | [usage](docs/slide-deck-ai_usage.md) |
| 10 | BettaFish | Multi-agent opinion/sentiment analysis | Flask + Streamlit | `hoomzoom/bettafish` | Yes (API keys) | 4/5 | [usage](docs/BettaFish_usage.md) |
| 11 | localGPT | Local RAG system with document indexing and chat | Next.js + Python + Ollama | `hoomzoom/localgpt-*` (3 images) | No (local Ollama) | 10/10 | [usage](docs/localGPT_usage.md) |
| 12 | agenticSeek | Multi-agent assistant (chat, code, files, web browsing) | React + Python + Redis | `hoomzoom/agenticseek-*` (2 images) | Yes (OpenAI) | 8/8 | [usage](docs/agenticSeek_usage.md) |
| 13 | zshot | Zero-shot named entity recognition (IBM spaCy + T5) | FastAPI | `hoomzoom/zshot` | No | 4/4 | [usage](docs/zshot_usage.md) |
| 14 | AgentGPT | Autonomous AI agent platform (goal decomposition + task execution) | Next.js + FastAPI + MySQL | `hoomzoom/agentgpt-*` (2 images) | Yes (OpenAI) | 9/9 | [usage](docs/AgentGPT_usage.md) |
| 15 | DataFlow | Data preparation and training system for LLMs (100+ operators) | Gradio | `molyheci/dataflow:cu124` | No | 6/6 | [usage](docs/DataFlow_usage.md) |

### CLI Apps

| # | App | What It Does | Docker Image | Needs API Key | Tests | Docs |
|---|-----|-------------|-------------|---------------|-------|------|
| 16 | ChatDBG | LLM-powered debugger (pdb, lldb, gdb) | `hoomzoom/chatdbg` | Yes (OpenAI) | 7/7 | [usage](docs/ChatDBG_usage.md) |
| 17 | RD-Agent | Autonomous R&D for quant trading, Kaggle, ML papers | `hoomzoom/rd-agent` | Yes (OpenAI) | 5/5 | [usage](docs/RD-Agent_usage.md) |
| 18 | Paper2Poster | Converts academic papers to posters (PPTX) | `hoomzoom/paper2poster` | Yes (OpenAI) | 5/5 | [usage](docs/Paper2Poster_usage.md) |
| 19 | rawdog | CLI assistant that generates and runs Python scripts | `hoomzoom/rawdog` | Yes (OpenAI) | Infra only | [usage](docs/rawdog_usage.md) |
| 20 | bilingual_book_maker | Translates EPUB/TXT/SRT into bilingual books | `hoomzoom/bilingual_book_maker` | Yes (OpenAI) | Infra only | [usage](docs/bilingual_book_maker_usage.md) |
| 21 | gpt-engineer | Generates/improves code projects from natural language | `hoomzoom/gpt-engineer` | Yes (OpenAI) | 11/11 | [usage](docs/gpt-engineer_usage.md) |
| 22 | gpt-migrate | Migrates codebases between languages using LLMs | `hoomzoom/gpt-migrate` | Yes (OpenAI) | 5/6 | [usage](docs/gpt-migrate_usage.md) |
| 23 | SWE-agent | Autonomous agent that fixes GitHub issues | `hoomzoom/swe-agent` | Yes (OpenAI) | 10/10 | [usage](docs/SWE-agent_usage.md) |

### Libraries (no web interface)

| # | App | What It Does | Docker Image | Needs API Key | Docs |
|---|-----|-------------|-------------|---------------|------|
| 24 | codeinterpreter-api | ChatGPT Code Interpreter via LangChain + CodeBox | `hoomzoom/codeinterpreter-api` | Yes (OpenAI) | [usage](docs/codeinterpreter-api_usage.md) |
| 25 | chemcrow-public | LLM agent for chemistry tasks (RDKit, PubChem) | `hoomzoom/chemcrow` | Yes (OpenAI) | [usage](docs/chemcrow-public_usage.md) |

---

## Skipped Apps (5)

These cannot run meaningfully in Docker:

| App | Reason |
|-----|--------|
| autoMate | Desktop RPA tool -- requires GUI, mouse/keyboard control. Useless headless. |
| whispering | Requires microphone/audio device access. |
| TaskMatrix | Requires heavy GPU (Visual ChatGPT with multiple vision models). |
| MedRAX | Needs GPU + multiple large medical imaging models. No existing Dockerfile. |
| home-llm | Home Assistant integration -- not a standalone application. |

---

## Pull-Only Apps (1)

Image exists on Docker Hub but is a base environment only, not a ready-to-run app:

| App | Image | Notes |
|-----|-------|-------|
| HuixiangDou | `tpoisonooo/huixiangdou:20240814` | Base conda/CUDA env only. Package not installed in image, faiss-gpu incompatible with Python 3.12 in image. |

---

## Docker Hub Registry

All custom-built images are on Docker Hub under **hoomzoom/**:

```
docker pull hoomzoom/rawdog
docker pull hoomzoom/bilingual_book_maker
docker pull hoomzoom/chemcrow
docker pull hoomzoom/codeinterpreter-api
docker pull hoomzoom/pdfgpt-frontend
docker pull hoomzoom/pdfgpt-langchain-serve
docker pull hoomzoom/pdfgpt-backend
docker pull hoomzoom/pdfgpt-pdf-gpt
docker pull hoomzoom/agenticseek-frontend
docker pull hoomzoom/agenticseek-backend
docker pull hoomzoom/rd-agent
docker pull hoomzoom/pycorrector
docker pull hoomzoom/funclip
docker pull hoomzoom/chatdbg
docker pull hoomzoom/zshot
docker pull hoomzoom/slidedeckai
docker pull hoomzoom/codeqai
docker pull hoomzoom/paper2poster
docker pull hoomzoom/gpt-migrate
docker pull hoomzoom/bettafish
docker pull hoomzoom/localgpt-frontend
docker pull hoomzoom/localgpt-backend
docker pull hoomzoom/localgpt-rag-api
docker pull hoomzoom/omniparse
docker pull hoomzoom/manga-image-translator
docker pull hoomzoom/gpt_academic
docker pull hoomzoom/bettafish
docker pull hoomzoom/swe-agent
docker pull hoomzoom/gpt-engineer
docker pull hoomzoom/narratoai
docker pull hoomzoom/agentgpt-platform
docker pull hoomzoom/agentgpt-frontend
docker pull ollama/ollama
```

---

## Notes for the Team

- **API keys:** About half the apps need an OpenAI API key (or similar) for full functionality. Without a key, the infrastructure still runs -- you just can't make LLM calls. Each usage doc specifies which env vars to set.
- **Multi-container apps:** pdfGPT (4 containers), agenticSeek (4 containers), localGPT (4 containers), AgentGPT (3 containers), and BettaFish (2 containers) use docker-compose. The usage docs have the exact compose commands.
- **Port conflicts:** Each app's usage doc specifies which port it runs on. If running multiple apps at once, check for port collisions.
- **GPU required:** DataFlow requires an NVIDIA GPU with CUDA 12.4+ and the NVIDIA Container Toolkit. Run with `--gpus all`. Works on GTX 1650 (4GB VRAM) for WebUI and data processing operators.
- **Model downloads:** Some apps (FunClip, omniparse, manga-image-translator, zshot, pycorrector) download ML models on first startup. First launch will be slow; subsequent launches are fast if you don't delete the container.
- **Testing coverage:** Apps that don't need API keys were fully tested end-to-end. Apps that need keys were tested for infrastructure (container starts, endpoints respond, UI loads) and marked accordingly. The reasoning docs explain what was and wasn't tested for each app.

---

## Repo Structure

```
app-deployments/
  apps/              # Cloned source repos (one per app)
  docs/              # Usage docs (*_usage.md) and reasoning docs (*_reasoning.md)
  tracker.md         # Status tracker with test counts
```
