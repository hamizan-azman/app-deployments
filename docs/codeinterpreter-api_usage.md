# codeinterpreter-api -- Usage Documentation

## Overview
Python library implementing ChatGPT's Code Interpreter using LangChain and CodeBox. Sends user prompts to an LLM (OpenAI/Azure/Anthropic), which generates Python code, executes it in a sandboxed Jupyter kernel (CodeBox), and returns results including text, files, and images.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/codeinterpreter-api

# Or build from source
docker build -t codeinterpreter-api apps/codeinterpreter-api/

docker run --rm -e OPENAI_API_KEY=sk-... hoomzoom/codeinterpreter-api
```

## Type
Library (no web server, no HTTP endpoints). Use interactively or via Python scripts.

## Usage

### Basic Session
```bash
docker run --rm -it -e OPENAI_API_KEY=sk-... codeinterpreter-api python
```
```python
from codeinterpreterapi import CodeInterpreterSession

with CodeInterpreterSession() as session:
    response = session.generate_response("Plot a sin wave")
    print(response.content)
    for f in response.files:
        f.save(f.name)
```

### Run an Example Script
```bash
docker run --rm -e OPENAI_API_KEY=sk-... codeinterpreter-api python examples/plot_sin_wave.py
```

### Async Usage
```python
import asyncio
from codeinterpreterapi import CodeInterpreterSession

async def main():
    async with CodeInterpreterSession() as session:
        response = await session.agenerate_response("What is 2+2?")
        print(response.content)

asyncio.run(main())
```

### With File Input
```python
from codeinterpreterapi import CodeInterpreterSession, File

with CodeInterpreterSession() as session:
    response = session.generate_response(
        "Analyze this dataset",
        files=[File.from_path("data.csv")]
    )
    print(response.content)
```

### Custom Model
```python
from codeinterpreterapi import CodeInterpreterSession, settings

settings.MODEL = "gpt-4-turbo"
# or for Anthropic:
# settings.ANTHROPIC_API_KEY = "sk-ant-..."
# settings.MODEL = "claude-3-sonnet-20240229"
```

## Key Classes

### CodeInterpreterSession
- `start()` / `stop()` -- manage session lifecycle
- `generate_response(user_msg, files=[])` -- send prompt, get response
- `agenerate_response(user_msg, files=[])` -- async version
- Context manager support (`with` / `async with`)

### CodeInterpreterResponse
- `content` -- text response from the LLM
- `files` -- list of File objects (images, generated files)
- `code_log` -- list of (code, output) tuples showing executed code

### File
- `File.from_path(path)` -- load file from disk
- `File.from_url(url)` -- download file from URL
- `save(path)` -- save file to disk
- `show_image()` -- display image (Jupyter/IPython)

### settings (CodeInterpreterAPISettings)
- `OPENAI_API_KEY` -- OpenAI API key
- `MODEL` -- model name (default: gpt-3.5-turbo)
- `TEMPERATURE` -- LLM temperature (default: 0.03)
- `MAX_ITERATIONS` -- max agent iterations (default: 12)
- `CUSTOM_PACKAGES` -- additional pip packages for CodeBox

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes* | None | OpenAI API key |
| AZURE_OPENAI_API_KEY | No | None | Azure OpenAI key (alternative to OpenAI) |
| AZURE_API_BASE | No | None | Azure endpoint URL |
| AZURE_API_VERSION | No | None | Azure API version |
| AZURE_DEPLOYMENT_NAME | No | None | Azure deployment name |
| ANTHROPIC_API_KEY | No | None | Anthropic API key (alternative to OpenAI) |
| CODEBOX_API_KEY | No | None | CodeBox cloud API key (uses local by default) |

*One of OPENAI_API_KEY, AZURE_OPENAI_API_KEY, or ANTHROPIC_API_KEY is required.

## Test Summary
| Test | Result |
|------|--------|
| Library import | PASS |
| Session creation | PASS |
| Session start (local CodeBox) | PASS |
| generate_response (simple math) | PASS -- "2 + 2 is 4" |
| generate_response (fibonacci) | PASS -- code executed, correct output |
| Code log capture | PASS -- code and output recorded |
| Session stop | PASS |

## Notes
- CodeBox runs a local Jupyter kernel inside the container for code execution
- No external services needed beyond the LLM API
- The library uses LangChain 0.1.x (pinned <0.2)
- Streamlit frontend available at `examples/frontend/app.py` but is not the primary interface
- `.env` file support via pydantic-settings
- **Security: executes arbitrary code.** Code Interpreter runs LLM-generated Python in a sandboxed CodeBox, but the container itself has network access. High-value target for code injection research.

## Changes from Original
None. Installed from the developer's pyproject.toml. This is a library with no web server -- deployed as-is.
