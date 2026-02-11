# Task 2: All 84 Applications

Source: Applist.xlsx, Total_Task_84 tab. Extracted 2026-04-07.

## Discrepancies to Note

1. **gptme**: Spreadsheet says `github.com/gptme/gptme`, Task 1 used `github.com/ErikBjare/gptme`. Repo was transferred to the gptme org. Same project. Mark as success.
2. **TaskMatrix**: Spreadsheet says `github.com/chenfei-wu/TaskMatrix`, Task 1 used `github.com/microsoft/TaskMatrix`. Repo was transferred. Same project. Mark as fail (skipped, needs 16GB+ VRAM).
3. **Count**: Spreadsheet says "50 deployed in Task 1" but Task1_50 sheet has 49 data rows. Our Task 1 had 49 apps. The 84 list has 49 overlapping with Task 1, leaving 35 new apps (not 34).

## 49 Apps from Task 1 (pre-filled status)

| ID | App | GitHub URL | Status | Remark |
|----|-----|-----------|--------|--------|
| 1 | gpt_academic | https://github.com/binary-husky/gpt_academic | success | Gradio app. Docker image: hoomzoom/gpt_academic |
| 2 | AgentGPT | https://github.com/reworkd/AgentGPT | success | Next.js + FastAPI + MySQL compose. Docker images: hoomzoom/agentgpt-frontend, hoomzoom/agentgpt-platform |
| 3 | RD-Agent | https://github.com/microsoft/RD-Agent | success | Streamlit + CLI. Docker image: hoomzoom/rd-agent |
| 4 | magentic-ui | https://github.com/microsoft/magentic-ui | success | FastAPI + Web UI. Docker image: hoomzoom/magentic-ui |
| 5 | TaskWeaver | https://github.com/microsoft/TaskWeaver | success | Chainlit app. Docker image: hoomzoom/taskweaver |
| 7 | zshot | https://github.com/IBM/zshot | success | FastAPI app. Docker image: hoomzoom/zshot |
| 9 | Windrecorder | https://github.com/yuka-friends/Windrecorder | fail | Windows-only desktop app, requires screen capture. Cannot be containerized. |
| 10 | whispering | https://github.com/Sharrnah/whispering | fail | Requires microphone/audio device access. Cannot be containerized. |
| 13 | TradingAgents | https://github.com/TauricResearch/TradingAgents | success | CLI tool. Docker image: hoomzoom/tradingagents |
| 14 | TaskMatrix | https://github.com/chenfei-wu/TaskMatrix | fail | Needs 16GB+ VRAM (multiple vision models). Cannot be containerized. |
| 15 | SWE-agent | https://github.com/SWE-agent/SWE-agent | success | Web UI + CLI. Docker image: hoomzoom/swe-agent. Needs Docker socket access. |
| 16 | stride-gpt | https://github.com/mrwadams/stride-gpt | success | Streamlit app. Docker image: hoomzoom/stride-gpt |
| 17 | slide-deck-ai | https://github.com/barun-saha/slide-deck-ai | success | Streamlit app. Docker image: hoomzoom/slidedeckai |
| 20 | rawdog | https://github.com/AbanteAI/rawdog | success | CLI tool. Docker image: hoomzoom/rawdog |
| 21 | pyvideotrans | https://github.com/jianchang512/pyvideotrans | success | CLI tool. Docker image: hoomzoom/pyvideotrans |
| 22 | pycorrector | https://github.com/shibing624/pycorrector | success | Gradio app. Docker image: hoomzoom/pycorrector |
| 25 | pdfGPT | https://github.com/bhaskatripathi/pdfGPT | success | Gradio + langchain-serve compose. Docker images: hoomzoom/pdfgpt-frontend, hoomzoom/pdfgpt-backend |
| 26 | Paper2Poster | https://github.com/Paper2Poster/Paper2Poster | success | CLI tool. Docker image: hoomzoom/paper2poster |
| 30 | omniparse | https://github.com/adithya-s-k/omniparse | success | FastAPI + Gradio. Docker image: hoomzoom/omniparse |
| 31 | NarratoAI | https://github.com/linyqh/NarratoAI | success | Streamlit app. Docker image: hoomzoom/narratoai |
| 34 | MedRAX | https://github.com/bowang-lab/MedRAX | fail | Needs 12-16GB+ VRAM, multiple medical imaging models. Cannot be containerized. |
| 35 | manga-image-translator | https://github.com/zyddnys/manga-image-translator | success | Web API. Docker image: hoomzoom/manga-image-translator. Full translation needs GPU. |
| 36 | localGPT | https://github.com/PromtEngineer/localGPT | success | React + FastAPI compose. Docker images: hoomzoom/localgpt-backend, hoomzoom/localgpt-frontend, hoomzoom/localgpt-rag-api |
| 37 | local-deep-researcher | https://github.com/langchain-ai/local-deep-researcher | success | LangGraph API. Docker image: hoomzoom/local-deep-researcher |
| 38 | itext2kg | https://github.com/AuvaLab/itext2kg | fail | Library only, no web interface or entry point. Cannot be containerized. |
| 39 | Integuru | https://github.com/Integuru-AI/Integuru | success | CLI tool. Docker image: hoomzoom/integuru |
| 40 | HuixiangDou | https://github.com/InternLM/HuixiangDou | success | Gradio + FastAPI. Docker image: hoomzoom/huixiangdou |
| 41 | home-llm | https://github.com/acon96/home-llm | fail | Home Assistant integration, not standalone. Cannot be containerized. |
| 43 | gptme | https://github.com/gptme/gptme | success | Flask app. Docker image: hoomzoom/gptme-server. Note: Task 1 used ErikBjare/gptme (now transferred to gptme org). |
| 44 | gpt-researcher | https://github.com/assafelovic/gpt-researcher | success | FastAPI + Web UI. Docker image: hoomzoom/gpt-researcher |
| 46 | gpt-migrate | https://github.com/joshpxyne/gpt-migrate | success | CLI tool. Docker image: hoomzoom/gpt-migrate |
| 47 | gpt-engineer | https://github.com/AntonOsika/gpt-engineer | success | CLI tool. Docker image: hoomzoom/gpt-engineer |
| 49 | FunClip | https://github.com/modelscope/FunClip | success | Gradio app. Docker image: hoomzoom/funclip. Downloads 1.2GB models on first start. |
| 53 | django-ai-assistant | https://github.com/vintasoftware/django-ai-assistant | success | Django + React. Docker image: hoomzoom/django-ai-assistant |
| 54 | devika | https://github.com/stitionai/devika | success | Svelte + Flask compose. Docker images: hoomzoom/devika-backend, hoomzoom/devika-frontend |
| 58 | DataFlow | https://github.com/OpenDCAI/DataFlow | success | Gradio app. Docker image: hoomzoom/dataflow. Requires GPU with CUDA 12.4+. |
| 59 | Data-Copilot | https://github.com/zwq2018/Data-Copilot | success | Gradio app. Docker image: hoomzoom/data-copilot. Needs Tushare token for full functionality. |
| 61 | codeqai | https://github.com/fynnfluegge/codeqai | success | Streamlit app. Docker image: hoomzoom/codeqai |
| 62 | codeinterpreter-api | https://github.com/shroominic/codeinterpreter-api | success | Library. Docker image: hoomzoom/codeinterpreter-api |
| 63 | chemcrow-public | https://github.com/ur-whitelab/chemcrow-public | success | Library. Docker image: hoomzoom/chemcrow |
| 66 | ChatDBG | https://github.com/plasma-umass/ChatDBG | success | CLI debugger. Docker image: hoomzoom/chatdbg |
| 69 | Biomni | https://github.com/snap-stanford/Biomni | success | Gradio app. Docker image: hoomzoom/biomni |
| 71 | bilingual_book_maker | https://github.com/yihong0618/bilingual_book_maker | success | CLI tool. Docker image: hoomzoom/bilingual_book_maker |
| 72 | BettaFish | https://github.com/666ghj/BettaFish | success | Flask + PostgreSQL compose. Docker image: hoomzoom/bettafish |
| 75 | autoMate | https://github.com/yuruotong1/autoMate | fail | Desktop RPA, requires GUI and mouse/keyboard control. Cannot be containerized. |
| 76 | auto-news | https://github.com/finaldie/auto-news | success | Airflow compose (9 containers). External image: finaldie/auto-news:0.9.15 |
| 77 | attackgen | https://github.com/mrwadams/attackgen | success | Streamlit app. Docker image: hoomzoom/attackgen |
| 79 | AiNiee | https://github.com/NEKOparapa/AiNiee | fail | Desktop GUI (PyQt5), no headless mode. Cannot be containerized. |
| 83 | agenticSeek | https://github.com/Fosowl/agenticSeek | success | React + FastAPI compose. Docker images: hoomzoom/agenticseek-backend, hoomzoom/agenticseek-frontend |

## 35 New Apps to Deploy

| ID | App | GitHub URL | Status | Remark |
|----|-----|-----------|--------|--------|
| 6 | hackingBuddyGPT | https://github.com/ipa-lab/hackingBuddyGPT | | |
| 8 | wiseflow | https://github.com/TeamWiseFlow/wiseflow | | |
| 11 | vulnhuntr | https://github.com/protectai/vulnhuntr | | |
| 12 | UFO | https://github.com/microsoft/UFO | | |
| 18 | skyvern | https://github.com/Skyvern-AI/skyvern | | |
| 19 | readme-ai | https://github.com/eli64s/readme-ai | | |
| 23 | pr-agent | https://github.com/qodo-ai/pr-agent | | |
| 24 | PocketFlow-Tutorial-Codebase-Knowledge | https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge | | |
| 27 | pandas-ai | https://github.com/sinaptik-ai/pandas-ai | | |
| 28 | Open-LLM-VTuber | https://github.com/Open-LLM-VTuber/Open-LLM-VTuber | | |
| 29 | Open-Interface | https://github.com/AmberSahdev/Open-Interface | | |
| 32 | morphik-core | https://github.com/morphik-org/morphik-core | | |
| 33 | MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | | |
| 42 | hcaptcha-challenger | https://github.com/QIN2DIM/hcaptcha-challenger | | |
| 45 | gpt-pilot | https://github.com/Pythagora-io/gpt-pilot | | |
| 48 | GLaDOS | https://github.com/dnhkng/GLaDOS | | |
| 50 | FinGenius | https://github.com/HuaYaoAI/FinGenius | | |
| 51 | ExtractThinker | https://github.com/enoch3712/ExtractThinker | | |
| 52 | docetl | https://github.com/ucbepic/docetl | | |
| 55 | deepwiki-open | https://github.com/AsyncFuncAI/deepwiki-open | | |
| 56 | DeepGit | https://github.com/zamalali/DeepGit | | |
| 57 | DATAGEN | https://github.com/starpig1129/DATAGEN | | |
| 60 | Cradle | https://github.com/BAAI-Agents/Cradle | | |
| 64 | chatgpt_telegram_bot | https://github.com/father-bot/chatgpt_telegram_bot | | |
| 65 | ChatDev | https://github.com/OpenBMB/ChatDev | | |
| 67 | BruteForceAI | https://github.com/MorDavid/BruteForceAI | | |
| 68 | browser-use | https://github.com/browser-use/browser-use | | |
| 70 | BiliNote | https://github.com/JefferyHcool/BiliNote | | |
| 73 | BallonsTranslator | https://github.com/dmMaze/BallonsTranslator | | |
| 74 | BabelDOC | https://github.com/funstory-ai/BabelDOC | | |
| 78 | AppAgent | https://github.com/TencentQQGYLab/AppAgent | | |
| 80 | aider | https://github.com/Aider-AI/aider | | |
| 81 | ai-goofish-monitor | https://github.com/Usagi-org/ai-goofish-monitor | | |
| 82 | AI_NovelGenerator | https://github.com/YILING0013/AI_NovelGenerator | | |
| 84 | Decepticon | https://github.com/PurpleAILAB/Decepticon | | |
