# pdfGPT. Reasoning Log

## Understanding the architecture

### Initial analysis
- **README.md**: Confirmed pdfGPT is a PDF Q&A app using Universal Sentence Encoder for embeddings and OpenAI for LLM completion. The README explicitly mentions langchain-serve for production API deployment. Docker instructions say `docker-compose -f docker-compose.yaml up`.
- **api.py**: The backend. Uses `@serving` decorator from `lcserve` (langchain-serve) to expose two endpoints: `ask_url` (PDF from URL) and `ask_file` (uploaded PDF). Imports tensorflow_hub, scikit-learn, PyMuPDF, litellm, openai.
- **app.py**: The frontend. Gradio UI that sends HTTP requests to the langchain-serve backend. Takes an API host URL, OpenAI key, PDF URL or file, and a question.
- **docker-compose.yaml**: Defines two services with multi-stage build targets: `langchain-serve-img` (port 8080) and `pdf-gpt-img` (port 7860).
- **Dockerfile (original from repo)**: Multi-stage but broken. The langchain-serve stage runs `RUN pip3 install api` (tries to install a PyPI package called "api" instead of copying api.py) and never copies any source files.
- **requirements.txt**: Shared file for both stages. Pins gradio==4.11.0 but app.py uses Gradio 3.x patterns (btn.style(), enable_queue, demo.app.server.timeout).
- **Git history**: Checked to confirm what files were original vs. modified. Found `app_docker.py` was our custom merged version that violated architectural fidelity by replacing the two-service architecture with a single process.

### Why the two-service architecture matters
This is a supply chain security research project. Other researchers will pentest these deployed apps. If we merge the backend and frontend into a single process (like app_docker.py did), pentesters would be testing our custom code, not the original developer's attack surface. The langchain-serve/Jina gateway, the `@serving` decorator, and the HTTP communication between services are all part of the real attack surface that needs to be preserved.

## Changes and rationale

### Architectural fidelity rule
Established a formal rule for all future deployments: no custom API wrappers, no replacing core dependencies, no adding web servers the developer didn't create. Allowed changes are limited to: Dockerfiles, network binding, env vars, dependency pins, bug fixes.

### Delete app_docker.py
This file merged the backend and frontend into a single Gradio app with direct function calls, bypassing langchain-serve entirely. It violated the fidelity rule. Deleted.

### Multi-stage Dockerfile rewrite
The original Dockerfile was broken (never copied source code, tried to `pip install api`). I rewrote it as a proper multi-stage build:
- **Stage 1 (langchain-serve-img)**: Installs all backend dependencies, pre-downloads the Universal Sentence Encoder model (~1GB), copies api.py, runs `lc-serve deploy local api`
- **Stage 2 (pdf-gpt-img)**: Installs only gradio + requests (all app.py needs), copies source, runs `python app.py`

### Separating frontend dependencies
The original Dockerfile installs requirements.txt in the frontend stage too, but the frontend (app.py) only imports gradio, requests, json, and os. Installing the full requirements.txt in the frontend caused pip resolution failures (resolution-too-deep) because langchain-serve's dependency tree is enormous and conflicts with itself. The fix: install only what app.py actually needs. This is a bug fix, not an architectural change.

### Era-matched dependency pins
langchain-serve is abandoned software from mid-2023. Its dependency chain is a minefield. Here's what broke and how each was fixed:

1. **pkg_resources missing**: `setuptools>=71` removed `pkg_resources`. langchain-serve's setup.py uses it during build. Fix: upgrade pip (need >=23.1 for PIP_BUILD_CONSTRAINT support) and set `PIP_BUILD_CONSTRAINT` to pin `setuptools<71` in build isolation environments.

2. **opentelemetry-exporter-prometheus yanked**: `jina 3.14.1+` requires `opentelemetry-exporter-prometheus>=1.12.0rc1`, but that version was yanked from PyPI ("Version is deprecated"). The entire 1.x line never existed. all available versions are 0.x betas. Fix: pre-install the specific yanked version (`pip install opentelemetry-exporter-prometheus==1.12.0rc1`) before installing langchain-serve. pip will install yanked versions when explicitly pinned, and since it's already installed, the resolver won't try to find it.

3. **langchain community split**: langchain-serve imports from `langchain.agents.AgentExecutor` which moved to `langchain-community` in langchain >=0.1.0 (Jan 2024). Even langchain 0.0.350 had started the migration. Fix: pin `langchain==0.0.267` which is fully monolithic (pre-split).

4. **litellm/openai version mismatch**: Modern litellm (>=1.0) requires openai>=1.0 (new API with different exception classes). The original repo uses openai 0.27.x (old API). Fix: pin `litellm==0.1.424` (contemporary with openai 0.27.x era).

5. **pydantic v1/v2 incompatibility**: Jina 3.x was written for pydantic v1. With pydantic v2 installed, the Jina gateway crashes with `TypeError: 'type' object is not iterable` during initialization. Fix: pin `pydantic<2`.

6. **openai version bump**: `litellm==0.1.424` requires `openai>=0.27.8`, not `0.27.4` as in the original requirements.txt. Fix: use `openai==0.27.8`.

The final working combination: pydantic==1.10.26, langchain==0.0.267, langchain-serve==0.0.61, litellm==0.1.424, openai==0.27.8, tensorflow-cpu==2.11.1, tensorflow_hub==0.13.0.

### app.py bug fixes (Gradio 3.x to 4.x compatibility)
The requirements.txt pins gradio==4.11.0 but app.py was written for Gradio 3.x. Three incompatible patterns:
- `btn.style(full_width=True)`: Removed in Gradio 4.x. Replaced with `variant='primary'` on Button constructor.
- `demo.app.server.timeout = 60000`: Internal server attribute not available in Gradio 4.x. Removed.
- `demo.launch(server_port=7860, enable_queue=True)`: `enable_queue` deprecated (always on in Gradio 4.x). Removed parameter, added `server_name="0.0.0.0"` for Docker network binding.

### Backend host configuration
The frontend's API host defaults to `http://localhost:8080`, which doesn't work in docker-compose (separate containers). Added `import os` and changed the default to `os.environ.get('LCSERVE_HOST', 'http://localhost:8080')`. The docker-compose.yaml sets `LCSERVE_HOST=http://langchain-serve:8080` for the frontend service. This is environment variable configuration, explicitly allowed by the fidelity rule.

### huggingface_hub version pin
Gradio 4.11.0 imports `HfFolder` from `huggingface_hub`, which was removed in huggingface_hub >=1.0. Fix: pin `huggingface_hub<1.0` in the frontend stage.

## Roads not taken

### Replacing langchain-serve with a custom FastAPI wrapper
This is what the previous app_docker.py did. Rejected because it violates architectural fidelity. pentesters need to test the real langchain-serve/Jina attack surface.

### Using the original Dockerfile as-is
Impossible. It has `RUN pip3 install api` which tries to install a PyPI package, and never copies api.py into the container. It also uses python:3.8-slim-buster which is EOL.

### Using python:3.8
The original Dockerfile uses 3.8. Rejected because Python 3.8 is EOL and many current packages have dropped support. Python 3.10 is the sweet spot for this dependency matrix.

### Using python:3.11 or newer
Rejected because some dependencies in the langchain-serve tree have strict Python version constraints (e.g., certain jina versions require exactly >=3.7,<3.10 or >=3.11). Python 3.10 works for all the pinned versions.

### Skipping pdfGPT entirely
The plan included a SKIP option if langchain-serve was truly broken. After significant dependency wrangling, I got it working with era-matched pins. The app runs faithfully, so no need to SKIP.

### Single-stage Dockerfile
Would be simpler but doesn't match the original two-service architecture. The frontend and backend have very different dependency requirements. the backend needs TensorFlow, scikit-learn, langchain-serve (hundreds of packages, ~4GB image) while the frontend only needs gradio and requests (~500MB image).

## Test coverage

1. **docker compose up starts both services**: Proves the multi-stage Dockerfile builds correctly for both targets, docker-compose networking works, and both services start without crashing. The backend takes ~30s to initialize TensorFlow.

2. **Backend /healthz returns {"status":"ok"}**: Proves the Jina gateway is running and responsive. This is the first layer. if the gateway is healthy, it means jina, langchain-serve, and all their dependencies loaded correctly.

3. **Backend /docs returns Swagger UI**: Proves the FastAPI application inside the Jina gateway is serving the auto-generated API documentation. This validates that the `@serving` decorators in api.py were properly processed and registered as HTTP routes.

4. **Frontend returns 200**: Proves the Gradio UI is running and accessible. The frontend is simpler so this mainly validates that the Gradio 4.x compatibility fixes work.

5. **ask_url endpoint (NOT TESTED)**: Would prove the full pipeline: PDF download, text extraction (PyMuPDF), embedding (TF Hub Universal Sentence Encoder), semantic search (scikit-learn KNN), and LLM completion (litellm -> OpenAI). Requires an OpenAI API key.

6. **ask_file endpoint (NOT TESTED)**: Same as ask_url but with file upload instead of URL download. Would validate the multipart form handling in langchain-serve.

## Trouble spots

### curl timeouts on Windows
curl from Git Bash sometimes times out when connecting to Docker containers on localhost, even though the service is healthy. PowerShell's Invoke-WebRequest works reliably. Always verify with PowerShell if curl fails on Windows.

### The opentelemetry-exporter-prometheus rabbit hole
This package's version 1.12.0rc1 was yanked from PyPI, meaning pip's resolver will never select it automatically. But jina 3.14.1+ has a hard requirement `>=1.12.0rc1`. The trick: pip WILL install yanked versions when you explicitly pin them (`pip install opentelemetry-exporter-prometheus==1.12.0rc1`). Pre-installing it before the main pip install means the resolver finds it already satisfied.

### langchain's confusing version history
langchain went through a major restructuring:
- 0.0.1 to ~0.0.300: Monolithic package, everything in one place
- ~0.0.300 to 0.0.352: Transition period, started importing from langchain-community
- 0.1.0+: Fully split into langchain, langchain-core, langchain-community
langchain-serve was written for the monolithic era. Pin to 0.0.267 or earlier.

### pydantic v1 vs v2
Jina 3.x uses pydantic v1 internals extensively. With pydantic v2, the Jina gateway initialization fails with cryptic TypeErrors. Always pin `pydantic<2` when using jina 3.x.

### TF Hub model download during build
The Universal Sentence Encoder model is ~1GB. Pre-downloading it during `docker build` means the image is large but container startup is fast. Without pre-download, every container start would download 1GB. The build step `RUN python -c "import tensorflow_hub as hub. hub.load('...')"` takes 1-2 minutes.

### text-davinci-003 deprecation
The original api.py hardcodes `text-davinci-003` as the model. OpenAI deprecated this model. litellm 0.1.424 may or may not handle the routing gracefully. This is a bug in the original code, not something we fix per the fidelity rule.
