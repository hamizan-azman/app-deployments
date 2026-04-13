# zotero-arxiv-daily. Reasoning Log

## Initial Assessment

zotero-arxiv-daily is a Python package with no existing Dockerfile. It is a one-shot CLI tool: run once, fetch papers from arXiv, score them against your Zotero library using an LLM, and send an email digest. There is no web server or persistent process.

## What Was Checked

1. **README.md**: Describes the tool as a daily digest generator. Install via pip. Run via `python -m zotero_arxiv_daily` or the `zotero-arxiv-daily` console script. Lists required environment variables for Zotero API, LLM provider, and SMTP email.

2. **pyproject.toml**: Python >= 3.10 constraint. Uses hatchling as build backend. Entry point registered as `zotero-arxiv-daily` console script.

3. **Source code**: Single package `zotero_arxiv_daily/`. The main module fetches from Zotero API, queries arXiv, calls an LLM for relevance scoring, and sends email via smtplib. No HTTP server in the code.

## Decisions Made

### One-shot container pattern
The ENTRYPOINT is `python -m zotero_arxiv_daily`. The container exits after one run. No `restart: unless-stopped` in any compose file. This matches the intended use case of a cron-scheduled daily job.

### Python 3.13-slim
The upstream pyproject.toml requires Python >=3.10. Using 3.13-slim uses the latest stable Python release, has a smaller attack surface, and is explicitly mentioned in the upstream README as a tested version.

### No HTTP endpoint
The healthcheck probes `python -c "import zotero_arxiv_daily"` rather than a network endpoint. This verifies the package installed correctly without requiring a running process.

### Environment variables only for credentials
Zotero API key, LLM API key, and SMTP password are all passed at runtime via environment variables. None are baked into the image. This follows the principle of not storing credentials in tracked files.

## Testing

### Tests Performed
1. **Import check** (`python -c "import zotero_arxiv_daily"`): Module imports successfully. Pass.
2. **Help command** (`python -m zotero_arxiv_daily --help`): Prints usage. Pass.

### What Was Not Tested
- Zotero API fetch (requires valid Zotero API key and user/group ID)
- arXiv paper retrieval (requires network access and valid date range)
- LLM relevance scoring (requires OpenAI or Anthropic API key)
- Email delivery (requires SMTP credentials)

All functional features require external API credentials and are not testable in CI.

## Gotchas

1. **Both user and group ID**: The tool requires either ZOTERO_USER_ID or ZOTERO_GROUP_ID. Providing neither causes a runtime error that is not immediately obvious.

2. **Gmail app passwords**: Standard Gmail accounts require an App Password (not the account password) for SMTP access when 2FA is enabled. The README does not prominently document this.

3. **Run mode**: The container must be run with `--rm` to avoid accumulating exited containers when scheduled as a cron job.
