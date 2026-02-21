# LLM Application Deployment Collection

Dockerized deployment of 41 open-source LLM applications for supply chain security research. Each app is containerized, tested, and documented with usage guides and reasoning logs.

## At a Glance

- **41 apps deployed** across web UIs, CLI tools, and libraries
- **8 apps skipped** (incompatible with Docker, local install docs provided)
- **48 Docker images** published to [Docker Hub](https://hub.docker.com/u/hoomzoom) under `hoomzoom/`
- **Every app tested** with documented pass/fail results per endpoint

## Quick Start

Pick any app and pull from Docker Hub:

```bash
docker pull hoomzoom/attackgen
docker run -p 8501:8501 hoomzoom/attackgen
```

For multi-container apps (devika, auto-news, localGPT, etc.), use the provided docker-compose files:

```bash
cp dockerfiles/devika/docker-compose.yml .
cp dockerfiles/devika/.env.example .env
docker compose up
```

Each app's usage doc has the exact commands.

## Full App Catalog

See **[App Catalog](Task1.md)** for the complete list with:
- GitHub links, Docker images, and test results for all 41 apps
- API key requirements and security warnings
- Multi-container setup instructions
- Notes on deprecated dependencies and supply chain concerns

## Repo Structure

```
dockerfiles/       Dockerfiles, docker-compose files, and .env.example templates
docs/              Usage docs (*_usage.md) and reasoning docs (*_reasoning.md)
tracker.md         Status tracker with test counts
Task1.md           Full app catalog with Docker images and test results
```

## Documentation

Every deployed app has two docs in `docs/`:

- **Usage doc** (`<app>_usage.md`): Docker commands, API endpoints, curl examples, environment variables, test results, and changes from original source
- **Reasoning doc** (`<app>_reasoning.md`): Deployment decisions, debugging steps, alternatives considered, and gotchas

Skipped apps also have usage docs with local install instructions.

## Highlights

| Category | Apps | Examples |
|----------|------|----------|
| AI agents | 12 | SWE-agent, devika, AgentGPT, gpt-engineer, TaskWeaver, agenticSeek |
| Research tools | 8 | gpt-researcher, local-deep-researcher, RD-Agent, Data-Copilot, TradingAgents |
| NLP/ML | 7 | pycorrector, zshot, HuixiangDou, FunClip, omniparse |
| Security | 3 | attackgen, stride-gpt, Integuru |
| Developer tools | 6 | ChatDBG, codeqai, gptme, rawdog, gpt-migrate, codeinterpreter-api |
| Content generation | 6 | NarratoAI, slide-deck-ai, bilingual_book_maker, manga-image-translator, pyvideotrans, Paper2Poster |
| RAG/Q&A | 5 | pdfGPT, localGPT, BettaFish, Biomni, chemcrow-public |
| Other | 3 | auto-news, django-ai-assistant, gpt_academic |

## Security Notes

- 8 apps execute arbitrary code by design (rawdog, gpt-engineer, SWE-agent, codeinterpreter-api, gpt-migrate, gptme, TaskWeaver, devika). Run in isolated environments only.
- SWE-agent requires Docker socket access (`-v /var/run/docker.sock`), giving the container full control over the host Docker daemon.
- About half the apps require an OpenAI API key (or similar) for full functionality. Without a key, infrastructure still runs.
