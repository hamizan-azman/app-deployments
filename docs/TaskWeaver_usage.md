# TaskWeaver. Usage Documentation

## Overview
Microsoft's code-first agent framework that uses LLMs to plan tasks and generate Python code for execution. Provides both a CLI and a Chainlit web UI for interactive sessions.

## Quick Start
```bash
docker pull hoomzoom/taskweaver
docker run -d -p 8000:8000 -e LLM_OPENAI_API_KEY=your-key hoomzoom/taskweaver
```

Open http://localhost:8000 in your browser.

## Base URL
http://localhost:8000

## Core Features
- Task planning and decomposition using LLMs
- Automatic Python code generation and execution
- Chainlit web UI for interactive chat
- Configurable roles: planner, code interpreter, web search
- Multiple LLM provider support (OpenAI, Google Gemini, ZhipuAI, DashScope)

## Endpoints

### Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Chainlit web interface for interactive task conversations.
- **Tested:** Yes (200)

### Readme
- **URL:** `/readme`
- **Method:** GET
- **Description:** Application readme/about page.
- **Tested:** Yes (200)

### Project Settings
- **URL:** `/project/settings`
- **Method:** GET
- **Description:** Chainlit project configuration and settings.
- **Response:** JSON with UI configuration, auth settings, and features.
- **Tested:** Yes (200)

### Project Translations
- **URL:** `/project/translations`
- **Method:** GET
- **Description:** UI translation strings.
- **Tested:** Yes (200)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| LLM_OPENAI_API_KEY | Yes* | None | OpenAI API key |
| LLM_OPENAI_MODEL | No | gpt-4-1106-preview | OpenAI model name |
| LLM_OPENAI_API_BASE | No | https://api.openai.com/v1 | OpenAI API base URL |

*At least one LLM API key is required. The server will not start without one.

Environment variable format: config key in uppercase with dots replaced by underscores. For example, `llm.openai.api_key` becomes `LLM_OPENAI_API_KEY`.

## Notes
- The container runs as a dynamically created non-root user `taskweaver` (UID 10002 by default).
- Code execution happens locally inside the container (kernel mode: local). TaskWeaver executes generated Python code directly, so treat the container as an untrusted execution environment.
- The web search role is included by default but requires the `WITH_WEB_SEARCH=true` build argument to install dependencies (sentence-transformers, FAISS, LangChain). Building with web search downloads a ~500 MB embedding model during image build. Use `--build-arg WITH_WEB_SEARCH=false` for a smaller image without web search.
- Security warning: TaskWeaver generates and executes arbitrary Python code. Run in an isolated environment only.

## Changes from Original
- Changed the default ENTRYPOINT from CLI mode (`entrypoint.sh`) to Chainlit web UI mode (`entrypoint_chainlit.sh`). The original Dockerfile starts an interactive terminal session, which is not useful for Docker deployment. The web UI provides the same functionality through a browser.
- Built with `WITH_WEB_SEARCH=false` for the Docker Hub image to avoid network timeouts downloading the sentence-transformers model during build. Web search can be added by rebuilding with `--build-arg WITH_WEB_SEARCH=true`.

## V2 Dependency Changes (Minimum Version Pinning)
- `matplotlib==3.4` → `matplotlib==3.7.0` (3.4 has no prebuilt wheels for Python 3.12, fails to build from source)
- `seaborn==0.11` → `seaborn==0.11.0` (version format fix)
- `pyyaml==6.0` → `pyyaml==6.0.0` (version format fix)
- `numpy==1.24.2` → `numpy==1.26.0` (needed for compatibility with sentence-transformers numpy 2.x transitive dep)
- `scikit-learn==1.2.2` → `scikit-learn==1.5.0` (1.2.2/1.3.0 incompatible with numpy 2.x pulled by sentence-transformers)
