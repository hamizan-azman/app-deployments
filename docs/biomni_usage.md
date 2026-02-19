# Biomni -- Usage Documentation

## Overview
Stanford's general-purpose biomedical AI agent. Uses LLMs with retrieval-augmented planning to execute biomedical research tasks: literature extraction, database queries, computational biology analyses.

## Quick Start
```bash
docker pull hoomzoom/biomni:latest
docker run -d -p 7860:7860 \
  -e ANTHROPIC_API_KEY=your-key \
  hoomzoom/biomni:latest
```

## Base URL
http://localhost:7860

## Requirements
- API key: Anthropic (default) or OpenAI
- First run downloads ~11GB biomedical data lake (takes several minutes)
- No GPU required for agent reasoning (API-based LLMs)

## API Endpoints

### Gradio Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Interactive chat interface for biomedical research tasks
- **Tested:** Infrastructure verified (import + config OK, Gradio launch blocked by data download on first run)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ANTHROPIC_API_KEY | Yes* | - | Anthropic API key (default LLM) |
| OPENAI_API_KEY | Alt | - | OpenAI API key (alternative) |
| BIOMNI_LLM | No | claude-sonnet-4-20250514 | LLM model to use |

*At least one LLM API key required.

## Docker Hub
```bash
docker pull hoomzoom/biomni:latest
```

## Notes
- First startup downloads biomedical data lake (~11GB). Subsequent runs use cached data if volume is mounted: `-v biomni-data:/app/data`
- The agent executes LLM-generated Python code. Run in a sandboxed environment.
- For persistent data, mount a volume: `-v biomni-data:/app/data`
