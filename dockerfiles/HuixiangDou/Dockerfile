FROM python:3.10-slim

# System deps for document parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install requirements: use main requirements.txt but swap faiss-gpu for faiss-cpu
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir faiss-cpu && \
    sed -i 's/faiss-gpu/# faiss-gpu (replaced by faiss-cpu)/' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        "gradio==4.44.1" "gradio_client==1.3.0" \
        "huggingface_hub==0.24.7" \
        "transformers==4.44.2" \
        "sentence_transformers==3.0.1" \
        "tokenizers==0.19.1"

# Patch gradio_client: pydantic v2 emits additionalProperties:true (bool), crashes schema parsing
COPY <<'PATCH' /tmp/patch_gradio.py
p = '/usr/local/lib/python3.10/site-packages/gradio_client/utils.py'
with open(p) as f:
    c = f.read()
c = c.replace(
    'def get_type(schema: dict):',
    'def get_type(schema: dict):\n    if not isinstance(schema, dict): return "Any"'
)
c = c.replace(
    'def _json_schema_to_python_type(schema: Any, defs) -> str:',
    'def _json_schema_to_python_type(schema: Any, defs) -> str:\n    if not isinstance(schema, dict): return "Any"'
)
with open(p, 'w') as f:
    f.write(c)
print('Patched gradio_client/utils.py')
PATCH
RUN python /tmp/patch_gradio.py && rm /tmp/patch_gradio.py

# Copy the full repo
COPY . /app/

# Set PYTHONPATH so huixiangdou package is importable from /app
ENV PYTHONPATH=/app

# Create workdir so gradio_ui skips feature store build on startup
RUN mkdir -p workdir

EXPOSE 7860 23333

# Default: launch Gradio UI
CMD ["python", "-m", "huixiangdou.gradio_ui", "--config_path", "config-cpu.ini"]
