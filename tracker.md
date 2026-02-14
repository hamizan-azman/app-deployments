# App Deployment Tracker

## Completed (10/31)
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

## Remaining (23) -- Ranked Easiest to Hardest

### Easy
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 9 | autoMate | https://github.com/yuruotong1/autoMate | Desktop RPA | No | None | OpenAI | SKIP -- desktop automation tool, useless in Docker |
| 10 | ~~pdfGPT~~ | ~~https://github.com/bhaskatripathi/pdfGPT~~ | ~~Gradio~~ | ~~Yes~~ | ~~None~~ | ~~OpenAI~~ | ~~DONE~~ |
| 11 | codeinterpreter-api | https://github.com/shroominic/codeinterpreter-api | Library/SDK | No | None | OpenAI | Easy |
| 12 | gpt-engineer | https://github.com/AntonOsika/gpt-engineer | CLI | Yes | None | OpenAI | Easy |

### Medium
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 13 | codeqai | https://github.com/fynnfluegge/codeqai | CLI + Streamlit | No | None | OpenAI | Medium |
| 14 | gpt_academic | https://github.com/binary-husky/gpt_academic | Gradio web | Yes | None | OpenAI | Medium |
| 15 | DataFlow | https://github.com/OpenDCAI/DataFlow | CLI/web/lib | Yes | None | Optional | Medium |
| 16 | NarratoAI | https://github.com/linyqh/NarratoAI | Streamlit web | Yes | None | LLM + TTS | Medium |
| 17 | FunClip | https://github.com/modelscope/FunClip | Gradio | No | None | Optional | Medium |
| 18 | SWE-agent | https://github.com/SWE-agent/SWE-agent | CLI | No | None | OpenAI | Medium |
| 19 | gpt-migrate | https://github.com/joshpxyne/gpt-migrate | CLI | No | Docker-in-Docker | OpenAI | Medium |
| 20 | chemcrow-public | https://github.com/ur-whitelab/chemcrow-public | Library | Yes | Optional | OpenAI + SerpAPI | Medium |
| 21 | manga-image-translator | https://github.com/zyddnys/manga-image-translator | CLI/Web/API | Yes | None | Optional | Medium |
| 22 | ~~omniparse~~ | ~~https://github.com/adithya-s-k/omniparse~~ | ~~API + Gradio~~ | ~~Yes~~ | ~~None~~ | ~~None (local)~~ | ~~DONE~~ |
| 23 | whispering | https://github.com/Sharrnah/whispering | CLI | No | None | None | Medium |

### Hard
| # | App | URL | Type | Has Dockerfile | External Services | API Keys | Difficulty |
|---|-----|-----|------|----------------|-------------------|----------|------------|
| 24 | agenticSeek | https://github.com/Fosowl/agenticSeek | Web + API | Yes | Redis + SearxNG | Optional | Hard |
| 25 | BettaFish | https://github.com/666ghj/BettaFish | Web | Yes | PostgreSQL + Playwright | Multiple LLMs | Hard |
| 26 | HuixiangDou | https://github.com/InternLM/HuixiangDou | CLI/Web/API | Yes | FAISS + Redis | LLM services | Hard |
| 27 | AgentGPT | https://github.com/reworkd/AgentGPT | Web | Yes | MySQL | OpenAI | Hard |
| 28 | TaskMatrix | https://github.com/chenfei-wu/TaskMatrix | CLI | Yes | None (GPU req) | OpenAI | Hard |
| 29 | MedRAX | https://github.com/bowang-lab/MedRAX | Web | No | None (GPU req) | OpenAI | Hard |
| 30 | localGPT | https://github.com/PromtEngineer/localGPT | Web + API | Yes | Ollama | None | Hard |
| 31 | home-llm | https://github.com/acon96/home-llm | HA integration | No (compose) | Home Assistant | None | Hard |
