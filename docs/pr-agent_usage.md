# pr-agent. Usage Documentation

## Overview
FastAPI webhook server and CLI tool for AI-powered pull request review, analysis, and automation. Receives GitHub webhook events and uses an LLM to perform code review, generate PR descriptions, answer questions, and run other PR-related commands. Supports OpenAI, Anthropic, Azure, and other LLM providers.

## Quick Start
```bash
docker pull hoomzoom/pr-agent
docker run -d -p 3000:3000 \
  -e OPENAI.KEY=your_openai_key \
  -e GITHUB.APP_ID=your_app_id \
  -e GITHUB.PRIVATE_KEY="$(cat your_private_key.pem)" \
  -e GITHUB.WEBHOOK_SECRET=your_webhook_secret \
  hoomzoom/pr-agent
```

## Base URL
http://localhost:3000

## Endpoints

### Webhook Receiver
- **URL:** http://localhost:3000/
- **Method:** POST
- **Description:** Receives GitHub App webhook events (pull_request, issue_comment). Routes events to the appropriate PR-Agent command handler.
- **Tested:** Infrastructure only. Full webhook flow requires a configured GitHub App and valid API keys.

### Health Check (import test)
- **Command:** `docker exec <container> python -c "from pr_agent import cli"`
- **Description:** Verifies the pr_agent package imports correctly. Warnings about missing secrets.toml are expected and do not indicate failure.
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI.KEY | Yes (if using OpenAI) | None | OpenAI API key |
| OPENAI.ORG | No | None | OpenAI organization ID |
| ANTHROPIC.KEY | No | None | Anthropic API key (alternative LLM provider) |
| AZURE.OPENAI_KEY | No | None | Azure OpenAI API key (alternative LLM provider) |
| GITHUB.APP_ID | Yes (webhook mode) | None | GitHub App numeric ID |
| GITHUB.PRIVATE_KEY | Yes (webhook mode) | None | GitHub App private key (PEM format, newlines escaped) |
| GITHUB.WEBHOOK_SECRET | Yes (webhook mode) | None | GitHub App webhook secret |
| GITHUB.USER_TOKEN | Yes (CLI mode) | None | GitHub personal access token for CLI usage |
| PORT | No | 3000 | Port the Gunicorn server binds to |
| PYTHONPATH | Set in image | /app | Python module search path |

## CLI Usage
The container can also be used for one-off CLI commands against a specific PR without running the webhook server. Override the entrypoint:

```bash
docker run --rm \
  -e OPENAI.KEY=your_openai_key \
  -e GITHUB.USER_TOKEN=your_github_token \
  hoomzoom/pr-agent \
  python -m pr_agent.cli --pr_url https://github.com/owner/repo/pull/1 review
```

Available CLI commands: `review`, `describe`, `improve`, `ask`, `add_docs`, `generate_labels`.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- The webhook server starts with Gunicorn and Uvicorn workers, bound to 0.0.0.0:3000.
- Warnings about a missing `secrets.toml` file appear at startup. These are expected. Configuration is supplied entirely through environment variables.
- GitHub App mode requires setting up a GitHub App in your GitHub account or organization, installing it on target repos, and pointing the webhook URL to your server.
- API features (actual PR review calls) were NOT TESTED. Infrastructure (server startup, package import) was verified.
- The container is stateless. No database or persistent storage is required.

## Changes from Original
See pr-agent_reasoning.md for full details.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied. A custom requirements.txt was generated from the upstream pyproject.toml dependency list, with all version specifiers converted to exact `==` pins. See v2_pinned_versions.md for the full manifest.
