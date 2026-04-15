# pr-agent. Reasoning Log

## App Type
FastAPI webhook server (GitHub App mode) with a secondary CLI interface. Receives GitHub webhook events and dispatches AI-powered PR review commands. Port 3000.

## Deployment Decision
Deployed. The app has a well-defined server entrypoint and clear dependency list. It does not require desktop GUI or special hardware. API features require a configured GitHub App and LLM key, but the server infrastructure runs without them.

## Dockerfile Approach
The upstream repository provides a multi-target Dockerfile at `docker/Dockerfile` with separate build stages for different deployment targets (GitHub App, GitHub Action, GitLab, etc.). That Dockerfile is tightly coupled to the upstream build system and includes targets we do not need.

We wrote a simplified single-target Dockerfile from scratch, focused on the GitHub App webhook server target. This matches the architectural fidelity rule: we deploy the app as the original developer intended (GitHub App webhook server), using only the components needed for that target.

Key Dockerfile decisions:
- Base image: `python:3.12-slim`. The upstream uses Python 3.12 and this matches the project's declared requirement.
- System deps: `git` and `curl`. Git is needed because pr_agent internally calls git operations when analyzing diffs. Curl is included for general debugging.
- Non-root user: `appuser` at UID 1000, following standard practice.
- PYTHONPATH set to `/app` so the `pr_agent` package resolves correctly from the working directory.
- Entrypoint: `gunicorn` with `UvicornWorker`, bound to `0.0.0.0:3000`, pointing at `pr_agent.servers.github_app:app`. This matches the upstream's recommended launch command for the GitHub App server.
- The `gunicorn_config.py` inside the upstream repo controls worker count and timeout. We reference it via `-c pr_agent/servers/gunicorn_config.py` so those settings are preserved without modification.

## Healthcheck Rationale
The server requires valid GitHub App credentials before the webhook endpoint becomes functional. A standard HTTP GET to `/` without credentials returns an error, making it unsuitable for a healthcheck. Instead, we use a Python import test: `from pr_agent import cli`. This confirms the package is installed correctly and the Python environment is intact, which is the meaningful infrastructure check for this container. Warnings about a missing secrets.toml during the import are expected behavior from the upstream code and do not affect the test result.

## What Was Tested
- Container starts successfully with Gunicorn and Uvicorn workers.
- Python import test (`from pr_agent import cli`) passes. Expected warnings about secrets.toml appear and are benign.
- Actual PR review, webhook dispatch, and LLM calls were NOT TESTED. These require a configured GitHub App (APP_ID, private key, webhook secret) and a valid LLM API key.

## Environment Variable Notes
The upstream uses a dotenv-style configuration where nested keys use dot notation as environment variable names (e.g., `OPENAI.KEY`, `GITHUB.APP_ID`). These are not standard environment variable names on most systems but the upstream configuration loader reads them correctly. Pass them as-is using `-e` flags in docker run.

The private key for the GitHub App is a multi-line PEM file. When passing it as an environment variable, newlines must be preserved. The recommended approach is to use `$(cat key.pem)` in a shell command or to store it in a `.env` file and pass `--env-file`.

## Port
3000 (default). Configurable via the `PORT` environment variable. The Gunicorn bind address in the entrypoint uses the hardcoded value 3000. To change the port, override the CMD and update the EXPOSE accordingly, or pass `PORT` and use a custom gunicorn config.

## V2 Pinning Notes
The upstream uses `pyproject.toml` for dependency management with `>=` version constraints throughout. We extracted the direct dependencies and generated a `requirements.txt` with exact `==` pins. Transitive dependencies were resolved by installing into a clean Python 3.12 environment and capturing the resulting versions with `pip freeze`. All minimum declared versions were available on PyPI and resolved without conflicts.
