# sql-explorer. Reasoning Log

## Initial Assessment

sql-explorer is a Django application with a Node.js frontend build step. The upstream repo has no Dockerfile. The application requires database migrations before it can serve requests and needs Node.js only for compiling frontend assets (not at runtime).

## What Was Checked

1. **README.md**: Describes sql-explorer as a Django app for query management. Installation via pip. Lists Django management commands for setup. No Docker documentation present.

2. **requirements/dev.txt**: Python dependencies for the development setup. Includes Django, django-explorer, and supporting libraries.

3. **package.json and package-lock.json**: Node.js dependencies for frontend assets. npm install produces a node_modules directory used by the asset pipeline.

4. **entrypoint.sh**: Shell script that starts the application. Contains Windows CRLF line endings when checked out on Windows.

5. **manage.py**: Standard Django entry point. `python manage.py migrate` runs database migrations. Django shell command creates the admin user and a sample query.

## Decisions Made

### Multi-stage build for Python + Node
The Dockerfile uses a builder stage to install both Python and Node.js dependencies, then copies the results to a runtime stage. This keeps the final image from including build tools and NVM installer scripts while ensuring Node.js is available at runtime (needed by the entrypoint for asset serving).

### NVM for Node.js
The upstream does not specify a Node version constraint. NVM v0.39.0 is used to install Node 20.15.1 (LTS at time of writing). The NVM installation uses a `curl | bash` pattern inside Docker, which is acceptable here since it is a controlled build environment.

### Migrations and admin user at build time
Running `python manage.py migrate` at build time produces a ready-to-use SQLite database baked into the image. This means researchers can start the container and immediately log in without a setup step. The tradeoff is that the SQLite database is embedded in the image layer, not on a volume. For supply chain research purposes this is appropriate.

### Sample query at build time
A sample query (`select * from explorer_query`) is created if no queries exist. This provides a working starting point visible immediately on first login.

### Fixed CRLF in entrypoint.sh
`sed -i 's/\r$//' /app/entrypoint.sh` is applied twice (once at the initial copy location and once at the final entrypoint location) to ensure both copies have LF line endings.

### python:3.12.4 (not slim) for runtime
The runtime stage uses `python:3.12.4` without the `-slim` suffix because several Django dependencies (including lxml and database drivers) require shared libraries present in the full image.

## Testing

### Tests Performed
1. **Health check** (GET `http://localhost:8000/`): Returns HTTP 200. Pass.
2. **Django admin** (GET `http://localhost:8000/admin`): Login page loads. Pass.
3. **Admin login**: Login with admin/admin succeeds. Pass.
4. **Query editor**: Explorer interface loads with sample query. Pass.

### What Was Not Tested
- AI SQL generation (requires OPENAI_API_KEY)
- Connecting to external databases via DATABASE_URL
- CSV and JSON export

## Gotchas

1. **SQLite baked in**: The SQLite database containing migrations and the admin user is baked into the image at build time. Starting a new container gives a fresh database with admin user and sample query. There is no volume persistence by default.

2. **NVM curl pipe bash**: The Dockerfile installs NVM via `curl ... | bash`. This is the official NVM installation method. The risk is acceptable in a Docker build context with a pinned NVM version.

3. **entrypoint.sh starts two processes**: The entrypoint starts both Django dev server (port 8000) and a Node process (port 5173). Only port 8000 is exposed. If the Node process fails, the container continues serving Django normally.

4. **python:3.12.4 full image**: Using the full Python image (not slim) adds approximately 300MB to the final image size compared to slim. This is necessary for the database driver and XML processing libraries.
