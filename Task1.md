# Task 1: Application Dockerization and Deployment

## Summary

Assigned 31 of the 49 applications from the team applist. Each app was cloned, analyzed, containerized (Dockerfile written or pre-built image used), tested, and documented. Custom-built images are published to Docker Hub under `hoomzoom/`.

**Results:** 31 deployed, 5 skipped (incompatible with Docker), 11 remaining.

---

## How to Use This

Each deployed app has a **usage doc** (`docs/<appname>_usage.md`) in the repo with:
- Exact `docker build` / `docker run` / `docker compose` commands
- All API endpoints or CLI commands
- curl/test examples
- Environment variables and configuration
- Test results (pass/fail per endpoint)
- **Changes from original** -- what was modified from the developer's source code (if anything)

There is also a **reasoning doc** (`docs/<appname>_reasoning.md`) explaining why each deployment decision was made, what broke, and how it was fixed.

> **To access the docs:** They are all in the `docs/` folder of the [app-deployments repo](https://github.com/hamizan-azman/app-deployments). You can also find them attached below if I've uploaded them to this Lark doc.

---

## Deployed Apps (31)

### Web UI Apps

| # | App | What It Does | Interface | Docker Image | Needs API Key | Tests | Docs |
|---|-----|-------------|-----------|-------------|---------------|-------|------|
| 1 | [pycorrector](https://github.com/shibing624/pycorrector) | Chinese text error correction (MacBERT) | Gradio | `hoomzoom/pycorrector` | No | 6/6 | [usage](docs/pycorrector_usage.md) |
| 2 | [FunClip](https://github.com/modelscope/FunClip) | Video/audio clipping with ASR + speaker diarization | Gradio | `hoomzoom/funclip` | No | 4/4 | [usage](docs/FunClip_usage.md) |
| 3 | [omniparse](https://github.com/adithya-s-k/omniparse) | Parses PDFs, images, web pages into structured markdown | Gradio + FastAPI | `hoomzoom/omniparse` | No | 5/5 | [usage](docs/omniparse_usage.md) |
| 4 | [manga-image-translator](https://github.com/zyddnys/manga-image-translator) | Translates text in manga/comic images | Web UI + REST API | `hoomzoom/manga-image-translator` | No | 5/5 | [usage](docs/manga-image-translator_usage.md) |
| 5 | [pdfGPT](https://github.com/bhaskatripathi/pdfGPT) | PDF question-answering with embeddings + LLM | Gradio + langchain-serve | `hoomzoom/pdfgpt-*` (4 images) | Yes (OpenAI) | 5/5 | [usage](docs/pdfGPT_usage.md) |
| 6 | [gpt_academic](https://github.com/binary-husky/gpt_academic) | Academic writing assistant, code interpreter, Latex | Gradio | `hoomzoom/gpt_academic` | Yes (OpenAI) | 7/7 | [usage](docs/gpt_academic_usage.md) |
| 7 | [NarratoAI](https://github.com/linyqh/NarratoAI) | Automated video narration (script + TTS + subtitles) | Streamlit | `hoomzoom/narratoai` | Yes (LLM provider) | 5/5 | [usage](docs/NarratoAI_usage.md) |
| 8 | [codeqai](https://github.com/fynnfluegge/codeqai) | Semantic code search + GPT chat over codebases | Streamlit + CLI | `hoomzoom/codeqai` | Yes (OpenAI) | 5/5 | [usage](docs/codeqai_usage.md) |
| 9 | [slide-deck-ai](https://github.com/barun-saha/slide-deck-ai) | Generates PowerPoint decks from a topic | Streamlit | `hoomzoom/slidedeckai` | Yes (OpenAI) | 3/3 | [usage](docs/slide-deck-ai_usage.md) |
| 10 | [BettaFish](https://github.com/666ghj/BettaFish) | Multi-agent opinion/sentiment analysis | Flask + Streamlit | `hoomzoom/bettafish` | Yes (API keys) | 4/5 \* | [usage](docs/BettaFish_usage.md) |
| 11 | [localGPT](https://github.com/PromtEngineer/localGPT) | Local RAG system with document indexing and chat | Next.js + Python + Ollama | `hoomzoom/localgpt-*` (3 images) | No (local Ollama) | 10/10 | [usage](docs/localGPT_usage.md) |
| 12 | [agenticSeek](https://github.com/Fosowl/agenticSeek) | Multi-agent assistant (chat, code, files, web browsing) | React + Python + Redis | `hoomzoom/agenticseek-*` (2 images) | Yes (OpenAI) | 8/8 | [usage](docs/agenticSeek_usage.md) |
| 13 | [zshot](https://github.com/IBM/zshot) | Zero-shot named entity recognition (IBM spaCy + T5) | FastAPI | `hoomzoom/zshot` | No | 4/4 | [usage](docs/zshot_usage.md) |
| 14 | [AgentGPT](https://github.com/reworkd/AgentGPT) | Autonomous AI agent platform (goal decomposition + task execution) | Next.js + FastAPI + MySQL | `hoomzoom/agentgpt-*` (2 images) | Yes (OpenAI) | 9/9 | [usage](docs/AgentGPT_usage.md) |
| 15 | [DataFlow](https://github.com/OpenDCAI/DataFlow) | Data preparation and training system for LLMs (100+ operators) | Gradio | `hoomzoom/dataflow` | No | 6/6 | [usage](docs/DataFlow_usage.md) |
| 16 | [HuixiangDou](https://github.com/InternLM/HuixiangDou) | Knowledge assistant with RAG pipeline for document Q&A | Gradio + FastAPI | `hoomzoom/huixiangdou` | Yes (LLM provider) | 7/7 | [usage](docs/HuixiangDou_usage.md) |
| 17 | [attackgen](https://github.com/mrwadams/attackgen) | Incident response scenario generator using MITRE ATT&CK | Streamlit | `hoomzoom/attackgen` | Yes (via UI) | 5/5 | [usage](docs/attackgen_usage.md) |
| 18 | [stride-gpt](https://github.com/mrwadams/stride-gpt) | AI-powered STRIDE threat modeling | Streamlit | `hoomzoom/stride-gpt` | Yes (via UI) | 2/2 | [usage](docs/stride-gpt_usage.md) |
| 19 | [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Autonomous web research agent with report generation | FastAPI + Web UI | `hoomzoom/gpt-researcher` | Yes (OpenAI + Tavily) | 4/4 | [usage](docs/gpt-researcher_usage.md) |
| 20 | [gptme](https://github.com/ErikBjare/gptme) | AI coding assistant with shell/file execution | Flask + Web UI | `hoomzoom/gptme-server` | Yes (OpenAI) | 2/2 | [usage](docs/gptme_usage.md) |
| 21 | [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | Iterative web research using local LLMs via Ollama | LangGraph API | `hoomzoom/local-deep-researcher` | No (local Ollama) | 4/4 | [usage](docs/local-deep-researcher_usage.md) |

### CLI Apps

| # | App | What It Does | Docker Image | Needs API Key | Tests | Docs |
|---|-----|-------------|-------------|---------------|-------|------|
| 22 | [ChatDBG](https://github.com/plasma-umass/ChatDBG) | LLM-powered debugger (pdb, lldb, gdb) | `hoomzoom/chatdbg` | Yes (OpenAI) | 7/7 | [usage](docs/ChatDBG_usage.md) |
| 23 | [RD-Agent](https://github.com/microsoft/RD-Agent) | Autonomous R&D for quant trading, Kaggle, ML papers | `hoomzoom/rd-agent` | Yes (OpenAI) | 5/5 | [usage](docs/RD-Agent_usage.md) |
| 24 | [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) | Converts academic papers to posters (PPTX) | `hoomzoom/paper2poster` | Yes (OpenAI) | 5/5 | [usage](docs/Paper2Poster_usage.md) |
| 25 | [rawdog](https://github.com/AbanteAI/rawdog) | CLI assistant that generates and runs Python scripts | `hoomzoom/rawdog` | Yes (OpenAI) | 3/3 | [usage](docs/rawdog_usage.md) |
| 26 | [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Translates EPUB/TXT/SRT into bilingual books | `hoomzoom/bilingual_book_maker` | Yes (OpenAI) | 3/3 | [usage](docs/bilingual_book_maker_usage.md) |
| 27 | [gpt-engineer](https://github.com/AntonOsika/gpt-engineer) | Generates/improves code projects from natural language | `hoomzoom/gpt-engineer` | Yes (OpenAI) | 11/11 | [usage](docs/gpt-engineer_usage.md) |
| 28 | [gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Migrates codebases between languages using LLMs | `hoomzoom/gpt-migrate` | Yes (OpenAI) | 5/6 \* | [usage](docs/gpt-migrate_usage.md) |
| 29 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Autonomous agent that fixes GitHub issues | `hoomzoom/swe-agent` | Yes (OpenAI) | 10/10 | [usage](docs/SWE-agent_usage.md) |

\* **BettaFish 4/5:** The analysis engine endpoints require provider-specific API keys (not just OpenAI) that were unavailable during testing. Infrastructure and all other endpoints work.
\* **gpt-migrate 5/6:** The interactive chat mode requires gpt-4-32k, which OpenAI has deprecated. All other modes (migrate, create, test) work.

### Libraries (no web interface)

| # | App | What It Does | Docker Image | Needs API Key | Docs |
|---|-----|-------------|-------------|---------------|------|
| 30 | [codeinterpreter-api](https://github.com/shroominic/codeinterpreter-api) | ChatGPT Code Interpreter via LangChain + CodeBox | `hoomzoom/codeinterpreter-api` | Yes (OpenAI) | [usage](docs/codeinterpreter-api_usage.md) |
| 31 | [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) | LLM agent for chemistry tasks (RDKit, PubChem) | `hoomzoom/chemcrow` | Yes (OpenAI) | [usage](docs/chemcrow-public_usage.md) |

---

## Skipped Apps (5)

These cannot run meaningfully in Docker:

| App | Reason |
|-----|--------|
| [autoMate](https://github.com/yuruotong1/autoMate) | Desktop RPA tool -- requires GUI, mouse/keyboard control. Useless headless. |
| [whispering](https://github.com/Sharrnah/whispering) | Requires microphone/audio device access. |
| [TaskMatrix](https://github.com/chenfei-wu/TaskMatrix) | Requires heavy GPU (Visual ChatGPT with multiple vision models). |
| [MedRAX](https://github.com/bowang-lab/MedRAX) | Needs GPU + multiple large medical imaging models. No existing Dockerfile. |
| [home-llm](https://github.com/acon96/home-llm) | Home Assistant integration -- not a standalone application. |

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
docker pull hoomzoom/dataflow
docker pull hoomzoom/huixiangdou
docker pull hoomzoom/attackgen
docker pull hoomzoom/stride-gpt
docker pull hoomzoom/gpt-researcher
docker pull hoomzoom/gptme-server
docker pull hoomzoom/local-deep-researcher
docker pull ollama/ollama
```

---

## Notes for the Team

- **API keys:** About half the apps need an OpenAI API key (or similar) for full functionality. Without a key, the infrastructure still runs -- you just can't make LLM calls. Each usage doc specifies which env vars to set.
- **Multi-container apps:** pdfGPT (4 containers), agenticSeek (4 containers), localGPT (4 containers), AgentGPT (3 containers), and BettaFish (2 containers) use docker-compose. The usage docs have the exact compose commands.
- **Port conflicts:** Each app's usage doc specifies which port it runs on. If running multiple apps at once, check for port collisions.
- **GPU required:** DataFlow requires an NVIDIA GPU with CUDA 12.4+ and the NVIDIA Container Toolkit. Run with `--gpus all`. Works on GTX 1650 (4GB VRAM) for WebUI and data processing operators.
- **Code execution by design:** 6 apps execute arbitrary code as their core function: rawdog, gpt-engineer, SWE-agent, codeinterpreter-api, gpt-migrate, gptme. These are high-value targets for code injection research. Do not run them with access to sensitive data or networks.
- **Docker socket (SWE-agent):** SWE-agent requires `-v /var/run/docker.sock:/var/run/docker.sock`, giving the container full control over the host's Docker daemon. Run it on an isolated machine or VM only.
- **Model downloads:** FunClip, omniparse, manga-image-translator, zshot, and pycorrector download ML models on first startup (1-5 GB depending on the app). First launch takes 5-30 minutes depending on connection speed. The container will appear to hang during download -- check logs with `docker logs -f <container>` to monitor progress. Subsequent launches are fast if you don't delete the container.
- **Deprecated/abandoned dependencies:** pdfGPT depends on abandoned software (langchain-serve, jina 3.x, openai 0.27.x) pinned to 2023-era versions. AgentGPT's langchain (0.0.335) does not match the developer's lockfile (0.0.295). These version mismatches are worth investigating from a supply chain perspective. See each app's usage doc for details.
- **Testing coverage:** All apps were tested with API keys where applicable. pdfGPT's LLM-dependent endpoints require additional testing with a valid key. The reasoning docs explain what was and wasn't tested for each app.

---

## Building from Source

All Docker Hub images can be rebuilt from the Dockerfiles in `dockerfiles/`. The workflow is the same for every app:

```bash
# 1. Clone the original repo
git clone https://github.com/<org>/<repo>.git

# 2. Copy the Dockerfile (and any config files) into the cloned repo
cp dockerfiles/<app>/Dockerfile <repo>/
cp dockerfiles/<app>/.env.example <repo>/   # if it exists

# 3. Build
cd <repo>
docker build -t <app> .
```

For multi-container apps (pdfGPT, agenticSeek, localGPT, AgentGPT, BettaFish, gpt_academic), the compose files in `dockerfiles/<app>/` are pre-configured to pull from Docker Hub. To build from source instead, edit the compose file to replace `image:` with `build:` and point to the cloned repo.

---

## Repo Structure

```
app-deployments/
  dockerfiles/       # Dockerfiles, docker-compose files, and config templates for all 31 apps
  docs/              # Usage docs (*_usage.md) and reasoning docs (*_reasoning.md)
  tracker.md         # Status tracker with test counts
```

Note: The `apps/` directory (cloned source repos) is local working data and not included in this repository. Source code lives at the original GitHub URLs linked in the tables above.

### dockerfiles/

Each app has a subdirectory in `dockerfiles/` containing everything needed to rebuild or run:
- **Dockerfiles** for all 29 custom-built apps
- **docker-compose.yml** for 6 multi-container apps (AgentGPT, agenticSeek, BettaFish, gpt_academic, localGPT, pdfGPT) -- pre-configured to pull from `hoomzoom/` Docker Hub, no build required
- **.env.example** templates and **config files** where needed

To run a multi-container app, copy its compose file, create the `.env`, and run `docker compose up -d`. See the app's usage doc for details.
