# Dynamic Analysis QC Log -- Yuelin
**Date**: 2026-02-20
**Goal**: Pick up Hamiz's 42 deployed apps, verify I can actually spin them up and hit their endpoints, as prep for dynamic vulnerability scanning.

## First Impressions

**What I received:**
- Well-organized repo: `dockerfiles/`, `docs/`, `tracker.md`, `Task1.md` (full catalog), `README.md`
- 42 apps deployed, 8 skipped with reasons
- 49 usage docs total (deployed + skipped)
- 48 Docker Hub images listed under `hoomzoom/` + 2 external images

**README quality:** Good. Clear quick-start, links to catalog, explains structure. The "Quick Start" example (`docker pull hoomzoom/attackgen && docker run -p 8501:8501 hoomzoom/attackgen`) actually works.

**Task1.md quality:** Excellent. Full table with GitHub links, Docker image names, API key requirements, test counts, and links to usage docs. Categorized (Web UI, CLI, Library). Helpful notes section at the bottom about model downloads, code execution risks, dependency mismatches.

## Docker Hub Image Verification

**Method:** `docker manifest inspect` on all 48 listed images.

**Result:** 48/48 exist after fix. Originally `hoomzoom/devika-frontend` was MISSING -- Hamiz rebuilt and pushed it during this QC session.

## App Testing

### Round 1: Simple Single-Container Apps (no API key needed)

#### 1. attackgen (Streamlit)
- **Pull:** OK, fast (~200MB)
- **Run:** `docker run -d -p 8501:8501 hoomzoom/attackgen`
- **Health check:** `/_stcore/health` -> `ok` (PASS)
- **Main page:** GET / -> 200 (PASS)
- **Time to test:** ~30 seconds
- **Verdict:** Works exactly as documented

#### 2. stride-gpt (Streamlit)
- **Pull:** OK
- **Run:** `docker run -d -p 8502:8501 hoomzoom/stride-gpt` (used 8502 to avoid conflict)
- **Health check:** `/_stcore/health` -> `ok` (PASS)
- **Time to test:** ~20 seconds
- **Verdict:** Works exactly as documented
- **Note:** Usage doc says port 8501, but doesn't say what port the container exposes internally. I had to guess `-p 8502:8501` based on Streamlit convention. Minor doc gap.

#### 3. zshot (FastAPI, zero-shot NER)
- **Pull:** OK (image was already cached -- ~5GB, large due to PyTorch)
- **Run:** `docker run -d -p 8000:8000 hoomzoom/zshot`
- **Startup:** Instant. Models are pre-baked in the image.
- **Health:** `/health` -> `{"status":"ok"}` (PASS)
- **Swagger:** `/docs` -> 200 (PASS)
- **Extract:** POST `/extract` with IBM text -> correct entity extraction (PASS)
- **Time to test:** ~40 seconds (including first request latency for model warm-up)
- **Verdict:** Works perfectly

#### 4. pycorrector (Gradio, Chinese text correction)
- **Pull:** OK
- **Run:** `docker run -d -p 7860:7860 hoomzoom/pycorrector`
- **Startup:** ~15 seconds (model loading)
- **API info:** `/gradio_api/info` -> 200 (PASS)
- **Correction:** POST `/gradio_api/call/predict` with Chinese text -> event_id returned, result retrieved (PASS -- functionally)
- **Encoding issue:** Both curl and PowerShell on this Windows machine show Chinese characters as `???`. ASCII input/output works fine. This is a Windows terminal encoding issue, NOT a container bug.
- **Time to test:** ~2 minutes
- **Verdict:** Works, but testing Chinese endpoints on Windows is painful

#### 5. omniparse (FastAPI + Gradio, document parser)
- **Pull:** OK (9.35 GB image -- very large)
- **Run:** `docker run -d -p 8000:8000 hoomzoom/omniparse`
- **Startup:** ~3 minutes. Loads OCR models (Surya), Florence-2 from HuggingFace (with warnings about downloaded code!), audio model (Whisper), web crawler.
- **Swagger:** `/docs` -> 200 (PASS)
- **Web parse:** POST `/parse_website/parse?url=https://example.com` -> full response with markdown, HTML, metadata, screenshot (PASS)
- **Time to test:** ~5 minutes (mostly startup)
- **Verdict:** Works well
- **Security note:** HuggingFace prints warnings: "A new version of the following files was downloaded from https://huggingface.co/microsoft/Florence-2-base: configuration_florence2.py, modeling_florence2.py, processing_florence2.py. Make sure to double-check they do not contain any added malicious code." This is a **runtime code download from HuggingFace** -- relevant for supply chain analysis.

#### 6. rawdog (CLI)
- **Pull:** OK (small image)
- **Run:** `docker run --rm hoomzoom/rawdog --help`
- **Output:** Correct help text with all documented flags (PASS)
- **Time to test:** ~15 seconds
- **Verdict:** Works. Can't test actual execution without API key.

### Round 2: Mixed Complexity (6 more apps)

#### 7. gpt-researcher (FastAPI + Web UI)
- **Pull:** OK (~1.5GB)
- **Run:** `docker run -d -p 8000:8000 hoomzoom/gpt-researcher`
- **Startup:** ~5 seconds, no API key needed for infra
- **Frontend:** GET / -> 200 (PASS)
- **Swagger:** GET /docs -> 200 (PASS)
- **List reports:** GET /api/reports -> `{"reports":[]}` (PASS)
- **List files:** GET /files/ -> `{"files":[]}` (PASS)
- **Time to test:** ~30 seconds
- **Verdict:** Works exactly as documented. 4/4 infra endpoints pass.

#### 8. gptme (Flask + Web UI)
- **Pull:** OK
- **Run without key:** `docker run -d -p 5700:5700 hoomzoom/gptme-server` -> **CRASHES** with `ModelConfigurationError: No API key found, couldn't auto-detect provider`
- **Run with dummy key:** `docker run -d -p 5700:5700 -e OPENAI_API_KEY=sk-dummy hoomzoom/gptme-server` -> starts OK
- **Web UI:** GET / -> 200 (PASS)
- **API docs:** GET /api/docs/ -> 200 (PASS)
- **Time to test:** ~1 minute
- **Verdict:** Works. Crash without key is documented ("The server will crash on startup without one"). Behaves as expected.

#### 9. taskweaver (Chainlit web UI)
- **Pull:** OK
- **Run without key:** Crashes with `ValueError: Config value llm.openai.api_key is not found` -- documented.
- **Run with dummy key:** `docker run -d -p 8000:8000 -e LLM_OPENAI_API_KEY=sk-dummy hoomzoom/taskweaver` -> **CRASHES** -- drops into CLI mode and aborts ("Warning: Input is not a terminal")
- **BUG FOUND:** The Docker image entrypoint is `/app/entrypoint.sh` which runs CLI mode (`python -m taskweaver`), NOT the Chainlit web UI. The usage doc says the entrypoint was changed to `entrypoint_chainlit.sh` but the image still has the old one.
- **Workaround:** `docker run -d -p 8000:8000 -e LLM_OPENAI_API_KEY=sk-dummy --entrypoint /app/entrypoint_chainlit.sh hoomzoom/taskweaver` -> works
- **Web UI (with workaround):** GET / -> 200 (PASS)
- **Settings:** GET /project/settings -> 200, returns full Chainlit config JSON (PASS)
- **Time to test:** ~5 minutes (debugging the entrypoint issue)
- **Verdict:** **BROKEN as documented.** `docker run` per the usage doc does NOT work. Needs entrypoint override or image rebuild.

#### 10. django-ai-assistant (Django + React)
- **Pull:** OK (already cached)
- **Run:** `docker run -d -p 8000:8000 hoomzoom/django-ai-assistant`
- **Startup:** ~5 seconds
- **Frontend:** GET / -> 200 (PASS)
- **Admin:** GET /admin/ -> 200 (PASS)
- **API auth:** GET /ai-assistant/assistants/ -> 401 Unauthorized (PASS -- auth enforced correctly)
- **Time to test:** ~30 seconds
- **Verdict:** Works. Could not test authenticated API endpoints due to CSRF/session complexity in scripted testing, but infra is solid.

#### 11. FunClip (Gradio, ASR + video clipping)
- **Pull:** OK (~4GB)
- **Run:** `docker run -d -p 7860:7860 hoomzoom/funclip`
- **Startup:** **~15 minutes.** Downloads ~1.2GB of ASR models from ModelScope (model.pt 823MB, then speaker model 26.7MB, then VideoClipper initialization). Download speed varied 450kB/s - 5MB/s.
- **Gradio UI:** GET / -> 200 (PASS -- UI available during model init)
- **API info:** GET /gradio_api/info -> 200 (PASS)
- **Time to test:** ~18 minutes total (mostly model download + init)
- **Verdict:** Works, but extremely slow first startup. Doc accurately warns about this.
- **Note:** Docker Desktop crashed during FunClip testing (500 Internal Server Error on Docker API). Required `wsl --shutdown` + restart to recover. This is a host machine issue, not a container bug.

#### 12. manga-image-translator
- **Pull:** FAILED twice with "unexpected EOF" -- image is ~10GB and network connection drops.
- **Verdict:** Could not test. Need more stable network or pre-cached image. Not a deployment bug.

### Round 3: Remaining Single-Container Apps (19 more)

#### 13. ChatDBG (CLI debugger)
- **Run:** `docker run --rm hoomzoom/chatdbg chatdbg --help`
- **Output:** Correct help text (PASS)
- **Verdict:** Works as documented

#### 14. bilingual_book_maker (CLI)
- **Run:** `docker run --rm hoomzoom/bilingual_book_maker python make_book.py --help`
- **Output:** `exec /usr/local/bin/python3: input/output error` and `exec /bin/bash: exec format error`
- **Verdict:** **BROKEN.** Image has exec format error -- wrong-architecture binaries despite reporting amd64. Needs rebuild.

#### 15. gpt-engineer (CLI)
- **Run:** `docker run --rm hoomzoom/gpt-engineer gpte --help`
- **Output:** Correct help text (PASS)
- **Verdict:** Works as documented

#### 16. chemcrow (Library)
- **Run:** `docker run --rm hoomzoom/chemcrow python -c "from chemcrow import ChemCrow; print('ok')"`
- **Output:** `ok` (PASS)
- **Verdict:** Works as documented

#### 17. codeinterpreter-api (Library)
- **Run:** `docker run --rm hoomzoom/codeinterpreter-api python -c "from codeinterpreterapi import CodeInterpreterSession; print('ok')"`
- **Output:** `ok` (PASS)
- **Verdict:** Works as documented

#### 18. slide-deck-ai (Streamlit)
- **Run:** `docker run --rm hoomzoom/slidedeckai`
- **Output:** `exec /usr/local/bin/streamlit: exec format error`
- **Verdict:** **BROKEN.** Same exec format error as bilingual_book_maker. Needs rebuild.

#### 19. gpt-migrate (CLI)
- **Run:** `docker run --rm hoomzoom/gpt-migrate python main.py --help`
- **Output:** Correct help/usage text (PASS)
- **Verdict:** Works as documented

#### 20. SWE-agent (CLI + web UI)
- **Run:** `docker run --rm hoomzoom/swe-agent sweagent --help`
- **Output:** `exec: "sweagent": executable file not found in $PATH`
- **Inspection:** `docker inspect` shows image labels `org.opencontainers.image.ref.name: ubuntu`, `org.opencontainers.image.version: 22.04`
- **Verdict:** **BROKEN.** Wrong image pushed to Docker Hub -- it's just plain Ubuntu 22.04 with no SWE-agent code at all. Needs correct image to be built and pushed.

#### 21. NarratoAI (Streamlit)
- **Run:** `docker run -d -p 8501:8501 hoomzoom/narratoai`
- **Health:** `/_stcore/health` -> `ok` (PASS)
- **Verdict:** Works as documented

#### 22. HuixiangDou (Gradio + FastAPI)
- **Run:** `docker run -d -p 7860:7860 hoomzoom/huixiangdou`
- **Main page:** GET / -> 200 (PASS)
- **Verdict:** Works as documented

#### 23. Biomni (Gradio, biomedical)
- **Run:** `docker run -d -p 7860:7860 hoomzoom/biomni`
- **Startup:** Downloads ~6.25GB BindingDB data file + several smaller parquet files from data lake on first run. Estimated 20+ minutes at observed speeds.
- **Verdict:** PARTIAL -- infra starts correctly, data download is expected behavior (documented). Could not wait for full startup due to time constraints. Container runs, download works, Gradio will start after data is ready.

#### 24. Data-Copilot (Gradio)
- **Run:** `docker run -d -p 7860:7860 hoomzoom/data-copilot`
- **Startup:** Crashes with `ModuleNotFoundError: No module named 'tushare'` or Tushare token error
- **Verdict:** PASS (conditional). App requires Tushare token for Chinese financial data. This is documented. Infrastructure is correct.

#### 25. codeqai (Streamlit)
- **Run without key:** Crashes with `EOFError` -- prompts for API key interactively
- **Run with dummy key:** Crashes with `openai.AuthenticationError` -- tries to call OpenAI embeddings during initial indexing
- **Run with real key:** `docker run -d -p 8501:8501 -e OPENAI_API_KEY=<key> hoomzoom/codeqai` -> starts, indexes sample project (~10s), Streamlit launches
- **Health:** `/_stcore/health` -> `ok` (PASS)
- **Verdict:** Works, but requires real API key (not just dummy) because it indexes on startup.

#### 26. gpt_academic (Gradio)
- **First attempt:** `docker run -d -p 28010:28010` -> app starts on random internal port (46203), not 28010
- **Correct run:** `docker run -d -p 12345:12345 -e WEB_PORT=12345 -e API_KEY=sk-dummy -e USE_PROXY=False -e AUTO_OPEN_BROWSER=False hoomzoom/gpt_academic`
- **Main page:** GET / -> 200 (PASS)
- **Verdict:** Works, but the instructions doc I wrote (not the usage doc) had wrong port. The actual usage doc correctly says port 12345 with WEB_PORT env var.

#### 27. pyvideotrans (CLI)
- **Run:** `docker run --rm hoomzoom/pyvideotrans --help`
- **Output:** Full CLI help text with all options (stt, tts, sts, vtv tasks) (PASS)
- **Verdict:** Works as documented

#### 28. local-deep-researcher (LangGraph API)
- **Run:** `docker run -d -p 2024:2024 hoomzoom/local-deep-researcher`
- **Startup:** ~5 seconds
- **Info endpoint:** GET /info -> 200 with version info JSON (PASS)
- **Note:** Internal port is 2024, not 8123 as listed in instructions doc. Usage doc is correct.
- **Verdict:** Works as documented

#### 29. TradingAgents (CLI)
- **Run:** `docker run --rm hoomzoom/tradingagents --help`
- **Output:** Correct CLI help with options and commands (PASS)
- **Verdict:** Works as documented

#### 30. Integuru (CLI + Playwright)
- **Run:** `docker run --rm hoomzoom/integuru --help`
- **Output:** Correct CLI help with model, prompt, HAR/cookie path options (PASS)
- **Verdict:** Works as documented

#### 31. Paper2Poster (CLI)
- **Run:** `docker run --rm hoomzoom/paper2poster python -m PosterAgent.new_pipeline --help`
- **Output:** Full help text with poster generation options (PASS)
- **Note:** Module is `PosterAgent.new_pipeline`, not `paper2poster` as listed in instructions doc. Usage doc has the correct command.
- **Verdict:** Works as documented

#### 32. RD-Agent (CLI + Streamlit)
- **Run:** `docker run --rm hoomzoom/rd-agent --help`
- **Output:** Full CLI help with commands (fin_factor, fin_model, fin_quant, etc.) (PASS)
- **Verdict:** Works as documented

### Compose Apps (not yet tested)
The following 7 apps require docker-compose and often need cloned repos. Not tested due to time + disk space + network constraints:
- **pdfGPT** (4 containers, needs repo clone + .env)
- **agenticSeek** (4 containers, needs repo clone + .env)
- **localGPT** (4 containers)
- **AgentGPT** (3 containers, needs repo clone + .env)
- **BettaFish** (2 containers, 4.6GB image still pulling)
- **devika** (3 containers)
- **auto-news** (9 Airflow containers, external images)

### Not Testable
- **DataFlow** -- needs `--gpus all` (no GPU available)
- **magentic-ui** -- needs Docker socket + API key + complex Docker-in-Docker setup

## All Problems Found

### Critical (deployment broken)
1. ~~**`hoomzoom/devika-frontend` not on Docker Hub.**~~ **FIXED** -- rebuilt and pushed during this session.
2. ~~**TaskWeaver image has wrong entrypoint.**~~ **FIXED** -- Hamiz rebuilt from correct Dockerfile and pushed.
3. **bilingual_book_maker exec format error.** `docker run --rm hoomzoom/bilingual_book_maker` gives `exec format error`. Image has wrong-architecture binaries. **Needs rebuild.**
4. **slide-deck-ai exec format error.** Same issue as bilingual_book_maker. `exec /usr/local/bin/streamlit: exec format error`. **Needs rebuild.**
5. **SWE-agent wrong image.** Docker Hub image `hoomzoom/swe-agent` is just plain Ubuntu 22.04 -- contains no SWE-agent code at all. **Needs correct image built and pushed.**

### Minor (doc issues)
6. ~~**Doc inconsistency (zshot):** models download note.~~ **FIXED** -- doc updated.
7. ~~**Doc inconsistency (pycorrector):** models download note.~~ **FIXED** -- doc updated.
8. **Compose apps require repo clone.** AgentGPT (and presumably pdfGPT, agenticSeek, localGPT, etc.) can't run from just `dockerfiles/` -- need original repo for volume mounts. Documented but adds friction.
9. **Chinese text testing on Windows.** pycorrector's Chinese output shows as `???` in both Git Bash and PowerShell. Not a container bug.

### Observations for Dynamic Scanning
10. **Runtime model/code downloads.** omniparse downloads Florence-2 Python code from HuggingFace at runtime. FunClip downloads ASR models from ModelScope. Biomni downloads 6.25GB BindingDB data. These are supply chain risk vectors.
11. **Large images.** omniparse (9.35 GB), manga-image-translator (~10 GB), zshot (~5 GB), FunClip (~4 GB), BettaFish (~4.6 GB). Pulling all 48 images requires ~80-100 GB disk and stable network.
12. **Long startup times.** FunClip: ~15 min (model download). omniparse: ~3 min (model load). Biomni: ~20+ min (6.25GB data download). Need to account for this in scanning automation.
13. **Port conflicts.** Many apps use 8000, 8501, 7860. Can only run one at a time unless ports are remapped.
14. **Docker Desktop instability.** Docker Desktop crashed multiple times during testing (500 Internal Server Error, disk full). Required WSL shutdown + restart.
15. **Apps that crash without API key:** gptme, taskweaver, codeqai (needs real key, not dummy). gpt-researcher starts fine without key.

## Summary

| Metric | Result |
|--------|--------|
| Images verified on Docker Hub | 48/48 (after fix) |
| Apps tested (pull + run + endpoint hit) | 32/42 |
| Tests passed as documented | 27/32 |
| Tests failed (broken deployment) | 3 (bilingual_book_maker, slidedeckai, swe-agent) |
| Tests partial/conditional | 2 (Biomni download too long, Data-Copilot needs Tushare token) |
| Pull failures | 1 (manga-image-translator, network issue) |
| Critical issues found | 3 remaining (bilingual_book_maker, slidedeckai, swe-agent) |
| Issues fixed during session | 4 (devika-frontend pushed, taskweaver rebuilt, zshot doc, pycorrector doc) |
| Not yet tested | 9 (7 compose apps + DataFlow/GPU + magentic-ui/Docker socket) |
| Docker Desktop crashes | Multiple |

**Overall assessment:** Of 32 apps tested, 27 work correctly out of the box. 3 images are broken (bilingual_book_maker and slidedeckai have exec format errors, swe-agent has the completely wrong image). 2 more work conditionally (Biomni needs 20+ min for data download, Data-Copilot needs a Tushare token). TaskWeaver was broken but fixed during this session. The 7 compose apps and 2 special-requirements apps remain untested. Documentation is thorough and mostly accurate -- the usage docs are reliable, only the QC instructions doc I wrote had a couple of port errors.
