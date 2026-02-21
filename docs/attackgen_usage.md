# AttackGen -- Usage Documentation

## Overview
Streamlit web application that generates tailored cybersecurity incident response testing scenarios based on the MITRE ATT&CK framework. Supports multiple LLM providers including OpenAI, Anthropic, Google, Mistral, Groq, and Ollama.

## Quick Start
```bash
docker pull hoomzoom/attackgen
docker run -d -p 8501:8501 hoomzoom/attackgen
```

Open http://localhost:8501 in your browser.

## Base URL
http://localhost:8501

## Core Features
- Generate attack scenarios based on MITRE ATT&CK threat actor groups
- Create custom scenarios from individually selected ATT&CK techniques
- Supports both Enterprise and ICS ATT&CK matrices
- Chat assistant for refining generated scenarios
- Multiple LLM provider support (configured via web UI)

## Pages

### Welcome (Home)
- **URL:** http://localhost:8501
- **Description:** Configuration page where you select LLM provider, enter API credentials, and set organization details (industry, company size).
- **Tested:** Yes

### Threat Group Scenarios
- **URL:** http://localhost:8501/Threat_Group_Scenarios
- **Description:** Select a known threat actor group to auto-extract their ATT&CK techniques and generate an incident response scenario.
- **Tested:** Yes (page loads, scenario generation requires valid API key)

### Custom Scenarios
- **URL:** http://localhost:8501/Custom_Scenarios
- **Description:** Manually select individual ATT&CK techniques to generate a custom scenario.
- **Tested:** Yes (page loads, scenario generation requires valid API key)

### AttackGen Assistant
- **URL:** http://localhost:8501/AttackGen_Assistant
- **Description:** Chat interface to refine and iterate on generated scenarios.
- **Tested:** Yes (page loads, chat requires valid API key)

## Health Check
- **URL:** `/_stcore/health`
- **Method:** GET
- **Response:** `ok`
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | No | None | OpenAI API key |
| ANTHROPIC_API_KEY | No | None | Anthropic API key |
| GOOGLE_API_KEY | No | None | Google AI API key |
| MISTRAL_API_KEY | No | None | Mistral API key |
| GROQ_API_KEY | No | None | Groq API key |
| AZURE_OPENAI_API_KEY | No | None | Azure OpenAI API key |
| AZURE_OPENAI_ENDPOINT | No | None | Azure OpenAI endpoint URL |
| AZURE_DEPLOYMENT | No | None | Azure deployment name |
| LANGCHAIN_API_KEY | No | None | LangSmith tracing key |

API keys can also be entered through the web UI on the Welcome page. Environment variables are optional.

## Notes
- All API keys are optional. The app functions without them but cannot generate scenarios until a valid key is provided.
- MITRE ATT&CK data files (~55 MB) are bundled in the image under `/app/data/`.
- The container runs as non-root user `attackgen` (UID 1000).
- Stateless application. No database or persistent storage required.
- The published Docker Hub image is `mrwadams/attackgen`. We republish under `hoomzoom/attackgen` for this project.

## Changes from Original
- Removed SHA256 pin from base image (`python:3.12-slim@sha256:...` to `python:3.12-slim`) to avoid Docker credential helper issues on remote builds. No functional change.
- Replaced curl-based healthcheck with Python urllib (matching the original Dockerfile's approach). The original `docker-compose.yml` used curl but the Dockerfile used Python urllib. We use the Dockerfile's approach.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed — all minimum versions resolved successfully.
