# LLM Application Deployment Collection

Dockerized deployment of 79 open-source LLM applications for supply chain security research. Each app is containerized, tested, and documented with usage guides and reasoning logs.

- **79 apps deployed** across web UIs, CLI tools, and libraries
- **23 apps skipped** (incompatible with Docker). Local install docs per app plus a [categorised failure analysis](docs/DEPLOYMENT_FAILURE_ANALYSIS.md) with pie chart
- **83 Docker images** published to [Docker Hub](https://hub.docker.com/u/hoomzoom) under `hoomzoom/`
- **Every app tested** with documented pass/fail results per endpoint

---

## Web UI / API Apps (53)

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
| 31 | [DeepGit](https://github.com/zamalali/DeepGit) | GitHub repo deep search with LLM agents | 7860 | Gradio | `hoomzoom/deepgit` | Yes | 1/1  [usage](docs/DeepGit_usage.md) |
| 32 | [ChatDev](https://github.com/OpenBMB/ChatDev) | Multi-agent software development | 6400 | FastAPI | `hoomzoom/chatdev` | Yes | 1/1  [usage](docs/ChatDev_usage.md) |
| 33 | [pr-agent](https://github.com/qodo-ai/pr-agent) | AI-powered PR review and analysis | 3000 | FastAPI webhook | `hoomzoom/pr-agent` | Yes | 1/1  [usage](docs/pr-agent_usage.md) |
| 34 | [ai-goofish-monitor](https://github.com/Usagi-org/ai-goofish-monitor) | AI-powered marketplace price monitor | 8000 | FastAPI + Vue | `hoomzoom/ai-goofish-monitor` | Yes | 1/1  [usage](docs/ai-goofish-monitor_usage.md) |
| 35 | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | Automated short video generation | 8501, 8080 | Streamlit + FastAPI | `hoomzoom/moneyprinterturbo` | Yes | 1/1  [usage](docs/MoneyPrinterTurbo_usage.md) |
| 36 | [BiliNote](https://github.com/JefferyHcool/BiliNote) | AI video note generation from Bilibili/YouTube | 8483 | FastAPI (backend) | `hoomzoom/bilinote` | Yes | 1/1  [usage](docs/BiliNote_usage.md) |
| 37 | [deepwiki-open](https://github.com/AsyncFuncAI/deepwiki-open) | AI wiki generator from code repos | 3000, 8001 | Next.js + FastAPI | `hoomzoom/deepwiki-open` | Yes | 1/1  [usage](docs/deepwiki-open_usage.md) |
| 38 | [docetl](https://github.com/ucbepic/docetl) | LLM-powered document ETL pipeline | 3000, 8000 | FastAPI + Next.js | `hoomzoom/docetl` | Yes | 1/1  [usage](docs/docetl_usage.md) |
| 39 | [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) | AI VTuber with Live2D and speech | 12393 | FastAPI/WebSocket | `hoomzoom/open-llm-vtuber` | Yes | 1/1  [usage](docs/Open-LLM-VTuber_usage.md) |
| 40 | [skyvern](https://github.com/Skyvern-AI/skyvern) | AI browser automation with visual understanding | 8000, 6080 | FastAPI + React + VNC (compose) | `hoomzoom/skyvern` | Yes | 1/1  [usage](docs/skyvern_usage.md) |
| 41 | [morphik-core](https://github.com/morphik-org/morphik-core) | Document processing and retrieval system | 8000 | FastAPI (compose) | `hoomzoom/morphik-core` | Yes | 1/1  [usage](docs/morphik-core_usage.md) |
| 42 | [chatgpt_telegram_bot](https://github.com/father-bot/chatgpt_telegram_bot) | ChatGPT Telegram bot with voice support | - | Telegram bot (compose) | `hoomzoom/chatgpt-telegram-bot` | Yes | 1/1  [usage](docs/chatgpt_telegram_bot_usage.md) |
| 43 | [Decepticon](https://github.com/PurpleAILAB/Decepticon) | Autonomous offensive security platform | - | Compose (pre-built) | (pre-built images) | Yes | -  [usage](docs/Decepticon_usage.md) |
| 44 | [sparrow](https://github.com/katanaml/sparrow) | Document data extraction with LLM agents | 7860 | FastAPI | `hoomzoom/sparrow` | No | 1/1 | [usage](docs/sparrow_usage.md) |
| 45 | [SurfSense](https://github.com/MODSetter/SurfSense) | Personal AI assistant with web browsing | 8929, 3929 | FastAPI + Next.js (compose) | (GHCR pre-built) | Yes | - | [usage](docs/SurfSense_usage.md) |
| 46 | [khoj](https://github.com/khoj-ai/khoj) | Self-hosted AI assistant with search | 42110 | FastAPI + Django (compose) | (upstream pre-built) | No | - | [usage](docs/khoj_usage.md) |
| 47 | [onyx](https://github.com/onyx-dot-app/onyx) | Enterprise AI knowledge assistant | 80 | FastAPI + Next.js (compose) | (upstream pre-built) | Yes | - | [usage](docs/onyx_usage.md) |
| 48 | [Verba](https://github.com/weaviate/Verba) | RAG chatbot with Weaviate vector DB | 8000 | FastAPI (compose) | `hoomzoom/verba` | No | 1/1 | [usage](docs/Verba_usage.md) |
| 49 | [kotaemon](https://github.com/Cinnamon/kotaemon) | Document QA with RAG pipeline | 7860 | Gradio | `hoomzoom/kotaemon` | No | 1/1 | [usage](docs/kotaemon_usage.md) |
| 50 | [screenshot-to-code](https://github.com/abi/screenshot-to-code) | Convert screenshots to frontend code | 7001, 5173 | FastAPI + Vite (compose) | `hoomzoom/screenshot-to-code-*` | Yes | 1/1 | [usage](docs/screenshot-to-code_usage.md) |
| 51 | [sql-explorer](https://github.com/explorerhq/sql-explorer) | Collaborative SQL query editor | 8000 | Django | `hoomzoom/sql-explorer` | No | 1/1 | [usage](docs/sql-explorer_usage.md) |
| 52 | [DeepBI](https://github.com/DeepInsight-AI/DeepBI) | AI-powered business intelligence | 8338 | Flask (compose) | `hoomzoom/deepbi` | No | 1/1 | [usage](docs/DeepBI_usage.md) |
| 53 | [openclaw](https://github.com/openclaw/openclaw) | Local gateway for AI coding tools | 18789 | Node.js (compose) | `hoomzoom/openclaw` | No | 1/1 | [usage](docs/openclaw_usage.md) |

## CLI / Library Apps (26)

Run commands inside the container with `docker exec` or `docker run`.

| # | App | What It Does | Usage | Docker Image | API Key | Tests | Docs |
|---|-----|-------------|-------|-------------|---------|-------|------|
| 54 | [ChatDBG](https://github.com/plasma-umass/ChatDBG) | LLM-powered debugger (pdb, lldb, gdb) | `chatdbg` | `hoomzoom/chatdbg` | Yes | 7/7 | [usage](docs/ChatDBG_usage.md) |
| 55 | [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) | Convert academic papers to posters | `python pipeline.py` | `hoomzoom/paper2poster` | Yes | 5/5 | [usage](docs/Paper2Poster_usage.md) |
| 56 | [rawdog](https://github.com/AbanteAI/rawdog) | CLI assistant that generates and runs Python | `rawdog` | `hoomzoom/rawdog` | Yes | 3/3 | [usage](docs/rawdog_usage.md) |
| 57 | [bilingual_book_maker](https://github.com/yihong0618/bilingual_book_maker) | Translate EPUB/TXT/SRT into bilingual books | `python make_book.py` | `hoomzoom/bilingual_book_maker` | Yes | 3/3 | [usage](docs/bilingual_book_maker_usage.md) |
| 58 | [gpt-engineer](https://github.com/AntonOsika/gpt-engineer) | Generate/improve code from natural language | `gpte` | `hoomzoom/gpt-engineer` | Yes | 11/11 | [usage](docs/gpt-engineer_usage.md) |
| 59 | [gpt-migrate](https://github.com/joshpxyne/gpt-migrate) | Migrate codebases between languages | `python main.py` | `hoomzoom/gpt-migrate` | Yes | 5/6 | [usage](docs/gpt-migrate_usage.md) |
| 60 | [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Multi-agent stock analysis | `python main.py` | `hoomzoom/tradingagents` | Yes | 3/3 | [usage](docs/tradingagents_usage.md) |
| 61 | [Integuru](https://github.com/Integuru-AI/Integuru) | Reverse-engineer API integrations | `python main.py` | `hoomzoom/integuru` | Yes | 3/3 | [usage](docs/integuru_usage.md) |
| 62 | [pyvideotrans](https://github.com/jianchang512/pyvideotrans) | Video translation with speech recognition | `python cli.py` | `hoomzoom/pyvideotrans` | No | 2/2 | [usage](docs/pyvideotrans_usage.md) |
| 63 | [codeinterpreter-api](https://github.com/shroominic/codeinterpreter-api) | Code Interpreter via LangChain + CodeBox | `from codeinterpreterapi import CodeInterpreterSession` | `hoomzoom/codeinterpreter-api` | Yes | - | [usage](docs/codeinterpreter-api_usage.md) |
| 64 | [chemcrow-public](https://github.com/ur-whitelab/chemcrow-public) | LLM agent for chemistry tasks | `from chemcrow import ChemCrow` | `hoomzoom/chemcrow` | Yes | - | [usage](docs/chemcrow-public_usage.md) |
| 65 | [vulnhuntr](https://github.com/protectai/vulnhuntr) | Zero-shot vulnerability scanner for Python | `vulnhuntr -r /target -l claude` | `hoomzoom/vulnhuntr` | Yes | 1/1  [usage](docs/vulnhuntr_usage.md) |
| 66 | [readme-ai](https://github.com/eli64s/readme-ai) | AI-powered README generator | `readmeai --repo <url>` | `hoomzoom/readme-ai` | Yes | 1/1  [usage](docs/readme-ai_usage.md) |
| 67 | [PocketFlow](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) | Codebase tutorial generator | `python main.py --repo <url>` | `hoomzoom/pocketflow` | Yes | 1/1 | [usage](docs/PocketFlow-Tutorial-Codebase-Knowledge_usage.md) |
| 68 | [aider](https://github.com/Aider-AI/aider) | AI pair programming in the terminal | `aider` | `hoomzoom/aider` | Yes | 1/1  [usage](docs/aider_usage.md) |
| 69 | [hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT) | LLM-powered penetration testing framework | `wintermute` | `hoomzoom/hackingbuddygpt` | Yes | 1/1  [usage](docs/hackingBuddyGPT_usage.md) |
| 70 | [FinGenius](https://github.com/HuaYaoAI/FinGenius) | Multi-agent financial analysis | `python main.py <stock>` | `hoomzoom/fingenius` | Yes | 1/1  [usage](docs/FinGenius_usage.md) |
| 71 | [BabelDOC](https://github.com/funstory-ai/BabelDOC) | PDF document translator | `babeldoc` | `hoomzoom/babeldoc` | Yes | 1/1  [usage](docs/BabelDOC_usage.md) |
| 72 | [gpt-pilot](https://github.com/Pythagora-io/gpt-pilot) | AI coding agent that builds apps | `python main.py` | `hoomzoom/gpt-pilot` | Yes | 1/1  [usage](docs/gpt-pilot_usage.md) |
| 73 | [DATAGEN](https://github.com/starpig1129/DATAGEN) | Multi-agent data analysis pipeline | `python main.py` | `hoomzoom/datagen` | Yes | 1/1  [usage](docs/DATAGEN_usage.md) |
| 74 | [BruteForceAI](https://github.com/MorDavid/BruteForceAI) | AI-powered login brute force tool | `python BruteForceAI.py analyze` | `hoomzoom/bruteforceai` | Yes | 1/1  [usage](docs/BruteForceAI_usage.md) |
| 75 | [browser-use](https://github.com/browser-use/browser-use) | AI browser automation library | `browser-use` | `hoomzoom/browser-use` | Yes | 1/1  [usage](docs/browser-use_usage.md) |
| 76 | [hcaptcha-challenger](https://github.com/QIN2DIM/hcaptcha-challenger) | AI hCaptcha solver with Playwright | `hc` | `hoomzoom/hcaptcha-challenger` | Yes | 1/1  [usage](docs/hcaptcha-challenger_usage.md) |
| 77 | [BallonsTranslator](https://github.com/dmMaze/BallonsTranslator) | Manga/comic translator with OCR+inpainting | `python launch.py --headless` | `hoomzoom/ballonstranslator` | No | 1/1  [usage](docs/BallonsTranslator_usage.md) |
| 78 | [shell_gpt](https://github.com/TheR1D/shell_gpt) | CLI assistant with shell integration | `sgpt` | `hoomzoom/shell-gpt` | Yes | 1/1 | [usage](docs/shell_gpt_usage.md) |
| 79 | [zotero-arxiv-daily](https://github.com/TideDra/zotero-arxiv-daily) | Automated arxiv paper digest for Zotero | `python -m zotero_arxiv_daily` | `hoomzoom/zotero-arxiv-daily` | Yes | 1/1 | [usage](docs/zotero-arxiv-daily_usage.md) |

---

## Skipped Apps (23)

Cannot run meaningfully in Docker. Local install docs provided in `docs/`.

![Failure reasons pie chart](docs/benchmark/failure_reasons_pie.png)

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
| [AI_NovelGenerator](https://github.com/YILING0013/AI_NovelGenerator) | Desktop GUI (CustomTkinter), no headless mode |
| [AppAgent](https://github.com/TencentQQGYLab/AppAgent) | Requires Android device/ADB, no standalone mode |
| [Cradle](https://github.com/BAAI-Agents/Cradle) | Windows GUI automation (pyautogui, ahk), requires desktop + ADB |
| [ExtractThinker](https://github.com/enoch3712/ExtractThinker) | Library only, no entry point or web interface |
| [GLaDOS](https://github.com/dnhkng/GLaDOS) | Voice assistant requiring microphone/speaker hardware |
| [Open-Interface](https://github.com/AmberSahdev/Open-Interface) | Desktop GUI (Tkinter), controls host mouse/keyboard. macOS-only deps |
| [pandas-ai](https://github.com/sinaptik-ai/pandas-ai) | Library only, server/client dirs missing from repo |
| [UFO](https://github.com/microsoft/UFO) | Windows GUI automation agent (pywinauto, pywin32, UIA) |
| [wiseflow](https://github.com/TeamWiseFlow/wiseflow) | Requires real non-headless Chrome browser. No Docker support |
| [contextgem](https://github.com/shcherbak-ai/contextgem) | Library only, no entry point or web interface |
| [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) | Desktop GUI (PyQt5), no headless mode |
| [functionary](https://github.com/MeetKai/functionary) | Requires 24GB+ VRAM, no CPU fallback. vLLM/SGLang are GPU-only |
| [Linly-Talker](https://github.com/Kedreamix/Linly-Talker) | GPU required for video synthesis pipeline, no CPU fallback |
| [Codex-CLI](https://github.com/microsoft/Codex-CLI) | Shell integration hook, no HTTP interface. Targets deprecated OpenAI Codex model |
| [droidrun](https://github.com/droidrun/droidrun) | Requires physical Android/iOS device via ADB |

Full categorised breakdown, classification criteria, and per-category technical blockers: **[docs/DEPLOYMENT_FAILURE_ANALYSIS.md](docs/DEPLOYMENT_FAILURE_ANALYSIS.md)**. Pie chart is there too. Vector PDF and per-app CSV mapping in [`docs/benchmark/`](docs/benchmark/).

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
  docs/                    # Usage docs (*_usage.md), reasoning docs (*_reasoning.md), DEPLOYMENT_FAILURE_ANALYSIS.md
  docs/benchmark/          # Failure pie chart (PNG + PDF), PoC benchmark protocol, Dockerfile + attack.py templates
  v2_pinned_versions.md    # Manifest of all V2 dependency version changes
```

| What you need | Where to look |
|---------------|---------------|
| Original upstream source code | `apps/<name>/` (git submodules) |
| Pinned dependency files used for builds | `dockerfiles/<name>/` (requirements.txt, pyproject.toml, etc.) |
| Dockerfiles and compose files | `dockerfiles/<name>/` |
| What was changed and why | `docs/<name>_usage.md`, "V2 Dependency Changes" section |
| Quick reference of all version bumps | `v2_pinned_versions.md` |
| Why each skipped app was skipped, with categorised pie chart | `docs/DEPLOYMENT_FAILURE_ANALYSIS.md` |
| PoC benchmark protocol and per-PoC Dockerfile + attack.py templates | `docs/benchmark/BENCHMARK_PROTOCOL.md`, `docs/benchmark/_template_cli/`, `docs/benchmark/_template_server/` |

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
