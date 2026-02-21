# V2 Minimum Version Pinning - Manifest

This document summarizes all dependency version changes made during V2 minimum version pinning across all 49 apps.

**Goal:** Convert all `>=`, `~=`, `^` specifiers to `==` (exact pins at the minimum declared version). Where the minimum version doesn't exist or causes conflicts, bump to the nearest working version.

---

## Apps With Dependency Bumps

### agenticSeek
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| playsound3 | >=1.0.0 | ==3.0.0 | 1.0.0 doesn't exist on PyPI. 2.0.0 requires pygobject/Cairo system deps |
| together | >=1.5.0 | ==1.5.2 | 1.5.0 doesn't exist on PyPI |
| tqdm | >=4 | ==4.66.2 | together 1.5.2 requires tqdm>=4.66.2 |

### BettaFish
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| opencv-python | >=4.8.0 | ==4.8.0.74 | 4.8.0 doesn't exist on PyPI |
| black | >=23.0.0 | ==23.1.0 | 23.0.0 doesn't exist on PyPI |
| psycopg[binary] | >=3.1.0 | ==3.1.8 | 3.1.0 binary wheel not available for Python 3.11 |
| lxml | >=4.9.0 | ==4.9.3 | 4.9.0 fails to build from source without libxml2-dev |
| aiohttp | >=3.8.0 | ==3.9.0 | 3.8.0 fails on Python 3.11 due to missing longintrepr.h |

### Biomni
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| setuptools | >=61.0 | *(left unpinned)* | Project uses PEP 639 license format requiring setuptools>=77 |
| gradio | >=5.0 | ==5.0 | No bump needed |

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
| tiktoken | >=0.0.4 | ==0.7.0 | 0.0.4 doesn't exist. langchain-openai requires >=0.7 |
| langchain | ^0.1.2 | ==0.2.0 | 0.1.2 incompatible with langchain-community==0.2.0 |
| langchain-anthropic | ^0.1.1 | ==0.1.13 | 0.1.1 needs langchain-core<0.2 |
| langchain_openai | * | ==0.1.7 | Compatible version for langchain 0.2.x |
| openai | ^1.0 | ==1.24.0 | langchain-openai 0.1.7 requires openai>=1.24.0 |
| typer | ^0.3.2 | ==0.9.0 | 0.3.2 needs click<7.2 which conflicts with black |
| poetry-core | >=1.0.0 | *(left unpinned)* | 1.0.0 doesn't support PEP 660 editable installs |

### gpt-researcher
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| unstructured | >=0.13 | ==0.14.2 | 0.13 doesn't exist on PyPI. 0.13.x requires Python <3.12 |
| lxml | >=4.9.2 | ==4.9.3 | 4.9.2 fails to build on Python 3.12 |
| langgraph | >=0.2.76 | ==1.0.0 | langchain 1.0.0 requires langgraph>=1.0.0 |
| pydantic | >=2.5.1 | ==2.9.0 | ollama 0.6.0 requires pydantic>=2.9 |
| requests | >=2.31.0 | ==2.32.5 | langchain-community 0.4 requires requests>=2.32.5 |
| ollama | >=0.4.8 | ==0.6.0 | langchain-ollama 1.0.0 requires ollama>=0.6.0 |
| openai | >=1.3.3 | ==1.109.1 | langchain-openai 1.0.0 requires openai>=1.109.1 |
| arxiv | >=2.0.0 | ==2.1.3 | 2.0.0 pins requests==2.31.0 which conflicts |
| fastapi | >=0.104.1 | ==0.115.0 | 0.104.1 needs anyio<4.0.0 which conflicts with mcp |
| python-multipart | >=0.0.6 | ==0.0.9 | mcp 1.9.1 requires >=0.0.9 |
| langchain-mcp-adapters | >=0.1.0 | ==0.2.0 | 0.1.x needs langchain-core<0.4 |
| mcp | >=1.9.1 | ==1.9.2 | langchain-mcp-adapters 0.2.0 requires mcp>=1.9.2 |

### HuixiangDou
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| pydantic | ==1.10.13 | ==2.0.2 | gradio 4.44.1 requires pydantic>=2.0. fastapi 0.100.0 excludes 2.0.0 |
| fastapi | *(unpinned)* | ==0.100.0 | First version compatible with pydantic v2 (QC fix) |
| gradio | *(unpinned)* | ==4.44.1 | Era-match with huggingface_hub <1.0 |
| gradio_client | *(unpinned)* | ==1.3.0 | Match gradio 4.44.1 |
| huggingface_hub | *(unpinned)* | ==0.24.7 | gradio 4.x requires <1.0 |
| transformers | *(unpinned)* | ==4.44.2 | Must work with huggingface_hub 0.x |
| sentence_transformers | *(unpinned)* | ==3.0.1 | Compatible with transformers 4.44 |
| tokenizers | *(unpinned)* | ==0.19.1 | Match transformers 4.44 |

### local-deep-researcher
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| openai | ==1.12.0 | ==1.66.3 | langchain-openai==0.3.9 requires openai>=1.66.3 (QC fix) |

### NarratoAI
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| openai | ==1.77.0 | ==1.75.0 | litellm 1.70.0 requires openai<1.76.0 |

### Paper2Poster
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| docling_parse | *(unpinned)* | ==4.0.0 | Newer versions removed `pdf_parser_v2` API used by vendored docling code |
| setuptools | *(unpinned)* | <71 | Build constraint. pkg_resources compatibility |

### pdfGPT
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| langchain | *(unpinned)* | ==0.0.267 | langchain-serve requires pre-split monolithic langchain |
| litellm | *(unpinned)* | ==0.1.424 | Modern litellm requires openai>=1.0 which is incompatible |
| openai | *(unpinned)* | ==0.27.8 | litellm 0.1.424 requires >=0.27.8 |
| pydantic | *(unpinned)* | <2 | Jina 3.x crashes with pydantic v2 |
| huggingface_hub | *(unpinned)* | <1.0 | Gradio 4.x imports HfFolder removed in hub >=1.0 |
| setuptools | *(unpinned)* | <71 | Build constraint. langchain-serve uses pkg_resources |
| opentelemetry-exporter-prometheus | *(unpinned)* | ==1.12.0rc1 | Yanked from PyPI but required by jina 3.14.1 |

### stride-gpt
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| streamlit | >=1.40 | ==1.40.0 | 1.40 doesn't exist on PyPI. 1.40.0 is the actual release |

### TaskWeaver
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| matplotlib | ==3.4 | ==3.7.0 | 3.4 has no prebuilt wheels for Python 3.12, fails to build from source |
| seaborn | ==0.11 | ==0.11.0 | Version format fix |
| pyyaml | ==6.0 | ==6.0.0 | Version format fix |
| pandas | ==2.0.3 | ==2.1.0 | Binary incompatibility with numpy 1.26.x ABI (QC fix) |
| numpy | ==1.24.2 | ==1.26.0 | Needed for compatibility with sentence-transformers numpy 2.x transitive dep |
| scikit-learn | ==1.2.2 | ==1.5.0 | 1.2.2 incompatible with numpy 2.x pulled by sentence-transformers |

### zshot
| Package | Original | Pinned | Reason |
|---------|----------|--------|--------|
| torch | ==1 | ==2.0.0 | 1.x fails with libtorch executable stack error under QEMU. version "1" invalid |
| requests | ==2.28 | ==2.28.0 | Version format fix |
| prettytable | ==3.4 | ==3.4.0 | Version format fix |
| transformers | ==4.20 | ==4.30.0 | 4.20.0 can't download models from new HuggingFace Hub API |
| datasets | ==2.9.1 | ==2.9.0 | 2.9.1 doesn't exist on PyPI |
| numpy | *(unpinned)* | <1.25.0 | spacy 3.4.1 + thinc compiled against numpy<1.25 |
| pydantic | *(unpinned)* | <2.0.0 | spacy 3.4.1 requires pydantic v1 |
| fastapi | *(unpinned)* | <0.100.0 | fastapi >=0.100 requires pydantic v2 |

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
- localGPT
- pycorrector
- pyvideotrans
- rawdog
- slide-deck-ai
- TradingAgents

---

## Apps Where Pinning Was Not Applied

| App | Reason |
|-----|--------|
| attackgen | No version specifiers to pin (all deps unpinned) |
| gptme | 40+ interdependent packages create cascading conflicts. built with original caret/tilde constraints |
| RD-Agent | No `>=` specifiers to convert (all deps unpinned) |

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

## Skipped Apps (8) - Local Install Docs Only

These apps were not containerized. Local installation instructions are in `docs/`.

autoMate, whispering, TaskMatrix, MedRAX, home-llm, AiNiee, itext2kg, Windrecorder
