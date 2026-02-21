# Dynamic Analysis QC Log -- Yuelin (Fresh Run)
**Date**: 2026-02-21
**Goal**: Full QC of all 41 deployed apps. Verify every Docker image pulls, starts, and responds.

---

## Phase 1: Docker Hub Image Verification

**Method:** `docker manifest inspect` on all 50 images listed in Task1.md.

**Result:** 50/50 exist on Docker Hub (48 hoomzoom/ + 2 external).

---

## Phase 2: Single-Container App Testing

### CLI / Library Apps

| # | App | Test | Result | Notes |
|---|-----|------|--------|-------|
| 1 | ChatDBG | `chatdbg --help` | **PASS** | Shows ipdb debugger help |
| 2 | RD-Agent | `--help` | **PASS** | Shows rdagent CLI with fin_factor, fin_model etc. |
| 3 | Paper2Poster | `import PosterAgent` | **PASS** | Module imports successfully |
| 4 | rawdog | `rawdog --help` | **PASS** | Full CLI help with all flags |
| 5 | bilingual_book_maker | `python make_book.py --help` | **PASS** | Full help text (was exec format error in prior QC — now fixed!) |
| 6 | gpt-engineer | `gpte --help` | **FAIL** | `TypeError: TyperArgument.make_metavar() takes 1 positional argument but 2 were given` — V2 typer version incompatibility |
| 7 | gpt-migrate | `python main.py --help` | **PASS** | Full CLI help |
| 8 | chemcrow | `from chemcrow import ChemCrow` | **FAIL** | `ModuleNotFoundError: No module named 'langchain_core'` — V2 change removed langchain_core but streamlit_callback_handler still imports it |
| 9 | codeinterpreter-api | `from codeinterpreterapi import CodeInterpreterSession` | **PASS** | Import succeeds |
| 10 | TradingAgents | `--help` | **PASS** | Full CLI help |
| 11 | Integuru | `--help` | **PASS** | Full CLI help with model, prompt, HAR options |
| 12 | pyvideotrans | `--help` | **PASS** | Full CLI help with stt/tts/sts/vtv tasks |
| 13 | SWE-agent | `sweagent --help` | **PARTIAL** | Package installed (v0.7.0, import works) but CLI entry point `sweagent` not in PATH. Needs entrypoint fix. |

### Web UI Apps (Streamlit)

| # | App | Test | Result | Notes |
|---|-----|------|--------|-------|
| 14 | attackgen | `/_stcore/health` | **PASS** | Returns `ok` |
| 15 | stride-gpt | `/_stcore/health` | **PASS** | Returns `ok` |
| 16 | NarratoAI | `/_stcore/health` | **PASS** | Returns `ok` |
| 17 | slide-deck-ai | `/_stcore/health` | **FAIL** | Container exits after Streamlit first-run email prompt — missing `server.headless=true` config |
| 18 | codeqai | `import codeqai` | **PASS** | Import succeeds. Full Streamlit requires real API key (indexes on startup). |

### Web UI Apps (Gradio / FastAPI / Flask)

| # | App | Test | Result | Notes |
|---|-----|------|--------|-------|
| 19 | pycorrector | `/gradio_api/info` → 200 | **PASS** | Gradio API responds |
| 20 | zshot | `/health` → `{"status":"ok"}` | **PASS** | FastAPI health endpoint works |
| 21 | FunClip | Container starts, downloads models | **PASS** | Model download (~800MB) started successfully. Gradio UI available during init. |
| 22 | gpt-researcher | GET / → 200 | **PASS** | Frontend + API docs both respond |
| 23 | gptme | GET / → 200 | **PASS** | Requires API key env var to start (documented). With dummy key, web UI works. |
| 24 | django-ai-assistant | GET / → 200 | **PASS** | Frontend + admin both respond |
| 25 | gpt_academic | GET / → 200 | **PASS** | Needs WEB_PORT=12345 env var |
| 26 | HuixiangDou | Startup crash | **FAIL** | `ImportError: cannot import name 'Schema' from 'pydantic'` — V2 pinning set pydantic==2.0.0 but fastapi version expects pydantic v1 Schema import |
| 27 | Biomni | `from biomni.agent import A1` | **PASS** | Import succeeds. Full Gradio needs 11GB data download + API key. |
| 28 | Data-Copilot | Startup crash | **EXPECTED** | Crashes without Tushare token — documented behavior, not a bug |
| 29 | magentic-ui | `import magentic_ui` | **PASS** | Import succeeds. Full test needs Docker socket mount. |

### Apps Requiring Special Entrypoint

| # | App | Test | Result | Notes |
|---|-----|------|--------|-------|
| 30 | TaskWeaver | GET / → 200 (with workaround) | **FAIL** | `ValueError: numpy.dtype size changed` — numpy/pandas binary incompatibility from V2 pinning |
| 31 | local-deep-researcher | Startup crash | **FAIL** | Dependency resolution fails: `ollama-deep-researcher==0.0.1` incompatible with `langchain-openai==0.3.9` — V2 pinning broke resolution |

---

## Phase 3: Compose / Multi-Container Apps

### Rate-Limited — Could Not Pull

Docker Hub rate limiting kicked in after ~36 image pulls. The following images could not be pulled in this session:

- hoomzoom/bettafish
- hoomzoom/devika-backend
- hoomzoom/omniparse
- hoomzoom/manga-image-translator
- hoomzoom/dataflow
- hoomzoom/agenticseek-backend
- hoomzoom/localgpt-backend, localgpt-rag-api
- hoomzoom/pdfgpt-frontend, pdfgpt-langchain-serve, pdfgpt-backend, pdfgpt-pdf-gpt
- finaldie/auto-news:0.9.15

These compose apps could not be tested:
- **pdfGPT** (4 containers)
- **agenticSeek** (4 containers)
- **localGPT** (4 containers)
- **BettaFish** (2 containers)
- **devika** (3 containers)
- **auto-news** (9 containers)

### Not Testable Without Special Hardware/Setup

- **DataFlow** — needs `--gpus all` (no NVIDIA GPU available)
- **AgentGPT** — needs MySQL + compose setup (frontend image pulled, platform image pulled, but MySQL not started)
- **omniparse** — rate limited, could not pull
- **manga-image-translator** — rate limited, could not pull (~10GB image)

---

## Summary

### All Results

| Status | Count | Apps |
|--------|-------|------|
| **PASS** | 22 | ChatDBG, RD-Agent, Paper2Poster, rawdog, bilingual_book_maker, gpt-migrate, codeinterpreter-api, TradingAgents, Integuru, pyvideotrans, attackgen, stride-gpt, NarratoAI, codeqai, pycorrector, zshot, FunClip, gpt-researcher, gptme, django-ai-assistant, gpt_academic, Biomni |
| **PASS (conditional)** | 3 | Data-Copilot (needs Tushare token), magentic-ui (needs Docker socket), Biomni (needs 11GB data download) |
| **FAIL (V2 pinning broke it)** | 5 | gpt-engineer (typer compat), chemcrow (langchain_core removed), HuixiangDou (pydantic v1/v2), TaskWeaver (numpy/pandas binary compat), local-deep-researcher (langchain-openai vs ollama-deep-researcher) |
| **FAIL (image/config issue)** | 2 | slide-deck-ai (missing headless config), SWE-agent (CLI entry point missing from PATH) |
| **NOT TESTED (rate limited)** | 6 | pdfGPT, agenticSeek, localGPT, BettaFish, devika, auto-news |
| **NOT TESTED (special hw)** | 3 | DataFlow (GPU), omniparse (rate limited), manga-image-translator (rate limited) |

### Critical Issues — V2 Pinning Regressions (5 apps)

These apps worked before V2 minimum version pinning and are now broken:

1. **gpt-engineer**: `typer==0.9.0` incompatible with current click — `TyperArgument.make_metavar()` error
2. **chemcrow-public**: V2 change removed `langchain_core` but `streamlit_callback_handler.py` still imports from it
3. **HuixiangDou**: `pydantic==2.0.0` but old `fastapi` version tries `from pydantic import Schema` (removed in pydantic v2)
4. **TaskWeaver**: `numpy`/`pandas` binary incompatibility (`numpy.dtype size changed`)
5. **local-deep-researcher**: `langchain-openai==0.3.9` conflicts with `ollama-deep-researcher==0.0.1` dependency resolution

### Image/Config Issues (2 apps)

6. **slide-deck-ai**: Streamlit exits on first-run email prompt (needs `server.headless=true` in config)
7. **SWE-agent**: `sweagent` CLI not in PATH despite package being installed (v0.7.0)

### Previously Broken, Now Fixed (1 app)

- **bilingual_book_maker**: Was "exec format error" in prior QC — now works correctly

### Docker Hub Rate Limiting

Hit pull rate limit after ~36 images. 12 images could not be pulled. Need Docker Hub Pro or wait for rate limit reset to complete testing.
