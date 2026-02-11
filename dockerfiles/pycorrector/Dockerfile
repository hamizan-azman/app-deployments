FROM python:3.10-slim

WORKDIR /app

# System deps for kenlm and pyahocorasick build
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only first (smaller image)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install pycorrector and gradio
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir gradio

# Pre-download the MacBERT model at build time so startup is fast
RUN python -c "from pycorrector import MacBertCorrector; MacBertCorrector('shibing624/macbert4csc-base-chinese')"

EXPOSE 7860

CMD ["python", "examples/macbert/gradio_demo.py"]
