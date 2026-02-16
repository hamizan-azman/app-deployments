# TaskWeaver -- Reasoning Log

## Initial Assessment

TaskWeaver is Microsoft's code-first agent framework. The repo has an official Docker setup under `docker/all_in_one_container/` with a Dockerfile, two entrypoint scripts (CLI and Chainlit web UI), a config file, and a model downloader script. There is also a separate `ces_container` Docker setup for a code execution service, but the all-in-one container handles everything locally.

## What Was Checked

1. **docker/all_in_one_container/Dockerfile**: Single-stage build on `python:3.10-slim`. Installs requirements, chainlit, and optionally web search dependencies (sentence-transformers, FAISS, LangChain, DuckDuckGo). Also installs Google Gemini, ZhipuAI, and DashScope SDK for multi-provider LLM support. Downloads an embedding model via `model_downloader.py` when web search is enabled.

2. **entrypoint.sh (CLI mode)**: Creates a `taskweaver` user at runtime and runs `python -m taskweaver -p ./project`. This starts an interactive terminal session. Not useful for Docker deployment since it requires terminal attachment.

3. **entrypoint_chainlit.sh (Web UI mode)**: Same user creation, then runs `chainlit run --host 0.0.0.0 --port 8000 app.py` from the `playground/UI/` directory. This is the web-accessible mode.

4. **taskweaver_config.json (Docker version)**: Only contains `session.roles` with planner, code_interpreter, and web_search. The project-level config has LLM settings (api_base, api_key, model) but is overwritten by the Docker-specific config.

5. **config/config_mgt.py**: Configuration system supports environment variables. The format is uppercase with dots replaced by underscores. For example, `llm.openai.api_key` maps to `LLM_OPENAI_API_KEY`. This means all LLM configuration can be passed via env vars without modifying config files.

6. **playground/UI/app.py**: Chainlit application that creates TaskWeaver sessions per user. Uses event handlers for streaming updates. Sets the project path to `../../project` relative to the UI directory.

## Decisions Made

### Used Chainlit web UI as default entrypoint
The original Dockerfile defaults to CLI mode (`entrypoint.sh`), which starts an interactive terminal. This is unusable in a headless Docker container. The Chainlit entrypoint provides the same functionality through a web browser, making it the right choice for deployment. Both entrypoint scripts are included in the image, so users can switch to CLI mode with `--entrypoint /app/entrypoint.sh` if they need terminal access.

### Built without web search
The `WITH_WEB_SEARCH=true` build argument installs `sentence-transformers` (which pulls PyTorch, about 2 GB) and then runs `model_downloader.py` to download an embedding model. This step failed with a BrokenPipeError during the sentence-transformers pip install, likely due to the large download size and network instability. Rather than repeatedly retry, we built with `WITH_WEB_SEARCH=false`. The core functionality (task planning, code generation, code execution) works without web search. Users can rebuild with the flag enabled on a faster connection.

### Used environment variables for LLM configuration
The Docker-specific `taskweaver_config.json` only sets `session.roles` and does not include LLM settings. The original project config has empty `llm.api_key`. Rather than baking API keys into config files, we pass them via environment variables (LLM_OPENAI_API_KEY, LLM_OPENAI_MODEL, etc.), which is the standard Docker practice and is natively supported by TaskWeaver's config system.

## Testing

### Tests Performed
1. **Root endpoint** (GET `/`): Returns 200, serves Chainlit web UI. Pass.
2. **Readme** (GET `/readme`): Returns 200, application readme page. Pass.
3. **Project settings** (GET `/project/settings`): Returns 200, JSON with Chainlit configuration (UI name, theme, auth settings). Pass.
4. **Project translations** (GET `/project/translations`): Returns 200, UI translation strings. Pass.
5. **Startup without API key**: Server crashes with `ValueError: Config value llm.openai.api_key is not found`. This confirms the API key is required.
6. **Startup with placeholder key**: Server starts successfully with `LLM_OPENAI_API_KEY=sk-placeholder`. Chainlit UI loads and shows "Your app is available at http://0.0.0.0:8000".

### What Was Not Tested
- Actual task execution (requires valid OpenAI API key with access to GPT-4)
- Code generation and execution
- Web search functionality (not installed in current build)
- Multi-LLM provider support (Google Gemini, ZhipuAI, DashScope)

## Gotchas

1. **API key required at startup**: Unlike Streamlit apps where the app loads without keys, TaskWeaver crashes immediately if no LLM API key is provided. The env var format is non-obvious: `LLM_OPENAI_API_KEY` (not `OPENAI_API_KEY`).

2. **Two entrypoints**: The image has two entrypoint scripts. The Dockerfile in dockerfiles/ uses the Chainlit entrypoint by default. The original Dockerfile uses the CLI entrypoint, which requires an interactive terminal.

3. **Web search build**: The `WITH_WEB_SEARCH=true` build argument adds about 2 GB to the image (PyTorch + sentence-transformers + embedding model). Building this requires a stable, fast internet connection.

4. **Runtime user creation**: Both entrypoint scripts create a `taskweaver` user at runtime using `useradd`. This requires the container to start as root, then `su` to the created user. The UIDs can be customized via `TASKWEAVER_UID` and `TASKWEAVER_GID` env vars.

5. **Code execution security**: TaskWeaver generates and runs arbitrary Python code inside the container. The `EXECUTION_SERVICE_KERNEL_MODE=local` setting means code runs directly in the container's Python environment. This is by design but is a significant security concern for untrusted inputs.
