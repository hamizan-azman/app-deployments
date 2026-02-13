# App Deployment Tracker

## Docker Hub
All custom-built images pushed to `hoomzoom/` on Docker Hub.
Pre-pulled images also mirrored under `hoomzoom/` for convenience.

## Completed (19/31)
| # | App | Status | Docker Pull | Notes |
|---|-----|--------|-------------|-------|
| 1 | ChatDBG | DONE | `docker pull hoomzoom/chatdbg` | CLI debugger, 7/7 tests |
| 2 | RD-Agent | DONE | `docker pull hoomzoom/rd-agent` | CLI + Streamlit, 5/5 tests |
| 3 | Paper2Poster | DONE | `docker pull hoomzoom/paper2poster` | CLI poster generator, 5/5 tests |
| 4 | pycorrector | DONE | `docker pull hoomzoom/pycorrector` | Gradio UI, 6/6 tests |
| 5 | zshot | DONE | `docker pull hoomzoom/zshot` | FastAPI wrapper, 4/4 tests |
| 6 | bilingual_book_maker | DONE | `docker pull hoomzoom/bilingual_book_maker` | CLI translator |
| 7 | rawdog | DONE | `docker pull hoomzoom/rawdog` | CLI tool |
| 8 | slide-deck-ai | DONE | `docker pull hoomzoom/slidedeckai` | Slide generator |
| 9 | pdfGPT | DONE | `docker pull hoomzoom/pdfgpt-backend` | langchain-serve + Gradio, 4/4 infra tests. Also: pdfgpt-frontend, pdfgpt-langchain-serve, pdfgpt-pdf-gpt |
| 10 | omniparse | DONE | `docker pull hoomzoom/omniparse` | FastAPI + Gradio, 5/5 tests (PDF, image OCR, web crawl) |
| 11 | manga-image-translator | DONE | `docker pull hoomzoom/manga-image-translator` | FastAPI + Web UI, 6/6 tests (translate, queue, results, UI, docs, manual) |
| 12 | codeqai | DONE | `docker pull hoomzoom/codeqai` | Streamlit + CLI, 5/5 tests (UI, health, config, FAISS index, config file) |
| 13 | chemcrow-public | DONE | `docker pull hoomzoom/chemcrow` | Library, 6/6 tests (import, tools, MW, func groups, similarity, versions) |
| 14 | FunClip | DONE | `docker pull hoomzoom/funclip` | Gradio, deployed on laptop L2 |
| 15 | codeinterpreter-api | DONE | `docker pull hoomzoom/codeinterpreter-api` | Library/SDK, deployed on laptop L2 |
| 16 | gpt_academic | DONE | `docker pull hoomzoom/gpt_academic` | Gradio web, deployed on desktop D1 |
| 17 | gpt-engineer | DONE | `docker pull hoomzoom/gpt-engineer` | CLI, deployed on desktop D2 |
| 18 | NarratoAI | DONE | `docker pull hoomzoom/narratoai` | Streamlit web, deployed on desktop D1 |
| 19 | SWE-agent | DONE | `docker pull hoomzoom/swe-agent` | CLI, deployed on desktop D2 |

## In Progress
| App | Status | Notes |
|-----|--------|-------|
| agenticSeek | STARTED | Repo cloned, config.ini modified for OpenAI, needs docker compose build. Blocked by disk space. |

## Remaining (11) -- Ranked Easiest to Hardest

### Easy
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 1 | autoMate | https://github.com/yuruotong1/autoMate | Desktop RPA | No | None | OpenAI | SKIP -- desktop automation tool, useless in Docker |

### Medium
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 2 | DataFlow | https://github.com/OpenDCAI/DataFlow | CLI/web/lib | Yes | None | Optional | Medium |
| 3 | whispering | https://github.com/Sharrnah/whispering | CLI | No | None | None | Medium |
| 4 | gpt-migrate | https://github.com/joshpxyne/gpt-migrate | CLI | No | Docker-in-Docker | OpenAI | Medium |

### Hard
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 5 | agenticSeek | https://github.com/Fosowl/agenticSeek | Web + API | Yes | Redis + SearxNG | Optional | Hard |
| 6 | BettaFish | https://github.com/666ghj/BettaFish | Web | Yes | PostgreSQL + Playwright | Multiple LLMs | Hard |
| 7 | HuixiangDou | https://github.com/InternLM/HuixiangDou | CLI/Web/API | Yes | FAISS + Redis | LLM services | Hard |
| 8 | AgentGPT | https://github.com/reworkd/AgentGPT | Web | Yes | MySQL | OpenAI | Hard |
| 9 | TaskMatrix | https://github.com/chenfei-wu/TaskMatrix | CLI | Yes | None (GPU req) | OpenAI | Hard |
| 10 | MedRAX | https://github.com/bowang-lab/MedRAX | Web | No | None (GPU req) | OpenAI | Hard |
| 11 | localGPT | https://github.com/PromtEngineer/localGPT | Web + API | Yes | Ollama | None | Hard |
| 12 | home-llm | https://github.com/acon96/home-llm | HA integration | No (compose) | Home Assistant | None | Hard |
