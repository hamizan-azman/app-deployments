# magentic-ui -- Usage Documentation

## Overview
Microsoft's agentic web browsing UI built on AutoGen. Agents can browse the web, run code, and interact with pages via a VNC browser container.

## Quick Start
```bash
docker pull hoomzoom/magentic-ui:latest
docker run -d -p 8081:8081 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=your-key \
  hoomzoom/magentic-ui:latest
```

## Base URL
http://localhost:8081

## Requirements
- Docker socket access (mounts `/var/run/docker.sock`) -- the app spawns helper containers (VNC browser, Python executor)
- OpenAI API key for LLM-powered browsing agents
- On first run, pulls two internal images (~2-3 min)

## API Endpoints

### Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Main chat interface for creating browsing sessions
- **Tested:** Yes (200)

### Sessions API
- **URL:** `/api/sessions?user_id=test`
- **Method:** GET
- **Description:** List user sessions
- **Response:** `{"status":true,"data":[]}`
- **Tested:** Yes (200)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | OpenAI API key for agents |

## Docker Hub
```bash
docker pull hoomzoom/magentic-ui:latest
```

## Notes
- This is a Docker-in-Docker deployment. The container spawns other containers for web browsing (VNC) and code execution (Python).
- Must mount Docker socket: `-v /var/run/docker.sock:/var/run/docker.sock`
- First startup takes 2-3 minutes as it pulls internal helper images.
- Chat functionality requires a valid OpenAI API key.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning NOT applied. Uses official pre-built image — cannot control dependency versions.
