# home-llm -- Usage Documentation

## Status: SKIP (not compatible with Docker)

## Reason
- Not a standalone application -- Home Assistant custom integration/component
- Must be installed inside existing Home Assistant instance
- Cannot deploy independently in Docker without full HA ecosystem
- Out of scope for standalone app deployment project

## What It Does
Home Assistant custom integration for controlling smart home devices with local LLMs. Supports Ollama, llama.cpp, and external APIs.

## Original Repo
https://github.com/acon96/home-llm

## Manual Build Steps

Since this is a Home Assistant integration (not a standalone app), install it into an existing HA instance:

```bash
# Requires: Home Assistant 2025.7.0+, HACS installed

# Option 1: Via HACS (recommended)
# 1. Open Home Assistant
# 2. Go to Settings > Devices and Services > + Add Integration
# 3. Search for "Local LLM" and install
# 4. Configure the LLM backend (Ollama, llama.cpp, OpenAI-compatible API)

# Option 2: Manual installation
# 1. Clone into HA custom_components directory
git clone https://github.com/acon96/home-llm.git
cp -r home-llm/custom_components/llama_conversation <HA_CONFIG>/custom_components/

# 2. Restart Home Assistant
# 3. Go to Settings > Devices and Services > + Add Integration > Local LLM

# Option 3: Standalone dependency install (for code analysis only)
pip install -r requirements.txt
# Note: The code will not function without a running Home Assistant instance
```

## Core Features
- Local LLM control of smart home devices
- Supports multiple backends: Ollama, llama.cpp (built-in), Generic OpenAI API, LM Studio
- Fine-tuned models available on HuggingFace for home automation tasks
- No GPU required for basic setup (Raspberry Pi compatible)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| (via HA UI) | Yes | None | LLM backend URL and API key, configured through Home Assistant integration settings |
