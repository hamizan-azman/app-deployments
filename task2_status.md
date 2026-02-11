# Task 2 Deployment Status

84 total apps. 50 from Task 1 (mark status). 34 new (deploy and mark status).

## Task 1 Apps (Pre-filled from Task 1 results)

These 49 apps were handled in Task 1. Cross-reference with the Lark spreadsheet's 84-app list to identify which of the 50 overlap. The 50th app from the spreadsheet may be one not in Task 1.

### Successfully Deployed (41 apps)

| # | App | GitHub URL | Docker Image(s) | Status | Remark |
|---|-----|-----------|-----------------|--------|--------|
| 1 | AgentGPT | https://github.com/reworkd/AgentGPT | hoomzoom/agentgpt-frontend, hoomzoom/agentgpt-platform, mysql | success | Next.js + FastAPI + MySQL compose. Needs API key for chat. |
| 2 | agenticSeek | https://github.com/Fosowl/agenticSeek | hoomzoom/agenticseek-backend, hoomzoom/agenticseek-frontend | success | React + FastAPI compose. |
| 3 | attackgen | https://github.com/mrwadams/attackgen | hoomzoom/attackgen | success | Streamlit app. |
| 4 | auto-news | https://github.com/finaldie/auto-news | finaldie/auto-news:0.9.15 | success | Airflow compose (9 containers). External image used as-is. |
| 5 | BettaFish | https://github.com/666ghj/BettaFish | hoomzoom/bettafish | success | Flask + PostgreSQL compose. |
| 6 | bilingual_book_maker | https://github.com/yihong0618/bilingual_book_maker | hoomzoom/bilingual_book_maker | success | CLI tool. |
| 7 | Biomni | https://github.com/bowang-lab/Biomni | hoomzoom/biomni | success | Gradio app. |
| 8 | ChatDBG | https://github.com/plasma-umass/ChatDBG | hoomzoom/chatdbg | success | CLI debugger. |
| 9 | chemcrow-public | https://github.com/ur-whitelab/chemcrow-public | hoomzoom/chemcrow | success | Library. |
| 10 | codeinterpreter-api | https://github.com/shroominic/codeinterpreter-api | hoomzoom/codeinterpreter-api | success | Library. |
| 11 | codeqai | https://github.com/fynnfluegge/codeqai | hoomzoom/codeqai | success | Streamlit app. |
| 12 | Data-Copilot | https://github.com/zwq2018/Data-Copilot | hoomzoom/data-copilot | success | Gradio app. Conditional pass (needs Tushare token). |
| 13 | DataFlow | https://github.com/OpenDCAI/DataFlow | hoomzoom/dataflow | success | Gradio app. Requires GPU with CUDA 12.4+. |
| 14 | devika | https://github.com/stitionai/devika | hoomzoom/devika-backend, hoomzoom/devika-frontend | success | Svelte + Flask compose. |
| 15 | django-ai-assistant | https://github.com/vintasoftware/django-ai-assistant | hoomzoom/django-ai-assistant | success | Django + React. |
| 16 | FunClip | https://github.com/modelscope/FunClip | hoomzoom/funclip | success | Gradio app. Downloads 1.2GB models on first start. |
| 17 | gpt-engineer | https://github.com/AntonOsika/gpt-engineer | hoomzoom/gpt-engineer | success | CLI tool. |
| 18 | gpt-migrate | https://github.com/joshpxyne/gpt-migrate | hoomzoom/gpt-migrate | success | CLI tool. |
| 19 | gpt-researcher | https://github.com/assafelovic/gpt-researcher | hoomzoom/gpt-researcher | success | FastAPI + Web UI. |
| 20 | gpt_academic | https://github.com/binary-husky/gpt_academic | hoomzoom/gpt_academic | success | Gradio app. |
| 21 | gptme | https://github.com/ErikBjare/gptme | hoomzoom/gptme-server | success | Flask app. |
| 22 | HuixiangDou | https://github.com/InternLM/HuixiangDou | hoomzoom/huixiangdou | success | Gradio + FastAPI. Complex era-matched deps. |
| 23 | Integuru | https://github.com/Integuru-AI/Integuru | hoomzoom/integuru | success | CLI tool. Poetry-based. |
| 24 | local-deep-researcher | https://github.com/langchain-ai/local-deep-researcher | hoomzoom/local-deep-researcher | success | LangGraph API. |
| 25 | localGPT | https://github.com/PromtEngineer/localGPT | hoomzoom/localgpt-backend, hoomzoom/localgpt-frontend, hoomzoom/localgpt-rag-api | success | React + FastAPI compose (3 images). |
| 26 | magentic-ui | https://github.com/microsoft/magentic-one | hoomzoom/magentic-ui | success | FastAPI + Web UI. |
| 27 | manga-image-translator | https://github.com/zyddnys/manga-image-translator | hoomzoom/manga-image-translator | success | Web API. Conditional pass (full translation needs GPU). |
| 28 | NarratoAI | https://github.com/linyqh/NarratoAI | hoomzoom/narratoai | success | Streamlit app. |
| 29 | omniparse | https://github.com/adithya-s-k/omniparse | hoomzoom/omniparse | success | FastAPI + Gradio. |
| 30 | Paper2Poster | https://github.com/Paper2Poster/Paper2Poster | hoomzoom/paper2poster | success | CLI tool. |
| 31 | pdfGPT | https://github.com/bhaskatripathi/pdfGPT | hoomzoom/pdfgpt-frontend, hoomzoom/pdfgpt-backend | success | Gradio + langchain-serve compose (4 images). |
| 32 | pycorrector | https://github.com/shibing624/pycorrector | hoomzoom/pycorrector | success | Gradio app. |
| 33 | pyvideotrans | https://github.com/jianchang512/pyvideotrans | hoomzoom/pyvideotrans | success | CLI tool. |
| 34 | rawdog | https://github.com/AbanteAI/rawdog | hoomzoom/rawdog | success | CLI tool. |
| 35 | RD-Agent | https://github.com/microsoft/RD-Agent | hoomzoom/rd-agent | success | Streamlit + CLI. |
| 36 | slide-deck-ai | https://github.com/barun-saha/slide-deck-ai | hoomzoom/slidedeckai | success | Streamlit app. |
| 37 | stride-gpt | https://github.com/mrwadams/stride-gpt | hoomzoom/stride-gpt | success | Streamlit app. |
| 38 | SWE-agent | https://github.com/SWE-agent/SWE-agent | hoomzoom/swe-agent | success | Web UI + CLI. Needs Docker socket access. |
| 39 | TaskWeaver | https://github.com/microsoft/TaskWeaver | hoomzoom/taskweaver | success | Chainlit app. |
| 40 | TradingAgents | https://github.com/TauricResearch/TradingAgents | hoomzoom/tradingagents | success | CLI tool. |
| 41 | zshot | https://github.com/IBM/zshot | hoomzoom/zshot | success | FastAPI app. |

### Skipped / Failed (8 apps)

| # | App | GitHub URL | Status | Remark |
|---|-----|-----------|--------|--------|
| 1 | AiNiee | https://github.com/NEKOparapa/AiNiee | fail | Desktop GUI (PyQt5), no headless mode. Cannot be containerized. |
| 2 | autoMate | https://github.com/yuruotong1/autoMate | fail | Desktop RPA, requires GUI and mouse/keyboard control. Cannot be containerized. |
| 3 | home-llm | https://github.com/acon96/home-llm | fail | Home Assistant integration, not standalone. Cannot be containerized. |
| 4 | itext2kg | https://github.com/AuvaLab/itext2kg | fail | Library only, no web interface or entry point. Cannot be containerized. |
| 5 | MedRAX | https://github.com/bowang-lab/MedRAX | fail | Needs 12-16GB+ VRAM, multiple medical imaging models. Cannot be containerized. |
| 6 | TaskMatrix | https://github.com/chenfei-wu/TaskMatrix | fail | Needs 16GB+ VRAM (multiple vision models). Cannot be containerized. |
| 7 | whispering | https://github.com/Sharrnah/whispering | fail | Requires microphone/audio device access. Cannot be containerized. |
| 8 | Windrecorder | https://github.com/Antonoko/Windrecorder | fail | Windows-only desktop app, requires screen capture. Cannot be containerized. |

## Task 2 New Apps (35 apps)

35 new apps identified from Lark spreadsheet. 26 deployable, 9 skipped.

### Deployable (26 apps)

| # | App | GitHub URL | Docker Image(s) | Status | Remark |
|---|-----|-----------|-----------------|--------|--------|
| 1 | aider | https://github.com/Aider-AI/aider | hoomzoom/aider | success | CLI tool. Installed from PyPI. QC: --help passes. |
| 2 | BabelDOC | https://github.com/funstory-ai/BabelDOC | hoomzoom/babeldoc | success | CLI PDF translator. QC: --help passes. |
| 3 | BallonsTranslator | https://github.com/dmMaze/BallonsTranslator | hoomzoom/ballonstranslator | success | Headless manga translator. QC: torch+cv2 import passes. CPU-only PyTorch. |
| 4 | BiliNote | https://github.com/JefferyHcool/BiliNote | hoomzoom/bilinote | success | FastAPI backend (port 8483). Conditional: needs --security-opt seccomp=unconfined for ctranslate2. |
| 5 | browser-use | https://github.com/browser-use/browser-use | hoomzoom/browser-use | success | CLI/Library. Playwright+Chromium. QC: --help passes. |
| 6 | BruteForceAI | https://github.com/MorDavid/BruteForceAI | hoomzoom/bruteforceai | success | CLI. Playwright. QC: import passes. |
| 7 | ChatDev | https://github.com/OpenBMB/ChatDev | hoomzoom/chatdev | success | FastAPI backend (port 6400). QC: /docs returns 200. |
| 8 | chatgpt_telegram_bot | https://github.com/father-bot/chatgpt_telegram_bot | hoomzoom/chatgpt-telegram-bot | success | Telegram bot + MongoDB compose. QC: telegram import passes. |
| 9 | DATAGEN | https://github.com/starpig1129/DATAGEN | hoomzoom/datagen | success | CLI with Chrome+ChromeDriver. QC: langchain import passes. |
| 10 | Decepticon | https://github.com/PurpleAILAB/Decepticon | (pre-built images) | success | Compose-only deployment. Uses upstream pre-built images via docker-compose. |
| 11 | DeepGit | https://github.com/zamalali/DeepGit | hoomzoom/deepgit | success | Gradio (port 7860). QC: /gradio_api/info returns 200 from host. |
| 12 | deepwiki-open | https://github.com/AsyncFuncAI/deepwiki-open | hoomzoom/deepwiki-open | success | Next.js+FastAPI (ports 3000, 8001). QC: fastapi import passes. |
| 13 | docetl | https://github.com/ucbepic/docetl | hoomzoom/docetl | success | FastAPI+Next.js (ports 3000, 8000). QC: image built and pushed. |
| 14 | FinGenius | https://github.com/HuaYaoAI/FinGenius | hoomzoom/fingenius | success | CLI financial analysis. QC: main.py --help passes. |
| 15 | gpt-pilot | https://github.com/Pythagora-io/gpt-pilot | hoomzoom/gpt-pilot | success | CLI (custom slim Dockerfile, no code-server). QC: import passes. |
| 16 | hackingBuddyGPT | https://github.com/ipa-lab/hackingBuddyGPT | hoomzoom/hackingbuddygpt | success | CLI pentest framework. Conditional: template files missing from pip install, startup may fail on some usecases. |
| 17 | hcaptcha-challenger | https://github.com/QIN2DIM/hcaptcha-challenger | hoomzoom/hcaptcha-challenger | success | CLI+Playwright. Conditional: uv sync issue, package not fully installed in image. |
| 18 | MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | hoomzoom/moneyprinterturbo | success | Streamlit+FastAPI. QC: streamlit import passes. Needs config.toml for full startup. |
| 19 | morphik-core | https://github.com/morphik-org/morphik-core | hoomzoom/morphik-core | success | FastAPI+worker+PostgreSQL+Redis compose. CPU-only torch. QC: fastapi import passes. |
| 20 | Open-LLM-VTuber | https://github.com/Open-LLM-VTuber/Open-LLM-VTuber | hoomzoom/open-llm-vtuber | success | FastAPI/WebSocket (port 12393). QC: fastapi import passes. Needs conf.yaml volume mount. |
| 21 | pr-agent | https://github.com/qodo-ai/pr-agent | hoomzoom/pr-agent | success | FastAPI webhook (port 3000). QC: import passes. |
| 22 | PocketFlow-Tutorial-Codebase-Knowledge | https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge | hoomzoom/pocketflow | success | CLI codebase tutorial generator. QC: main.py runs. |
| 23 | readme-ai | https://github.com/eli64s/readme-ai | hoomzoom/readme-ai | success | CLI README generator. QC: --help passes. |
| 24 | skyvern | https://github.com/Skyvern-AI/skyvern | hoomzoom/skyvern | success | FastAPI+Playwright+VNC compose (ports 8000, 8080, 6080). QC: import passes. |
| 25 | vulnhuntr | https://github.com/protectai/vulnhuntr | hoomzoom/vulnhuntr | success | CLI vuln scanner. QC: --help passes. |
| 26 | ai-goofish-monitor | https://github.com/Usagi-org/ai-goofish-monitor | hoomzoom/ai-goofish-monitor | success | FastAPI+Vue (port 8000). Playwright. QC: fastapi import passes. |

### Skipped (9 apps)

| # | App | GitHub URL | Status | Remark |
|---|-----|-----------|--------|--------|
| 1 | AI_NovelGenerator | https://github.com/YILING0013/AI_NovelGenerator | fail | Desktop GUI (CustomTkinter), no headless mode. |
| 2 | AppAgent | https://github.com/TencentQQGYLab/AppAgent | fail | Requires Android device/ADB. No standalone mode. |
| 3 | Cradle | https://github.com/BAAI-Agents/Cradle | fail | Windows GUI automation (pyautogui, ahk). Requires desktop + ADB. |
| 4 | ExtractThinker | https://github.com/enoch3712/ExtractThinker | fail | Library only, no entry point or web interface. |
| 5 | GLaDOS | https://github.com/dnhkng/GLaDOS | fail | Voice assistant requiring microphone/speaker hardware. |
| 6 | Open-Interface | https://github.com/AmberSahdev/Open-Interface | fail | Desktop GUI (Tkinter), controls host mouse/keyboard. macOS-only deps. |
| 7 | pandas-ai | https://github.com/sinaptik-ai/pandas-ai | fail | Library only. docker-compose references missing server/client dirs. |
| 8 | UFO | https://github.com/microsoft/UFO | fail | Windows GUI automation agent (pywinauto, pywin32, UIA). |
| 9 | wiseflow | https://github.com/TeamWiseFlow/wiseflow | fail | Requires real non-headless Chrome browser. No Docker support. |
