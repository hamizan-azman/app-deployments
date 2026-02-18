# TradingAgents -- Usage Documentation

## Overview
Multi-agent LLM financial trading framework using LangGraph. Orchestrates analyst, researcher, trader, and risk management agents to generate structured investment decisions.

## Quick Start

```bash
docker pull hoomzoom/tradingagents
```

### Interactive CLI
```bash
docker run -it -e OPENAI_API_KEY=sk-... hoomzoom/tradingagents
```

### Library Mode (non-interactive)
```bash
docker run --rm -e OPENAI_API_KEY=sk-... \
  -v ./results:/app/results \
  --entrypoint python hoomzoom/tradingagents main.py
```

## CLI Interface

The interactive CLI prompts for:
1. Ticker symbol (e.g. NVDA)
2. Analysis date
3. Analyst team selection (market, sentiment, news, fundamentals)
4. Research depth (debate rounds)
5. LLM provider and model selection
6. Thinking/reasoning effort levels

## Supported LLM Providers

| Provider | Env Variable | Models |
|----------|-------------|--------|
| OpenAI | `OPENAI_API_KEY` | gpt-5.2, gpt-5-mini |
| Google | `GOOGLE_API_KEY` | Gemini |
| Anthropic | `ANTHROPIC_API_KEY` | Claude |
| xAI | `XAI_API_KEY` | Grok |
| OpenRouter | `OPENROUTER_API_KEY` | Various |
| Ollama | (local) | Any Ollama model |

## Data Sources

Default: yfinance (no API key needed for stock data).
Optional: Alpha Vantage (`ALPHA_VANTAGE_API_KEY`) for enhanced data.

## Output

Reports are written to `./results/{ticker}/{date}/reports/`:
- `1_analysts/` -- market, sentiment, news, fundamentals analysis
- `2_research/` -- bull/bear/manager debate
- `3_trading/` -- trader recommendation
- `4_risk/` -- aggressive/conservative/neutral assessment
- `5_portfolio/` -- final decision
- `complete_report.md` -- consolidated report

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (for OpenAI) | None | OpenAI API key |
| GOOGLE_API_KEY | No | None | Google Gemini API key |
| ANTHROPIC_API_KEY | No | None | Anthropic Claude API key |
| XAI_API_KEY | No | None | xAI Grok API key |
| OPENROUTER_API_KEY | No | None | OpenRouter API key |
| ALPHA_VANTAGE_API_KEY | No | None | Enhanced stock data |
| TRADINGAGENTS_RESULTS_DIR | No | ./results | Output directory |

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | CLI --help | PASS |
| 2 | Library import (TradingAgentsGraph, DEFAULT_CONFIG) | PASS |
| 3 | yfinance data fetch (NVDA 5-day history) | PASS |
| 4 | Full analysis run | NOT TESTED (requires LLM API key) |

## Notes
- CLI is interactive (uses typer + questionary). Run with `-it` flag.
- For non-interactive use, override entrypoint and run `main.py` or custom script.
- DuckDuckGo is not used here; stock data comes from yfinance by default.
- Redis is in requirements but not actively used in the codebase.
- Chainlit is a dependency but not the primary interface.
