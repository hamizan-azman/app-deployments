# codeqai. Reasoning Log

## Understanding the App

### Repository Structure
Read `pyproject.toml` to understand dependencies and entry points. Key findings:
- Uses poetry for dependency management (poetry-core build backend)
- Entry point: `codeqai = "codeqai.__main__:main"`
- Python constraint: `>=3.9,<3.9.7 || >3.9.7,<3.12` (excludes 3.9.7 specifically, likely a bug in that version)
- Dependencies include langchain, openai, streamlit, tree-sitter, faiss (optional), sentence-transformers (via langchain-huggingface)

### Application Architecture (app.py)
The main `run()` function:
1. Verifies current directory is a git repo (`git rev-parse --is-inside-work-tree`)
2. Loads config from `~/.config/codeqai/config.yaml`
3. Sets up environment variables from `~/.config/codeqai/.env`
4. Creates embeddings model based on config
5. If no FAISS index exists: parses codebase with tree-sitter, creates embeddings, saves FAISS index
6. For `app` action: launches Streamlit via click group that reads sys.argv
7. For `search`/`chat`: enters interactive CLI loop

### Configuration (config.py)
`codeqai configure` is interactive (uses inquirer library). Not usable in Docker non-interactively. The config is a YAML file with keys: `embeddings`, `llm-host`, `chat-model`. I pre-created this file to bypass the interactive wizard.

### Environment Variable Handling (app.py:env_loader)
Critical behavior: the app creates `~/.config/codeqai/.env` with empty values for required keys, then checks `os.getenv()`. If the env var is not set AND the .env value is empty, it prompts for input (stdin). In Docker without TTY, this causes an EOFError crash. Solution: pass `OPENAI_API_KEY` via `docker run -e` so `os.getenv("OPENAI_API_KEY")` returns a value before the input prompt is reached.

### Streamlit Module (streamlit.py)
The Streamlit app runs at module level:
```python
config = load_config()
repo_name = repo.repo_name()
vector_store, memory, qa = bootstrap(config, repo_name)
```
This means FAISS index MUST exist before Streamlit starts. The `codeqai app` command handles this by running indexing first, then launching Streamlit.

### Vector Store (vector_store.py)
Uses FAISS with langchain's FAISS wrapper. Index is serialized to `~/.cache/codeqai/{repo_name}.faiss.bytes`. A JSON cache maps filenames to vector IDs and commit hashes for incremental sync.

## Key Decisions

### Base Image: python:3.11-slim
- Python 3.11 is within the required range (>=3.9,<3.12)
- Slim variant to minimize base size (though torch makes the final image large anyway)
- 3.11 has pre-built wheels for all dependencies (tree-sitter, faiss-cpu, etc.)

### Install via PyPI (not from source)
- `pip install codeqai` installs version 0.0.20, matching the repo's pyproject.toml
- PyPI install is cleaner and more reproducible than building from source with poetry
- All dependencies resolve correctly

### Pre-created Config for OpenAI
```yaml
embeddings: OpenAI-text-embedding-ada-002
llm-host: OpenAI
chat-model: gpt-4o-mini
```
- OpenAI embeddings are the simplest to set up (just needs API key, no local model downloads)
- gpt-4o-mini is cheap and fast for chat responses
- Pre-creating config avoids the interactive `codeqai configure` wizard which can't run in Docker

### Sample Git Repo: codeqai Source Code
Copied the codeqai Python package + pyproject.toml into the image as a sample project. Reasons:
- The app MUST run inside a git repo (hard requirement in code)
- Using codeqai's own source as demo is self-consistent and demonstrates real functionality
- 32 Python files. small enough for fast indexing, large enough to be meaningful
- Initialized with `git init && git add -A && git commit`

### Streamlit Environment Variables
Set `STREAMLIT_SERVER_ADDRESS=0.0.0.0`, `STREAMLIT_SERVER_PORT=8501`, `STREAMLIT_SERVER_HEADLESS=true` to:
- Bind to all interfaces (required for Docker port mapping)
- Use standard Streamlit port
- Suppress the "open browser" prompt

### Entrypoint: `codeqai app`
Uses the original CLI command, not a custom script. The `codeqai app` flow:
1. Checks git repo (working dir is the sample project)
2. Loads pre-created config
3. Creates OpenAI embeddings model
4. Indexes codebase if no FAISS file exists (first run)
5. Launches Streamlit via internal click group
This is the exact flow the developer intended, no architectural modifications.

## Test Plan

### Test 1: Streamlit UI (GET /)
Confirms the web interface loads. Streamlit returns an HTML shell that bootstraps the React frontend. 200 OK with 1.5KB response.

### Test 2: Streamlit Health (GET /_stcore/health)
Streamlit's built-in health endpoint. Returns "ok" when the server is running and the Python backend is functional. Confirms Streamlit framework is operational.

### Test 3: Host Config (GET /_stcore/host-config)
Returns Streamlit's configuration as JSON. Confirms server settings (address, port, headless mode) are applied correctly.

### Test 4: FAISS Index Exists
Checked `/root/.cache/codeqai/` inside the container. Found:
- `sample-project.faiss.bytes` (1.8MB). the vector index
- `sample-project.json` (14.5KB). the filename-to-vector cache
This proves the indexing pipeline works: tree-sitter parsed the Python files, OpenAI embeddings API was called, FAISS stored the vectors.

### Test 5: Config File
Verified the pre-created config at `/root/.config/codeqai/config.yaml` is correctly formatted and readable.

### Tests Not Run
- Search functionality (requires WebSocket interaction with Streamlit, not simple HTTP)
- Chat functionality (requires WebSocket + active LLM calls)
- CLI commands (require TTY for interactive mode)
- Dataset export (CLI only, not web-accessible)
These are functional tests that require Streamlit's WebSocket protocol. The infrastructure tests confirm the full stack is operational (Streamlit + FAISS + OpenAI connection).

## Things That Broke

### EOFError on Missing API Key
If `OPENAI_API_KEY` is not passed via `docker run -e`, the app crashes with `EOFError: EOF when reading a line`. The env_loader function tries to prompt for the key via stdin, which fails in non-interactive Docker. Always pass the key as an environment variable.

### Git Bash OPENAI_API_KEY Not Inherited
On Windows, if `OPENAI_API_KEY` is set as a User environment variable via PowerShell but the Git Bash terminal was opened before it was set, the variable won't be available. Fix: `export OPENAI_API_KEY=$(powershell -Command "[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY', 'User')")`.

### Large Image Size
The image is ~5GB because `langchain-huggingface` pulls in `sentence-transformers` which depends on `torch` (915MB) + NVIDIA CUDA libraries. These are needed even when using OpenAI embeddings because the dependency is unconditional in codeqai's pyproject.toml. No way to avoid this without modifying the package.

### Click + Argparse Interaction
The `codeqai app` command uses argparse for its main CLI, then delegates to a click group (`run_streamlit`) for launching Streamlit. The click group reads `sys.argv` and finds "app" as its subcommand, which triggers `stcli._main_run()`. This works but is fragile. sys.argv must contain "app" at the right position. In Docker CMD `["codeqai", "app"]`, this works correctly.

### First Run Indexing Time
First container startup takes ~10-30 seconds for indexing (tree-sitter parsing + OpenAI embeddings API calls). Subsequent runs with the same container are instant since the FAISS index is cached in the container filesystem. If the container is removed, indexing repeats.
