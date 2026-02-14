# MedRAX -- Usage Documentation

## Status: SKIP

## Reason
- Requires GPU for medical imaging model inference
- Multiple large models from HuggingFace (CheXagent, LLaVA-Med, MedSAM, Maira-2)
- No Dockerfile provided
- Specialized medical imaging pipeline requiring manual model download
- GPU-only inference with torch, transformers, accelerate, bitsandbytes

## What It Does
Medical reasoning agent for chest X-ray interpretation using specialized AI tools and multimodal LLMs. Gradio web interface.

## Original Repo
https://github.com/bowang-lab/MedRAX
