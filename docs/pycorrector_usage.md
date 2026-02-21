# pycorrector -- Usage Documentation

## Overview
Chinese text correction toolkit. Detects and corrects spelling errors (phonetic similarity, visual similarity, grammar) in Chinese text using MacBERT model. Exposes a Gradio web UI and API.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/pycorrector

# Or build from source
docker build -t pycorrector apps/pycorrector/

docker run -p 7860:7860 hoomzoom/pycorrector
```

## Base URL
http://localhost:7860

## Core Features
- Chinese spelling correction (phonetic/visual similarity errors)
- Error detection with position info
- Gradio web UI with example inputs
- REST API via Gradio

## API Endpoints

### Gradio Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Interactive web interface for text correction
- **Tested:** Yes

### API Info
- **URL:** `/gradio_api/info`
- **Method:** GET
- **Description:** Returns available API endpoints and parameter schemas
- **Tested:** Yes

### Submit Correction (Step 1)
- **URL:** `/gradio_api/call/predict`
- **Method:** POST
- **Description:** Submit Chinese text for correction. Returns an event_id.
- **Request:**
```bash
curl -s http://localhost:7860/gradio_api/call/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["少先队员因该为老人让坐"]}'
```
- **Response:** `{"event_id": "06fda41caabb42b7a7d4e016ae06ba90"}`
- **Tested:** Yes

### Get Correction Result (Step 2)
- **URL:** `/gradio_api/call/predict/{event_id}`
- **Method:** GET
- **Description:** Retrieve correction result using event_id from step 1.
- **Request:**
```bash
curl -s http://localhost:7860/gradio_api/call/predict/06fda41caabb42b7a7d4e016ae06ba90
```
- **Response:**
```
event: complete
data: ["{'source': '少先队员因该为老人让坐', 'target': '少先队员应该为老人让座', 'errors': [('因', '应', 4)]}"]
```
- **Tested:** Yes

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| HF_TOKEN | No | None | HuggingFace token for faster model downloads |

## Test Summary
| Test | Result |
|------|--------|
| Gradio UI (GET /) | PASS (HTTP 200) |
| API Info (GET /gradio_api/info) | PASS (HTTP 200) |
| Correction: 今天新情很好 -> 今天心情很好 | PASS |
| Correction: 你找到你最喜欢的工作，我也很高心。 -> ...高兴。 | PASS |
| Correction: 机七学习...领遇... -> 机器学习...领域... | PASS |
| Correction: 少先队员因该为老人让坐 -> ...应该...让座 | PASS |

6/6 tests pass.

## Notes
- Model (macbert4csc-base-chinese, ~400MB) is pre-downloaded at build time. Container starts in ~2s.
- This is a Chinese spelling correction model (CSC). It handles phonetic and visual similarity errors, not grammar restructuring.
- CPU-only. No GPU required.
- Gradio API is async (two-step: submit, then poll for result).
- MacBERT model (~400MB) is pre-downloaded in the Docker Hub image. No additional downloads needed at runtime.

## Changes from Original
**Category: Modified.** One source file changed.

| File | Change | Why |
|------|--------|-----|
| `examples/macbert/gradio_demo.py` | `.launch()` changed to `.launch(server_name="0.0.0.0", server_port=7860)` | Standard Docker network binding. Without this, Gradio only listens on 127.0.0.1 inside the container |

No impact on application logic. Network binding change only.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed — all minimum versions resolved successfully.
