# Instructions for Yuelin Quality Control

## Context

You are performing quality control on 41 Dockerized LLM applications deployed by Hamiz for supply chain security research. Your goal is to verify that each app can be pulled from Docker Hub, started, and has its documented endpoints responding correctly. This is prep work for dynamic vulnerability scanning.

**Important files to read first:**
- `Task1.md` -- full app catalog with Docker images, test counts, and usage doc links
- `tracker.md` -- deployment status tracker
- `docs/yuelin_qc_log.md` -- QC log with results so far (12 apps tested, 30 remaining)
- Each app's `docs/<appname>_usage.md` -- exact commands, endpoints, and expected responses

## What Has Been Done

### Apps Already Tested (12/41)
These have been pulled, started, and endpoint-tested. Results in `docs/yuelin_qc_log.md`.

| # | App | Image | Result |
|---|-----|-------|--------|
| 1 | attackgen | hoomzoom/attackgen | PASS |
| 2 | stride-gpt | hoomzoom/stride-gpt | PASS |
| 3 | zshot | hoomzoom/zshot | PASS |
| 4 | pycorrector | hoomzoom/pycorrector | PASS |
| 5 | omniparse | hoomzoom/omniparse | PASS |
| 6 | rawdog | hoomzoom/rawdog | PASS |
| 7 | gpt-researcher | hoomzoom/gpt-researcher | PASS |
| 8 | gptme | hoomzoom/gptme-server | PASS |
| 9 | taskweaver | hoomzoom/taskweaver | **FAIL** (wrong entrypoint) |
| 10 | django-ai-assistant | hoomzoom/django-ai-assistant | PASS |
| 11 | FunClip | hoomzoom/funclip | PASS |
| 12 | manga-image-translator | hoomzoom/manga-image-translator | PULL FAILED (network) |

### Issues Found and Fixed
- `hoomzoom/devika-frontend` was missing from Docker Hub -- rebuilt and pushed
- zshot and pycorrector usage docs had incorrect "first startup downloads models" notes -- fixed

### Issues Found, NOT Yet Fixed
- **TaskWeaver wrong entrypoint**: The Docker Hub image `hoomzoom/taskweaver` has ENTRYPOINT `/app/entrypoint.sh` (CLI mode) instead of `/app/entrypoint_chainlit.sh` (Chainlit web UI). Running `docker run -p 8000:8000 hoomzoom/taskweaver` as the usage doc says will crash. Needs image rebuild from `dockerfiles/TaskWeaver/Dockerfile` (which has the correct entrypoint) and push to Docker Hub. The repo needs to be cloned first: `git clone --depth 1 https://github.com/microsoft/TaskWeaver.git apps/TaskWeaver`

### Docker Hub Verification
All 48 images verified present on Docker Hub via `docker manifest inspect`.

## Apps Remaining to Test (30)

### Single-Container Web UI Apps (no API key needed for infra)
These are the easiest to test. Pull, run, hit health endpoint + main page.

| App | Image | Port | Health/Test Endpoint | Notes |
|-----|-------|------|---------------------|-------|
| gpt_academic | hoomzoom/gpt_academic | 28010 | GET / | Gradio UI |
| NarratoAI | hoomzoom/narratoai | 8501 | GET /_stcore/health | Streamlit |
| codeqai | hoomzoom/codeqai | 8501 | GET /_stcore/health | Streamlit |
| slide-deck-ai | hoomzoom/slidedeckai | 8501 | GET /_stcore/health | Streamlit |
| DataFlow | hoomzoom/dataflow | 7860 | GET / | Gradio, **needs GPU** (`--gpus all`) |
| HuixiangDou | hoomzoom/huixiangdou | 7860 | GET /, GET /docs | Gradio + FastAPI |
| magentic-ui | hoomzoom/magentic-ui | 8081 | GET / | Needs API key + Docker socket |
| Biomni | hoomzoom/biomni | 7860 | GET / | Gradio |
| Data-Copilot | hoomzoom/data-copilot | 7860 | GET / | Gradio |
| pyvideotrans | hoomzoom/pyvideotrans | N/A | `docker run --rm hoomzoom/pyvideotrans --help` | CLI only |
| local-deep-researcher | hoomzoom/local-deep-researcher | 8123 | GET /info | LangGraph API |

### Single-Container CLI Apps
Test with `docker run --rm <image> --help` or similar non-interactive command.

| App | Image | Test Command | Notes |
|-----|-------|-------------|-------|
| ChatDBG | hoomzoom/chatdbg | `docker run --rm hoomzoom/chatdbg chatdbg --help` | CLI debugger |
| RD-Agent | hoomzoom/rd-agent | `docker run --rm hoomzoom/rd-agent rdagent --help` | CLI + Streamlit (port 80) |
| Paper2Poster | hoomzoom/paper2poster | `docker run --rm hoomzoom/paper2poster python -c "import paper2poster; print('ok')"` | CLI |
| bilingual_book_maker | hoomzoom/bilingual_book_maker | `docker run --rm hoomzoom/bilingual_book_maker python make_book.py --help` | CLI |
| gpt-engineer | hoomzoom/gpt-engineer | `docker run --rm hoomzoom/gpt-engineer gpte --help` | CLI |
| gpt-migrate | hoomzoom/gpt-migrate | `docker run --rm hoomzoom/gpt-migrate python main.py --help` | CLI |
| SWE-agent | hoomzoom/swe-agent | `docker run --rm hoomzoom/swe-agent sweagent --help` | CLI + web UI (port 3000) |
| TradingAgents | hoomzoom/tradingagents | `docker run --rm hoomzoom/tradingagents python -c "import tradingagents; print('ok')"` | CLI |
| Integuru | hoomzoom/integuru | `docker run --rm hoomzoom/integuru python -c "import integuru; print('ok')"` | CLI + Playwright |

### Libraries (no web interface)
Test that imports work inside the container.

| App | Image | Test Command |
|-----|-------|-------------|
| codeinterpreter-api | hoomzoom/codeinterpreter-api | `docker run --rm hoomzoom/codeinterpreter-api python -c "from codeinterpreterapi import CodeInterpreterSession; print('ok')"` |
| chemcrow-public | hoomzoom/chemcrow | `docker run --rm hoomzoom/chemcrow python -c "from chemcrow import ChemCrow; print('ok')"` |

### Multi-Container (compose) Apps
These require docker-compose files from `dockerfiles/<app>/` and often need the original repo cloned. More complex to test.

| App | Compose Location | Services | Notes |
|-----|-----------------|----------|-------|
| pdfGPT | dockerfiles/pdfGPT/ | 4 containers | Needs repo clone + .env |
| agenticSeek | dockerfiles/agenticSeek/ | 4 containers (backend+frontend+SearxNG+Redis) | Needs repo clone + .env |
| localGPT | dockerfiles/localGPT/ | 4 containers (frontend+backend+rag-api+Ollama) | |
| AgentGPT | dockerfiles/AgentGPT/ | 3 containers (Next.js+FastAPI+MySQL) | Needs repo clone + .env |
| BettaFish | dockerfiles/BettaFish/ | 2 containers (app+PostgreSQL) | |
| devika | dockerfiles/devika/ | 3 containers (backend+frontend+Playwright) | |
| auto-news | N/A | 9 containers (Airflow) | Uses `finaldie/auto-news:0.9.15`, see usage doc |

## How to Test Each App

### General Procedure
```bash
# 1. Read the usage doc
cat docs/<appname>_usage.md

# 2. Pull the image
docker pull hoomzoom/<image-name>

# 3. Run the container (check usage doc for exact command, port, env vars)
docker run -d --name <app>-test -p <port>:<port> hoomzoom/<image-name>

# 4. Wait for startup (check logs)
docker logs -f <app>-test

# 5. Test endpoints (use PowerShell on Windows -- curl sometimes times out)
powershell -Command "(Invoke-WebRequest -Uri http://localhost:<port>/ -UseBasicParsing).StatusCode"

# For Streamlit apps:
powershell -Command "(Invoke-WebRequest -Uri http://localhost:<port>/_stcore/health -UseBasicParsing).Content"

# For FastAPI apps:
powershell -Command "(Invoke-WebRequest -Uri http://localhost:<port>/docs -UseBasicParsing).StatusCode"
powershell -Command "(Invoke-WebRequest -Uri http://localhost:<port>/health -UseBasicParsing).Content"

# For Gradio apps:
powershell -Command "(Invoke-WebRequest -Uri http://localhost:<port>/gradio_api/info -UseBasicParsing).StatusCode"

# 6. Clean up
docker stop <app>-test && docker rm <app>-test
```

### Apps That Need API Keys
About half the apps need an OpenAI API key (or similar). Without a key:
- Some apps start fine but LLM features don't work (attackgen, gpt-researcher, django-ai-assistant)
- Some apps crash on startup (gptme, taskweaver)
- To test infrastructure only, try with a dummy key: `-e OPENAI_API_KEY=sk-dummy`

The actual key is available as `$OPENAI_API_KEY` environment variable on the host.

### Apps With Long Startup
These download ML models on first run and take 5-20 minutes to start:
- **FunClip**: ~15 min (1.2GB ASR models from ModelScope)
- **omniparse**: ~3 min (OCR + Florence-2 models)
- **manga-image-translator**: downloads 622MB sugoi models
- **zshot**: instant (models pre-baked)
- **pycorrector**: ~15 sec (model pre-baked)

Check startup with `docker logs -f <container>`. The container may look hung but it's downloading.

### Apps That Need GPU
- **DataFlow**: needs `--gpus all` and NVIDIA Container Toolkit

### Apps That Need Docker Socket
- **SWE-agent**: needs `-v /var/run/docker.sock:/var/run/docker.sock`
- **magentic-ui**: needs Docker-in-Docker setup

## Windows-Specific Gotchas

1. **Use PowerShell for HTTP testing**, not curl. Git Bash curl sometimes times out to Docker containers.
   ```bash
   powershell -Command "(Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing).StatusCode"
   ```

2. **MSYS path mangling**: When passing paths to docker, prefix with `MSYS_NO_PATHCONV=1`:
   ```bash
   MSYS_NO_PATHCONV=1 docker run --entrypoint /app/entrypoint_chainlit.sh hoomzoom/taskweaver
   ```

3. **Chinese text encoding**: Chinese characters show as `???` in Git Bash and PowerShell. Not a container bug -- it's Windows terminal encoding. Apps still work correctly.

4. **Docker Desktop crashes**: Docker Desktop on this machine crashes occasionally (500 Internal Server Error). Fix:
   ```bash
   # Soft restart
   powershell -Command "Stop-Process -Name 'Docker Desktop' -Force"
   sleep 5
   powershell -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"

   # Hard restart (if soft doesn't work)
   wsl --shutdown
   sleep 10
   powershell -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"
   ```
   Wait 1-3 minutes for Docker engine to be ready. Verify with `docker info`.

5. **Port conflicts**: Many apps share ports (8000, 8501, 7860). Only run one app at a time, or remap: `-p 8502:8501`.

## What to Record

For each app, log in `docs/yuelin_qc_log.md`:
1. Pull result (OK / FAIL with error)
2. Run command used
3. Startup time and any issues
4. Each endpoint tested and result (HTTP status, response snippet)
5. Whether it matches the usage doc
6. Any problems found (doc errors, missing images, crashes, etc.)

## Summary of What Needs Doing

1. **Test remaining 30 apps** (follow procedures above)
2. **Fix TaskWeaver image** -- rebuild from `dockerfiles/TaskWeaver/Dockerfile` and push to Docker Hub
3. **Retry manga-image-translator pull** -- failed due to network (10GB image)
4. **Update `docs/yuelin_qc_log.md`** with all results
