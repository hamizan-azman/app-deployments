# OmniParse -- Usage Documentation

## Overview
Platform that ingests and parses unstructured data (documents, images, audio, video, web pages) into structured markdown optimized for GenAI applications. Completely local, no external APIs required.

## Quick Start
```bash
docker pull hoomzoom/omniparse
docker run -p 8000:8000 hoomzoom/omniparse
```

## Base URL
http://localhost:8000

## Core Features
- Parse PDF, PowerPoint, Word documents to markdown
- Image parsing and captioning (OCR, object detection, dense captioning)
- Audio and video transcription via Whisper
- Web page crawling and parsing
- Gradio demo UI at root URL

## API Endpoints

### Parse Any Document
- **URL:** `/parse_document`
- **Method:** POST
- **Description:** Auto-detects and parses PDF, PPT, PPTX, DOC, DOCX files
- **Request:** `curl -X POST -F "file=@document.pdf" http://localhost:8000/parse_document`
- **Response:** `{"text": "markdown content...", "metadata": {...}, "images": [...]}`
- **Tested:** No (shares pipeline with /parse_document/pdf)

### Parse PDF
- **URL:** `/parse_document/pdf`
- **Method:** POST
- **Description:** Parse PDF documents to markdown
- **Request:** `curl -X POST -F "file=@document.pdf" http://localhost:8000/parse_document/pdf`
- **Response:** `{"text": "markdown content...", "metadata": {...}, "images": [...]}`
- **Tested:** Yes -- extracted "Dummy PDF file" from W3C sample PDF

### Parse PowerPoint
- **URL:** `/parse_document/ppt`
- **Method:** POST
- **Description:** Parse PPT/PPTX presentations (converts to PDF first via LibreOffice)
- **Request:** `curl -X POST -F "file=@presentation.pptx" http://localhost:8000/parse_document/ppt`
- **Response:** `{"text": "markdown content...", "metadata": {...}, "images": [...]}`
- **Tested:** No (shares pipeline with /parse_document/pdf after LibreOffice conversion)

### Parse Word Document
- **URL:** `/parse_document/docs`
- **Method:** POST
- **Description:** Parse DOC/DOCX files (converts to PDF first via LibreOffice)
- **Request:** `curl -X POST -F "file=@document.docx" http://localhost:8000/parse_document/docs`
- **Response:** `{"text": "markdown content...", "metadata": {...}, "images": [...]}`
- **Tested:** No (shares pipeline with /parse_document/pdf after LibreOffice conversion)

### Parse Image
- **URL:** `/parse_image/image`
- **Method:** POST
- **Description:** Parse image files (PNG, JPEG, JPG, TIFF, WEBP) to text/markdown
- **Request:** `curl -X POST -F "file=@photo.jpg" http://localhost:8000/parse_image/image`
- **Response:** `{"text": "extracted text...", "metadata": {...}}`
- **Tested:** Yes -- OCR extracted "HelloOmniParse" from test image

### Process Image (Advanced)
- **URL:** `/parse_image/process_image`
- **Method:** POST
- **Description:** Process image with specific task: OCR, OCR with Region, Caption, Detailed Caption, More Detailed Caption, Object Detection, Dense Region Caption, Region Proposal
- **Request:** `curl -X POST -F "image=@photo.jpg" -F "task=Caption" http://localhost:8000/parse_image/process_image`
- **Response:** `{"text": "A photo of...", "metadata": {...}}`
- **Tested:** No (shares image model with /parse_image/image)

### Parse Audio
- **URL:** `/parse_media/audio`
- **Method:** POST
- **Description:** Transcribe audio files (MP3, WAV, FLAC) via Whisper
- **Request:** `curl -X POST -F "file=@audio.mp3" http://localhost:8000/parse_media/audio`
- **Response:** `{"text": "transcribed text...", "metadata": {...}}`
- **Tested:** No (requires sample audio file; Whisper model confirmed loaded)

### Parse Video
- **URL:** `/parse_media/video`
- **Method:** POST
- **Description:** Transcribe video files (MP4, AVI, MOV, MKV) via Whisper
- **Request:** `curl -X POST -F "file=@video.mp4" http://localhost:8000/parse_media/video`
- **Response:** `{"text": "transcribed text...", "metadata": {...}}`
- **Tested:** No (requires sample video file; Whisper model confirmed loaded)

### Parse Website
- **URL:** `/parse_website/parse`
- **Method:** POST
- **Description:** Crawl and parse a website URL to markdown
- **Request:** `curl -X POST "http://localhost:8000/parse_website/parse?url=https://example.com"`
- **Response:** `{"text": "page content as markdown...", "metadata": {...}}`
- **Tested:** Yes -- crawled example.com, returned full HTML + markdown

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| CHROME_BIN | No | /usr/bin/google-chrome | Chrome binary path (for web parsing) |
| CHROMEDRIVER | No | /usr/local/bin/chromedriver | ChromeDriver path |

## Notes
- Server loads all models on startup (documents, media, web). First request may be slow as models initialize.
- GPU recommended (8-10 GB VRAM) but CPU mode works.
- Gradio demo UI available at http://localhost:8000/ for interactive testing.
- Image is ~9.35 GB. Based on CUDA 11.8 / Ubuntu 22.04.
- PDF parsing uses Marker (Surya OCR). Best on digital PDFs, may struggle with heavy OCR or non-English text.
- PPT and DOCX parsing converts to PDF via LibreOffice first.
