# Zshot -- Deployment Reasoning Log

## What is Zshot?

Zshot is an IBM Research library for zero-shot named entity recognition (NER). It extends spaCy pipelines with components that can recognize entities without needing task-specific training data. You provide entity descriptions (e.g., "IBM -- an American multinational technology corporation") and Zshot uses transformer models to match spans of text to those entities.

The library itself is a Python package with no built-in web interface. It's designed to be used as a library in Python code, not as a standalone service. This means we need to write a web wrapper ourselves.

## Step 1: Analyzing the Repository

### Files checked and why

- **README.md**: First thing to read for any repo. Tells you what the project does, how to install it, and how to use it. Zshot's README showed it's a spaCy pipeline component, uses `nlp.add_pipe("zshot", ...)`, and has multiple backend options (LinkerRegen, LinkerSMXM, LinkerBlink, etc.).

- **setup.py / setup.cfg**: These define the package's dependencies. setup.cfg listed core deps (spacy, torch, transformers, etc.) and optional dep groups like `[blink]`, `[tars]`, `[relik]`, `[gliner]`. This told me that many backends are optional and their dependencies are not installed by default.

- **zshot/config.py**: Found the critical constant `MODELS_CACHE_PATH = os.path.join(Path.home(), ".cache", "zshot")`. This tells us where Zshot looks for downloaded models -- not the default HuggingFace cache location, but `~/.cache/zshot/`. This became important later.

- **zshot/__init__.py, zshot/linker/__init__.py, zshot/mentions_extractor/__init__.py, zshot/knowledge_extractor/__init__.py**: These `__init__.py` files control what gets imported when you `import zshot`. Several of them had unconditional imports of optional backends (relik, gliner, blink, flair), which would cause ImportError at runtime if those optional packages weren't installed.

- **Dockerfile**: The repo had no Dockerfile, confirming we need to write one from scratch.

- **Docker Hub**: No pre-built image available.

### What I learned

1. Zshot is a library, not a service. Need to write a FastAPI wrapper.
2. The core pipeline needs: spaCy + a mentions extractor + a linker + entity definitions.
3. LinkerRegen (T5-based) is the default/simplest linker that doesn't need extra optional deps beyond transformers.
4. MentionsExtractorSpacy is the simplest extractor, using spaCy's built-in NER to find mention spans.
5. Models get cached to `~/.cache/zshot/`, not the default HuggingFace cache.

## Step 2: Writing the FastAPI Wrapper (app.py)

### Design decisions

I wrote a minimal FastAPI app with three endpoints:

- **GET /health**: Standard health check. Every containerized service needs one.
- **POST /extract**: The core NER endpoint. Takes text, returns structured JSON with entity spans, labels, and positions.
- **POST /visualize**: Returns displacy HTML rendering of entities. Zshot already provides a `displacy` module, so this was easy to expose.

### Why these specific components

- **MentionsExtractorSpacy**: Uses spaCy's built-in NER to identify candidate spans. Simplest option, no extra dependencies.
- **LinkerRegen**: Uses IBM's `ibm/regen-disambiguation` T5 model to link mention spans to entity descriptions. This is the default linker shown in Zshot's README examples.
- **en_core_web_sm**: The smallest spaCy English model. Sufficient for mention extraction since we only need basic NER spans.

### Default entities

I included 6 entities from the README example (Paris, IBM, New York, Florida, American, Armonk). These serve as the default entity set for the API. In a production setting you'd want a `/configure` endpoint to update entities, but the user explicitly said to keep app.py simple and not add features that could make it less reproducible for team members.

## Step 3: Writing the Dockerfile

### Base image: python:3.10-slim

- Python 3.10 because zshot's setup.cfg specifies `python_requires = >=3.8`. 3.10 is a safe middle ground.
- `-slim` variant to reduce image size (though the final image is still ~5GB due to PyTorch and model weights).
- Not alpine because many Python packages need glibc and compiling from source on alpine is painful.

### Build steps explained

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
```
build-essential is needed because some transitive dependencies (like sentencepiece) compile C extensions during pip install.

```dockerfile
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
```
CPU-only PyTorch. The full PyTorch with CUDA is ~2GB larger and we don't need GPU support for this deployment. Using the CPU wheel index keeps the image smaller.

```dockerfile
COPY setup.py setup.cfg README.md ./
COPY zshot/ zshot/
RUN pip install --no-cache-dir "transformers>=4.20,<5" && pip install --no-cache-dir -e .
```
Two important things here:
1. **transformers pinned to <5**: This was a fix for a runtime error. transformers v5 removed `batch_encode_plus` from slow tokenizers (like T5Tokenizer). Zshot's LinkerRegen calls this method, so we need transformers v4.x.
2. **Install transformers before zshot**: Because zshot's setup.cfg just says `transformers`, which would pull v5. By installing v4.x first, pip sees the constraint is already satisfied and doesn't upgrade.

```dockerfile
RUN python -m spacy download en_core_web_sm
```
Pre-download the spaCy model so it's baked into the image. Without this, the first import of `spacy.load("en_core_web_sm")` would fail.

```dockerfile
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; cache = '/root/.cache/zshot/'; AutoTokenizer.from_pretrained('ibm/regen-disambiguation', cache_dir=cache); AutoModelForSeq2SeqLM.from_pretrained('ibm/regen-disambiguation', cache_dir=cache)"
```
Pre-download the LinkerRegen model. Critical detail: we specify `cache_dir='/root/.cache/zshot/'` because that's where Zshot's `config.py` looks for cached models. If we let HuggingFace download to its default cache (`~/.cache/huggingface/`), Zshot wouldn't find the model at runtime and would try to re-download it (which would fail in an air-gapped environment or add startup latency).

## Step 4: Errors Encountered and Fixes

### Error 1: ModuleNotFoundError -- relik, gliner, blink, flair

**What happened**: Container started, Python imported zshot, and immediately crashed because `zshot/knowledge_extractor/__init__.py` had `from zshot.knowledge_extractor.knowledge_extractor_relik import KnowledgeExtractorRelik` without a try/except guard. Same issue in linker and mentions_extractor __init__ files.

**Root cause**: The upstream code assumes all optional dependencies are installed. The setup.cfg has optional dependency groups (`[blink]`, `[tars]`, `[relik]`, `[gliner]`) but the `__init__.py` files don't guard their imports.

**Fix**: Wrapped the optional imports in try/except ImportError blocks in three files:
- `zshot/knowledge_extractor/__init__.py` -- wrapped relik import
- `zshot/linker/__init__.py` -- wrapped blink, tars, relik, gliner imports
- `zshot/mentions_extractor/__init__.py` -- wrapped gliner import

**Why this is safe**: These are optional backends. If someone needs LinkerBlink, they install the `[blink]` extras. Our deployment only uses LinkerRegen and MentionsExtractorSpacy, neither of which requires these optional packages.

### Error 2: AttributeError -- T5Tokenizer.batch_encode_plus

**What happened**: After fixing the import errors, the /extract endpoint crashed with `AttributeError: 'T5Tokenizer' object has no attribute 'batch_encode_plus'`.

**Root cause**: transformers v5.1.0 (released 2025) removed `batch_encode_plus` from "slow" tokenizers. The T5Tokenizer in LinkerRegen's code calls this method. This is a known breaking change in transformers v5.

**Fix**: Pin `transformers>=4.20,<5` in the Dockerfile pip install step. This keeps us on the v4.x line where batch_encode_plus exists.

**Why >=4.20**: Zshot's setup.cfg requires `transformers>=4.20` as the minimum version.

### Error 3: OSError -- Can't load model ibm/regen-disambiguation

**What happened**: The model pre-download step in the Dockerfile used the default HuggingFace cache, but Zshot looks in `~/.cache/zshot/`.

**Root cause**: Zshot's `config.py` sets `MODELS_CACHE_PATH = ~/.cache/zshot/`. When LinkerRegen loads the model, it passes this path as `cache_dir` to the transformers `from_pretrained` call. The model was downloaded to `~/.cache/huggingface/hub/` (default) but Zshot looked in `~/.cache/zshot/` and didn't find it.

**Fix**: Added `cache_dir='/root/.cache/zshot/'` to the Dockerfile pre-download command so the model is cached in the exact location Zshot expects.

### Error 4: AttributeError -- Zshot.cfg

**What happened**: An earlier version of app.py had a `/configure` endpoint that tried to modify the pipeline's entity list at runtime. This called methods that accessed `self.cfg` on the Zshot pipeline component, which doesn't exist in the current version.

**Fix**: Removed the `/configure` endpoint entirely. The user also pointed out that modifying app.py with extra features makes it less reproducible for team members. Keeping the API minimal (health, extract, visualize) with hardcoded default entities is the right approach.

## Step 5: Testing

### Test 1: GET /health
- **Why**: Confirms the container started, uvicorn is listening, and the app module loaded without errors.
- **Result**: `{"status":"ok"}` -- PASS

### Test 2: GET /docs
- **Why**: Confirms FastAPI's auto-generated Swagger docs are accessible. This validates that the FastAPI framework is properly configured.
- **Result**: HTTP 200 -- PASS

### Test 3: POST /extract
- **Why**: This is the core functionality. Sends a text about IBM and checks that the NER pipeline correctly identifies and links entities.
- **Input**: "International Business Machines Corporation (IBM) is an American multinational technology corporation headquartered in Armonk, New York."
- **Expected**: Should find IBM, American, Armonk, New York as entities matching the default entity descriptions.
- **Result**: Correctly extracted 5 entities: "International Business Machines Corporation"->IBM, "IBM"->IBM, "American"->American, "Armonk"->Armonk, "New York"->New York -- PASS

### Test 4: POST /visualize
- **Why**: Tests the displacy HTML rendering path. Different code path from /extract (uses zshot's displacy module instead of just returning JSON).
- **Result**: HTTP 200, returns HTML content -- PASS

## Summary

| Test | Result |
|------|--------|
| GET /health | PASS |
| GET /docs | PASS |
| POST /extract | PASS |
| POST /visualize | PASS |

4/4 tests pass. The deployment required:
- Writing app.py (FastAPI wrapper) from scratch
- Writing Dockerfile from scratch
- Fixing 3 source code files (optional import guards)
- Pinning transformers<5 (breaking API change)
- Fixing model cache path mismatch
