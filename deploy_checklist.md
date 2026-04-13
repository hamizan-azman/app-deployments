# Per-App Deployment Checklist

Copy this for each new app. Check off each step as you go.

## App: ___________

### 1. Setup
- [ ] `git submodule add <github_url> apps/<name>`
- [ ] Read app README, existing Dockerfile, docker-compose, source code
- [ ] Identify type: Streamlit / Gradio / FastAPI / Flask / CLI / Library / Compose
- [ ] Identify Python version requirement
- [ ] Identify system dependencies (libgl1, libcairo2-dev, etc.)
- [ ] Identify API key requirements
- [ ] Identify GPU/hardware requirements
- [ ] Decision: Deploy / Skip (if skip, document reason and write usage doc only)

### 2. Dockerfile
- [ ] Create `dockerfiles/<name>/` directory
- [ ] If app has Dockerfile: copy and apply minimal fixes only (architectural fidelity)
- [ ] If no Dockerfile: create from scratch using patterns in CLAUDE.md
- [ ] Pin all dependencies to `==` exact versions
- [ ] Copy pinned requirements.txt or pyproject.toml to `dockerfiles/<name>/`
- [ ] Add HEALTHCHECK
- [ ] Add non-root user (UID 1000)
- [ ] Set EXPOSE for documented port(s)
- [ ] Add `RUN sed -i 's/\r$//' ...` for any shell scripts (Windows line ending fix)

### 3. Build and Push
- [ ] `docker build --platform linux/amd64 -t hoomzoom/<name> apps/<name>/ -f dockerfiles/<name>/Dockerfile`
- [ ] Verify build succeeds
- [ ] `docker push hoomzoom/<name>:latest`
- [ ] For compose apps: build and push each image separately

### 4. QC Test
- [ ] Start container: `docker run -d -p <port>:<port> hoomzoom/<name>`
- [ ] Wait for startup (check logs: `docker logs -f <container>`)
- [ ] Test health endpoint (see CLAUDE.md for endpoint by app type)
- [ ] Test at least one functional endpoint
- [ ] Record test results

### 5. Documentation
- [ ] Write `docs/<name>_usage.md` (Docker commands, endpoints, env vars, test results)
- [ ] Write `docs/<name>_reasoning.md` (decisions, build issues, workarounds)
- [ ] Add V2 dependency changes section if any bumps were needed

### 6. Track
- [ ] Update `task2_status.md` with status and remark
- [ ] Clean up: `docker stop` and `docker rm` test container
