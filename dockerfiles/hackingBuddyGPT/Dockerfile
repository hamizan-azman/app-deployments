FROM python:3.11-slim

# System dependencies
# tmux: required for some interactive use cases
# openssh-client: required for SSH-based pentest use cases (conn.* params)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy source and install package with pinned deps from pyproject.toml
COPY --chown=appuser:appuser . .

RUN pip install --no-cache-dir -e .

# .env file is mounted at runtime by the user (see .env.example)
# Required env vars (passed via --env-file or -e at runtime):
#   llm.api_key        - OpenAI API key
#   llm.model          - model name (e.g. gpt-3.5-turbo)
#   llm.context_size   - context window size
#   conn.host          - target SSH host IP
#   conn.hostname      - target hostname (for root detection)
#   conn.port          - SSH port
#   conn.username      - SSH username
#   conn.password      - SSH password (or '' for key auth)
#   conn.keyfilename   - SSH key path (or '' for password auth)
#   log_db.connection_string - SQLite path (e.g. log_db.sqlite3)
#   max_turns          - number of agent iterations

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import hackingBuddyGPT" || exit 1

ENTRYPOINT ["wintermute"]
