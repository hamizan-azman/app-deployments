FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install zshot and API deps
COPY setup.py setup.cfg README.md ./
COPY zshot/ zshot/
RUN pip install --no-cache-dir "transformers>=4.20,<5" && pip install --no-cache-dir -e .
RUN pip install --no-cache-dir "fastapi<0.100.0" uvicorn

# Download spaCy model
RUN pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.4.1/en_core_web_sm-3.4.1-py3-none-any.whl

# Pre-download the LinkerRegen model to zshot's cache path
RUN python -c "\
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
cache = '/root/.cache/zshot/'; \
AutoTokenizer.from_pretrained('ibm/regen-disambiguation', cache_dir=cache); \
AutoModelForSeq2SeqLM.from_pretrained('ibm/regen-disambiguation', cache_dir=cache)"

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
