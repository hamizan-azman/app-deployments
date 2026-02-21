# V2 Minimum Version Pinning — Manifest

This document summarizes all dependency version changes made during V2 minimum version pinning across all 49 apps.

**Goal:** Convert all `>=`, `~=`, `^` specifiers to `==` (exact pins at the minimum declared version). Where the minimum version doesn't exist or causes conflicts, bump to the nearest working version.

---

## Apps With Dependency Bumps

### agenticSeek
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| playsound3 | >=1.0.0 | ==3.0.0 | 1.0.0 doesn't exist on PyPI; 2.0.0 requires pygobject/Cairo system deps |
| together | >=1.5.0 | ==1.5.2 | 1.5.0 doesn't exist on PyPI |
| tqdm | >=4 | ==4.66.2 | together 1.5.2 requires tqdm>=4.66.2 |

### BettaFish
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| opencv-python | >=4.8.0 | ==4.8.0.74 | 4.8.0 doesn't exist on PyPI |
| black | >=23.0.0 | ==23.1.0 | 23.0.0 doesn't exist on PyPI |
| psycopg[binary] | >=3.1.0 | ==3.1.8 | 3.1.0 binary wheel not available for Python 3.11 |

### chemcrow-public
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| langchain_core | >=0.0.1 | *(removed)* | Incompatible with langchain==0.0.234 which predates the langchain_core split |

### django-ai-assistant
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| openai | ^1.48.0 | ==1.109.1 | langchain-openai==1.1.7 requires openai>=1.109.1 |

### gpt-engineer
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| tiktoken | >=0.0.4 | ==0.7.0 | 0.0.4 doesn't exist; langchain-openai requires >=0.7 |
| langchain | ^0.1.2 | ==0.2.0 | 0.1.2 incompatible with langchain-community==0.2.0 |
| langchain-anthropic | ^0.1.1 | ==0.1.13 | 0.1.1 needs langchain-core<0.2 |
| langchain_openai | * | ==0.1.7 | Compatible version for langchain 0.2.x |
| openai | ^1.0 | ==1.24.0 | langchain-openai 0.1.7 requires openai>=1.24.0 |
| typer | ^0.3.2 | ==0.9.0 | 0.3.2 needs click<7.2 which conflicts with black |
| poetry-core | >=1.0.0 | *(left unpinned)* | 1.0.0 doesn't support PEP 660 editable installs |

### gpt-researcher
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| unstructured | >=0.13 | ==0.14.2 | 0.13 doesn't exist on PyPI; 0.13.x requires Python <3.12 |
| lxml | >=4.9.2 | ==4.9.3 | 4.9.2 fails to build on Python 3.12 |
| langgraph | >=0.2.76 | ==1.0.0 | langchain 1.0.0 requires langgraph>=1.0.0 |

### HuixiangDou
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| pydantic | ==1.10.13 | ==2.0.0 | gradio 4.44.1 requires pydantic>=2.0 |

### NarratoAI
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| openai | ==1.77.0 | ==1.75.0 | litellm 1.70.0 requires openai<1.76.0 |

### stride-gpt
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| streamlit | >=1.40 | ==1.40.0 | 1.40 doesn't exist on PyPI; 1.40.0 is the actual release |

### TaskWeaver
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| matplotlib | ==3.4 | ==3.7.0 | 3.4 has no prebuilt wheels for Python 3.12, fails to build from source |
| seaborn | ==0.11 | ==0.11.0 | Version format fix |
| pyyaml | ==6.0 | ==6.0.0 | Version format fix |

### zshot
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| torch | ==1 | ==2.0.0 | 1.x fails with libtorch executable stack error under QEMU; version "1" invalid |
| requests | ==2.28 | ==2.28.0 | Version format fix |
| prettytable | ==3.4 | ==3.4.0 | Version format fix |

### Biomni (partial)
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| setuptools | >=61.0 | *(left unpinned)* | Project uses PEP 639 license format requiring setuptools>=77 |
| gradio | >=5.0 | ==5.0 | No bump needed |

### Paper2Poster
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| docling_parse | *(unpinned)* | ==4.0.0 | Newer versions removed `pdf_parser_v2` API used by vendored docling code |

---

## Apps With No Bumps Needed (>= to == only)

All `>=`/`~=`/`^` specifiers converted to `==` at the originally declared minimum version. No dependency conflicts.

- AgentGPT
- bilingual_book_maker
- ChatDBG
- codeinterpreter-api
- codeqai
- Data-Copilot
- devika
- FunClip
- gpt-migrate
- Integuru (Poetry-based, lock file regenerated)
- local-deep-researcher
- localGPT
- pdfGPT
- pycorrector
- pyvideotrans
- rawdog
- slide-deck-ai
- TradingAgents

---

## Apps Where Pinning Was Not Applied

| App | Reason |
|-----|--------|
| gptme | 40+ interdependent packages create cascading conflicts; built with original caret/tilde constraints |
| RD-Agent | No `>=` specifiers to convert (all deps unpinned) |
| attackgen | No version specifiers to pin (all deps unpinned) |

---

## Pre-Built Images (No Pinning Possible)

These apps use official or third-party pre-built Docker images. Dependency versions are controlled by the upstream maintainer.

- auto-news
- DataFlow
- gpt_academic
- magentic-ui
- manga-image-translator
- omniparse
- SWE-agent

---

## Skipped Apps (8) — Local Install Docs Only

These apps were not containerized. Local installation instructions are in `docs/`.

autoMate, whispering, TaskMatrix, MedRAX, home-llm, AiNiee, itext2kg, Windrecorder
