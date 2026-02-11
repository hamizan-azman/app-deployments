# SWE-agent

Pull pre-built image:
```bash
docker pull hoomzoom/swe-agent
docker pull sweagent/swe-agent:latest
```

## No custom Dockerfile
This app uses the official pre-built image (`sweagent/swe-agent-run:latest`) retagged to `hoomzoom/swe-agent`. No source code modifications were made.

The `sweagent/swe-agent:latest` image is also required -- it's the environment image spawned by the runner via Docker socket.

See `docs/SWE-agent_usage.md` for run commands and `docs/SWE-agent_reasoning.md` for details.
