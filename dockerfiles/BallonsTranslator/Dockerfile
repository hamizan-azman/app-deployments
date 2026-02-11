FROM python:3.11-slim

# System dependencies:
# - libgl1, libglib2.0-0: OpenCV runtime requirements
# - libxcb1, libx11-6: Qt minimal X11 libraries (needed even in offscreen mode)
# - mecab, libmecab-dev, mecab-ipadic-utf8: Japanese morphological analyzer (mecab-python3 dep)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Critical: run Qt in offscreen mode so PyQt6 does not try to connect to a display
ENV QT_QPA_PLATFORM=offscreen
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy application source
COPY . /app

# Install PyTorch CPU-only first to avoid the default CUDA build being pulled in
# by later packages (e.g. transformers, ultralytics) that list torch as a dependency.
# Installing it explicitly beforehand pins the resolver to the CPU wheel index.
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the requirements.
# Exclude platform-specific packages that only apply to Windows or macOS.
# pillow-jxl-plugin is excluded: it requires Pillow build flags not available in slim.
RUN pip install --no-cache-dir \
    "PyQt6-Qt6>=6.6.2" \
    "PyQt6>=6.6.1" \
    "numpy<2" \
    urllib3 \
    jaconv \
    "transformers==4.57.1" \
    fugashi \
    unidic_lite \
    tqdm \
    "opencv-python>=4.8.1.78" \
    shapely \
    pyclipper \
    einops \
    termcolor \
    bs4 \
    "deepl>=1.16.0" \
    qtpy \
    spacy-pkuseg \
    sentencepiece \
    ctranslate2 \
    python-docx \
    docx2txt \
    piexif \
    keyboard \
    ordered-set \
    opencc-python-reimplemented \
    requests \
    "ultralytics>=8.4.14" \
    beautifulsoup4 \
    colorama \
    "openai>=2.8.1" \
    pyyaml \
    natsort \
    py7zr \
    multivolumefile \
    "httpx[socks,brotli]" \
    langdetect \
    "translators==5.9.5" \
    json5 \
    betterproto

# Create a non-root user for runtime.
# Some Qt plugin paths may need read access to /app; ownership is set accordingly.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Declare volume mount points for batch translation input/output.
# The caller maps host directories here: docker run -v /host/in:/input -v /host/out:/output
VOLUME ["/input", "/output"]

USER appuser

# Verify that the two heaviest runtime imports succeed.
# If torch or cv2 fail to import the container is considered unhealthy.
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD python -c "import torch; import cv2"

# --headless: skip the PyQt6 GUI event loop entirely and run batch translation.
# Pass --exec_dirs and a config via CMD or docker run arguments, e.g.:
#   docker run ... hoomzoom/ballonstranslator --exec_dirs /input --config_path /app/config.json
ENTRYPOINT ["python", "launch.py", "--headless"]
