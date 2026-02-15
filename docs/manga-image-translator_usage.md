# manga-image-translator -- Usage Documentation

## Overview
One-click translation of text in manga/comic images. Detects text regions, performs OCR, translates (Japanese to English by default), inpaints the original text, and renders translated text. Supports 20+ languages.

## Quick Start
```bash
docker pull hoomzoom/manga-image-translator
docker run -p 5003:5003 --ipc=host --entrypoint python hoomzoom/manga-image-translator server/main.py --verbose --start-instance --host=0.0.0.0 --port=5003
```

First run downloads translator models (~622MB sugoi-models.zip). Wait for logs to show model loading complete before sending translation requests.

No API key needed for the default "sugoi" translator (Japanese to English). For GPT-based translation to other languages, add your OpenAI key:
```bash
docker run -p 5003:5003 --ipc=host -e OPENAI_API_KEY=sk-your-key \
  --entrypoint python hoomzoom/manga-image-translator \
  server/main.py --verbose --start-instance --host=0.0.0.0 --port=5003
```

## Base URL
http://localhost:5003

## Core Features
- Translate manga/comic images from Japanese (and other languages) to English
- Text detection, OCR, translation, inpainting, and text rendering pipeline
- Web UI for interactive use
- REST API with JSON, image, and byte response formats
- Streaming endpoints for progress tracking
- Batch translation support
- Result storage and retrieval

## API Endpoints

### Translate (JSON body, JSON response)
- **URL:** `/translate/json`
- **Method:** POST
- **Description:** Translate an image. Accepts image as URL, base64, or raw bytes in JSON body. Returns structured JSON with all detected text regions, translations, and background patches.
- **Request:** `curl -X POST http://localhost:5003/translate/json -H "Content-Type: application/json" -d '{"image": "https://example.com/manga.png", "config": {}}'`
- **Response:** `{"translations": [{"minX": 0, "minY": 0, "maxX": 100, "maxY": 100, "text": {"ENG": "Hello", "ja": "..."}, "background": "data:image/png;base64,..."}]}`
- **Tested:** Yes -- translated manga page with 14 Japanese text regions to English, 200 OK, 386KB response

### Translate (JSON body, image response)
- **URL:** `/translate/image`
- **Method:** POST
- **Description:** Same input as /translate/json but returns the translated image as PNG.
- **Request:** `curl -X POST http://localhost:5003/translate/image -H "Content-Type: application/json" -d '{"image": "https://example.com/manga.png", "config": {}}' -o translated.png`
- **Response:** PNG image binary
- **Tested:** No (shares pipeline with /translate/json)

### Translate (JSON body, bytes response)
- **URL:** `/translate/bytes`
- **Method:** POST
- **Description:** Returns custom byte structure. See examples/response.* in repo for decoding.
- **Request:** `curl -X POST http://localhost:5003/translate/bytes -H "Content-Type: application/json" -d '{"image": "https://example.com/manga.png", "config": {}}'`
- **Tested:** No (shares pipeline with /translate/json)

### Translate with Form (multipart upload, JSON response)
- **URL:** `/translate/with-form/json`
- **Method:** POST
- **Description:** Upload image as multipart form data. Returns JSON.
- **Request:** `curl -X POST http://localhost:5003/translate/with-form/json -F "image=@manga.png" -F "config={}"`
- **Response:** Same as /translate/json
- **Tested:** No (shares pipeline with /translate/json)

### Translate with Form (multipart upload, image response)
- **URL:** `/translate/with-form/image`
- **Method:** POST
- **Description:** Upload image as multipart form data. Returns translated PNG.
- **Request:** `curl -X POST http://localhost:5003/translate/with-form/image -F "image=@manga.png" -F "config={}" -o translated.png`
- **Tested:** No (shares pipeline with /translate/json)

### Translate with Form (multipart upload, bytes response)
- **URL:** `/translate/with-form/bytes`
- **Method:** POST
- **Description:** Upload image as multipart form data. Returns custom byte structure.
- **Request:** `curl -X POST http://localhost:5003/translate/with-form/bytes -F "image=@manga.png" -F "config={}"`
- **Tested:** No (shares pipeline with /translate/json)

### Streaming Variants (JSON body)
- **URLs:** `/translate/json/stream`, `/translate/bytes/stream`, `/translate/image/stream`
- **Method:** POST
- **Description:** Streaming versions of the JSON-body endpoints. Returns octet-stream with progress updates. Protocol: 1 byte status code (0=result, 1=progress, 2=error, 3=queue position, 4=waiting for instance), 4 bytes size, N bytes data.
- **Tested:** No

### Streaming Variants (Form upload)
- **URLs:** `/translate/with-form/json/stream`, `/translate/with-form/bytes/stream`, `/translate/with-form/image/stream`, `/translate/with-form/image/stream/web`
- **Method:** POST
- **Description:** Streaming versions of the form-upload endpoints. The `/web` variant uses placeholder optimization for faster web UI response.
- **Tested:** No

### Batch Translate (JSON response)
- **URL:** `/translate/batch/json`
- **Method:** POST
- **Description:** Translate multiple images at once. Returns list of translation results.
- **Request:** `curl -X POST http://localhost:5003/translate/batch/json -H "Content-Type: application/json" -d '{"images": ["url1", "url2"], "config": {}, "batch_size": 4}'`
- **Tested:** No

### Batch Translate (ZIP response)
- **URL:** `/translate/batch/images`
- **Method:** POST
- **Description:** Translate multiple images, returns ZIP archive of translated PNGs.
- **Request:** `curl -X POST http://localhost:5003/translate/batch/images -H "Content-Type: application/json" -d '{"images": ["url1", "url2"], "config": {}, "batch_size": 4}' -o results.zip`
- **Tested:** No

### Queue Size
- **URL:** `/queue-size`
- **Method:** POST
- **Description:** Returns number of tasks in the translation queue.
- **Request:** `curl -X POST http://localhost:5003/queue-size`
- **Response:** `0`
- **Tested:** Yes -- returned 0

### List Results
- **URL:** `/results/list`
- **Method:** GET
- **Description:** List all stored result directories (folders containing final.png).
- **Request:** `curl http://localhost:5003/results/list`
- **Response:** `{"directories": []}`
- **Tested:** Yes -- returned empty list

### Get Result Image
- **URL:** `/result/{folder_name}/final.png`
- **Method:** GET
- **Description:** Retrieve a previously translated result image by folder name.
- **Request:** `curl http://localhost:5003/result/some-folder/final.png -o result.png`
- **Tested:** No (no stored results to retrieve)

### Clear All Results
- **URL:** `/results/clear`
- **Method:** DELETE
- **Description:** Delete all stored result directories.
- **Request:** `curl -X DELETE http://localhost:5003/results/clear`
- **Response:** `{"message": "Deleted 0 result directories"}`
- **Tested:** No

### Delete Specific Result
- **URL:** `/results/{folder_name}`
- **Method:** DELETE
- **Description:** Delete a specific result directory.
- **Request:** `curl -X DELETE http://localhost:5003/results/some-folder`
- **Tested:** No

### Web UI
- **URL:** `/`
- **Method:** GET
- **Description:** Interactive web interface for uploading and translating manga images.
- **Tested:** Yes -- 200 OK, 75KB HTML

### Manual Page
- **URL:** `/manual`
- **Method:** GET
- **Description:** Manual/help page with usage instructions.
- **Tested:** Yes -- 200 OK, 6.9KB HTML

### OpenAPI Docs
- **URL:** `/docs`
- **Method:** GET
- **Description:** Auto-generated FastAPI/Swagger documentation.
- **Tested:** Yes -- 200 OK

## Config Object
The `config` field in translation requests accepts a JSON object. Key fields (all optional):
- `translator`: Translator to use (default: "sugoi" for JA->EN, "gpt4" etc. for others)
- `tgt_lang`: Target language code (default: "ENG")
- `detector`: Text detector model
- `ocr`: OCR model
- `inpainter`: Inpainting model
- `render`: Rendering options

See `/docs` endpoint for full schema or the repo's README for all configuration options.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | No | None | Required only if using GPT-based translators |
| DEEPL_AUTH_KEY | No | None | Required only if using DeepL translator |
| MT_WEB_NONCE | No | auto-generated | Security nonce for internal API |

## Notes
- Image is ~10GB (15GB reported but actual pull is smaller). Based on Ubuntu with Python ML stack.
- First translation request triggers model downloads (~622MB for sugoi translator). Subsequent requests are fast.
- CPU mode works but is slow (~30-60s per image). GPU (NVIDIA) significantly faster. Use `--gpus all` with docker run for GPU.
- Default translator is "sugoi" (offline, no API key needed) for Japanese-to-English. Other language pairs may require online translators (GPT, DeepL) with API keys.
- The server runs on port 5003 (API) and spawns a translator instance on port 5004 internally.
- `--ipc=host` flag recommended for shared memory when processing large images.
