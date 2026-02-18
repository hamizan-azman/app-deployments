# home-llm -- Local Install Guide

## Overview
home-llm is a Home Assistant custom integration that connects local LLMs (via Ollama, llama.cpp, or an OpenAI-compatible API) to Home Assistant, enabling voice and chat control of smart home devices without cloud services.

## Why Not Dockerized
home-llm is not a standalone application. It is a Home Assistant custom component (`custom_components/llama_conversation`) that must be installed inside a running Home Assistant instance. It has no server, no CLI entrypoint, and no independent function outside the HA ecosystem.

## Requirements
- Home Assistant 2025.7.0 or newer (running instance)
- HACS (Home Assistant Community Store) for easy install, or manual file copy
- An LLM backend: Ollama, llama.cpp, LM Studio, or any OpenAI-compatible API
- No dedicated GPU required for small models (Phi-3-mini, Llama-3.2-3B); larger models benefit from GPU

## Installation

### Option 1: HACS (recommended)

1. In Home Assistant, go to **HACS > Integrations > Custom Repositories**.
2. Add `https://github.com/acon96/home-llm` as an Integration repository.
3. Search for "Local LLM Conversation" in HACS and install it.
4. Restart Home Assistant.
5. Go to **Settings > Devices & Services > Add Integration** and search for "Local LLM".

### Option 2: Manual file copy

```bash
# From a machine with access to your HA config directory
git clone https://github.com/acon96/home-llm.git
cp -r home-llm/custom_components/llama_conversation /path/to/homeassistant/custom_components/
```

Restart Home Assistant, then add the integration via **Settings > Devices & Services > Add Integration > Local LLM**.

## Usage

After installation and HA restart:

1. Add the "Local LLM Conversation" integration.
2. Select a backend: Ollama (recommended), llama.cpp built-in, or Generic OpenAI API.
3. Enter the backend URL (e.g., `http://localhost:11434` for Ollama).
4. Set the model name (e.g., `acon96/Home-3B-v3-GGUF`).
5. Assign the integration as your voice assistant in **Settings > Voice Assistants**.

### Recommended models (available on HuggingFace)
- `acon96/Home-3B-v3-GGUF` (small, Raspberry Pi compatible)
- `acon96/Home-8B-v3-GGUF` (better accuracy, needs 8GB+ RAM)

## Notes
- Pre-trained "Home" models fine-tuned for smart home commands are available at https://huggingface.co/collections/acon96/home-llm.
- The built-in llama.cpp backend runs the model directly inside Home Assistant. Ollama is easier to set up on separate hardware.
- Controlled device types: lights, switches, fans, covers, locks, climate, media players, vacuums, buttons, timers, scripts.
- GitHub: https://github.com/acon96/home-llm
