# auto-news -- Usage Documentation

## Overview
Automated news aggregation and summarization system built on Apache Airflow. Pulls content from multiple sources (RSS, Reddit, Twitter, YouTube, articles), summarizes with LLMs, and optionally pushes to Notion. Uses Celery for distributed task execution.

## Quick Start

```bash
docker pull finaldie/auto-news:0.9.15
```

Download the docker-compose.yml and .env.example from `dockerfiles/auto-news/`, then:

```bash
# Create workspace directories
mkdir -p workspace/airflow/{logs,config,plugins,data} workspace/postgres/data workspace/redis/data workspace/mysql/data

# Copy and edit environment file
cp .env.example workspace/airflow/config/.env
# Edit workspace/airflow/config/.env with your API keys

# Start all services
docker compose up -d
```

## Base URL
- Airflow Web UI: `http://localhost:8080` (airflow/airflow)
- Adminer (DB admin): `http://localhost:8070`

## Architecture
13 services total:
- Airflow: webserver, scheduler, worker, triggerer, init
- PostgreSQL 13 (Airflow metadata)
- Redis (Celery broker)
- MySQL 8.4 (application data)
- Adminer (database admin UI)

## Airflow DAGs

| DAG | Description |
|-----|-------------|
| news_pulling | Fetches content from configured sources |
| sync_dist | Distributes content to destinations |
| collection_weekly | Weekly content collection summary |
| journal_daily | Daily journal generation |
| action | Action processing pipeline |

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (if using OpenAI) | None | OpenAI API key |
| LLM_PROVIDER | No | openai | LLM backend: openai, google, ollama |
| CONTENT_SOURCES | No | Article,RSS | Content source types |
| NOTION_TOKEN | No | None | Notion API token |
| EMBEDDING_PROVIDER | No | openai | Embedding provider |

## Tests

| # | Test | Result |
|---|------|--------|
| 1 | Image pull | PASS |
| 2 | Airflow webserver health | PASS |
| 3 | Airflow scheduler health | PASS |
| 4 | PostgreSQL connection | PASS |
| 5 | Redis connection | PASS |
| 6 | MySQL connection | PASS |
| 7 | DAG trigger | NOT TESTED (requires .env with API keys) |

## Notes
- Requires 4GB+ RAM for Airflow stack.
- Worker requires `.env` file in `workspace/airflow/config/` or it will exit.
- Milvus vector DB (etcd + minio + milvus) is optional and not included in our compose for simplicity. Add from the original compose if needed.
- Default credentials: Airflow (airflow/airflow), MySQL (bot/bot), PostgreSQL (airflow/airflow).

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning NOT applied. Uses official pre-built image — cannot control dependency versions.
