# Biomni -- Reasoning Log

## What Was Checked
- pyproject.toml: minimal deps (pydantic, langchain, python-dotenv) with optional gradio
- Source code imports: found langchain_openai, langchain_anthropic, langchain_text_splitters used at runtime but not declared in pyproject.toml
- Agent entry point: `A1` class with `launch_gradio_demo()` method

## Dockerfile Strategy
Python 3.11-slim (requires >=3.11 per pyproject.toml). Installed as editable package with gradio extra plus undeclared runtime deps.

## Key Decisions

### Editable install (`-e ".[gradio]"`)
The package uses a `src/` layout with `biomni/` as the importable package. A standard `pip install .` would work, but editable mode was chosen because the Gradio demo imports from `biomni.agent` which relies on package metadata being discoverable. This matches how the developers run it locally.

### Undeclared runtime dependencies
This is the most significant finding. The pyproject.toml declares `langchain` as a dependency, but the source code imports three additional langchain ecosystem packages that are NOT declared:
- `langchain_openai` (used in `biomni/agent.py` for ChatOpenAI)
- `langchain_anthropic` (used for Claude model support)
- `langchain_text_splitters` (used in RAG pipeline)

These are separate PyPI packages since the langchain 0.2.x ecosystem split. Without explicitly adding them, the container builds but crashes at runtime with `ModuleNotFoundError`. This is a supply chain concern — undeclared dependencies mean the app silently depends on packages not auditable from pyproject.toml alone.

### Custom entrypoint.py
The repo has no CLI entry point, server script, or `__main__.py`. The only way to launch the Gradio demo is programmatically: instantiate `A1()` and call `launch_gradio_demo()`. Created a minimal 5-line script for this.

### No data lake pre-download
The data lake (~11GB of biomedical databases) downloads on first `A1()` initialization. Baking it into the image would create an 11GB+ image unsuitable for distribution. Instead, users should mount a volume (`-v biomni_data:/app/data`) for persistence across container restarts.

## Testing
1. **Import test**: `from biomni.agent import A1` succeeds, proving all dependencies resolve correctly
2. **Config output**: Agent prints its configuration (LLM model, timeout, tool retriever settings) -- proves initialization works
3. **Gradio launch**: Blocked by data lake download on first run. The download is the app's design -- it fetches biomedical databases before serving

Full Gradio UI testing would require waiting for the 11GB download and providing a valid API key.

## Build Iterations
1. First build: missing `langchain_openai` at runtime. Added langchain-openai, langchain-anthropic, langchain-text-splitters
2. Second build: successful, all imports resolve
