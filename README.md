# LLM Application Deployment Collection

Dockerized deployment of 41 open-source LLM applications for supply chain security research. Each app is containerized, tested, and documented with usage guides and reasoning logs.

## At a Glance

- **41 apps deployed** across web UIs, CLI tools, and libraries
- **8 apps skipped** (incompatible with Docker, local install docs provided)
- **48 Docker images** published to [Docker Hub](https://hub.docker.com/u/hoomzoom) under `hoomzoom/`
- **Every app tested** with documented pass/fail results per endpoint

## Quick Start

Pick any app and pull from Docker Hub:

```bash
docker pull hoomzoom/attackgen
docker run -p 8501:8501 hoomzoom/attackgen
```

For multi-container apps (devika, auto-news, localGPT, etc.), use the provided docker-compose files:

```bash
cp dockerfiles/devika/docker-compose.yml .
cp dockerfiles/devika/.env.example .env
docker compose up
```

Each app's usage doc has the exact commands.

---

## Repo Structure

```
app-deployments/
  apps/              # Git submodules pointing to original upstream repos (reference only)
  dockerfiles/       # Dockerfiles, compose files, config templates, AND pinned dependency files
  docs/              # Usage docs (*_usage.md) and reasoning docs (*_reasoning.md)
  tracker.md         # Status tracker with test counts
  v2_pinned_versions.md  # Manifest of all V2 dependency version changes
```

### Important: Where to find what

| What you're looking for | Where to look |
|------------------------|---------------|
| **Original upstream source code** | `apps/<name>/` (git submodules, points to upstream GitHub repos) |
| **Pinned dependency files used for builds** | `dockerfiles/<name>/` (requirements.txt, pyproject.toml, etc.) |
| **Dockerfiles and compose files** | `dockerfiles/<name>/` |
| **What was changed and why** | `docs/<name>_usage.md` → "V2 Dependency Changes" section |
| **Quick reference of all version bumps** | `v2_pinned_versions.md` |

> **Why the separation?** The `apps/` submodules contain the original developers' code with their original version specifiers. For V2 (supply chain security analysis), we pinned all `>=` versions to `==` minimums. Those pinned files live in `dockerfiles/` — this is what was actually used to build the Docker images on Docker Hub. See `v2_pinned_versions.md` for the full manifest.

---

## Deployed Apps

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
| 22 | [TaskWeaver](https://github.com/microsoft/TaskWeaver) | LLM-powered task planning and code execution agent | Chainlit | `hoomzoom/taskweaver` | Yes (OpenAI) | 4/4 | [usage](docs/TaskWeaver_usage.md) |
| 23 | [devika](https://github.com/stitionai/devika) | AI software engineer with planning, coding, and browser automation | Flask-SocketIO + Svelte | `hoomzoom/devika-backend`, `hoomzoom/devika-frontend` | Yes (via UI) | 16/16 | [usage](docs/devika_usage.md) |
| 24 | [django-ai-assistant](https://github.com/vintasoftware/django-ai-assistant) | Django framework for building AI assistants with tool calling | Django + React | `hoomzoom/django-ai-assistant` | Yes (OpenAI) | 5/5 | [usage](docs/django-ai-assistant_usage.md) |
| 25 | [magentic-ui](https://github.com/microsoft/magentic-one) | Multi-agent web automation with Docker-in-Docker sandbox | FastAPI + Web UI | `hoomzoom/magentic-ui` | Yes (OpenAI) | 2/2 | [usage](docs/magentic-ui_usage.md) |
| 26 | [Biomni](https://github.com/bowang-lab/Biomni) | Biomedical AI assistant with multi-modal capabilities | Gradio | `hoomzoom/biomni` | Yes (OpenAI) | 2/2 | [usage](docs/biomni_usage.md) |
| 27 | [Data-Copilot](https://github.com/zwq2018/Data-Copilot) | Chinese financial data analysis and visualization | Gradio | `hoomzoom/data-copilot` | Yes (OpenAI) | 2/2 | [usage](docs/data-copilot_usage.md) |
| 28 | [auto-news](https://github.com/finaldie/auto-news) | Automated news aggregation and summarization pipeline | Airflow (9-service compose) | `finaldie/auto-news:0.9.15` | Yes (OpenAI) | 6/6 | [usage](docs/auto-news_usage.md) |
| 29 | [pyvideotrans](https://github.com/jianchang512/pyvideotrans) | Video translation with speech recognition and TTS | CLI | `hoomzoom/pyvideotrans` | No | 2/2 | [usage](docs/pyvideotrans_usage.md) |

### CLI Apps

| # | App | What It Does | Docker Image | Needs API Key | Tests | Docs |
|---|-----|-------------|-------------|---------------|-------|------|
| 30 | [ChatDBG](https://github.com/plasma-umass/ChatDBG) | LLM-powered debugger (pdb, lldb, gdb) | `hoomzoom/chatdbg` | Yes (OpenAI) | 7/7 | [usage](docs/ChatDBG_usage.md) |
| 31 | [RD-Agent](https://github.com/microsoft/RD-Agent) | Autonomous R&D for quant trading, Kaggle, ML papers | `hoomzoom/rd-agent` | Yes (OpenAI) | 5/5 | [usage](docs/RD-Agent_usage.md) |
| 32 | [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) | Converts academic papers to posters (PPTX) | `hoomzoom/paper2poster` | Yes (OpenAI) | 5/5 | [usage](docs/Paper2Poster_usage.md) |
| 33 | [rawdog](https://github.com/AbanteAI/rawdog) | CLI assistant that generates and runs Python scripts | `hoomzoom/rawdog` | Yes (OpenAI) | 3/3 | [usage](docs/rawdog_usage.md) |
| 34 | [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Translates EPUB/TXT/SRT into bilingual books | `hoomzoom/bilingual_book_maker` | Yes (OpenAI) | 3/3 | [usage](docs/bilingual_book_maker_usage.md) |
| 35 | [gpt-engineer](https://github.com/AntonOsika/gpt-engineer) | Generates/improves code projects from natural language | `hoomzoom/gpt-engineer` | Yes (OpenAI) | 11/11 | [usage](docs/gpt-engineer_usage.md) |
| 36 | [gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Migrates codebases between languages using LLMs | `hoomzoom/gpt-migrate` | Yes (OpenAI) | 5/6 \* | [usage](docs/gpt-migrate_usage.md) |
| 37 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Autonomous agent that fixes GitHub issues | `hoomzoom/swe-agent` | Yes (OpenAI) | 10/10 | [usage](docs/SWE-agent_usage.md) |
| 38 | [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Multi-agent stock analysis and trading decisions | `hoomzoom/tradingagents` | Yes (OpenAI) | 3/3 | [usage](docs/tradingagents_usage.md) |
| 39 | [Integuru](https://github.com/Integuru-AI/Integuru) | Reverse-engineers API integrations via browser capture | `hoomzoom/integuru` | Yes (OpenAI) | 3/3 | [usage](docs/integuru_usage.md) |

\* **BettaFish 4/5:** The analysis engine endpoints require provider-specific API keys (not just OpenAI) that were unavailable during testing. Infrastructure and all other endpoints work.
\* **gpt-migrate 5/6:** The interactive chat mode requires gpt-4-32k, which OpenAI has deprecated. All other modes (migrate, create, test) work.

### Libraries (no web interface)

| # | App | What It Does | Docker Image | Needs API Key | Docs |
|---|-----|-------------|-------------|---------------|------|
| 40 | [codeinterpreter-api](https://github.com/shroominic/codeinterpreter-api) | ChatGPT Code Interpreter via LangChain + CodeBox | `hoomzoom/codeinterpreter-api` | Yes (OpenAI) | [usage](docs/codeinterpreter-api_usage.md) |
| 41 | [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) | LLM agent for chemistry tasks (RDKit, PubChem) | `hoomzoom/chemcrow` | Yes (OpenAI) | [usage](docs/chemcrow-public_usage.md) |

---

## Skipped Apps

These cannot run meaningfully in Docker. Local install docs are provided in `docs/` for each.

| App | Reason |
|-----|--------|
| [autoMate](https://github.com/yuruotong1/autoMate) | Desktop RPA tool, requires GUI, mouse/keyboard control. Useless headless. |
| [whispering](https://github.com/Sharrnah/whispering) | Requires microphone/audio device access. |
| [TaskMatrix](https://github.com/chenfei-wu/TaskMatrix) | Needs 16GB+ VRAM (multiple vision models). |
| [MedRAX](https://github.com/bowang-lab/MedRAX) | Needs 12-16GB+ VRAM, multiple large medical imaging models. |
| [home-llm](https://github.com/acon96/home-llm) | Home Assistant integration, not a standalone application. |
| [AiNiee](https://github.com/NEKOparapa/AiNiee) | Desktop GUI (PyQt5), no headless mode. |
| [itext2kg](https://github.com/AuvaLab/itext2kg) | Library only, no web interface or entry point. |
| [Windrecorder](https://github.com/Antonoko/Windrecorder) | Windows-only desktop app (pywin32), requires screen capture. |

---

## Documentation

Every deployed app has two docs in `docs/`:

- **Usage doc** (`<app>_usage.md`): Docker commands, API endpoints, curl examples, environment variables, test results, changes from original source, and V2 dependency changes
- **Reasoning doc** (`<app>_reasoning.md`): Deployment decisions, debugging steps, alternatives considered, and gotchas

Skipped apps also have usage docs with local install instructions.

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
docker pull hoomzoom/taskweaver
docker pull hoomzoom/devika-backend
docker pull hoomzoom/devika-frontend
docker pull hoomzoom/django-ai-assistant
docker pull hoomzoom/magentic-ui
docker pull hoomzoom/biomni
docker pull hoomzoom/data-copilot
docker pull hoomzoom/tradingagents
docker pull hoomzoom/integuru
docker pull hoomzoom/pyvideotrans
docker pull ollama/ollama
docker pull finaldie/auto-news:0.9.15
```

---

## Notes

- **API keys:** About half the apps need an OpenAI API key (or similar) for full functionality. Without a key, the infrastructure still runs -- you just can't make LLM calls. Each usage doc specifies which env vars to set.
- **Multi-container apps:** pdfGPT (4 containers), agenticSeek (4 containers), localGPT (4 containers), AgentGPT (3 containers), BettaFish (2 containers), devika (3 containers), and auto-news (9 containers) use docker-compose. The usage docs have the exact compose commands.
- **Port conflicts:** Each app's usage doc specifies which port it runs on. If running multiple apps at once, check for port collisions.
- **GPU required:** DataFlow requires an NVIDIA GPU with CUDA 12.4+ and the NVIDIA Container Toolkit. Run with `--gpus all`. Works on GTX 1650 (4GB VRAM) for WebUI and data processing operators.
- **Code execution by design:** 8 apps execute arbitrary code as their core function: rawdog, gpt-engineer, SWE-agent, codeinterpreter-api, gpt-migrate, gptme, TaskWeaver, devika. These are high-value targets for code injection research. Do not run them with access to sensitive data or networks.
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

# 2. Copy the Dockerfile and pinned dependency files into the cloned repo
cp dockerfiles/<app>/Dockerfile <repo>/
cp dockerfiles/<app>/requirements.txt <repo>/   # or pyproject.toml
cp dockerfiles/<app>/.env.example <repo>/        # if it exists

# 3. Build
cd <repo>
docker build -t <app> .
```

For multi-container apps (pdfGPT, agenticSeek, localGPT, AgentGPT, BettaFish, gpt_academic), the compose files in `dockerfiles/<app>/` are pre-configured to pull from Docker Hub. To build from source instead, edit the compose file to replace `image:` with `build:` and point to the cloned repo.
