# zotero-arxiv-daily. Usage Documentation

## Overview
CLI tool that fetches new arXiv papers matching your Zotero library topics and sends a daily digest email. Runs as a one-shot process: fetch papers, filter by relevance using an LLM, format a digest, and send via SMTP. Designed for use as a scheduled container (cron job or CI schedule).

## Quick Start
```bash
docker pull hoomzoom/zotero-arxiv-daily
docker run --rm \
  -e ZOTERO_API_KEY=your_zotero_key \
  -e ZOTERO_USER_ID=your_user_id \
  -e ZOTERO_GROUP_ID=your_group_id \
  -e OPENAI_API_KEY=your_openai_key \
  -e EMAIL_ADDRESS=your@email.com \
  -e EMAIL_PASSWORD=your_app_password \
  hoomzoom/zotero-arxiv-daily
```

## Base Command
```bash
docker run --rm [ENV_VARS] hoomzoom/zotero-arxiv-daily [OPTIONS]
```

The container exits after completing one run. It is not a persistent service.

## Core Features
- Reads your Zotero library to understand your research interests
- Fetches recent arXiv preprints matching relevant categories
- Uses LLM scoring to rank papers by relevance to your library
- Sends a formatted HTML digest via email (SMTP)
- One-shot execution model, suitable for daily cron scheduling

## CLI Options
```bash
docker run --rm -e ... hoomzoom/zotero-arxiv-daily --help
```

Common options include specifying date ranges, arXiv categories, and number of papers to include.

## Health Check
The container health check verifies the module imports successfully:
```bash
python -c "import zotero_arxiv_daily"
```
There is no HTTP endpoint.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ZOTERO_API_KEY | Yes | None | Zotero API key (from zotero.org/settings/keys) |
| ZOTERO_USER_ID | Conditional | None | Zotero user ID (for personal libraries) |
| ZOTERO_GROUP_ID | Conditional | None | Zotero group ID (for group libraries) |
| OPENAI_API_KEY | Conditional | None | OpenAI key for LLM relevance scoring |
| ANTHROPIC_API_KEY | Conditional | None | Anthropic key (alternative to OpenAI) |
| EMAIL_ADDRESS | Yes | None | Sender email address |
| EMAIL_PASSWORD | Yes | None | SMTP password or app-specific password |
| SMTP_HOST | No | smtp.gmail.com | SMTP server host |
| SMTP_PORT | No | 587 | SMTP server port |

Either ZOTERO_USER_ID or ZOTERO_GROUP_ID must be provided. Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be provided for LLM scoring.

## Scheduled Execution

To run daily at 08:00:
```bash
# Using docker run in a cron job
0 8 * * * docker run --rm \
  -e ZOTERO_API_KEY=your_key \
  -e ZOTERO_USER_ID=your_id \
  -e OPENAI_API_KEY=your_openai_key \
  -e EMAIL_ADDRESS=your@email.com \
  -e EMAIL_PASSWORD=your_password \
  hoomzoom/zotero-arxiv-daily
```

## Notes
- This is a one-shot CLI tool. The container exits after each run.
- Python 3.13-slim base image is used, matching upstream requirements.
- The container runs as non-root user `appuser` (UID 1000).
- Email credentials should be passed via environment variables, never stored in the image.
- Gmail users should use an App Password, not their account password.
- API features (LLM scoring, Zotero fetch, email send) are NOT TESTED in CI.

## Changes from Original
No existing Dockerfile in the upstream repo. Dockerfile written from scratch following the CLI one-shot pattern.

## V2 Dependency Changes (Minimum Version Pinning)
Package installed via `pip install .` from pyproject.toml. Exact versions resolved by pip at build time.
