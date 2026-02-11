# Stage 1: langchain-serve backend (serves api.py via lc-serve)
FROM python:3.10-slim AS langchain-serve-img

WORKDIR /app

# Upgrade pip and pin setuptools<71 for build isolation (old packages use pkg_resources)
RUN pip install --no-cache-dir --upgrade pip && \
    echo 'setuptools<71' > /tmp/build-constraints.txt
ENV PIP_BUILD_CONSTRAINT=/tmp/build-constraints.txt

# Pre-install yanked opentelemetry dep that jina 3.14.1 requires
RUN pip install --no-cache-dir opentelemetry-exporter-prometheus==1.12.0rc1

# Install backend dependencies: langchain-serve + everything api.py imports
# Era-matched pins: all deps from mid-2023 when langchain-serve was active
# - langchain==0.0.267: pre community-split
# - pydantic<2: jina 3.x needs pydantic v1
# - litellm==0.1.424: last version compatible with openai 0.27.x
# - openai==0.27.4: original repo pin
RUN pip install --no-cache-dir \
    "pydantic<2" \
    "langchain==0.0.267" \
    langchain-serve \
    "litellm==0.1.424" \
    tensorflow-cpu \
    tensorflow_hub==0.13.0 \
    PyMuPDF==1.22.1 \
    numpy==1.23.5 \
    scikit-learn==1.2.2 \
    openai==0.27.8

# Pre-download Universal Sentence Encoder (~1GB) so it's baked into the image
RUN python -c "import tensorflow_hub as hub; hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')"

COPY api.py .

EXPOSE 8080

CMD ["lc-serve", "deploy", "local", "api"]

# Stage 2: Gradio frontend (app.py calls langchain-serve backend via HTTP)
FROM python:3.10-slim AS pdf-gpt-img

WORKDIR /app

# Frontend only needs gradio + requests (app.py does not import backend deps)
# Pin huggingface_hub<1.0 (gradio 4.11.0 uses deprecated HfFolder)
RUN pip install --no-cache-dir gradio==4.11.0 "huggingface_hub<1.0" requests

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
