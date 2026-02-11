FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1-dev libportaudio2 portaudio19-dev \
    git curl build-essential cmake \
    libegl1 libgl1 libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch CPU first
RUN pip install --no-cache-dir \
    torch==2.7.1+cpu torchaudio==2.7.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install PySide6
RUN pip install --no-cache-dir PySide6==6.9.2

# Install faster-whisper from GitHub
RUN pip install --no-cache-dir \
    "faster-whisper @ https://github.com/SYSTRAN/faster-whisper/archive/refs/heads/master.tar.gz"

# Copy requirements and install with --no-deps to avoid conflict resolution
# (all versions are exact pins from the developer's pyproject.toml)
COPY requirements-docker.txt /tmp/requirements-docker.txt
RUN pip install --no-cache-dir --no-deps -r /tmp/requirements-docker.txt && \
    pip install --no-cache-dir azure-core azure-identity

# Copy source
COPY . .

RUN mkdir -p output tmp models logs

ENTRYPOINT ["python", "cli.py"]
