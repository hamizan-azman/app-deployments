# LLM Application Deployment Collection

102 open-source LLM applications deployed and documented for supply chain security research. 94 deployed (79 Docker plus 15 non-Docker). 8 cannot deploy.

83 Docker images published to [Docker Hub](https://hub.docker.com/u/hoomzoom) under `hoomzoom/`. Every Docker app tested with documented pass/fail results per endpoint.

## Summary

| Method | Count |
|---|---:|
| Docker (`hoomzoom/` on Docker Hub) | 79 |
| Workstation source install | 10 |
| Library (`pip install`) | 4 |
| Plugin (Home Assistant via HACS) | 1 |
| **Deployed** | **94** |
| Cannot deploy | 8 |
| **Total** | **102** |

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

Each app's `docs/<app>_usage.md` has the exact commands.

---

## Web UI / API Apps (53)

Start with `-p` port mapping and access from a browser or HTTP client.

| # | App | What It Does | Port | UI Type | Docker Image | API Key | Tests | Docs |
|---|-----|-------------|------|---------|-------------|---------|-------|------|
| 1 | [pycorrector](https://github.com/shibing624/pycorrector) | Chinese text error correction | 7860 | Gradio | `hoomzoom/pycorrector` | No | 6/6 | [usage](docs/docker/pycorrector_usage.md) |
| 2 | [FunClip](https://github.com/modelscope/FunClip) | Video/audio clipping with ASR | 7860 | Gradio | `hoomzoom/funclip` | No | 4/4 | [usage](docs/docker/FunClip_usage.md) |
| 3 | [omniparse](https://github.com/adithya-s-k/omniparse) | Parse PDFs, images, web pages to markdown | 8000 | FastAPI + Gradio | `hoomzoom/omniparse` | No | 5/5 | [usage](docs/docker/omniparse_usage.md) |
| 4 | [manga-image-translator](https://github.com/zyddnys/manga-image-translator) | Translate text in manga/comic images | 5003 | Web API | `hoomzoom/manga-image-translator` | No | 5/5 | [usage](docs/docker/manga-image-translator_usage.md) |
| 5 | [pdfGPT](https://github.com/bhaskatripathi/pdfGPT) | PDF question-answering with embeddings | 7860 | Gradio (compose, 4 images) | `hoomzoom/pdfgpt-*` | Yes | 5/5 | [usage](docs/docker/pdfGPT_usage.md) |
| 6 | [gpt_academic](https://github.com/binary-husky/gpt_academic) | Academic writing assistant, code interpreter | 12345 | Gradio | `hoomzoom/gpt_academic` | Yes | 7/7 | [usage](docs/docker/gpt_academic_usage.md) |
| 7 | [NarratoAI](https://github.com/linyqh/NarratoAI) | Automated video narration | 8501 | Streamlit | `hoomzoom/narratoai` | Yes | 5/5 | [usage](docs/docker/NarratoAI_usage.md) |
| 8 | [codeqai](https://github.com/fynnfluegge/codeqai) | Semantic code search + GPT chat | 8501 | Streamlit | `hoomzoom/codeqai` | Yes | 5/5 | [usage](docs/docker/codeqai_usage.md) |
| 9 | [slide-deck-ai](https://github.com/barun-saha/slide-deck-ai) | Generate PowerPoint decks from a topic | 8501 | Streamlit | `hoomzoom/slidedeckai` | Yes | 3/3 | [usage](docs/docker/slide-deck-ai_usage.md) |
| 10 | [BettaFish](https://github.com/666ghj/BettaFish) | Multi-agent opinion/sentiment analysis | 8000 | Flask + PostgreSQL (compose) | `hoomzoom/bettafish` | Yes | 4/5 | [usage](docs/docker/BettaFish_usage.md) |
| 11 | [localGPT](https://github.com/PromtEngineer/localGPT) | Local RAG with document indexing and chat | 3000, 8000 | React + FastAPI (compose, 3 images) | `hoomzoom/localgpt-*` | No | 10/10 | [usage](docs/docker/localGPT_usage.md) |
| 12 | [agenticSeek](https://github.com/Fosowl/agenticSeek) | Multi-agent assistant (chat, code, web) | 3000, 8000 | React + FastAPI (compose, 2 images) | `hoomzoom/agenticseek-*` | Yes | 8/8 | [usage](docs/docker/agenticSeek_usage.md) |
| 13 | [zshot](https://github.com/IBM/zshot) | Zero-shot named entity recognition | 8000 | FastAPI | `hoomzoom/zshot` | No | 4/4 | [usage](docs/docker/zshot_usage.md) |
| 14 | [AgentGPT](https://github.com/reworkd/AgentGPT) | Autonomous AI agent platform | 3000, 8000 | Next.js + FastAPI + MySQL (compose, 2 images) | `hoomzoom/agentgpt-*` | Yes | 9/9 | [usage](docs/docker/AgentGPT_usage.md) |
| 15 | [DataFlow](https://github.com/OpenDCAI/DataFlow) | Data preparation and training for LLMs | 7860 | Gradio (GPU required) | `hoomzoom/dataflow` | No | 6/6 | [usage](docs/docker/DataFlow_usage.md) |
| 16 | [HuixiangDou](https://github.com/InternLM/HuixiangDou) | Knowledge assistant with RAG pipeline | 7860, 8888 | Gradio + FastAPI | `hoomzoom/huixiangdou` | Yes | 7/7 | [usage](docs/docker/HuixiangDou_usage.md) |
| 17 | [attackgen](https://github.com/mrwadams/attackgen) | Incident response scenario generator | 8501 | Streamlit | `hoomzoom/attackgen` | Yes | 5/5 | [usage](docs/docker/attackgen_usage.md) |
| 18 | [stride-gpt](https://github.com/mrwadams/stride-gpt) | STRIDE threat modeling | 8501 | Streamlit | `hoomzoom/stride-gpt` | Yes | 2/2 | [usage](docs/docker/stride-gpt_usage.md) |
| 19 | [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Autonomous web research agent | 8000 | FastAPI + Web UI | `hoomzoom/gpt-researcher` | Yes | 4/4 | [usage](docs/docker/gpt-researcher_usage.md) |
| 20 | [gptme](https://github.com/ErikBjare/gptme) | AI coding assistant with shell execution | 5000 | Flask | `hoomzoom/gptme-server` | Yes | 2/2 | [usage](docs/docker/gptme_usage.md) |
| 21 | [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | Iterative web research with local LLMs | 8123 | LangGraph API | `hoomzoom/local-deep-researcher` | No | 4/4 | [usage](docs/docker/local-deep-researcher_usage.md) |
| 22 | [TaskWeaver](https://github.com/microsoft/TaskWeaver) | Task planning and code execution agent | 8000 | Chainlit | `hoomzoom/taskweaver` | Yes | 4/4 | [usage](docs/docker/TaskWeaver_usage.md) |
| 23 | [devika](https://github.com/stitionai/devika) | AI software engineer with browser automation | 3000, 1337 | Svelte + Flask (compose, 2 images) | `hoomzoom/devika-*` | Yes | 16/16 | [usage](docs/docker/devika_usage.md) |
| 24 | [django-ai-assistant](https://github.com/vintasoftware/django-ai-assistant) | Django framework for AI assistants | 8000 | Django + React | `hoomzoom/django-ai-assistant` | Yes | 5/5 | [usage](docs/docker/django-ai-assistant_usage.md) |
| 25 | [magentic-ui](https://github.com/microsoft/magentic-one) | Multi-agent web automation | 8000 | FastAPI + Web UI | `hoomzoom/magentic-ui` | Yes | 2/2 | [usage](docs/docker/magentic-ui_usage.md) |
| 26 | [Biomni](https://github.com/bowang-lab/Biomni) | Biomedical AI assistant | 7860 | Gradio | `hoomzoom/biomni` | Yes | 2/2 | [usage](docs/docker/biomni_usage.md) |
| 27 | [Data-Copilot](https://github.com/zwq2018/Data-Copilot) | Chinese financial data analysis | 7860 | Gradio | `hoomzoom/data-copilot` | Yes | 2/2 | [usage](docs/docker/data-copilot_usage.md) |
| 28 | [auto-news](https://github.com/finaldie/auto-news) | News aggregation and summarization | 8080 | Airflow (compose, 9 containers) | `finaldie/auto-news:0.9.15` | Yes | 6/6 | [usage](docs/docker/auto-news_usage.md) |
| 29 | [RD-Agent](https://github.com/microsoft/RD-Agent) | Autonomous R&D for quant trading | 8501 | Streamlit (also has CLI) | `hoomzoom/rd-agent` | Yes | 5/5 | [usage](docs/docker/RD-Agent_usage.md) |
| 30 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Autonomous agent that fixes GitHub issues | 8000 | Web UI (also has CLI) | `hoomzoom/swe-agent` | Yes | 10/10 | [usage](docs/docker/SWE-agent_usage.md) |
| 31 | [DeepGit](https://github.com/zamalali/DeepGit) | GitHub repo deep search with LLM agents | 7860 | Gradio | `hoomzoom/deepgit` | Yes | 1/1 | [usage](docs/docker/DeepGit_usage.md) |
| 32 | [ChatDev](https://github.com/OpenBMB/ChatDev) | Multi-agent software development | 6400 | FastAPI | `hoomzoom/chatdev` | Yes | 1/1 | [usage](docs/docker/ChatDev_usage.md) |
| 33 | [pr-agent](https://github.com/qodo-ai/pr-agent) | AI-powered PR review and analysis | 3000 | FastAPI webhook | `hoomzoom/pr-agent` | Yes | 1/1 | [usage](docs/docker/pr-agent_usage.md) |
| 34 | [ai-goofish-monitor](https://github.com/Usagi-org/ai-goofish-monitor) | AI-powered marketplace price monitor | 8000 | FastAPI + Vue | `hoomzoom/ai-goofish-monitor` | Yes | 1/1 | [usage](docs/docker/ai-goofish-monitor_usage.md) |
| 35 | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Automated short video generation | 8501, 8080 | Streamlit + FastAPI | `hoomzoom/moneyprinterturbo` | Yes | 1/1 | [usage](docs/docker/MoneyPrinterTurbo_usage.md) |
| 36 | [BiliNote](https://github.com/JefferyHcool/BiliNote) | AI video note generation from Bilibili/YouTube | 8483 | FastAPI (backend) | `hoomzoom/bilinote` | Yes | 1/1 | [usage](docs/docker/BiliNote_usage.md) |
| 37 | [deepwiki-open](https://github.com/AsyncFuncAI/deepwiki-open) | AI wiki generator from code repos | 3000, 8001 | Next.js + FastAPI | `hoomzoom/deepwiki-open` | Yes | 1/1 | [usage](docs/docker/deepwiki-open_usage.md) |
| 38 | [docetl](https://github.com/ucbepic/docetl) | LLM-powered document ETL pipeline | 3000, 8000 | FastAPI + Next.js | `hoomzoom/docetl` | Yes | 1/1 | [usage](docs/docker/docetl_usage.md) |
| 39 | [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) | AI VTuber with Live2D and speech | 12393 | FastAPI/WebSocket | `hoomzoom/open-llm-vtuber` | Yes | 1/1 | [usage](docs/docker/Open-LLM-VTuber_usage.md) |
| 40 | [skyvern](https://github.com/Skyvern-AI/skyvern) | AI browser automation with visual understanding | 8000, 6080 | FastAPI + React + VNC (compose) | `hoomzoom/skyvern` | Yes | 1/1 | [usage](docs/docker/skyvern_usage.md) |
| 41 | [morphik-core](https://github.com/morphik-org/morphik-core) | Document processing and retrieval system | 8000 | FastAPI (compose) | `hoomzoom/morphik-core` | Yes | 1/1 | [usage](docs/docker/morphik-core_usage.md) |
| 42 | [chatgpt_telegram_bot](https://github.com/father-bot/chatgpt_telegram_bot) | ChatGPT Telegram bot with voice support | - | Telegram bot (compose) | `hoomzoom/chatgpt-telegram-bot` | Yes | 1/1 | [usage](docs/docker/chatgpt_telegram_bot_usage.md) |
| 43 | [Decepticon](https://github.com/PurpleAILAB/Decepticon) | Autonomous offensive security platform | - | Compose (pre-built) | (pre-built images) | Yes | -  [usage](docs/docker/Decepticon_usage.md) |
| 44 | [sparrow](https://github.com/katanaml/sparrow) | Document data extraction with LLM agents | 7860 | FastAPI | `hoomzoom/sparrow` | No | 1/1 | [usage](docs/docker/sparrow_usage.md) |
| 45 | [SurfSense](https://github.com/MODSetter/SurfSense) | Personal AI assistant with web browsing | 8929, 3929 | FastAPI + Next.js (compose) | (GHCR pre-built) | Yes | - | [usage](docs/docker/SurfSense_usage.md) |
| 46 | [khoj](https://github.com/khoj-ai/khoj) | Self-hosted AI assistant with search | 42110 | FastAPI + Django (compose) | (upstream pre-built) | No | - | [usage](docs/docker/khoj_usage.md) |
| 47 | [onyx](https://github.com/onyx-dot-app/onyx) | Enterprise AI knowledge assistant | 80 | FastAPI + Next.js (compose) | (upstream pre-built) | Yes | - | [usage](docs/docker/onyx_usage.md) |
| 48 | [Verba](https://github.com/weaviate/Verba) | RAG chatbot with Weaviate vector DB | 8000 | FastAPI (compose) | `hoomzoom/verba` | No | 1/1 | [usage](docs/docker/Verba_usage.md) |
| 49 | [kotaemon](https://github.com/Cinnamon/kotaemon) | Document QA with RAG pipeline | 7860 | Gradio | `hoomzoom/kotaemon` | No | 1/1 | [usage](docs/docker/kotaemon_usage.md) |
| 50 | [screenshot-to-code](https://github.com/abi/screenshot-to-code) | Convert screenshots to frontend code | 7001, 5173 | FastAPI + Vite (compose) | `hoomzoom/screenshot-to-code-*` | Yes | 1/1 | [usage](docs/docker/screenshot-to-code_usage.md) |
| 51 | [sql-explorer](https://github.com/explorerhq/sql-explorer) | Collaborative SQL query editor | 8000 | Django | `hoomzoom/sql-explorer` | No | 1/1 | [usage](docs/docker/sql-explorer_usage.md) |
| 52 | [DeepBI](https://github.com/DeepInsight-AI/DeepBI) | AI-powered business intelligence | 8338 | Flask (compose) | `hoomzoom/deepbi` | No | 1/1 | [usage](docs/docker/DeepBI_usage.md) |
| 53 | [openclaw](https://github.com/openclaw/openclaw) | Local gateway for AI coding tools | 18789 | Node.js (compose) | `hoomzoom/openclaw` | No | 1/1 | [usage](docs/docker/openclaw_usage.md) |

## CLI / Library Apps (26)

Run commands inside the container with `docker exec` or `docker run`.

| # | App | What It Does | Usage | Docker Image | API Key | Tests | Docs |
|---|-----|-------------|-------|-------------|---------|-------|------|
| 54 | [ChatDBG](https://github.com/plasma-umass/ChatDBG) | LLM-powered debugger (pdb, lldb, gdb) | `chatdbg` | `hoomzoom/chatdbg` | Yes | 7/7 | [usage](docs/docker/ChatDBG_usage.md) |
| 55 | [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) | Convert academic papers to posters | `python pipeline.py` | `hoomzoom/paper2poster` | Yes | 5/5 | [usage](docs/docker/Paper2Poster_usage.md) |
| 56 | [rawdog](https://github.com/AbanteAI/rawdog) | CLI assistant that generates and runs Python | `rawdog` | `hoomzoom/rawdog` | Yes | 3/3 | [usage](docs/docker/rawdog_usage.md) |
| 57 | [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Translate EPUB/TXT/SRT into bilingual books | `python make_book.py` | `hoomzoom/bilingual_book_maker` | Yes | 3/3 | [usage](docs/docker/bilingual_book_maker_usage.md) |
| 58 | [gpt-engineer](https://github.com/AntonOsika/gpt-engineer) | Generate/improve code from natural language | `gpte` | `hoomzoom/gpt-engineer` | Yes | 11/11 | [usage](docs/docker/gpt-engineer_usage.md) |
| 59 | [gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Migrate codebases between languages | `python main.py` | `hoomzoom/gpt-migrate` | Yes | 5/6 | [usage](docs/docker/gpt-migrate_usage.md) |
| 60 | [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Multi-agent stock analysis | `python main.py` | `hoomzoom/tradingagents` | Yes | 3/3 | [usage](docs/docker/tradingagents_usage.md) |
| 61 | [Integuru](https://github.com/Integuru-AI/Integuru) | Reverse-engineer API integrations | `python main.py` | `hoomzoom/integuru` | Yes | 3/3 | [usage](docs/docker/integuru_usage.md) |
| 62 | [pyvideotrans](https://github.com/jianchang512/pyvideotrans) | Video translation with speech recognition | `python cli.py` | `hoomzoom/pyvideotrans` | No | 2/2 | [usage](docs/docker/pyvideotrans_usage.md) |
| 63 | [codeinterpreter-api](https://github.com/shroominic/codeinterpreter-api) | Code Interpreter via LangChain + CodeBox | `from codeinterpreterapi import CodeInterpreterSession` | `hoomzoom/codeinterpreter-api` | Yes | - | [usage](docs/docker/codeinterpreter-api_usage.md) |
| 64 | [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) | LLM agent for chemistry tasks | `from chemcrow import ChemCrow` | `hoomzoom/chemcrow` | Yes | - | [usage](docs/docker/chemcrow-public_usage.md) |
| 65 | [vulnhuntr](https://github.com/protectai/vulnhuntr) | Zero-shot vulnerability scanner for Python | `vulnhuntr -r /target -l claude` | `hoomzoom/vulnhuntr` | Yes | 1/1 | [usage](docs/docker/vulnhuntr_usage.md) |
| 66 | [readme-ai](https://github.com/eli64s/readme-ai) | AI-powered README generator | `readmeai --repo <url>` | `hoomzoom/readme-ai` | Yes | 1/1 | [usage](docs/docker/readme-ai_usage.md) |
| 67 | [PocketFlow](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) | Codebase tutorial generator | `python main.py --repo <url>` | `hoomzoom/pocketflow` | Yes | 1/1 | [usage](docs/docker/PocketFlow-Tutorial-Codebase-Knowledge_usage.md) |
| 68 | [aider](https://github.com/Aider-AI/aider) | AI pair programming in the terminal | `aider` | `hoomzoom/aider` | Yes | 1/1 | [usage](docs/docker/aider_usage.md) |
| 69 | [hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT) | LLM-powered penetration testing framework | `wintermute` | `hoomzoom/hackingbuddygpt` | Yes | 1/1 | [usage](docs/docker/hackingBuddyGPT_usage.md) |
| 70 | [FinGenius](https://github.com/HuaYaoAI/FinGenius) | Multi-agent financial analysis | `python main.py <stock>` | `hoomzoom/fingenius` | Yes | 1/1 | [usage](docs/docker/FinGenius_usage.md) |
| 71 | [BabelDOC](https://github.com/funstory-ai/BabelDOC) | PDF document translator | `babeldoc` | `hoomzoom/babeldoc` | Yes | 1/1 | [usage](docs/docker/BabelDOC_usage.md) |
| 72 | [gpt-pilot](https://github.com/Pythagora-io/gpt-pilot) | AI coding agent that builds apps | `python main.py` | `hoomzoom/gpt-pilot` | Yes | 1/1 | [usage](docs/docker/gpt-pilot_usage.md) |
| 73 | [DATAGEN](https://github.com/starpig1129/DATAGEN) | Multi-agent data analysis pipeline | `python main.py` | `hoomzoom/datagen` | Yes | 1/1 | [usage](docs/docker/DATAGEN_usage.md) |
| 74 | [BruteForceAI](https://github.com/MorDavid/BruteForceAI) | AI-powered login brute force tool | `python BruteForceAI.py analyze` | `hoomzoom/bruteforceai` | Yes | 1/1 | [usage](docs/docker/BruteForceAI_usage.md) |
| 75 | [browser-use](https://github.com/browser-use/browser-use) | AI browser automation library | `browser-use` | `hoomzoom/browser-use` | Yes | 1/1 | [usage](docs/docker/browser-use_usage.md) |
| 76 | [hcaptcha-challenger](https://github.com/QIN2DIM/hcaptcha-challenger) | AI hCaptcha solver with Playwright | `hc` | `hoomzoom/hcaptcha-challenger` | Yes | 1/1 | [usage](docs/docker/hcaptcha-challenger_usage.md) |
| 77 | [BallonsTranslator](https://github.com/dmMaze/BallonsTranslator) | Manga/comic translator with OCR+inpainting | `python launch.py --headless` | `hoomzoom/ballonstranslator` | No | 1/1 | [usage](docs/docker/BallonsTranslator_usage.md) |
| 78 | [shell_gpt](https://github.com/TheR1D/shell_gpt) | CLI assistant with shell integration | `sgpt` | `hoomzoom/shell-gpt` | Yes | 1/1 | [usage](docs/docker/shell_gpt_usage.md) |
| 79 | [zotero-arxiv-daily](https://github.com/TideDra/zotero-arxiv-daily) | Automated arxiv paper digest for Zotero | `python -m zotero_arxiv_daily` | `hoomzoom/zotero-arxiv-daily` | Yes | 1/1 | [usage](docs/docker/zotero-arxiv-daily_usage.md) |

---

## Non-Docker deployed (15)

Click the app name to open its install guide. The "How to start" column has the launch command after install.

| # | App | Method | How to start | Notes |
|---|---|---|---|---|
| 1 | [AiNiee](docs/non-docker/AiNiee_usage.md) | workstation | `python main.py` (or run the prebuilt installer) | Cross-platform desktop GUI (PyQt5). Source install on Python 3.11. Drag a folder into the window, configure source / target language, click Start. |
| 2 | [AI_NovelGenerator](docs/non-docker/AI_NovelGenerator_usage.md) | workstation | `python main.py` | Cross-platform desktop GUI (CustomTkinter). Source install on Python 3.11. Tabs for LLM Settings, Novel Settings, Writing, Logs. |
| 3 | [AppAgent](docs/non-docker/AppAgent_usage.md) | workstation | `python learn.py` (explore) or `python run.py` (task) | Workstation + connected Android device via ADB. End-to-end demo on a rooted Samsung Galaxy S9 over WSL2 + usbipd-win USB bridge. Required config edits: `OPENAI_API_MODEL: "gpt-4o"` (default `gpt-4-vision-preview` is deprecated) and a real key in `OPENAI_API_KEY`. Required ADB prep on rooted phones: `adb shell wm size reset`. |
| 4 | [autoMate](docs/non-docker/autoMate_usage.md) | workstation | `automate` | "Smart NAS for AI" MCP-over-HTTP tool hub. Web UI at http://127.0.0.1:8765. Upstream replaced the v0.x OmniParser-based RPA tool with a different product. Install: `pip install 'automate-hub[full]'` on Python 3.10+. See finding 1. |
| 5 | [Cradle](docs/non-docker/Cradle_usage.md) | workstation | `python runner.py --envConfig conf\env_config_<env>.json` | Windows 10/11 + NVIDIA GPU + target game on host. Drives the target on host display, no separate UI. Install on Python 3.10 with `pip install -r requirements.txt`. Runtime needs a game so verification stops at install. See finding 4. |
| 6 | [contextgem](docs/non-docker/contextgem_usage.md) | library | `from contextgem import Document, DocumentAnalyzer` in Python | Python library, no standalone UI. `pip install contextgem` v0.22.0 on Python 3.12. |
| 7 | [ExtractThinker](docs/non-docker/ExtractThinker_usage.md) | library | `from extract_thinker import Extractor, Contract` in Python | Python library, no standalone UI. `pip install extract-thinker` v0.1.14 on Python 3.12. |
| 8 | [GLaDOS](docs/non-docker/GLaDOS_usage.md) | workstation | `uv run glados start` | Workstation with mic + speaker. Voice in / out. NVIDIA GPU recommended for usable latency. `uv sync` on Python 3.11. LLM backend swappable to any OpenAI-compatible endpoint via `LLM_BASE_URL` and `LLM_MODEL` env vars. |
| 9 | [home-llm](docs/non-docker/home-llm_usage.md) | plugin | Inside Home Assistant: Settings -> Devices & Services -> Add Integration -> Local LLM | Custom integration for Home Assistant 2025.7.0+. Installed via HACS. End-to-end exercised inside `homeassistant/home-assistant:stable` Docker with HACS 2026.4.4 plus a Local LLM Conversation Agent on `gpt-4o-mini`. See finding 6. |
| 10 | [itext2kg](docs/non-docker/itext2kg_usage.md) | library | `from itext2kg import iText2KG` in Python | Python library, no standalone UI. `pip install itext2kg` v1.0.0 on Python 3.12. |
| 11 | [pandas-ai](docs/non-docker/pandas-ai_usage.md) | library | `from pandasai import SmartDataframe` in Python | Python library, no standalone UI. `pip install pandasai` v3.0.0. Use Python 3.11 (3.12 has no pandas wheel and builds from source which fails on a fresh system). |
| 12 | [UFO](docs/non-docker/UFO_usage.md) | workstation | `python -m ufo --task <task_name>` | Windows 10/11 only. pywinauto + Windows UI Automation. Install on Windows Python 3.11.9 with `pip install colorama` first. `from ufo import ufo` imports cleanly. |
| 13 | [VideoCaptioner](docs/non-docker/VideoCaptioner_usage.md) | workstation | `videocaptioner` (PyPI install) or `python main.py` (source install) | Cross-platform desktop GUI (PyQt5) + FFmpeg. PyPI v1.4.1 on Python 3.11. Source install uses `pip install .` (no `requirements.txt`). |
| 14 | [whispering](docs/non-docker/whispering_usage.md) | workstation | Launch from prebuilt installer (or `pnpm tauri dev` for source) | Desktop app with microphone (Tauri). System-wide hotkey (`Ctrl+Shift+.` on Windows). End-to-end on Windows host with live mic and OpenAI Whisper API. Successor org is `EpicenterHQ/epicenter`. |
| 15 | [Windrecorder](docs/non-docker/windrecorder_usage.md) | workstation | `start_app.bat` (or `.venv\Scripts\python.exe -m streamlit run webui.py` if the bat fails on the host) | Windows-only. Continuous screen recording via DirectX. Streamlit at http://localhost:8501. Install via `install_update.bat` (Poetry). See finding 5. |

## Cannot deploy (8)

| # | App | Reason | Notes |
|---|---|---|---|
| 1 | [TaskMatrix](docs/non-docker/TaskMatrix_usage.md) | GPU server unavailable | NVIDIA GPU 16+ GB VRAM minimum (60+ GB for full set). |
| 2 | [MedRAX](docs/non-docker/MedRAX_usage.md) | GPU server unavailable | NVIDIA GPU 12+ GB VRAM minimum. |
| 3 | [functionary](docs/non-docker/functionary_usage.md) | GPU server unavailable | NVIDIA GPU 24+ GB VRAM minimum. vLLM/SGLang backend. |
| 4 | [Linly-Talker](docs/non-docker/Linly-Talker_usage.md) | GPU server unavailable | NVIDIA GPU 8+ GB VRAM minimum. SadTalker + Wav2Lip pipeline. |
| 5 | [droidrun](docs/non-docker/droidrun_usage.md) | Upstream blocked | droidrun 0.5.9 imports `AsyncMobilerun` from the mobilerun package. The latest mobilerun (v0.6.0rc2) no longer exports it. Mid-migration. The repo was also renamed `droidrun/droidrun` to `droidrun/mobilerun`. See finding 3. |
| 6 | [wiseflow](docs/non-docker/wiseflow_usage.md) | Upstream blocked | Upstream rewrote the project as a TypeScript/Node codebase. The Python + Chromium + PocketBase install path the doc describes is stale. The doc needs a full rewrite before deployment. See finding 2. |
| 7 | [Open-Interface](docs/non-docker/Open-Interface_usage.md) | macOS required | Primary platform is macOS. Linux and Windows reported with caveats. No macOS host available. |
| 8 | [Codex-CLI](docs/non-docker/Codex-CLI_usage.md) | Model retired | OpenAI retired the Codex model in March 2023. The endpoint `/v1/engines/davinci-codex/completions` returns HTTP 404. |


---

## Repo Structure

```
app-deployments/
  apps/                    # Git submodules pointing to upstream repos (reference only)
  dockerfiles/             # Dockerfiles, compose files, configs, pinned dependency files
  docs/                    # Per-app usage docs (*_usage.md)
  v2_pinned_versions.md    # Manifest of all V2 dependency version changes
  README.md                # This document
```

The `apps/` submodules contain original code with original version specifiers. For V2 (supply chain security analysis), all `>=` versions were pinned to `==` minimums. Those pinned files live in `dockerfiles/`, which is what was actually used to build the Docker images.

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
