# DeepGit. Reasoning Log

## Initial Assessment

DeepGit is a Gradio application that uses LLM agents to perform deep semantic search over GitHub repositories. The upstream repo does not include a Dockerfile, so one was written from scratch. The app requires two external API keys (GitHub and Groq) and downloads sentence-transformers models at runtime. The architecture is a single container with no database or secondary services, making it straightforward to deploy.

## What Was Checked

1. **README.md**: Describes the app as a multi-step GitHub search tool driven by LLM agents. Lists GITHUB_API_KEY and GROQ_API_KEY as required. Documents a local `pip install -r requirements.txt && python app.py` setup. No Docker instructions in the upstream repo.

2. **app.py**: Entry point. Launches a Gradio interface. Does not set `server_name` in the `demo.launch()` call, which means Gradio uses its default of `127.0.0.1`. This is a problem inside Docker.

3. **requirements.txt**: Lists dependencies with range specifiers. Includes gradio, groq, sentence-transformers, and GitHub API client libraries. No conflicting version constraints.

4. **Application structure**: Single Python file entry point (`app.py`) with a supporting modules directory. No multi-container dependencies. No local model weights bundled in the repo. Models are fetched from Hugging Face at runtime.

## Decisions Made

### Wrote a new Dockerfile from scratch
The upstream repo has no Dockerfile. Used `python:3.11-slim` as the base, matching the Python version the README targets. Installed `build-essential` and `curl` as system dependencies since some Python packages require compilation. Created a non-root user (`appuser`, UID 1000). Copied pinned requirements from `dockerfiles/DeepGit/requirements.txt` and installed before copying app source to maximise Docker layer cache reuse.

### Used repo root as build context
The pinned requirements file lives at `dockerfiles/DeepGit/requirements.txt` in the outer monorepo, not inside `apps/DeepGit/`. The Dockerfile needs to COPY from both locations. This requires the build context to be the repo root so both paths are accessible. The build command is therefore run from the repo root with `-f dockerfiles/DeepGit/Dockerfile`.

### Added GRADIO_SERVER_NAME=0.0.0.0
Took me a while to figure out why the container was healthy internally but unreachable from the host. Turns out Gradio defaults to 127.0.0.1 binding which is basically invisible outside the container.
This is the critical fix that makes the container usable. Gradio defaults to binding on `127.0.0.1`. Inside a Docker container, `127.0.0.1` is the loopback interface of the container itself. Any port published with `-p 7860:7860` still maps the host port to the container's network interface, but Gradio only listens on loopback, so connections from outside the container are refused. Setting `GRADIO_SERVER_NAME=0.0.0.0` tells Gradio to listen on all interfaces, which is the standard Docker pattern for web servers. This was added as an `ENV` instruction in the Dockerfile so it applies automatically without requiring the user to pass the variable at runtime.

### Set HEALTHCHECK to import check with curl fallback
`python:3.11-slim` does not include curl. The primary healthcheck uses `python -c "import gradio"` to verify the Python environment is intact. A curl fallback is included in the command chain for completeness, but the Python import is the one that actually runs. A 60-second start period is used because Gradio applications and their model downloads can take time to initialise.

## Testing

### Tests Performed
1. **Health endpoint** (GET `/gradio_api/info`): Returns HTTP 200 with JSON. Pass.
2. **Main UI** (GET `/`): Gradio interface loads in browser. Pass.

### What Was Not Tested
- Actual repository search (requires valid GITHUB_API_KEY and GROQ_API_KEY)
- Model download behaviour on first start (models download successfully but timing varies by network)

## Gotchas

1. **Gradio binds to 127.0.0.1 by default**: Every Gradio app deployed in Docker needs `GRADIO_SERVER_NAME=0.0.0.0` unless the upstream developer has already set it. The upstream DeepGit app does not set it. This is an easy mistake to miss because the container starts and reports healthy, but all connections from the host are refused.

2. **Model download on first start**: sentence-transformers downloads embedding models from Hugging Face during the first request or at import time, depending on how the app initialises them. This adds startup latency. The healthcheck start period of 60 seconds accounts for a fast network. On a slow connection the container may appear unhealthy during the first startup until the download completes.

3. **Build context must be repo root**: Because this project uses a split layout (app source in `apps/`, pinned deps in `dockerfiles/`), the Docker build context cannot be the app subdirectory alone. Any attempt to build with `apps/DeepGit/` as context will fail because `dockerfiles/DeepGit/requirements.txt` is outside that path. The build command must be run from the repo root.

4. **API keys required for meaningful use**: Unlike apps that degrade gracefully without keys, DeepGit's core function (search) is entirely blocked without both GITHUB_API_KEY and GROQ_API_KEY. The container will start and the UI will render, but any search attempt will fail at the API call stage.
