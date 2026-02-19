# Biomni -- Reasoning Log

## What Was Checked
- pyproject.toml: minimal deps (pydantic, langchain, python-dotenv) with optional gradio
- Source code imports: found langchain_openai, langchain_anthropic, langchain_text_splitters used at runtime but not declared in pyproject.toml
- Agent entry point: `A1` class with `launch_gradio_demo()` method

## Dockerfile Strategy
Python 3.11-slim (requires >=3.11 per pyproject.toml). Installed as editable package with gradio extra plus undeclared runtime deps.

## Key Decisions
- **Editable install**: Used `-e ".[gradio]"` to install the package in development mode since it's a library
- **Extra langchain packages**: The pyproject.toml only lists `langchain` but the code imports `langchain_openai`, `langchain_anthropic`, and `langchain_text_splitters`. Added these explicitly
- **Custom entrypoint.py**: The repo has no CLI or server script. Created a minimal script that instantiates A1 and launches the Gradio demo
- **No data lake pre-download**: The data lake is ~11GB and downloads on first run. Baking it into the image would make it huge. Users should mount a volume for persistence

## Testing
1. **Import test**: `from biomni.agent import A1` succeeds, proving all dependencies resolve correctly
2. **Config output**: Agent prints its configuration (LLM model, timeout, tool retriever settings) -- proves initialization works
3. **Gradio launch**: Blocked by data lake download on first run. The download is the app's design -- it fetches biomedical databases before serving

Full Gradio UI testing would require waiting for the 11GB download and providing a valid API key.

## Build Iterations
1. First build: missing `langchain_openai` at runtime. Added langchain-openai, langchain-anthropic, langchain-text-splitters
2. Second build: successful, all imports resolve
