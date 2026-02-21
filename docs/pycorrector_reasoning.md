# pycorrector. Reasoning Log

## Starting point

### Repository structure
First read: `README.md`, `Dockerfile`, `requirements.txt`, `requirements-dev.txt`, `setup.py`, and the `pycorrector/` package directory. The README is in Chinese but comprehensive. It documents multiple correction models (kenlm, MacBERT, T5, ERNIE, GPT-based) with code examples for each.

### Existing Dockerfile
The repo ships a Dockerfile but it is outdated and not useful for deployment:
```dockerfile
FROM nikolaik/python-nodejs:python3.8-nodejs20
WORKDIR /app
COPY . .
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pycorrector -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /app/examples
CMD /bin/bash
```

Problems:
1. Uses Python 3.8 (the project supports 3.8+ but there is no reason to use an old version)
2. Uses `nikolaik/python-nodejs`. unnecessary Node.js included
3. Uses Chinese pip mirror (tsinghua.edu.cn). slow from outside China
4. Installs pycorrector from PyPI *after* already copying the source. redundant
5. CMD is `/bin/bash`. just opens a shell, does not serve anything
6. No EXPOSE, no port binding, no web service

### Identifying the web interface
Searched `examples/` and found `examples/macbert/gradio_demo.py`. This is a clean Gradio app that loads the MacBERT model and exposes a text correction interface. The MacBERT model (macbert4csc-base-chinese) is the recommended model per the README's evaluation table. it has 224 QPS and good accuracy on SIGHAN-2015.

### Choosing MacBERT over other models
The repo supports many models. I chose MacBERT because:
- It is the one the Gradio demo uses
- The README marks it as "recommended" (推荐)
- It auto-downloads from HuggingFace (~400MB), no manual setup
- It runs on CPU without issues
- The kenlm model requires downloading a 2.8GB language model file, which is slower and more fragile
- T5, GPT, ERNIE models are heavier and need more dependencies

## Dockerfile choices

### Base image: python:3.10-slim
- Slim variant keeps the image smaller (no unnecessary system packages)
- Python 3.10 is well-supported by all dependencies
- No need for Node.js (the original Dockerfile used a python-nodejs image for no reason)

### Build-essential for kenlm
Even though we primarily use MacBERT, the `requirements.txt` includes `kenlm` which needs C compilation. Adding `build-essential` is required for the pip install to succeed. The alternative would be to strip kenlm from requirements, but that would mean modifying the upstream requirements file, which is fragile.

### CPU-only PyTorch
Installed PyTorch from the CPU index (`https://download.pytorch.org/whl/cpu`) before the other requirements. This avoids pulling in CUDA libraries (~2GB) since this is a BERT model that runs fine on CPU. The model inference is fast enough on CPU (224 QPS per the README's benchmarks).

### Pre-downloading the model at build time
Added this line in the Dockerfile:
```dockerfile
RUN python -c "from pycorrector import MacBertCorrector. MacBertCorrector('shibing624/macbert4csc-base-chinese')"
```
This downloads and caches the ~400MB model during `docker build`. Without this, the model downloads on first request, causing a ~6-7 minute delay on container startup. With it, the container starts and serves requests in ~2 seconds.

### Modifying gradio_demo.py
Changed the `launch()` call from:
```python
).launch()
```
to:
```python
).launch(server_name="0.0.0.0", server_port=7860)
```
Gradio defaults to `127.0.0.1` which is only accessible inside the container. Binding to `0.0.0.0` makes it accessible from the host. Port 7860 is Gradio's default and widely recognized.

### Not adding a separate FastAPI/Flask wrapper
The Gradio app already provides both a web UI and a REST API (`/gradio_api/call/predict`). Adding another layer would be unnecessary complexity. The Gradio API is two-step (submit -> poll), which is a minor inconvenience for curl users but works fine for programmatic access.

## Testing strategy

### Test 1: HTTP 200 on `/`
Validates that the Gradio web UI is serving. This confirms the container started, the model loaded, and Gradio bound to the port correctly. If any dependency was missing or the model failed to load, this would fail.

### Test 2: HTTP 200 on `/gradio_api/info`
Validates that the Gradio API is discoverable. Returns the schema of available endpoints.

### Tests 3-6: Chinese text correction
Each test sentence has known errors from the README examples:
- `今天新情很好`. "新" should be "心" (phonetic similarity: xin)
- `你找到你最喜欢的工作，我也很高心`. "心" should be "兴" (phonetic: xin vs xing)
- `机七学习是人工智能领遇最能体现智能的一个分知`. "七" should be "器", "遇" should be "域" (visual/phonetic similarity)
- `少先队员因该为老人让坐`. "因" should be "应" (phonetic: yin vs ying)

These test the core model inference pipeline: tokenization, BERT forward pass, error detection, correction lookup. All returned correct results.

## Debugging notes

### Chinese characters display as `?` in curl output
When testing from Git Bash on Windows, curl output shows Chinese characters as `?` because the terminal uses cp1252 encoding. The data is actually correct UTF-8. To verify, pipe through Python with `sys.stdout.reconfigure(encoding='utf-8')`.

### Gradio API is two-step (async)
Unlike a simple REST API, Gradio's API requires:
1. POST to `/gradio_api/call/predict` with the input. returns an `event_id`
2. GET `/gradio_api/call/predict/{event_id}`. returns the result as SSE

This is because Gradio uses Server-Sent Events internally. The older `/api/predict` endpoint does not exist in newer Gradio versions.

### UNEXPECTED key warning during model load
The log shows `bert.embeddings.position_ids | UNEXPECTED` during model loading. This is harmless. it means the saved model has a `position_ids` tensor that the current model architecture does not expect. This is normal when loading older HuggingFace checkpoints and does not affect results.

### Build time
The Docker build takes roughly 7-10 minutes:
- PyTorch CPU install: ~2 min
- requirements.txt install: ~2 min
- pycorrector install: ~30s
- gradio install: ~1 min
- Model download + warmup: ~2 min

Subsequent builds with cache hit the first layers and only re-run from COPY onward.
