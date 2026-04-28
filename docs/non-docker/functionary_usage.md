# functionary -- Local Install Guide

**Deployment**: GPU server. NVIDIA GPU 24+ GB VRAM minimum.

## Overview
functionary is an LLM inference server built around models trained for reliable function calling and structured JSON output. It exposes an OpenAI-compatible API endpoint and is designed for use with vLLM or SGLang as the inference backend. Models range from 7B to 70B parameters.

## Why Not Dockerized
functionary requires 24GB or more of VRAM for its full-scale models. The research workstation (GTX 1650, 4 GB VRAM) is well below that. vLLM and SGLang are GPU-only runtimes with no practical CPU fallback for inference at these model sizes. Running it inside Docker also adds overhead without benefit when the blocking constraint is hardware. The canonical deployment target is the lab GPU server.

## Requirements
- OS: Linux (strongly recommended). Windows via WSL2 is possible but not officially supported.
- NVIDIA GPU with 24GB+ VRAM (e.g. A100, RTX 4090, or multi-GPU setup)
- CUDA 12.1 or newer
- Python 3.10 or 3.11
- pip or conda

## Installation

```bash
# Install vLLM first (the recommended inference backend)
pip install vllm

# Install functionary
pip install functionary
```

For SGLang backend instead of vLLM:

```bash
pip install "sglang[all]"
pip install functionary
```

## Usage

**Serve a functionary model via vLLM:**

```bash
vllm serve meetkai/functionary-small-v3.2 --host 0.0.0.0 --port 8000
```

The server exposes an OpenAI-compatible API at `http://localhost:8000`. Send requests to `/v1/chat/completions` with tools defined in the standard OpenAI format.

**Minimal Python client example:**

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="ignored")

response = client.chat.completions.create(
    model="meetkai/functionary-small-v3.2",
    messages=[{"role": "user", "content": "What is the weather in Paris?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        }
    }]
)
print(response.choices[0].message.tool_calls)
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HUGGING_FACE_HUB_TOKEN` | Optional | None | Required if downloading gated models from Hugging Face |

## Notes
- Available models on Hugging Face under the `meetkai/` namespace: functionary-small-v3.2 (8B), functionary-medium-v3.2 (70B), and others.
- The small 8B model may fit in 16GB VRAM with quantization (bitsandbytes or GPTQ). Use `--quantization awq` with vLLM for reduced memory usage.
- functionary is API-key-free at the server level. No OpenAI API key is needed when self-hosting.
- GitHub: https://github.com/MeetKai/functionary
