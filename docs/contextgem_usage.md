# contextgem -- Local Install Guide

## Overview
contextgem is a Python library for LLM-powered document analysis. It provides a structured API for extracting concepts, entities, and relationships from documents using large language models. It is a developer-facing library with no web interface or entry point of its own.

## Why Not Dockerized
contextgem is a library only. It has no web server, CLI entry point, or runnable application. Containerising a library with no entry point serves no purpose for testing or research. It is installed as a dependency inside other applications.

## Requirements
- Python 3.10 or newer
- pip
- OpenAI API key or compatible LLM provider credentials

## Installation

```bash
pip install contextgem
```

To install from source:

```bash
git clone https://github.com/shcheklein/contextgem.git
cd contextgem
pip install -e .
```

## Usage

contextgem is used as a Python library inside your own scripts or notebooks. A minimal example:

```python
from contextgem import Document, DocumentAnalyzer

doc = Document(text="Your document text here.")
analyzer = DocumentAnalyzer(llm_provider="openai", model="gpt-4o")
result = analyzer.analyze(doc)
print(result)
```

Refer to the contextgem documentation and examples directory for full usage patterns including concept extraction, entity linking, and multi-document pipelines.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes (for OpenAI backend) | None | API key for the LLM provider |

## Notes
- contextgem supports multiple LLM backends. OpenAI is the primary supported provider. Check the README for alternatives.
- No web UI exists. All interaction is through the Python API.
- GitHub: https://github.com/shcheklein/contextgem
