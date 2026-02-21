# AgentGPT. Reasoning Log

## Why This App Was Initially Skipped

AgentGPT was originally marked as SKIP because the repo is archived and unmaintained. On second look, that was wrong. Archived means no new commits, not that the code is broken. The docker-compose, Dockerfiles, and application code are all complete and functional. It's a full-stack web app with a rich attack surface (auth, database, LLM agent execution, OAuth), making it valuable for security research.

## Repo Structure

The app has three services defined in docker-compose.yml:
- **frontend**: Next.js 13 app (node:19-alpine). Handles the UI, user auth (NextAuth with Prisma), and communicates with the platform API.
- **platform**: FastAPI backend (python:3.11). Handles agent logic, tool execution, database operations, and LLM calls via LangChain + OpenAI.
- **agentgpt_db**: MySQL 8.0 with a setup.sql that creates the reworkd_platform user with broad privileges.

Key files I looked at:
- `docker-compose.yml`: Service definitions, port mappings (3000, 8000, 3307), volume mounts, env file references
- `.env.example`: All configuration vars. The platform reads env from `next/.env` (shared env file)
- `platform/pyproject.toml`: Dependencies including langchain 0.0.295, lanarky 0.7.15, openai 0.28.0, pydantic <2
- `next/package.json`: Requires node >=18 <19 but Dockerfile uses node:19 (works anyway since npm doesn't enforce engine checks by default)
- `next/entrypoint.sh`: Waits for DB, runs Prisma migrate, generates Prisma client, then starts Next.js
- `platform/reworkd_platform/web/api/agent/views.py`: All agent endpoints (start, analyze, execute, create, summarize, chat, tools)
- `platform/reworkd_platform/settings.py`: Config management via pydantic settings, all prefixed with REWORKD_PLATFORM_

## Dockerfile Fix: Debian Buster EOL

The platform Dockerfile used `python:3.11-slim-buster`. Debian Buster went EOL and its apt repos were removed from the main mirrors, so `apt-get update` fails with 404 Not Found.

Fix: Changed base image to `python:3.11-slim-bookworm` and switched `openjdk-11-jdk` to `openjdk-17-jdk-headless` (Java 11 is available on bookworm but 17 is the default and headless is smaller). Also fixed the `FROM ... as` casing to `FROM ... AS` to satisfy the Dockerfile linter.

## langchain Version Mismatch

After building, the platform crashed on startup:
```
ModuleNotFoundError: No module named 'langchain.globals'
```

The poetry.lock resolved `lanarky==0.7.17` which imports `from langchain.globals import get_llm_cache`. But langchain was locked to 0.0.295, which doesn't have the `globals` module (added around 0.0.330).

First attempt: upgraded to langchain 0.0.350. This pulled in `langchain-community` and `langchain-core` (the transitional split packages), causing a different import error: `cannot import name '_signature' from 'langchain_community.chat_models.baichuan'`.

Working fix: `langchain==0.0.335`. This version has `langchain.globals` but predates the community/core split, so all imports from `langchain.chat_models` still work natively. Added `pip install langchain==0.0.335` to the Dockerfile after poetry install to override the locked version.

This is an era-matching problem similar to pdfGPT. The project was abandoned with a poetry.lock that pins specific versions, but lanarky's loose version constraint resolved to a newer minor version that needs a newer langchain. The fix is to find the narrow window where both packages' imports are satisfied.

## Test Rationale

Tested three categories:

**Infrastructure (no auth needed):**
- /api/monitoring/health: Confirms FastAPI app started and DB connected
- /api/monitoring/error: Confirms error handling pipeline works (intentional 500)
- /api/docs and /api/openapi.json: Confirms all routes registered correctly
- /api/agent/tools: Returns available tools (no auth needed for this endpoint)
- /api/metadata: URL metadata extraction (no auth needed)

**Auth-gated endpoints:**
- /api/agent/start: Returns 403 without auth token. Confirms auth middleware works.
- /api/models: Same. 403 without auth.

**Frontend:**
- GET localhost:3000: Confirms Next.js built and serves the UI

Full agent execution (start -> analyze -> execute -> create -> summarize) requires an OpenAI API key AND a valid auth session. Not tested since we don't have keys configured.

## What's Interesting for Security Research

- **Large dependency surface**: langchain, openai, lanarky, pinecone, boto3, stripe, grpcio, kafka. Many are from mid-2023 and have known CVEs.
- **Auth system**: NextAuth with Google/GitHub/Discord OAuth, Prisma adapter, MySQL backend. Multiple auth flows to test.
- **Agent execution**: User-supplied goals get decomposed into tasks, passed to LLMs, and tool results get executed. Prompt injection vectors.
- **Streaming responses**: Uses lanarky's StreamingResponse. SSE parsing and error handling paths.
- **Database**: Raw SQL in setup.sql with broad GRANT permissions. Prisma ORM for application queries.
- **Metadata extraction**: `/api/metadata?url=` fetches arbitrary URLs server-side (SSRF potential).

## Gotchas

1. **Shared .env file**: Both frontend and platform read from `next/.env`. The docker-compose mounts it as a volume, so you must create it before `docker compose up`.
2. **Prisma migration**: The frontend entrypoint runs `npx prisma migrate deploy` on first start. If the DB isn't ready, it retries via `wait-for-db.sh`.
3. **Dev mode only**: The docker-compose runs frontend with `npm run dev` (not a production build). Hot reload is enabled on both services.
4. **MySQL port**: MySQL listens on 3307 internally (not 3306). Mapped to 3308 on the host to avoid conflicts.
5. **Volume mounts**: The compose mounts source directories as volumes (`./platform:/app/src/`, `./next/:/next/`). This means the source code on disk overrides what's in the image. For a clean deploy, remove the volume mounts.
