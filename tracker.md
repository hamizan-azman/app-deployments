# App Deployment Tracker

## Completed (39/47)
| # | App | Status | Notes |
|---|-----|--------|-------|
| 1 | ChatDBG | DONE | CLI debugger, 7/7 tests |
| 2 | RD-Agent | DONE | CLI + Streamlit, 5/5 tests |
| 3 | Paper2Poster | DONE | CLI poster generator, 5/5 tests |
| 4 | pycorrector | DONE | Gradio UI, 6/6 tests |
| 5 | zshot | DONE | FastAPI wrapper, 4/4 tests |
| 6 | bilingual_book_maker | DONE | CLI translator |
| 7 | rawdog | DONE | CLI tool |
| 8 | slide-deck-ai | DONE | Slide generator |
| 9 | pdfGPT | DONE | langchain-serve + Gradio, 4/4 infra tests, API tests need key |
| 10 | omniparse | DONE | docker pull, FastAPI + Gradio, 5/5 tests (PDF, image OCR, web crawl) |
| 11 | agenticSeek | DONE | 4-service compose (backend+frontend+SearxNG+Redis), 8/8 tests |
| 12 | manga-image-translator | DONE | docker pull, web API, 5/5 tests |
| 13 | FunClip | DONE | Gradio, custom Dockerfile, 4/4 tests |
| 14 | gpt_academic | DONE | docker pull, Gradio |
| 15 | gpt-engineer | DONE | CLI, custom Dockerfile |
| 16 | codeqai | DONE | CLI + Streamlit, custom Dockerfile, 5/5 tests |
| 17 | codeinterpreter-api | DONE | Library, custom Dockerfile |
| 18 | chemcrow-public | DONE | Library, custom Dockerfile |
| 19 | gpt-migrate | DONE | CLI + Docker-in-Docker, custom Dockerfile, 5/6 tests (chat needs gpt-4-32k) |
| 20 | BettaFish | DONE | docker pull + PostgreSQL, 4/5 tests (engines need API keys) |
| 21 | localGPT | DONE | 4-service compose (frontend+backend+rag-api+ollama), 10/10 tests |
| 22 | NarratoAI | DONE | Streamlit |
| 23 | SWE-agent | DONE | docker pull, CLI + web UI, 10/10 tests |
| 24 | AgentGPT | DONE | 3-service compose (Next.js+FastAPI+MySQL), 9/9 tests |
| 25 | DataFlow | DONE | docker pull molyheci/dataflow:cu124, GPU, Gradio WebUI, 6/6 tests |
| 26 | HuixiangDou | DONE | Custom Dockerfile, Gradio + FastAPI, CPU-only, 7/7 tests |
| 27 | attackgen | DONE | Streamlit, existing Dockerfile, 5/5 tests |
| 28 | stride-gpt | DONE | Streamlit, existing Dockerfile, 2/2 tests |
| 29 | gpt-researcher | DONE | FastAPI + Web UI, existing Dockerfile, 4/4 tests |
| 30 | gptme | DONE | Flask + Web UI, two-stage build, 2/2 tests |
| 31 | local-deep-researcher | DONE | LangGraph API, existing Dockerfile, 4/4 tests |
| 32 | TaskWeaver | DONE | Chainlit web UI, custom Dockerfile, 4/4 tests |
| 33 | TradingAgents | DONE | CLI + library, custom Dockerfile, 3/3 tests (full run needs API key) |
| 34 | Integuru | DONE | CLI + Playwright, custom Dockerfile, 3/3 tests (HAR analysis needs API key) |
| 35 | django-ai-assistant | DONE | Django + React, multi-stage build, 5/5 tests (LLM chat needs API key) |
| 36 | pyvideotrans | DONE | CLI video translator, custom Dockerfile, 2/2 tests (transcription needs model download) |
| 37 | auto-news | DONE | docker pull finaldie/auto-news:0.9.15, Airflow 9-service compose, 6/6 tests |
| 38 | devika | IN PROGRESS | Dockerfiles + docs done, needs build + push (27GB backend) |
| 39 | magentic-ui | DONE | Docker-in-Docker, FastAPI + web UI, 2/2 tests (chat needs API key) |

## SKIP (8) -- local install docs in docs/
| App | Reason | Local Install Doc |
|-----|--------|-------------------|
| autoMate | Desktop RPA, requires GUI | docs/automate_usage.md |
| whispering | Requires audio device access | docs/whispering_usage.md |
| TaskMatrix | Needs 16GB+ VRAM (RTX 3070 insufficient) | docs/TaskMatrix_usage.md |
| MedRAX | Needs 12-16GB+ VRAM (RTX 3070 insufficient) | docs/MedRAX_usage.md |
| home-llm | Home Assistant integration, not standalone | docs/home-llm_usage.md |
| AiNiee | Desktop GUI (PyQt5), no headless mode | docs/AiNiee_usage.md |
| itext2kg | Library only, no web interface or entry point | docs/itext2kg_usage.md |
| Windrecorder | Windows-only desktop app (pywin32), requires screen | docs/windrecorder_usage.md |

## Docker Hub Images (hoomzoom/)
rawdog, bilingual_book_maker, chemcrow, codeinterpreter-api, pdfgpt-frontend, pdfgpt-langchain-serve, pdfgpt-backend, pdfgpt-pdf-gpt, agenticseek-frontend, agenticseek-backend, rd-agent, pycorrector, funclip, chatdbg, zshot, slidedeckai, codeqai, paper2poster, gpt-migrate, bettafish, localgpt-frontend, localgpt-backend, localgpt-rag-api, agentgpt-platform, agentgpt-frontend, dataflow, huixiangdou, omniparse, manga-image-translator, gpt_academic, swe-agent, gpt-engineer, narratoai, attackgen, stride-gpt, gpt-researcher, gptme-server, local-deep-researcher, taskweaver, tradingagents, integuru, django-ai-assistant, pyvideotrans, magentic-ui

## External Images (not ours)
ollama/ollama, finaldie/auto-news
