# sql-explorer. Usage Documentation

## Overview
Django web application for collaborative SQL query management and execution. Provides a browser-based SQL editor, saved query library, query history, and data export. Includes an AI assistant feature for natural language to SQL generation. Multi-stage build with Node.js (NVM) for frontend asset compilation alongside the Python/Django backend.

## Quick Start
```bash
docker pull hoomzoom/sql-explorer
docker run -d -p 8000:8000 hoomzoom/sql-explorer
```

Open http://localhost:8000 in your browser. Default credentials: `admin` / `admin`.

## Base URL
http://localhost:8000

## Core Features
- SQL query editor with syntax highlighting
- Saved query library with sharing
- Query history and result export (CSV, JSON)
- AI assistant for natural language to SQL (requires OpenAI API key)
- Django admin interface at `/admin`
- Sample query pre-loaded on first run

## Pages

### SQL Explorer Home
- **URL:** http://localhost:8000
- **Description:** Query editor and saved query browser.
- **Tested:** Yes

### Django Admin
- **URL:** http://localhost:8000/admin
- **Description:** Django admin interface for managing users and data.
- **Tested:** Yes (login with admin/admin)

## Health Check
- **URL:** http://localhost:8000/
- **Method:** GET
- **Response:** HTTP 200
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | No | None | Enables AI SQL generation feature |
| DATABASE_URL | No | SQLite (built-in) | Connection string for target database |
| DJANGO_SETTINGS_MODULE | No | explorer.settings.dev | Django settings module |
| SECRET_KEY | No | dev default | Django secret key (change for production) |

## Default Admin Account
- **Username:** admin
- **Password:** admin

This account is created at build time via a Django shell command. Change the password for any non-local deployment.

## Notes
- SQLite database is used by default and is baked into the image at build time with migrations already applied.
- The container runs as non-root user `appuser` (UID 1000).
- The entrypoint script starts both the Django development server on port 8000 and the Vite/Node frontend asset server on port 5173. Only port 8000 is exposed externally.
- Node.js (v20.15.1) is installed via NVM in the builder stage and copied to the runtime stage.
- AI SQL generation features are NOT TESTED in CI (require valid OpenAI API key).

## Changes from Original
Multi-stage build written from scratch (no upstream Dockerfile). Windows line endings in `entrypoint.sh` are fixed with `sed -i 's/\r$//'`. Database migrations and admin user creation run at image build time for a ready-to-use container.

## V2 Dependency Changes (Minimum Version Pinning)
Python dependencies installed from `requirements/dev.txt` via pip. Node dependencies installed from `package-lock.json` via npm.
