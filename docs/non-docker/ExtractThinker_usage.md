# ExtractThinker. Local Install Guide

**Deployment**: Library only. `pip install extract-thinker`.

## Overview
ExtractThinker is a Python library for LLM-powered document intelligence. It provides an ORM-style abstraction for describing the fields you want pulled out of a document (invoice, resume, contract, driver licence), routes pages through an OCR or LLM pipeline, and returns typed Python objects.

## Why Not Dockerized
ExtractThinker is a pure Python library.

- It exposes only an `Extractor`, `Contract`, and `DocumentLoader` API, imported from user code.
- There is no HTTP server, no CLI, and no long-running process in the repo.
- The `examples/` directory contains short notebook-style scripts, not deployable services.

Wrapping it in a Docker image would mean writing a custom FastAPI or Flask server on top of the library, which is outside the scope of the benchmark. The goal is to containerise each app in the form its authors ship it, not to invent a server for every library.

## Requirements
- Python 3.10 or newer
- `pip`
- One or more of.
  - OpenAI or Azure OpenAI key (most examples use OpenAI)
  - Anthropic key
  - A local Ollama instance
- Tesseract (only if using the Tesseract OCR loader. Not required for vision-LLM-only pipelines)

## Installation

```bash
pip install extract-thinker
```

For source install with examples.

```bash
git clone https://github.com/enoch3712/ExtractThinker.git
cd ExtractThinker
pip install -e .
```

## Usage

```python
from extract_thinker import Extractor, Contract
from extract_thinker.document_loader import DocumentLoaderPyPdf

class Invoice(Contract):
    invoice_number: str
    invoice_date: str
    total_amount: float

extractor = Extractor()
extractor.load_document_loader(DocumentLoaderPyPdf())
extractor.load_llm("gpt-4o")

result: Invoice = extractor.extract("path/to/invoice.pdf", Invoice)
print(result)
```

The `examples/` directory covers multi-page routing, async batches, Pydantic validation, and alternative loaders (Azure Document Intelligence, Tesseract, AWS Textract).

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY      | Yes (for OpenAI) | None | Passed to the underlying LLM client |
| ANTHROPIC_API_KEY   | Yes (for Claude) | None | Same |
| AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT | Yes (for Azure) | None | Same |

## Notes
- The library name on PyPI is `extract-thinker` (with a hyphen). The Python package is `extract_thinker` (underscore).
- Use Pydantic `Contract` subclasses to get typed, validated outputs instead of free-text JSON.
- Verified: `pip install extract-thinker` resolves to v0.1.14 and `from extract_thinker import Extractor, Contract` imports cleanly on Python 3.12 (Ubuntu WSL), 27 April 2026.
- Dependency conflict. `extract-thinker` pulls in `openai>=2.x` while `itext2kg 1.0.0` pins `openai<2.0.0,>=1.97.0`. They cannot share a venv. Install each in its own venv if you need both.
- GitHub. https://github.com/enoch3712/ExtractThinker
