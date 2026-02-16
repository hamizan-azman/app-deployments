# STRIDE GPT -- Usage Documentation

## Overview
Streamlit web application for AI-powered threat modeling using the STRIDE methodology. Generates threat models, attack trees, mitigations, and DREAD risk assessments for application architectures described in natural language. Supports multiple LLM providers.

## Quick Start
```bash
docker pull hoomzoom/stride-gpt
docker run -d -p 8501:8501 hoomzoom/stride-gpt
```

Open http://localhost:8501 in your browser.

## Base URL
http://localhost:8501

## Core Features
- STRIDE threat modeling from application descriptions
- Attack tree generation (Mermaid diagram format)
- Mitigation recommendations mapped to threats
- DREAD risk scoring for identified threats
- Test case generation for identified threats
- Multiple LLM provider support (OpenAI, Anthropic, Google, Mistral, Groq, Ollama, LM Studio)
- GitHub integration for creating threat model issues

## Usage
1. Open the web UI at http://localhost:8501
2. Select your LLM provider and enter API credentials in the sidebar
3. Describe your application (type, authentication, internet-facing, etc.)
4. Click "Generate Threat Model" to produce STRIDE analysis
5. Optionally generate attack trees, mitigations, DREAD assessment, or test cases

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
| GITHUB_API_KEY | No | None | GitHub API key for issue creation |
| OLLAMA_ENDPOINT | No | http://localhost:11434 | Ollama endpoint |
| LM_STUDIO_ENDPOINT | No | http://localhost:1234 | LM Studio endpoint |

API keys can also be entered through the web UI sidebar. Environment variables are optional.

## Notes
- All API keys are optional. The app loads without them but cannot generate outputs until a valid key is provided.
- The container runs as non-root user `appuser` (UID 1000) inside a virtual environment.
- Stateless application. No database or persistent storage required.
- The published Docker Hub image is `mrwadams/stridegpt`. We republish under `hoomzoom/stride-gpt` for this project.

## Changes from Original
- Removed SHA256 pin from base image (`python:3.12-slim@sha256:...` to `python:3.12-slim`) to avoid Docker credential helper issues on remote builds.
- Replaced curl-based healthcheck with Python urllib. The original Dockerfile's healthcheck uses `curl --fail` but `python:3.12-slim` does not include curl, causing the container to report as unhealthy despite functioning correctly. Our Dockerfile uses `python -c "import urllib.request; ..."` instead.
