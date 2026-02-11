# gptme. Usage Documentation

## Overview
CLI and web-based AI coding assistant with a Flask API server. Supports interactive conversations, code execution, conversation management, and MCP integration.

## Quick Start

Build the base image first, then the server image (two-stage build, must be run from the gptme repo root):

```bash
docker build -f scripts/Dockerfile -t gptme-base .
docker build -f scripts/Dockerfile.server --build-arg BASE=gptme-base -t gptme-server .
```

Or pull the pre-built image:

```bash
docker pull hoomzoom/gptme-server
```

Run the container (at least one LLM API key is required):

```bash
docker run -d -p 5700:5700 \
  -e OPENAI_API_KEY=your-key \
  hoomzoom/gptme-server
```

Check the container logs for the auto-generated auth token:

```bash
docker logs <container-id>
```

## Base URL
http://localhost:5700

## Authentication
The server uses token-based authentication. On startup it auto-generates a token and prints it to the logs. To use a persistent token, set the `GPTME_SERVER_TOKEN` environment variable.

Pass the token in requests using the Authorization header:

```
Authorization: Bearer <token>
```

## Core Features
- Interactive AI coding assistant
- Conversation management via REST API
- Code execution in sandboxed environment
- Flask web UI
- OpenAPI documentation
- MCP (Model Context Protocol) support

## API Endpoints

### Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Serves the web-based chat interface.
- **Request:** `curl http://localhost:5700/`
- **Tested:** Yes (200)

### OpenAPI Docs
- **URL:** `/api/docs/`
- **Method:** GET
- **Description:** Interactive OpenAPI/Swagger documentation for the REST API.
- **Request:** `curl http://localhost:5700/api/docs/`
- **Tested:** Yes (200)

### List Conversations
- **URL:** `/api/conversations`
- **Method:** GET
- **Description:** Returns a list of all conversations.
- **Request:**
  ```bash
  curl -H "Authorization: Bearer <token>" http://localhost:5700/api/conversations
  ```
- **Response:** `[]` (empty list when no conversations exist)
- **Tested:** Yes (200)

### Get Conversation
- **URL:** `/api/conversations/<name>`
- **Method:** GET
- **Description:** Retrieves a specific conversation by name.
- **Request:**
  ```bash
  curl -H "Authorization: Bearer <token>" http://localhost:5700/api/conversations/<name>
  ```

### Create/Send Message
- **URL:** `/api/conversations/<name>`
- **Method:** POST
- **Description:** Sends a message to a conversation (creates it if it does not exist).
- **Request:**
  ```bash
  curl -X POST -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"role": "user", "content": "Hello"}' \
    http://localhost:5700/api/conversations/<name>
  ```

### Generate Response
- **URL:** `/api/conversations/<name>/generate`
- **Method:** POST
- **Description:** Generates an assistant response for a conversation.
- **Request:**
  ```bash
  curl -X POST -H "Authorization: Bearer <token>" \
    http://localhost:5700/api/conversations/<name>/generate
  ```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | One key required | None | OpenAI API key |
| ANTHROPIC_API_KEY | One key required | None | Anthropic API key |
| GPTME_SERVER_TOKEN | No | Auto-generated | Persistent auth token for the API |
| GPTME_DISABLE_AUTH | No | false | Set to true to disable auth |

**At least one LLM API key must be set. The server will crash on startup without one.**

## Security Warning
This application can execute arbitrary code within the container. Do not expose to untrusted networks without proper access controls.

## Notes
- The container runs as a non-root user (appuser).
- The two-stage Docker build requires the base image to be built first.
- The healthcheck pings `http://localhost:5700/` every 30 seconds.
- The web UI and API docs endpoints do not require authentication. API endpoints do.

## V2 Dependency Changes (Minimum Version Pinning)
- Minimum version pinning NOT applied. gptme has 40+ interdependent packages (langchain, opentelemetry, dspy, litellm, openai, anthropic) whose minimum versions create cascading conflicts. Built with original caret/tilde constraints (poetry resolve).

## Changes from Original
No changes were made. Both Dockerfiles (`scripts/Dockerfile` and `scripts/Dockerfile.server`) are used exactly as provided by the original developer.
