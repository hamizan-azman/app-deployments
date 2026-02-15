# Zshot -- Usage Documentation

## Overview
Zero-shot named entity recognition using IBM's Zshot library. Uses spaCy pipeline with LinkerRegen (T5-based disambiguation) and MentionsExtractorSpacy to identify and link entities without task-specific training.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/zshot

# Or build from source
docker build -t zshot apps/zshot/

docker run -d --name zshot -p 8000:8000 hoomzoom/zshot
```

## Base URL
http://localhost:8000

## Core Features
- Zero-shot named entity recognition via REST API
- Entity extraction with label linking
- HTML visualization of extracted entities (displacy)
- Pre-loaded with 6 default entities (Paris, IBM, New York, Florida, American, Armonk)

## API Endpoints

### Health Check
- **URL:** `/health`
- **Method:** GET
- **Description:** Returns service status.
- **Request:** `curl http://localhost:8000/health`
- **Response:** `{"status":"ok"}`
- **Tested:** Yes

### API Docs (Swagger)
- **URL:** `/docs`
- **Method:** GET
- **Description:** Interactive Swagger UI for all endpoints.
- **Request:** `curl http://localhost:8000/docs`
- **Response:** HTML page
- **Tested:** Yes

### Extract Entities
- **URL:** `/extract`
- **Method:** POST
- **Description:** Extract named entities from input text using zero-shot NER.
- **Request:**
```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "International Business Machines Corporation (IBM) is an American multinational technology corporation headquartered in Armonk, New York."}'
```
- **Response:**
```json
{
  "text": "International Business Machines Corporation (IBM) is an American multinational technology corporation headquartered in Armonk, New York.",
  "entities": [
    {"text": "International Business Machines Corporation", "label": "IBM", "start": 0, "end": 43},
    {"text": "IBM", "label": "IBM", "start": 45, "end": 48},
    {"text": "American", "label": "American", "start": 56, "end": 64},
    {"text": "Armonk", "label": "Armonk", "start": 119, "end": 125},
    {"text": "New York", "label": "New York", "start": 127, "end": 135}
  ]
}
```
- **Tested:** Yes

### Visualize Entities
- **URL:** `/visualize`
- **Method:** POST
- **Description:** Returns displacy HTML visualization of extracted entities.
- **Request:**
```bash
curl -X POST http://localhost:8000/visualize \
  -H "Content-Type: application/json" \
  -d '{"text": "IBM is headquartered in Armonk, New York."}'
```
- **Response:** HTML with color-coded entity spans
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| None | -- | -- | No environment variables needed |

## Notes
- First request after startup may be slow (~30s) as the T5 model runs inference. Subsequent requests are faster.
- The container image is large (~5GB) due to PyTorch + T5 model weights.
- Build takes ~10 minutes (model download is the bottleneck).
- Default entities are hardcoded in app.py. To change them, edit the DEFAULT_ENTITIES list.
- Only CPU inference is supported (no GPU).
- **First startup downloads models (~1-2 GB).** The T5 model and spaCy pipelines are downloaded on first run. This takes 5-10 minutes depending on connection speed. The container may appear to hang -- check progress with `docker logs -f <container>`. Subsequent launches are fast.

## Changes from Original
**Category: Modified.** Import guards added, custom API wrapper added.

| File | Change | Why |
|------|--------|-----|
| `zshot/knowledge_extractor/__init__.py` | Wrapped `relik` import in try/except ImportError | Prevents crash when optional `relik` package is not installed |
| `zshot/linker/__init__.py` | Wrapped `blink`, `tars`, `relik`, `gliner` imports in try/except ImportError | Same -- optional backends |
| `zshot/mentions_extractor/__init__.py` | Wrapped `gliner` import in try/except ImportError | Same |
| `app.py` (NEW FILE) | FastAPI wrapper with `/health`, `/extract`, `/visualize` endpoints | Zshot is a library with no web interface. This custom wrapper was added to expose it as a service |

Dependency change: `transformers` pinned to `<5` (original unpinned). Transformers v5 removed `batch_encode_plus` from T5Tokenizer.

**WARNING:** The `app.py` FastAPI wrapper is entirely custom code not written by the original developer. It introduces HTTP endpoints that do not exist in the original library. Any vulnerability found in `app.py` is NOT a valid supply chain finding.
