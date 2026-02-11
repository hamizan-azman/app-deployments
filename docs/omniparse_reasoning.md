# OmniParse. Reasoning Log

## Files Reviewed

### README.md
First file to read for any deployment. Confirmed:
- OmniParse is a data ingestion/parsing platform for converting unstructured data to structured markdown
- Completely local. no external API keys needed (major advantage for easy deployment)
- Has official Docker image on Docker Hub: `savatar101/omniparse:0.1`
- Supports documents (PDF, PPT, DOCX), images, audio, video, and web pages
- Server runs on port 8000 via FastAPI + Gradio UI

### Dockerfile
Checked to understand what the pre-built image contains:
- Base: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04` (CUDA-capable but works on CPU too)
- Installs: Python 3, PyTorch (CUDA 11.8), LibreOffice (for PPT/DOCX conversion), ffmpeg (for media), Google Chrome + ChromeDriver (for web crawling), Xvfb (virtual display for headless Chrome)
- Entry point: `python server.py --host 0.0.0.0 --port 8000 --documents --media --web`
- All three model groups (documents, media, web) are loaded by default
- The image is large (~9.35 GB) because it includes CUDA, Chrome, LibreOffice, and PyTorch

### server.py
Main entry point. FastAPI app with four routers:
- `document_router` at `/parse_document`. PDF, PPT, DOCX parsing
- `image_router` at `/parse_image`. image parsing and processing
- `media_router` at `/parse_media`. audio and video transcription
- `website_router` at `/parse_website`. web page crawling
- Gradio demo UI mounted at root `/`

Note: the README has a minor error. it lists image parsing under `/parse_media/image` but the actual code mounts it at `/parse_image/image`. The usage doc reflects the actual code.

### Router files (documents/router.py, media/router.py, image/router.py, web/router.py)
Read all four to map the exact endpoints, parameters, and behavior:

**Document router:**
- `POST /parse_document`. auto-detects file type, routes accordingly
- `POST /parse_document/pdf`. direct PDF parsing via Marker (convert_single_pdf)
- `POST /parse_document/ppt`. converts PPT to PDF via LibreOffice, then parses
- `POST /parse_document/docs`. converts DOCX to PDF via LibreOffice, then parses
- All accept `file` as UploadFile form field

**Image router:**
- `POST /parse_image/image`. parses image, accepts `file` field
- `POST /parse_image/process_image`. advanced processing, accepts `image` field + `task` form field
- Tasks: OCR, OCR with Region, Caption, Detailed Caption, More Detailed Caption, Object Detection, Dense Region Caption, Region Proposal

**Media router:**
- `POST /parse_media/audio`. Whisper transcription for MP3, WAV, FLAC
- `POST /parse_media/video`. Whisper transcription for MP4, AVI, MOV, MKV

**Website router:**
- `POST /parse_website/parse`. accepts `url` as query parameter
- `POST /parse_website/crawl`. stub, returns "Coming soon"
- `POST /parse_website/search`. stub, returns "Coming soon"

## Approach

### Use the pre-built Docker Hub image
The repo provides an official image at `savatar101/omniparse:0.1`. No reason to build from source when the author published an image. This is the most faithful deployment. it is exactly what the developer shipped.

### CPU mode (no --gpus flag)
This Windows machine with Docker Desktop on WSL2 does not have NVIDIA Container Toolkit configured. The app works on CPU. it will be slower for inference but functionally identical. The CUDA base image does not require a GPU to run.

### No modifications to the app
Zero changes needed. The image includes everything: models download on first use, Chrome for web crawling, LibreOffice for document conversion. This is exactly what the architectural fidelity rule requires.

## Tests

### Test 1: Health check / Gradio UI
Verify the container starts and the web server is accepting connections. Hit the root URL which serves the Gradio demo. This proves FastAPI + Gradio are running.

### Test 2: Parse PDF document
Core use case. Upload a real PDF and verify we get markdown text back. Tests the document parsing pipeline: file upload -> Marker OCR -> markdown output.

### Test 3: Parse image
Upload an image and verify text extraction / captioning works. Tests the image processing pipeline: file upload -> Florence-2 model -> text output.

### Test 4: Parse website
POST a URL and verify the web crawler returns page content as markdown. Tests the Selenium/Chrome pipeline.

Note: Audio/video tests would require sample media files. We test the infrastructure endpoints. If they accept the request and return proper responses (even errors for missing models), that proves the routing and server stack work.

## Gotchas

### Image size
At 9.35 GB, the pull takes significant time. Plan for this on slow connections.

### Model loading on first request
Models may not be pre-loaded in the image. The first request to each endpoint type may be slow (downloading/loading models into memory). Subsequent requests will be fast.

### README endpoint mismatch
The README documents image parsing at `/parse_media/image` but the code actually routes it to `/parse_image/image`. Always verify endpoints against source code, not just documentation.

### CPU performance
On CPU, document parsing may take 30+ seconds per page. Image captioning may take 10+ seconds. This is expected behavior. the models are designed for GPU but fall back to CPU.

### Web parsing requires Chrome
The web parsing endpoint uses Selenium with headless Chrome. The Docker image includes Chrome and ChromeDriver, so this works out of the box in the container. The `DISPLAY=:99` env var and Xvfb handle the headless display.
