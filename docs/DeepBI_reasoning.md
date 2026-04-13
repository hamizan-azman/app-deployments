# DeepBI. Reasoning Log

## Initial Assessment

DeepBI is a business intelligence platform with a Flask backend and Celery worker architecture. The upstream repo includes a Dockerfile. All application services (server, worker, scheduler, AI API, WebSocket) use the same Docker image with different command arguments, following the Celery multi-container pattern.

## What Was Checked

1. **README.md**: Describes DeepBI as an AI BI tool. Docker Compose is the recommended deployment method. Documents environment variables and service ports.

2. **Dockerfile**: Uses `python:3.8.18-slim` base. Installs many system libraries including libpq-dev, unixodbc-dev, libsasl2-modules-gssapi-mit, xmlsec1, and freetds-dev. Heavy dependency list supporting various database connectors. Creates non-root user `deepbi`. Applies importlib_resources fix for Python 3.8 compatibility.

3. **vrequment.txt**: The typo in the filename is intentional (upstream spelling). Contains the full Python dependency list. pip is pinned to 20.2.4 before installing requirements.

4. **docker-compose.yml**: Defines 8 services using the same image for 5 of them (server, server_ai_api, server_socket, scheduler, worker). Redis and PostgreSQL use standard upstream images. maildev handles SMTP in development.

5. **importlib_resources patch**: The `saml2` library uses `from importlib_resources import path` which fails in Python 3.8.18 when `importlib_resources` is not installed as a separate package. The Dockerfile patches the affected files to use the standard library `from importlib.resources import path` instead.

## Decisions Made

### Used the upstream Dockerfile as-is
The upstream Dockerfile is complete and handles the Python 3.8 compatibility issues. The importlib_resources fix is already included. No structural changes were made.

### Kept Python 3.8.18
The upstream requires Python 3.8 due to dependency compatibility constraints. Upgrading to a newer Python version would break several of the pinned dependencies that lack newer-Python-compatible wheels.

### pip 20.2.4 pin
The upstream Dockerfile pins pip to 20.2.4 before installing requirements. This is preserved as-is. Some packages in `vrequment.txt` have resolver behaviors that differ between pip versions.

### PostgreSQL with fsync=off
The postgres service uses `postgres -c fsync=off -c full_page_writes=off -c synchronous_commit=OFF`. This configuration maximizes write performance at the cost of crash safety, appropriate for a development/research deployment where data durability is not critical.

### Redis 3-alpine
The compose file uses `redis:3-alpine`. This is an older Redis version but it is what the upstream specifies and the Celery version in use is compatible with it.

### maildev for SMTP
DeepBI sends email in some workflows. Using maildev means all emails are captured locally, visible at port 1080. No real email infrastructure is needed.

## Testing

### Tests Performed
1. **Docker Compose up**: All 8 services start. Redis and PostgreSQL start first. Pass.
2. **Server health** (GET `http://localhost:8338/`): Returns HTTP 200. Web UI loads. Pass.
3. **Mail dev UI** (http://localhost:1080): maildev interface accessible. Pass.

### What Was Not Tested
- AI analysis features (require OpenAI API key)
- Database connection configuration
- Celery task execution
- WebSocket real-time features

## Gotchas

1. **vrequment.txt typo**: The requirements file is named `vrequment.txt` (not `requirements.txt`). This is the upstream filename and must not be changed.

2. **importlib_resources in Python 3.8**: The saml2 library uses the third-party `importlib_resources` package instead of the standard library `importlib.resources`. On Python 3.8.18 the import fails if the third-party package is not installed. The sed fix in the Dockerfile patches both affected files in saml2.

3. **PostgreSQL trust authentication**: The compose file uses `POSTGRES_HOST_AUTH_METHOD: trust`, which disables password authentication for PostgreSQL. This is appropriate for a development stack where the database is not exposed externally.

4. **Service dependency ordering**: server_ai_api, server_socket, scheduler, and worker all depend on `server`. The server service has a 60s start_period healthcheck. All dependent services wait for server to be healthy before starting.
