FROM python:3.10-slim

WORKDIR /app

# System deps: ffmpeg, imagemagick, audio libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    libsndfile1 \
    git \
    && (find /etc -name policy.xml -exec sed -i 's/none/read,write/g' {} \; || true) \
    && rm -rf /var/lib/apt/lists/*

# Install torch CPU first to avoid pulling CUDA (~2GB savings)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install remaining deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 7860

CMD ["python", "funclip/launch.py", "--listen", "-l", "en"]
