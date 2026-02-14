# TaskMatrix (Visual ChatGPT) -- Usage Documentation

## Status: SKIP

## Reason
- Heavy GPU requirements: 3-15GB GPU memory per foundation model
- Designed for multi-GPU setup (4x Tesla V100 32GB for full features)
- No complete Dockerfile for main application
- Downloads many large models at runtime (ControlNet, Stable Diffusion, BLIP)
- No CPU fallback for visual foundation models

## What It Does
Connects ChatGPT with visual foundation models to enable sending/receiving images during chat. Supports image generation, editing, visual QA through multiple AI models.

## Original Repo
https://github.com/chenfei-wu/TaskMatrix
