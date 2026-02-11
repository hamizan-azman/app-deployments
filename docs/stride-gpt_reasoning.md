# stride-gpt. Reasoning Log

## Initial Assessment

STRIDE GPT is a Streamlit application for AI-powered threat modeling using the STRIDE methodology. Like AttackGen, it has an existing Dockerfile and docker-compose.yml with good security practices (non-root user, SHA256-pinned base image). Both apps are by the same developer (mrwadams) and follow similar patterns.

## What Was Checked

1. **README.md**: Describes STRIDE threat modeling with LLM support. Lists features: threat model generation, attack trees, mitigations, DREAD scoring, test case generation. Supports OpenAI, Anthropic, Google, Mistral, Groq, Ollama, LM Studio, and custom OpenAI-compatible endpoints.

2. **Dockerfile**: Similar structure to AttackGen. Uses `python:3.12-slim` with SHA256 pin. Creates non-root user `appuser` (UID 1000). Uses a virtual environment for dependencies. Healthcheck uses `curl --fail` (problematic since the slim image has no curl). Entry point runs Streamlit on 0.0.0.0:8501.

3. **docker-compose.yml**: Security hardening matching AttackGen (no-new-privileges, cap_drop ALL, tmpfs mounts, resource limits). Uses curl for healthcheck.

4. **.env.example**: Lists API keys for all supported providers plus Ollama and LM Studio endpoint URLs.

5. **Application structure**: Main entry is `main.py`. Single-file Streamlit application. No subpages directory, all functionality is in the main module with tabs.

6. **Docker Hub**: Published image exists at `mrwadams/stridegpt`.

## Decisions Made

### Used existing Dockerfile with two modifications
The Dockerfile is well-made. Two changes were needed.

### Removed SHA256 pin
Same issue as AttackGen. The SHA256 pin causes Docker credential helper failures when building via SSH to Windows Docker Desktop. Removed the pin, using `python:3.12-slim` instead.

### Replaced curl healthcheck with Python urllib
The original Dockerfile uses `curl --fail http://localhost:8501/_stcore/health` for the healthcheck. However, `python:3.12-slim` does not include curl. This means the container always reports as "unhealthy" even though the application works correctly. We replaced this with `python -c "import urllib.request. urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=2)"` which matches what AttackGen does and works without additional packages. This is a genuine bug fix in the original Dockerfile.

### Did not add curl to the image
An alternative fix would be to install curl in the Dockerfile. But adding packages increases attack surface and image size. Using Python's stdlib is cleaner and consistent with AttackGen's approach from the same developer.

## Testing

### Tests Performed
1. **Health check** (GET `/_stcore/health`): Returns `ok`. Pass.
2. **Main page** (GET `/`): Returns HTTP 200, Streamlit UI loads. Pass.

### What Was Not Tested
- Actual threat model generation (requires valid API key)
- Attack tree Mermaid diagram rendering
- GitHub issue creation
- Ollama and LM Studio provider connections

## Gotchas

1. **Curl not in slim image**: The original Dockerfile's healthcheck uses curl which is not available in `python:3.12-slim`. This causes Docker to mark the container as "unhealthy" even though the app works fine. Our fix uses Python urllib instead.

2. **Same credential/BuildKit issues as AttackGen**: Both repos are by the same developer, use the same base image and SHA256 pinning approach. Same workarounds needed for remote Docker builds.

3. **Virtual environment in container**: Unlike AttackGen which installs packages globally, STRIDE GPT creates a virtualenv at `/home/appuser/venv` and installs packages there. This is handled by the PATH configuration in the Dockerfile.
