# auto-news -- Reasoning Log

## Initial Assessment

auto-news by finaldie is an automated news aggregation system built on Apache Airflow. It pulls content from multiple sources (RSS, Reddit, Twitter, YouTube, web articles), summarizes them using LLMs, and optionally pushes to Notion. The project already has a production-quality docker-compose and a pre-built Docker Hub image.

## What Was Checked

1. **docker/docker-compose.yaml (original)**: 13 services including Airflow stack (webserver, scheduler, worker, triggerer, init, init-user, cli), PostgreSQL 13, Redis, MySQL 8.4, Adminer, and Milvus vector DB stack (etcd, minio, milvus-standalone, milvus-ui). Uses YAML anchors for shared Airflow configuration.

2. **docker/Dockerfile**: Based on `apache/airflow:2.8.4-python3.11`. Installs system deps (ffmpeg, git, etc.), custom Python requirements. The image is already pre-built and published as `finaldie/auto-news:0.9.15`.

3. **.env.template**: Configuration for LLM provider, API keys, content sources, Notion integration, embedding settings.

4. **Worker startup script**: The worker container runs a complex bootstrap that upgrades pip, installs local requirements, copies the .env file to the runtime directory, then starts the Celery worker. It exits with error if .env is missing.

## Decisions Made

### Use pre-built image (docker pull, not docker build)
The developer publishes `finaldie/auto-news:0.9.15` on Docker Hub. No reason to rebuild from source. This matches our pattern for docker-pull apps.

### Simplified docker-compose (13 → 9 services)
The original compose defines 13 services. We removed 4:

| Removed Service | Why |
|----------------|-----|
| etcd | Milvus coordination — only needed for vector search features |
| minio | Milvus object storage — only needed for vector search features |
| milvus-standalone | Vector DB — optional feature for embedding-based retrieval |
| milvus-ui (Attu) | Milvus admin UI — irrelevant without Milvus |

The 9 retained services form the complete Airflow pipeline: webserver, scheduler, worker, triggerer, init (schema migration), PostgreSQL (Airflow metadata), Redis (Celery broker), MySQL (app data), and Adminer (DB admin UI). This is the minimum needed for the news aggregation workflow.

### Removed airflow-init-user service
This service runs post-init to apply patches, copy .env, and unpause DAGs. For our research deployment, users can unpause DAGs manually through the Airflow UI after configuring .env. Removing it avoids a hard failure when .env is missing during first startup.

### Worker .env handling
Changed the worker's .env copy step from `exit 1` on missing file to a warning. This allows the worker to start even without a .env file, though it won't process content without API keys.

### Kept MySQL
The application uses MySQL for its own data storage (separate from Airflow's PostgreSQL metadata DB). Both are needed.

## Testing Plan

1. Pull image: Validates image exists on Docker Hub
2. docker compose up: Validates all services start
3. Airflow webserver health: GET http://localhost:8080/health
4. Airflow scheduler health: Check internal healthcheck
5. PostgreSQL: pg_isready
6. Redis: redis-cli ping
7. MySQL: mysqladmin ping
8. DAG trigger: Requires .env with API keys

## Gotchas

1. **Memory requirements**: Airflow + PostgreSQL + Redis + MySQL needs 4GB+ RAM. Docker Desktop may need memory limit increased.

2. **Worker requires .env**: The Celery worker copies .env from config volume to runtime. Without it, DAGs that process content will fail.

3. **Many services**: Even simplified, the stack runs 9 containers. This is inherent to Airflow's distributed architecture with CeleryExecutor.

4. **Milvus optional**: Vector search features require adding the Milvus stack (4 more containers). Not included by default.

5. **Port conflicts**: Uses ports 8080 (Airflow), 8070 (Adminer), 3306 (MySQL). Check for conflicts with other running services.

6. **Airflow credentials**: Default login is airflow/airflow. Created during init service.
