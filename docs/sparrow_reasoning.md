# sparrow. Reasoning Log

## Initial Assessment

Sparrow is a monorepo containing multiple components: a web UI, data pipeline, and LLM inference API. For this deployment, only the LLM component (`sparrow-ml/llm`) is containerized. This component is a FastAPI service that performs document extraction using configurable LLM backends.

## What Was Checked

1. **README.md**: Describes the full Sparrow system including UI, API, and data pipeline. The LLM component runs on port 7860 and exposes inference endpoints. Docker instructions reference the `sparrow-ml/llm` directory.

2. **sparrow-ml/llm/api.py**: FastAPI application. Accepts document uploads and extraction queries. Returns structured JSON. Supports multiple backends selected via request parameters.

3. **sparrow-ml/llm/requirements_sparrow_parse.txt**: Lists Python dependencies for the parse component only. Separate requirements files exist for other backends.

4. **System dependencies**: poppler-utils is required for PDF rendering. Without it, PDF uploads fail with a missing binary error.

## Decisions Made

### Deployed LLM component only
The architectural fidelity rule says deploy apps as the original developer intended. The LLM API component is the standalone runnable unit. The UI and data pipeline components depend on external services not relevant to our research deployment. Deploying only `sparrow-ml/llm` gives a clean, functional API surface.

### Port 7860
The upstream documentation and `api.py` default to port 7860. This is consistent with Gradio-style deployments but here it serves a FastAPI app.

### poppler-utils system dependency
Required for the PDF processing pipeline. Without it the `pdf2image` library cannot convert PDFs, and inference requests on PDF inputs fail silently or raise subprocess errors.

### Python 3.12-slim
The requirements file has no Python version constraint. 3.12-slim provides a recent runtime with good performance and a small image size.

### Healthcheck on /docs
The FastAPI /docs endpoint is served by Starlette without requiring any model initialization. It is the fastest and most reliable indicator that the service is up.

## Testing

### Tests Performed
1. **Health check** (GET `http://localhost:7860/docs`): Returns HTTP 200. Swagger UI loads. Pass.
2. **ReDoc** (GET `http://localhost:7860/redoc`): Returns HTTP 200. Pass.
3. **Inference endpoint**: NOT TESTED. Requires document input and model configuration. API key needed for cloud backends.

### What Was Not Tested
- Document extraction (requires input file and configured backend)
- OpenAI and Anthropic inference backends (require API keys)
- Local model backends (require model weights)

## Gotchas

1. **Monorepo structure**: The Dockerfile must copy from `sparrow-ml/llm` specifically, not the repo root. The `COPY --chown=user ./sparrow-ml/llm ...` pattern handles this when the build context is the repo root.

2. **Multiple requirements files**: The repo has several requirements files for different backends. `requirements_sparrow_parse.txt` covers the core parse functionality. Other requirements files cover additional backends and are not installed in this image.

3. **Port 7860**: This port is more commonly associated with Gradio but here serves a FastAPI app. The healthcheck correctly probes `/docs` rather than `/gradio_api/info`.
