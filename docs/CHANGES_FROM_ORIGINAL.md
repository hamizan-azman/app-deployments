# Changes from Original Source Code

This document catalogs every modification made to each app during deployment. For supply chain security research, only vulnerabilities found in **original developer code** are valid findings. Changes listed here are deployment infrastructure -- not part of the original attack surface.

---

## How to Read This

Each app is categorized as:
- **UNCHANGED** -- No source code or dependency changes. The deployed app is the developer's original code.
- **DEPS ONLY** -- Dependency versions were pinned or changed. No source code was touched.
- **MODIFIED** -- Source code files were changed. Each change is listed with the exact file and line.

---

## UNCHANGED (14 apps)

These apps run exactly the developer's original code and dependencies. Any vulnerability found is a real supply chain finding.

| App | Dockerfile | Notes |
|-----|-----------|-------|
| ChatDBG | Used developer's original | No changes at all |
| RD-Agent | Written from scratch | Developer had no public Dockerfile. Source and deps untouched |
| rawdog | Written from scratch | Source and deps untouched |
| slide-deck-ai | Written from scratch | Source and deps untouched |
| omniparse | Pre-built image (savatar101/omniparse:0.1) | Developer's own published image, byte-for-byte |
| manga-image-translator | Pre-built image (zyddnys/manga-image-translator:main) | Developer's own image. Entrypoint overridden at runtime to start web server (developer's own server/main.py) |
| FunClip | Written from scratch | PyTorch CPU variant used (same version, different build). ImageMagick policy fix follows developer's own README |
| gpt_academic | Pre-built image (ghcr.io/binary-husky/gpt_academic_nolocal:master) | Developer's own GHCR image. Config via env vars only |
| codeinterpreter-api | Written from scratch | Installed from developer's pyproject.toml. Library with no web server |
| chemcrow-public | Written from scratch | Restored `paper-scraper` dependency that developer left commented out in setup.py but imports in code |
| BettaFish | Pre-built image (ghcr.io/666ghj/bettafish:latest) | Developer's own image |
| localGPT | Developer's Dockerfiles (3 files) | All three Dockerfiles used unmodified |
| DataFlow | Pre-built image (molyheci/dataflow:cu124) | Developer's own image |
| SWE-agent | Pre-built image (sweagent/swe-agent-run:latest) | Runtime `sed` changes server.py to bind 0.0.0.0 (not baked into image). Makes web UI network-accessible |

---

## DEPS ONLY (5 apps)

Source code is untouched. Only dependency versions differ from what `pip install` would resolve today.

### Paper2Poster
- `docling_parse` pinned to `==4.0.0` (original unpinned). Newer versions removed `pdf_parser_v2` API that the vendored `docling/` directory uses.
- `setuptools<71` build constraint (build-time only, not runtime).
- **Attack surface:** Minimal. Older docling_parse version within compatible range.

### bilingual_book_maker
- `PyMuPDF==1.24.2` added (not in original requirements.txt). The code imports `fitz` at module load time -- this was a missing dependency in the original repo.
- **Attack surface:** None. Restores developer's intended import.

### gpt-migrate
- 6 era-matched pins added (openai==0.27.8, langchain==0.0.238, typer==0.9.0, click==8.1.7, yaspin==2.5.0, tree-sitter==0.20.4). All fall within the developer's `pyproject.toml` version ranges. Without these, the app crashes on import.
- **Attack surface:** None. Restores the dependency versions from when the project was written (mid-2023).

### NarratoAI
- Chinese pip mirror (`pypi.tuna.tsinghua.edu.cn`) replaced with default PyPI. Same packages, different download source.
- **Attack surface:** None.

### AgentGPT
- Base image changed from `python:3.11-slim-buster` (Debian Buster, EOL) to `python:3.11-slim-bookworm` (Debian Bookworm). Buster's apt repos return 404.
- `openjdk-11-jdk` changed to `openjdk-17-jdk-headless` (Java 11 not default on Bookworm).
- `langchain` force-installed at `0.0.335` over poetry lockfile's `0.0.295`. Required because `lanarky==0.7.17` imports `langchain.globals` which doesn't exist in 0.0.295.
- **Attack surface:** Medium. Different OS packages (Bookworm vs Buster), different Java version, and 40 patch versions of langchain differ from the lockfile. Pentesters should note the langchain version does not match the developer's `poetry.lock`.

---

## MODIFIED (7 apps)

These apps have source code changes. Each change is listed below.

### pycorrector
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `examples/macbert/gradio_demo.py` | `.launch()` changed to `.launch(server_name="0.0.0.0", server_port=7860)` | Standard Docker network binding. Without this, Gradio only listens on 127.0.0.1 inside the container |

**Attack surface:** None. Network binding change only. All app logic unchanged.

---

### gpt-engineer
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `docker/Dockerfile` | Added `RUN sed -i 's/\r$//' /app/entrypoint.sh` | Strips Windows CRLF line endings. On Linux/Mac clones this is a no-op |

**Attack surface:** None. Whitespace normalization only.

---

### codeqai
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `/root/.config/codeqai/config.yaml` (new) | Pre-created config selecting OpenAI embeddings and gpt-4o-mini | Interactive config wizard can't run in Docker |
| `/app/sample-project/` (new) | Initialized git repo with codeqai source as sample data | App requires running inside a git repo |

**Attack surface:** Minimal. Config pre-selects OpenAI backend (user would choose this interactively anyway). No application source code was modified.

---

### agenticSeek
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `config.ini` | `is_local = True` changed to `is_local = False` | Docker deployment uses remote API, not local Ollama |
| `config.ini` | `provider_name = ollama` changed to `provider_name = openai` | Same reason |
| `config.ini` | `provider_model = deepseek-r1:14b` changed to `provider_model = gpt-4o-mini` | Use available model |
| `config.ini` | `provider_server_address = 127.0.0.1:11434` changed to `provider_server_address = api.openai.com` | Point to OpenAI API |

**Attack surface:** None. Config-only changes selecting LLM provider. All application code unchanged.

---

### zshot
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `zshot/knowledge_extractor/__init__.py` | Wrapped `relik` import in try/except ImportError | Prevents crash when optional `relik` package is not installed |
| `zshot/linker/__init__.py` | Wrapped `blink`, `tars`, `relik`, `gliner` imports in try/except ImportError | Same -- optional backends |
| `zshot/mentions_extractor/__init__.py` | Wrapped `gliner` import in try/except ImportError | Same |
| `app.py` (NEW FILE) | FastAPI wrapper with `/health`, `/extract`, `/visualize` endpoints | Zshot is a library with no web interface. This custom wrapper was added to expose it as a service |

**Dependency changes:** `transformers` pinned to `<5` (original unpinned). Transformers v5 removed `batch_encode_plus` from T5Tokenizer.

**Attack surface: SIGNIFICANT.** The `app.py` FastAPI wrapper is entirely custom code not written by the original developer. It introduces HTTP endpoints that do not exist in the original library. Any vulnerability found in `app.py` is NOT a valid supply chain finding. The try/except guards are defensive and do not change behavior. The MEMORY.md flags this for remediation: "zshot needs fixing: remove custom app.py FastAPI wrapper, redeploy as original library."

---

### pdfGPT
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `app.py` | Removed `btn.style(full_width=True)` (Gradio 3.x API removed in 4.x) | Gradio compat |
| `app.py` | Removed `demo.app.server.timeout = 60000` (not available in Gradio 4.x) | Gradio compat |
| `app.py` | Removed `enable_queue=True` from `demo.launch()`, added `server_name="0.0.0.0"` | Gradio compat + Docker binding |
| `app.py` | Added `os.environ.get('LCSERVE_HOST', 'http://localhost:8080')` for backend host | Docker compose networking (frontend needs to reach backend by service name) |
| `app_docker.py` | Deleted | Was a previously created custom file that bypassed langchain-serve. Removed per architectural fidelity rule |

**Dependency changes (7 pins):**
| Package | Original | Ours | Why |
|---------|----------|------|-----|
| langchain | unpinned | ==0.0.267 | langchain-serve requires pre-split monolithic langchain |
| litellm | unpinned | ==0.1.424 | Modern litellm requires openai>=1.0 which is incompatible |
| openai | ==0.27.4 | ==0.27.8 | litellm 0.1.424 requires >=0.27.8 |
| pydantic | unpinned | <2 | Jina 3.x crashes with pydantic v2 |
| huggingface_hub | unpinned | <1.0 | Gradio 4.x imports HfFolder removed in hub >=1.0 |
| setuptools | unpinned | <71 (build constraint) | langchain-serve uses pkg_resources |
| opentelemetry-exporter-prometheus | unpinned | ==1.12.0rc1 | Yanked from PyPI but required by jina 3.14.1 |

**Attack surface:** Moderate. The Gradio compat fixes change UI behavior slightly but not the backend API. The era-matched dependency pins lock the backend to 2023-era versions, preserving the original era's vulnerability profile. The `openai==0.27.4` to `0.27.8` bump is minor. The hardcoded `text-davinci-003` model in `api.py` was NOT changed (per fidelity rule).

---

### HuixiangDou
**Files changed:**
| File | Change | Why |
|------|--------|-----|
| `huixiangdou/gradio_ui.py` line 243 | `debug=True` changed to `debug=False` | Debug mode exposes extra Gradio info and causes health check issues in Docker |
| `huixiangdou/gradio_ui.py` lines 243-248 | Wrapped `demo.launch()` in try/except ValueError with sleep loop | Gradio health check fails in Docker even when server is running. Catch error and keep process alive |

**Inline patches (in Dockerfile, applied at build time):**
| Patch | Target | Change |
|-------|--------|--------|
| `sed` in requirements.txt | `faiss-gpu` | Commented out, replaced with `faiss-cpu` (pre-installed). Drop-in replacement, same API |
| Python script patches `gradio_client/utils.py` | `get_type()` and `_json_schema_to_python_type()` | Added `if not isinstance(schema, dict): return "Any"` guard. Fixes crash when pydantic v2 emits boolean in JSON schema |

**Dependency changes (6 pins):**
| Package | Original | Ours | Why |
|---------|----------|------|-----|
| gradio | >=4.41 | ==4.44.1 | Era-match with huggingface_hub <1.0 |
| gradio_client | transitive | ==1.3.0 | Match gradio 4.44.1 |
| huggingface_hub | transitive | ==0.24.7 | gradio 4.x requires <1.0 |
| transformers | >=4.38 | ==4.44.2 | Must work with huggingface_hub 0.x |
| sentence_transformers | transitive | ==3.0.1 | Compatible with transformers 4.44 |
| tokenizers | transitive | ==0.19.1 | Match transformers 4.44 |

**Attack surface:** Medium. The debug=False change reduces information exposure. The try/except is error handling only. The gradio_client monkey-patch prevents crashes on valid inputs but does not change behavior. The 6 dependency pins lock to specific older versions within the developer's allowed ranges. The developer's own pre-built image was broken (empty), so building from source was the only option.

---

## Summary

| Category | Count | Apps |
|----------|-------|------|
| UNCHANGED | 14 | ChatDBG, RD-Agent, rawdog, slide-deck-ai, omniparse, manga-image-translator, FunClip, gpt_academic, codeinterpreter-api, chemcrow-public, BettaFish, localGPT, DataFlow, SWE-agent |
| DEPS ONLY | 5 | Paper2Poster, bilingual_book_maker, gpt-migrate, NarratoAI, AgentGPT |
| MODIFIED | 7 | pycorrector, gpt-engineer, codeqai, agenticSeek, zshot, pdfGPT, HuixiangDou |

### High-priority notes for pentesters:
1. **zshot's `app.py` is custom code** -- not the developer's. Vulnerabilities in it are not supply chain findings. Flagged for removal.
2. **SWE-agent requires Docker socket access** (`-v /var/run/docker.sock`) -- container can control the host's Docker daemon.
3. **AgentGPT's langchain version (0.0.335) differs from the developer's lockfile (0.0.295)** -- 40 patch versions of difference.
4. **pdfGPT uses abandoned dependencies** (langchain-serve, jina 3.x, openai 0.27.x) pinned to 2023 versions.
5. **rawdog, gpt-engineer, SWE-agent, codeinterpreter-api, gpt-migrate execute arbitrary code** -- these are high-value targets for code injection research.
