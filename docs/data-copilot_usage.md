# Data-Copilot -- Usage Documentation

## Overview
AI system connecting humans and Chinese financial data. Uses OpenAI GPT to generate and execute data analysis code for stocks, funds, economics, and company financials via Tushare API.

## Quick Start
```bash
docker pull hoomzoom/data-copilot:latest
docker run -d -p 7860:7860 \
  -e TUSHARE_TOKEN=your-tushare-token \
  hoomzoom/data-copilot:latest
```

## Base URL
http://localhost:7860

## Requirements
- Tushare Pro token (required for financial data): https://tushare.pro
- OpenAI API key (entered in web UI, or set via code)
- Optional: Azure OpenAI credentials
- No GPU required

## API Endpoints

### Gradio Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Interactive UI for Chinese financial data queries. Enter OpenAI key in the UI, select or type queries about stocks, funds, economy, or companies.
- **Tested:** Yes (200 OK, UI loads)

### API Info
- **URL:** `/info`
- **Method:** GET
- **Description:** Returns Gradio API endpoint metadata
- **Tested:** Yes (200 OK)

### Query Execution (Gradio API)
- **URL:** `/api/predict` (unnamed endpoint 6)
- **Method:** POST
- **Description:** Submit a financial data query for AI-powered analysis
- **Request:** `curl -X POST http://localhost:7860/api/predict -H "Content-Type: application/json" -d '{"data": ["show me CPI trends for the past 10 years"]}'`
- **Tested:** NOT TESTED (requires valid Tushare token + OpenAI key)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| TUSHARE_TOKEN | Yes | - | Tushare Pro API token for financial data |
| OPENAI_API_KEY | No | - | Can also be entered in web UI |
| GRADIO_SERVER_NAME | No | 0.0.0.0 | Server bind address |

## Docker Hub
```bash
docker pull hoomzoom/data-copilot:latest
```

## Notes
- Primarily designed for Chinese financial markets (A-shares, Chinese funds, Chinese economic data)
- UI and example queries are in Chinese
- ZhiPu AI (GLM) integration unavailable due to pydantic v1/v2 conflict. OpenAI and DashScope (Qwen) integrations work.
- CJK fonts pre-installed for matplotlib chart rendering
