# attackgen -- Reasoning Log

## Initial Assessment

AttackGen is a Streamlit application for generating cybersecurity incident response scenarios using MITRE ATT&CK data and LLMs. The repo already has an excellent Dockerfile and docker-compose.yml, both written with security best practices (non-root user, SHA256-pinned base image, healthcheck, resource limits).

## What Was Checked

1. **README.md**: Describes the app as a tool for generating tailored incident response scenarios. Lists supported LLM providers (OpenAI, Anthropic, Google, Mistral, Groq, Ollama, Azure OpenAI). Documents Docker usage with both standalone and docker-compose approaches.

2. **Dockerfile**: Well-structured. Uses `python:3.12-slim` with SHA256 pin. Creates non-root user `attackgen` (UID 1000). Installs deps, copies app, exposes 8501. Healthcheck uses Python urllib (smart choice since slim images lack curl). Entry point runs Streamlit on 0.0.0.0:8501.

3. **docker-compose.yml**: Adds security hardening (no-new-privileges, cap_drop ALL, tmpfs mounts, resource limits, read-only data volume). References `.env` file for API keys.

4. **.env.example**: Lists all supported API key variables. All optional since keys can be entered via the web UI.

5. **Application structure**: Main entry is `00_Welcome.py` (with emoji in filename). Pages directory contains three Streamlit pages for threat group scenarios, custom scenarios, and a chat assistant. Data directory contains MITRE ATT&CK STIX JSON files (~55 MB total).

6. **Docker Hub**: Published image exists at `mrwadams/attackgen`.

## Decisions Made

### Used the existing Dockerfile as-is (with one modification)
The Dockerfile is well-constructed and follows best practices. No reason to rewrite it. The only modification was removing the SHA256 pin from the base image reference.

### Removed SHA256 pin
The original Dockerfile pins `python:3.12-slim@sha256:d86b4c74b936c438cd4cc3a9f7256b9a7c27ad68c7caf8c205e18d9845af0164`. When building via SSH to a Windows desktop running Docker Desktop, the Docker credential helper (`docker-credential-desktop.exe`) fails because it cannot access the Windows Credential Manager from an SSH session. This causes all image pulls and builds to fail with "A specified logon session does not exist." The fix was to use `DOCKER_BUILDKIT=0` (legacy builder) and remove the SHA256 pin since the legacy builder still attempts credential lookups on pinned references. Using `python:3.12-slim` without a pin resolves this. The pin is a nice-to-have for reproducibility but does not affect functionality.

### Did not modify the docker-compose.yml
The compose file references `.env` which makes it fail if the file doesn't exist. For our deployment we use `docker run` directly without the compose file. The compose file is provided in the dockerfiles directory for reference.

### Kept all API keys optional
The app is designed to accept API keys through its web UI. No keys are required at container startup. This is ideal for our deployment since researchers can configure their own keys.

## Testing

### Tests Performed
1. **Health check** (GET `/_stcore/health`): Returns `ok`. Pass.
2. **Main page** (GET `/`): Returns HTTP 200, Streamlit page loads. Pass.
3. **Threat Group Scenarios page**: Accessible at `/Threat_Group_Scenarios`. Page loads with ATT&CK group selection. Pass (scenario generation requires a valid API key, not tested).
4. **Custom Scenarios page**: Accessible at `/Custom_Scenarios`. Page loads with technique selection. Pass.
5. **AttackGen Assistant page**: Accessible at `/AttackGen_Assistant`. Chat interface loads. Pass.

### What Was Not Tested
- Actual scenario generation (requires valid API key)
- LangSmith tracing integration
- Azure OpenAI and Ollama provider connections

## Gotchas

1. **SHA256 pin and Docker credential helper**: As described above, the SHA256-pinned base image reference causes credential lookups that fail in SSH sessions on Windows Docker Desktop. Solution: remove the pin for remote builds.

2. **DOCKER_BUILDKIT=0 required**: BuildKit also has credential issues in SSH sessions. Must use the legacy builder with `set DOCKER_BUILDKIT=0&&docker build ...` (no space before `&&` on Windows CMD to avoid trailing whitespace in the env var value).

3. **Emoji in filename**: The entry point file is `00_Welcome.py` (with a waving hand emoji). This works fine in Docker but could cause issues on filesystems that don't support Unicode. Not a problem for Linux containers.

4. **Healthcheck uses Python, not curl**: The Dockerfile correctly uses Python urllib for the healthcheck since `python:3.12-slim` doesn't include curl. The docker-compose.yml also uses the Python approach. This is a good pattern for slim-based images.
