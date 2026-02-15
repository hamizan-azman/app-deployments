# gpt-engineer

Pull pre-built image:
```bash
docker pull hoomzoom/gpt-engineer
docker run -it -e OPENAI_API_KEY=your-key hoomzoom/gpt-engineer
```

## Dockerfile
Uses the original repo's `docker/Dockerfile` with one added line to fix Windows line endings:
```dockerfile
RUN sed -i 's/\r$//' /app/entrypoint.sh
```

To rebuild from source:
```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer
cd gpt-engineer
# Add the sed line to docker/Dockerfile after the COPY of entrypoint.sh
docker build -f docker/Dockerfile -t gpt-engineer .
```

See `docs/gpt-engineer_reasoning.md` for full details on what was changed and why.
