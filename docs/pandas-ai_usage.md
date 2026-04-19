# pandas-ai. Local Install Guide

## Overview
pandas-ai (PandasAI) is a Python library that attaches natural-language querying to a `pandas.DataFrame`. The user passes a DataFrame and an LLM backend to a `SmartDataframe` or `Agent` wrapper, then issues English questions. The library rewrites them into `pandas` or `SQL` code, runs the code against the frame, and returns the answer or a chart.

## Why Not Dockerized
Two blockers.

1. The upstream repository contains a `docker-compose.yml` that references `./server` and `./client` directories which are not present in the public repo. Attempting to build the compose stack fails immediately with `ERROR. build path does not exist`. The hosted "PandaBI / PandasAI Platform" client and server components are closed-source, only available through the vendor's cloud offering.
2. The remainder of the repo is a pure Python library with no standalone HTTP interface, CLI, or long-running entry point. Libraries are installed into other applications. Containerising one in isolation serves no purpose for the benchmark.

Because the only containerisable artefact (the platform UI) is missing source, and the library itself is not a deployable unit, the app is skipped.

## Requirements
- Python 3.9 to 3.11
- `pip`
- An OpenAI, Azure OpenAI, Anthropic, or local LLM API key

## Installation

```bash
pip install pandasai
```

Optional extras for specific backends or databases.

```bash
pip install "pandasai[excel,google-ai,langchain]"
```

## Usage

```python
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

df = pd.DataFrame({
    "country". ["US", "UK", "DE", "FR"],
    "gdp".     [21.4, 2.83, 3.85, 2.78],
})

llm = OpenAI(api_token="sk-...")
sdf = SmartDataframe(df, config={"llm". llm})

print(sdf.chat("Which country has the highest GDP?"))
```

Charts are saved to `exports/charts/` by default.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PANDASAI_API_KEY | No  | None | Only required if using the hosted PandaBI cloud backend |
| OPENAI_API_KEY   | Yes (if using OpenAI backend) | None | Passed to the `OpenAI` LLM wrapper |

## Notes
- `docker-compose.yml` in the repo root is a stub for the closed-source platform product. Do not attempt to `docker compose up`. It errors out because `./server` and `./client` do not exist.
- For reproducible research, pin `pandasai==2.x` and pass the LLM explicitly. Do not rely on env-var fallbacks.
- GitHub. https://github.com/sinaptik-ai/pandas-ai
