# App Deployment Tracker

## Completed (23/31)
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
| 11 | agenticSeek | DONE | 4-service compose (backend+frontend+SearxNG+Redis), 8/8 tests, deployed on desktop |
| 12 | manga-image-translator | DONE | docker pull zyddnys/manga-image-translator:main, web API, 5/5 tests |
| 13 | FunClip | DONE | Gradio, custom Dockerfile, 4/4 tests |
| 14 | gpt_academic | DONE | docker pull ghcr.io/binary-husky/gpt_academic_nolocal:master, Gradio, deployed on desktop |
| 15 | gpt-engineer | DONE | CLI, custom Dockerfile, deployed on desktop |
| 16 | codeqai | DONE | CLI + Streamlit, custom Dockerfile, 5/5 tests |
| 17 | codeinterpreter-api | DONE | Library, custom Dockerfile |
| 18 | chemcrow-public | DONE | Library, custom Dockerfile |
| 19 | gpt-migrate | DONE | CLI + Docker-in-Docker, custom Dockerfile, 5/6 tests (chat needs gpt-4-32k) |
| 20 | BettaFish | DONE | docker pull ghcr.io/666ghj/bettafish:latest + PostgreSQL, 4/5 tests (engines need API keys) |
| 21 | localGPT | DONE | 4-service compose (frontend+backend+rag-api+ollama), 10/10 tests |
| 22 | NarratoAI | DONE | Streamlit, deployed on desktop |
| 23 | SWE-agent | DONE | docker pull sweagent/swe-agent-run:latest, CLI + web UI, 10/10 tests, deployed on desktop |

## SKIP (6)
| App | Reason |
|-----|--------|
| autoMate | Desktop RPA, requires GUI, useless in Docker |
| whispering | Requires audio device access |
| AgentGPT | Archived repo, unmaintained |
| TaskMatrix | Heavy GPU requirement |
| MedRAX | GPU + multiple large models, no Dockerfile |
| home-llm | Home Assistant integration, not standalone |

## PULL-ONLY (2)
| App | Image | Reason |
|-----|-------|--------|
| DataFlow | molyheci/dataflow:cu124 | GPU required (CUDA 12.4) |
| HuixiangDou | tpoisonooo/huixiangdou:20240814 | Needs manual LLM config |

## Remaining (0)
All apps accounted for: 23 deployed + 6 skipped + 2 pull-only = 31 total.

## Docker Hub Images (hoomzoom/)
rawdog, bilingual_book_maker, chemcrow, codeinterpreter-api, pdfgpt-frontend, pdfgpt-langchain-serve, pdfgpt-backend, pdfgpt-pdf-gpt, agenticseek-frontend, agenticseek-backend, rd-agent, pycorrector, funclip, chatdbg, zshot, slidedeckai, codeqai, paper2poster, gpt-migrate, bettafish, localgpt-frontend, localgpt-backend, localgpt-rag-api

## Pre-existing Public Images (not pushed)
savatar101/omniparse:0.1, zyddnys/manga-image-translator:main, ghcr.io/binary-husky/gpt_academic_nolocal:master, ghcr.io/666ghj/bettafish:latest, ollama/ollama, sweagent/swe-agent-run:latest, molyheci/dataflow:cu124, tpoisonooo/huixiangdou:20240814
