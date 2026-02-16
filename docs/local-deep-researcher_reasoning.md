# local-deep-researcher -- Reasoning Log

## Initial Assessment

Local Deep Researcher is a LangGraph application from the langchain-ai organization. It performs iterative web research using local LLMs through Ollama for inference and DuckDuckGo for web search. The repo ships with a Dockerfile that uses the LangGraph dev server. The app has no web UI of its own, just the LangGraph API and the optional LangGraph Studio UI.

## What Was Checked

1. **README.md**: Describes the app as a research assistant that uses Ollama for LLM inference and DuckDuckGo for web search. The main graph is called `ollama_deep_researcher`. It supports configurable search depth and iteration parameters. Alternative search providers (Tavily, Perplexity) are available but require API keys.

2. **Dockerfile**: Single-stage build on `python:3.11-slim`. Installs system-level build dependencies including Rust and Cargo (needed to compile the `cryptography` Python package from source on slim images). Installs `uv` as the package manager. Sets `OLLAMA_BASE_URL` as a default env var. Uses `uvx` at runtime to bootstrap the LangGraph CLI and dev server. The `--platform=$BUILDPLATFORM` directive enables cross-platform builds.

3. **langgraph.json**: The LangGraph configuration file that tells the dev server where to find the graph. It points to `src/ollama_deep_researcher/graph.py:graph`. This file is what makes the `/assistants/search` endpoint return `ollama_deep_researcher`.

4. **pyproject.toml**: Defines the Python package with its dependencies. Key dependencies include `langgraph`, `langchain-ollama`, `duckduckgo-search`, and `langchain-community`. The `--with-editable .` flag in the CMD installs this package in editable mode at runtime.

5. **Environment variables**: `OLLAMA_BASE_URL` is the primary configuration. It defaults to `http://localhost:11434/` in the Dockerfile. The `search_api` variable controls which search provider to use (defaults to `duckduckgo` in the graph code).

## Decisions Made

### Used the existing Dockerfile without modification
The developer's Dockerfile is functional and well-structured. It follows a standard pattern for LangGraph apps: install build dependencies, install uv, copy source, run with uvx. No modifications were needed.

### Did not add a non-root user
The original Dockerfile runs everything as root. The `uvx` command installs packages into `/root/.local/bin` at runtime, and the PATH is set accordingly. Adding a non-root user would require changing the PATH, the uvx cache location, and potentially the package installation behavior. Since the developer designed it this way and architectural fidelity is the priority, this was left as-is.

### Did not bundle Ollama into the container
The app requires a running Ollama instance for LLM inference. One option would have been to create a docker-compose.yml that brings up both the app and an Ollama container. This was not done because (a) the developer's architecture is a standalone LangGraph server that connects to an external Ollama, (b) Ollama containers are large and need GPU access for reasonable performance, and (c) users running this app likely already have Ollama running on their host. The `.env.example` documents the `host.docker.internal` pattern for connecting to host Ollama.

### Provided .env.example with host.docker.internal
Inside a Docker container, `localhost` refers to the container itself, not the host machine. The default `OLLAMA_BASE_URL` of `http://localhost:11434/` will not work in Docker. The `.env.example` uses `http://host.docker.internal:11434/` which is Docker's built-in DNS name for the host machine. This is documented in both the usage doc and the .env.example.

### Documented the search_api variable
Although the Dockerfile only sets `OLLAMA_BASE_URL`, the graph code reads a `search_api` configuration value that defaults to `duckduckgo`. Alternative values are `tavily` and `perplexity`, each requiring their own API keys. This was included in the .env.example and the environment variables table.

## Testing

### Why These Tests Were Chosen
The LangGraph dev server exposes a standard REST API. The four tested endpoints validate that the server starts correctly, the graph configuration is loaded, and the API is functional. These are the core infrastructure endpoints that do not require an actual LLM backend.

### Tests Performed
1. **GET /docs** (200): Returns the OpenAPI documentation page. This confirms the LangGraph dev server is running and serving its API correctly.
2. **GET /info** (200): Returns version information including the LangGraph version (0.7.37). Confirms the server's metadata endpoint is functional.
3. **POST /assistants/search** (200): Returns the list of available assistants. The response includes `ollama_deep_researcher`, which confirms that `langgraph.json` was parsed correctly and the graph module was loaded.
4. **POST /threads** (200): Creates a new thread and returns a thread ID. Confirms the thread management subsystem is working.

### What Was Not Tested
- **POST /threads/{thread_id}/runs**: This endpoint triggers actual research, which requires a running Ollama instance with a model loaded. Without Ollama, the request would fail at the LLM inference step. This is expected and documented.
- **Web search functionality**: DuckDuckGo search only executes as part of a research run, which requires Ollama.
- **Report generation**: Same dependency on Ollama for the summarization step.
- **Alternative search providers (Tavily, Perplexity)**: These require API keys and are outside the scope of the base deployment.

## Gotchas

1. **Ollama dependency**: The app is unusable without a running Ollama instance. The default `OLLAMA_BASE_URL` of `http://localhost:11434/` does not work inside Docker because localhost refers to the container. Users must override this to `http://host.docker.internal:11434/` (Docker Desktop) or the actual host IP.

2. **Runtime package installation via uvx**: The CMD uses `uvx --refresh` which downloads and installs the LangGraph CLI and all dependencies at container startup. This means (a) the first startup is slow (can take 1-2 minutes depending on network speed), (b) the container requires internet access at startup, and (c) if PyPI or the package registry is down, the container will fail to start. This is the developer's intended approach, where `uvx` acts as a runtime bootstrapper rather than baking everything into the image at build time.

3. **Python 3.11 pinning**: Both the base image and the `--python 3.11` flag in the CMD specify Python 3.11. The LangGraph ecosystem at this version may have compatibility issues with Python 3.12+. Do not change the Python version without testing.

4. **Dev server warning**: The LangGraph dev server prints a warning at startup that it is not intended for production use and recommends LangSmith Deployment. This is expected behavior and does not affect functionality for testing purposes.

5. **Rust and Cargo in build dependencies**: The `python:3.11-slim` image does not include pre-built wheels for the `cryptography` package, so it must be compiled from source. This requires Rust and Cargo, which are why they appear in the apt-get install list. This adds to the image size but is necessary for the build to succeed.
