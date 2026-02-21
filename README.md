# LLM Application Deployment Collection

Dockerized deployment of 41 open-source LLM applications for supply chain security research. Each app is containerized, tested, and documented with usage guides and reasoning logs.

- **41 apps deployed** across web UIs, CLI tools, and libraries
- **8 apps skipped** (incompatible with Docker, local install docs provided)
- **48 Docker images** published to [Docker Hub](https://hub.docker.com/u/hoomzoom) under `hoomzoom/`
- **Every app tested** with documented pass/fail results per endpoint

---

## Web UI / API Apps (30)

Start with `-p` port mapping and access from a browser or HTTP client.

| # | App | What It Does | Port | UI Type | Docker Image | API Key | Tests | Docs |
|---|-----|-------------|------|---------|-------------|---------|-------|------|
| 1 | [pycorrector](https://github.com/shibing624/pycorrector) | Chinese text error correction | 7860 | Gradio | `hoomzoom/pycorrector` | No | 6/6 | [usage](docs/pycorrector_usage.md) |
| 2 | [FunClip](https://github.com/modelscope/FunClip) | Video/audio clipping with ASR | 7860 | Gradio | `hoomzoom/funclip` | No | 4/4 | [usage](docs/FunClip_usage.md) |
| 3 | [omniparse](https://github.com/adithya-s-k/omniparse) | Parse PDFs, images, web pages to markdown | 8000 | FastAPI + Gradio | `hoomzoom/omniparse` | No | 5/5 | [usage](docs/omniparse_usage.md) |
| 4 | [manga-image-translator](https://github.com/zyddnys/manga-image-translator) | Translate text in manga/comic images | 5003 | Web API | `hoomzoom/manga-image-translator` | No | 5/5 | [usage](docs/manga-image-translator_usage.md) |
| 5 | [pdfGPT](https://github.com/bhaskatripathi/pdfGPT) | PDF question-answering with embeddings | 7860 | Gradio (compose, 4 images) | `hoomzoom/pdfgpt-*` | Yes | 5/5 | [usage](docs/pdfGPT_usage.md) |
| 6 | [gpt_academic](https://github.com/binary-husky/gpt_academic) | Academic writing assistant, code interpreter | 12345 | Gradio | `hoomzoom/gpt_academic` | Yes | 7/7 | [usage](docs/gpt_academic_usage.md) |
| 7 | [NarratoAI](https://github.com/linyqh/NarratoAI) | Automated video narration | 8501 | Streamlit | `hoomzoom/narratoai` | Yes | 5/5 | [usage](docs/NarratoAI_usage.md) |
| 8 | [codeqai](https://github.com/fynnfluegge/codeqai) | Semantic code search + GPT chat | 8501 | Streamlit | `hoomzoom/codeqai` | Yes | 5/5 | [usage](docs/codeqai_usage.md) |
| 9 | [slide-deck-ai](https://github.com/barun-saha/slide-deck-ai) | Generate PowerPoint decks from a topic | 8501 | Streamlit | `hoomzoom/slidedeckai` | Yes | 3/3 | [usage](docs/slide-deck-ai_usage.md) |
| 10 | [BettaFish](https://github.com/666ghj/BettaFish) | Multi-agent opinion/sentiment analysis | 8000 | Flask + PostgreSQL (compose) | `hoomzoom/bettafish` | Yes | 4/5 | [usage](docs/BettaFish_usage.md) |
| 11 | [localGPT](https://github.com/PromtEngineer/localGPT) | Local RAG with document indexing and chat | 3000, 8000 | React + FastAPI (compose, 3 images) | `hoomzoom/localgpt-*` | No | 10/10 | [usage](docs/localGPT_usage.md) |
| 12 | [agenticSeek](https://github.com/Fosowl/agenticSeek) | Multi-agent assistant (chat, code, web) | 3000, 8000 | React + FastAPI (compose, 2 images) | `hoomzoom/agenticseek-*` | Yes | 8/8 | [usage](docs/agenticSeek_usage.md) |
| 13 | [zshot](https://github.com/IBM/zshot) | Zero-shot named entity recognition | 8000 | FastAPI | `hoomzoom/zshot` | No | 4/4 | [usage](docs/zshot_usage.md) |
| 14 | [AgentGPT](https://github.com/reworkd/AgentGPT) | Autonomous AI agent platform | 3000, 8000 | Next.js + FastAPI + MySQL (compose, 2 images) | `hoomzoom/agentgpt-*` | Yes | 9/9 | [usage](docs/AgentGPT_usage.md) |
| 15 | [DataFlow](https://github.com/OpenDCAI/DataFlow) | Data preparation and training for LLMs | 7860 | Gradio (GPU required) | `hoomzoom/dataflow` | No | 6/6 | [usage](docs/DataFlow_usage.md) |
| 16 | [HuixiangDou](https://github.com/InternLM/HuixiangDou) | Knowledge assistant with RAG pipeline | 7860, 8888 | Gradio + FastAPI | `hoomzoom/huixiangdou` | Yes | 7/7 | [usage](docs/HuixiangDou_usage.md) |
| 17 | [attackgen](https://github.com/mrwadams/attackgen) | Incident response scenario generator | 8501 | Streamlit | `hoomzoom/attackgen` | Yes | 5/5 | [usage](docs/attackgen_usage.md) |
| 18 | [stride-gpt](https://github.com/mrwadams/stride-gpt) | STRIDE threat modeling | 8501 | Streamlit | `hoomzoom/stride-gpt` | Yes | 2/2 | [usage](docs/stride-gpt_usage.md) |
| 19 | [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Autonomous web research agent | 8000 | FastAPI + Web UI | `hoomzoom/gpt-researcher` | Yes | 4/4 | [usage](docs/gpt-researcher_usage.md) |
| 20 | [gptme](https://github.com/ErikBjare/gptme) | AI coding assistant with shell execution | 5000 | Flask | `hoomzoom/gptme-server` | Yes | 2/2 | [usage](docs/gptme_usage.md) |
| 21 | [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | Iterative web research with local LLMs | 8123 | LangGraph API | `hoomzoom/local-deep-researcher` | No | 4/4 | [usage](docs/local-deep-researcher_usage.md) |
| 22 | [TaskWeaver](https://github.com/microsoft/TaskWeaver) | Task planning and code execution agent | 8000 | Chainlit | `hoomzoom/taskweaver` | Yes | 4/4 | [usage](docs/TaskWeaver_usage.md) |
| 23 | [devika](https://github.com/stitionai/devika) | AI software engineer with browser automation | 3000, 1337 | Svelte + Flask (compose, 2 images) | `hoomzoom/devika-*` | Yes | 16/16 | [usage](docs/devika_usage.md) |
| 24 | [django-ai-assistant](https://github.com/vintasoftware/django-ai-assistant) | Django framework for AI assistants | 8000 | Django + React | `hoomzoom/django-ai-assistant` | Yes | 5/5 | [usage](docs/django-ai-assistant_usage.md) |
| 25 | [magentic-ui](https://github.com/microsoft/magentic-one) | Multi-agent web automation | 8000 | FastAPI + Web UI | `hoomzoom/magentic-ui` | Yes | 2/2 | [usage](docs/magentic-ui_usage.md) |
| 26 | [Biomni](https://github.com/bowang-lab/Biomni) | Biomedical AI assistant | 7860 | Gradio | `hoomzoom/biomni` | Yes | 2/2 | [usage](docs/biomni_usage.md) |
| 27 | [Data-Copilot](https://github.com/zwq2018/Data-Copilot) | Chinese financial data analysis | 7860 | Gradio | `hoomzoom/data-copilot` | Yes | 2/2 | [usage](docs/data-copilot_usage.md) |
| 28 | [auto-news](https://github.com/finaldie/auto-news) | News aggregation and summarization | 8080 | Airflow (compose, 9 containers) | `finaldie/auto-news:0.9.15` | Yes | 6/6 | [usage](docs/auto-news_usage.md) |
| 29 | [RD-Agent](https://github.com/microsoft/RD-Agent) | Autonomous R&D for quant trading | 8501 | Streamlit (also has CLI) | `hoomzoom/rd-agent` | Yes | 5/5 | [usage](docs/RD-Agent_usage.md) |
| 30 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Autonomous agent that fixes GitHub issues | 8000 | Web UI (also has CLI) | `hoomzoom/swe-agent` | Yes | 10/10 | [usage](docs/SWE-agent_usage.md) |

## CLI / Library Apps (11)

Run commands inside the container with `docker exec` or `docker run`.

| # | App | What It Does | Usage | Docker Image | API Key | Tests | Docs |
|---|-----|-------------|-------|-------------|---------|-------|------|
| 31 | [ChatDBG](https://github.com/plasma-umass/ChatDBG) | LLM-powered debugger (pdb, lldb, gdb) | `chatdbg` | `hoomzoom/chatdbg` | Yes | 7/7 | [usage](docs/ChatDBG_usage.md) |
| 32 | [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) | Convert academic papers to posters | `python pipeline.py` | `hoomzoom/paper2poster` | Yes | 5/5 | [usage](docs/Paper2Poster_usage.md) |
| 33 | [rawdog](https://github.com/AbanteAI/rawdog) | CLI assistant that generates and runs Python | `rawdog` | `hoomzoom/rawdog` | Yes | 3/3 | [usage](docs/rawdog_usage.md) |
| 34 | [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Translate EPUB/TXT/SRT into bilingual books | `python make_book.py` | `hoomzoom/bilingual_book_maker` | Yes | 3/3 | [usage](docs/bilingual_book_maker_usage.md) |
| 35 | [gpt-engineer](https://github.com/AntonOsika/gpt-engineer) | Generate/improve code from natural language | `gpte` | `hoomzoom/gpt-engineer` | Yes | 11/11 | [usage](docs/gpt-engineer_usage.md) |
| 36 | [gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Migrate codebases between languages | `python main.py` | `hoomzoom/gpt-migrate` | Yes | 5/6 | [usage](docs/gpt-migrate_usage.md) |
| 37 | [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Multi-agent stock analysis | `python main.py` | `hoomzoom/tradingagents` | Yes | 3/3 | [usage](docs/tradingagents_usage.md) |
| 38 | [Integuru](https://github.com/Integuru-AI/Integuru) | Reverse-engineer API integrations | `python main.py` | `hoomzoom/integuru` | Yes | 3/3 | [usage](docs/integuru_usage.md) |
| 39 | [pyvideotrans](https://github.com/jianchang512/pyvideotrans) | Video translation with speech recognition | `python cli.py` | `hoomzoom/pyvideotrans` | No | 2/2 | [usage](docs/pyvideotrans_usage.md) |
| 40 | [codeinterpreter-api](https://github.com/shroominic/codeinterpreter-api) | Code Interpreter via LangChain + CodeBox | `from codeinterpreterapi import CodeInterpreterSession` | `hoomzoom/codeinterpreter-api` | Yes | - | [usage](docs/codeinterpreter-api_usage.md) |
| 41 | [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) | LLM agent for chemistry tasks | `from chemcrow import ChemCrow` | `hoomzoom/chemcrow` | Yes | - | [usage](docs/chemcrow-public_usage.md) |

---

## Skipped Apps (8)

Cannot run meaningfully in Docker. Local install docs provided in `docs/`.

| App | Reason |
|-----|--------|
| [autoMate](https://github.com/yuruotong1/autoMate) | Desktop RPA, requires GUI and mouse/keyboard control |
| [whispering](https://github.com/Sharrnah/whispering) | Requires microphone/audio device access |
| [TaskMatrix](https://github.com/chenfei-wu/TaskMatrix) | Needs 16GB+ VRAM (multiple vision models) |
| [MedRAX](https://github.com/bowang-lab/MedRAX) | Needs 12-16GB+ VRAM, multiple medical imaging models |
| [home-llm](https://github.com/acon96/home-llm) | Home Assistant integration, not standalone |
| [AiNiee](https://github.com/NEKOparapa/AiNiee) | Desktop GUI (PyQt5), no headless mode |
| [itext2kg](https://github.com/AuvaLab/itext2kg) | Library only, no web interface or entry point |
| [Windrecorder](https://github.com/Antonoko/Windrecorder) | Windows-only desktop app, requires screen capture |

---

## Quick Start

Pull any app from Docker Hub:

```bash
docker pull hoomzoom/attackgen
docker run -p 8501:8501 hoomzoom/attackgen
```

For compose apps (devika, auto-news, localGPT, etc.):

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
  apps/                    # Git submodules pointing to upstream repos (reference only)
  dockerfiles/             # Dockerfiles, compose files, configs, pinned dependency files
  docs/                    # Usage docs (*_usage.md) and reasoning docs (*_reasoning.md)
  v2_pinned_versions.md    # Manifest of all V2 dependency version changes
```

| What you need | Where to look |
|---------------|---------------|
| Original upstream source code | `apps/<name>/` (git submodules) |
| Pinned dependency files used for builds | `dockerfiles/<name>/` (requirements.txt, pyproject.toml, etc.) |
| Dockerfiles and compose files | `dockerfiles/<name>/` |
| What was changed and why | `docs/<name>_usage.md`, "V2 Dependency Changes" section |
| Quick reference of all version bumps | `v2_pinned_versions.md` |

The `apps/` submodules contain original code with original version specifiers. For V2 (supply chain security analysis), all `>=` versions were pinned to `==` minimums. Those pinned files live in `dockerfiles/`, which is what was actually used to build the Docker images.

---

## Documentation

Every deployed app has two docs in `docs/`:

- **Usage doc** (`<app>_usage.md`): Docker commands, API endpoints, curl examples, environment variables, test results, changes from original source, V2 dependency changes
- **Reasoning doc** (`<app>_reasoning.md`): Deployment decisions, debugging steps, alternatives considered

Skipped apps also have usage docs with local install instructions.

---

## Notes

- **API keys:** About half the apps need an OpenAI API key (or similar) for full functionality. Without a key, the infrastructure still runs, you just can't make LLM calls. Each usage doc specifies which env vars to set.
- **Multi-container apps:** pdfGPT (4), agenticSeek (4), localGPT (4), AgentGPT (3), devika (3), BettaFish (2), auto-news (9) use docker-compose. Usage docs have the exact compose commands.
- **GPU required:** DataFlow requires NVIDIA GPU with CUDA 12.4+ and the NVIDIA Container Toolkit. Run with `--gpus all`.
- **Code execution by design:** rawdog, gpt-engineer, SWE-agent, codeinterpreter-api, gpt-migrate, gptme, TaskWeaver, devika all execute arbitrary code as their core function. Do not run them with access to sensitive data or networks.
- **Docker socket:** SWE-agent requires `-v /var/run/docker.sock:/var/run/docker.sock`, giving the container full Docker daemon access. Run on an isolated machine only.
- **Model downloads:** FunClip, omniparse, manga-image-translator, zshot, pycorrector download ML models on first startup (1-5 GB). First launch takes 5-30 minutes. Check logs with `docker logs -f <container>` to monitor progress.

---

## Building from Source

All Docker Hub images can be rebuilt from `dockerfiles/`:

```bash
git clone https://github.com/<org>/<repo>.git
cp dockerfiles/<app>/Dockerfile <repo>/
cp dockerfiles/<app>/requirements.txt <repo>/   # or pyproject.toml
cd <repo>
docker build -t <app> .
```

For compose apps, edit the compose file to replace `image:` with `build:` and point to the cloned repo.
