# django-ai-assistant. Reasoning Log

## Initial Assessment

django-ai-assistant by Vinta Software is a Django library for building AI assistants with LangChain/LangGraph. It includes a complete example application with React frontend, multiple demo assistants, and a django-ninja REST API. The example app is what we deploy.

## What Was Checked

1. **pyproject.toml**: Poetry-based. Python ^3.10, Django >=4.2, langchain ^1.2.6, langgraph ^1.0.6, langchain-openai ^1.1.7, django-ninja ^1.5.3. Example group adds webpack-loader, langchain-anthropic, scikit-learn, etc.

2. **example/example/settings.py**: Standard Django settings. SQLite database with WAL mode for concurrent access. webpack_loader configured for frontend bundles. django-ai-assistant settings for permissions. API keys via environment variables.

3. **example/example/urls.py**: Admin panel + demo app views. The django-ai-assistant API is mounted automatically via the init function.

4. **example/package.json**: Node 20, React 18, Webpack 5, Mantine UI components, pnpm for package management.

5. **example/webpack.config.js**: Dev server on port 3000 with publicPath pointing to localhost:3000. For production build, this needs to be changed to serve from Django static files.

## Decisions Made

### Multi-stage build (Node + Python)
Stage 1 builds the React frontend with webpack in production mode. Stage 2 installs Python dependencies and copies the built bundles. This avoids shipping Node.js in the final image.

### Changed webpack publicPath for production
The original webpack config sets `publicPath: "http://localhost:3000/webpack_bundles/"` which is for the dev server. Changed to `/static/webpack_bundles/` so Django can serve the bundles via STATIC_URL.

### Poetry --only main --no-root for library deps
Installs only production dependencies of the library. Example-specific deps (webpack-loader, langchain-anthropic, etc.) installed separately via pip since they're in a Poetry group that's harder to install selectively.

### Pre-created superuser
Created admin/admin superuser during build so testers can immediately access the admin panel and authenticate for API calls. The API requires Django session auth.

### Used runserver instead of gunicorn
The example is designed for development use. While gunicorn would be better for production, using runserver preserves the original developer's intent and serves static files without additional configuration.

### SQLite kept as database
The example uses SQLite with WAL mode. This is sufficient for a research deployment and avoids adding PostgreSQL to the stack. The WAL + IMMEDIATE transaction mode handles concurrent tool calls.

## Build Issues

### Poetry --no-dev deprecated
Same as Integuru. Fixed with `--only main`.

### Missing README.md
Same pattern. Fixed with `--no-root`.

### Frontend needs pnpm-lock.yaml
The example uses pnpm for package management. The lock file must be copied alongside package.json for reproducible installs.

## Testing Plan

1. Server starts without errors
2. Admin panel loads at /admin/
3. React frontend loads at / (webpack bundles served correctly)
4. API endpoints respond (list assistants, create/delete threads)
5. Message sending (requires OPENAI_API_KEY)

## Gotchas

1. **Session auth required**: All API endpoints require Django authentication. Must log in via admin panel first, then use the session cookie.

2. **Frontend publicPath**: If the webpack publicPath isn't changed from localhost:3000, the React app won't load its JS bundles when served by Django.

3. **Multiple API keys**: Different demo assistants need different keys (OpenAI for base, weather API for weather assistant, Brave for search, Jina for web scraping). Only OPENAI_API_KEY is mandatory.

4. **Node 20 required for build**: The frontend build requires Node 20. The final image doesn't need Node.
