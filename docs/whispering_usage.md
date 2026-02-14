# whispering (Whispering Tiger) -- Usage Documentation

## Status: SKIP

## Reason
- Requires live audio device (microphone) -- crashes without one
- Windows-centric: PyAudioWPatch, pywin32, winsdk, triton-windows
- WebSocket-only interface (no HTTP API)
- ~185 direct dependencies, many from custom GitHub forks
- No deployment Dockerfile (only PyInstaller build Dockerfiles)
- Would require significant architectural changes to run in Docker headless

## What It Does
Speech transcription tool using Whisper models. Streams audio from microphone, transcribes in real-time via WebSocket, outputs to OSC.

## Original Repo
https://github.com/Sharrnah/whispering
