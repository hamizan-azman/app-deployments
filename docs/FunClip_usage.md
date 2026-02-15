# FunClip -- Usage Documentation

## Overview
Open-source video/audio clipping tool powered by Alibaba FunASR. Recognizes speech, lets users select text segments or speakers, and clips the corresponding video/audio. Supports LLM-based smart clipping.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/funclip

# Or build from source
docker build -t funclip apps/FunClip/

docker run -d --name funclip -p 7860:7860 hoomzoom/funclip
```

First startup downloads ~1.2GB of ASR models from ModelScope (takes a few minutes). Subsequent starts use cached models in the container.

No API key needed for basic speech recognition and clipping. For LLM-based smart clipping, enter your API key (OpenAI, DeepSeek, or Qwen) in the web UI's LLM settings panel.

## Base URL
http://localhost:7860

## Core Features
- Speech recognition (ASR) for audio and video files
- Speaker diarization (identify different speakers)
- Text-based clipping (select text, get corresponding video/audio segment)
- Speaker-based clipping (clip all segments from a specific speaker)
- Subtitle embedding (burn subtitles into clipped video)
- LLM-based smart clipping (uses GPT/Qwen/g4f to identify interesting segments)
- English and Chinese language support

## Interface
FunClip is a Gradio web UI. Open http://localhost:7860 in a browser.

### Workflow
1. Upload video or audio file
2. Click "ASR" (recognition) or "ASR+SD" (recognition with speaker diarization)
3. Copy desired text to "Text to Clip" field, or set speaker ID
4. Click "Clip" or "Clip+Subtitles"

### LLM Clipping Workflow
1. After recognition, select an LLM model and enter API key
2. Click "LLM Inference" to get AI-suggested clip segments
3. Click "AI Clip" to clip based on LLM suggestions

## Gradio API Endpoints

### /mix_recog
- **Description:** Speech recognition (ASR) on uploaded audio or video
- **Parameters:** video_input (file), audio_input (file), hotwords (string), output_dir (string)
- **Returns:** recognition text, SRT subtitles, video_state, audio_state
- **Tested:** Yes -- PASS

### /mix_recog_speaker
- **Description:** ASR with speaker diarization
- **Parameters:** video_input (file), audio_input (file), hotwords (string), output_dir (string)
- **Returns:** recognition text with speaker IDs, SRT subtitles, video_state, audio_state
- **Tested:** Yes -- PASS

### /mix_clip
- **Description:** Clip audio/video based on recognized text
- **Parameters:** dest_text, speaker_id, start_offset_ms, end_offset_ms, video_state, audio_state, output_dir
- **Returns:** clipped video, clipped audio, log message, clipped SRT
- **Tested:** Yes -- PASS (direct Python call, matched text segment at 95.72s-97.94s, clipped 2.22s)

### /video_clip_addsub
- **Description:** Clip video with burned-in subtitles
- **Parameters:** dest_text, speaker_id, start_offset_ms, end_offset_ms, video_state, output_dir, font_size, font_color
- **Returns:** clipped video with subtitles, log message, clipped SRT
- **Tested:** Uses same clip logic as /mix_clip (verified above), subtitle overlay requires ImageMagick (installed)

### /llm_inference
- **Description:** Call LLM to analyze SRT and suggest clip segments
- **Parameters:** system_prompt, user_prompt, srt_text, model_name, api_key
- **Returns:** LLM response with timestamps
- **Tested:** Yes -- PASS (gpt-4-turbo with OpenAI key)

### /AI_clip
- **Description:** Clip based on LLM inference results
- **Parameters:** llm_result, dest_text, speaker_id, start_offset_ms, end_offset_ms, video_state, audio_state, output_dir
- **Returns:** clipped video, clipped audio, log message, clipped SRT
- **Tested:** Browser only (requires gr.State session + API key)

### /AI_clip_subti
- **Description:** AI clip with burned-in subtitles
- **Parameters:** Same as /AI_clip
- **Returns:** clipped video with subtitles, clipped audio, log message, clipped SRT
- **Tested:** Browser only (requires gr.State session + API key)

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| None required | - | - | API keys entered through web UI for LLM features |

## Supported LLM Models (for smart clipping)
- deepseek-chat (requires API key)
- qwen-plus (requires Alibaba Bailian API key)
- gpt-3.5-turbo, gpt-4-turbo (requires OpenAI API key)
- g4f-gpt-3.5-turbo (free, unstable)

## CLI Usage (inside container)
```bash
# Recognize
docker exec funclip python funclip/videoclipper.py --stage 1 --file /path/to/video.mp4 --output_dir /output

# Clip
docker exec funclip python funclip/videoclipper.py --stage 2 --file /path/to/video.mp4 --output_dir /output --dest_text 'text to clip' --output_file /output/result.mp4
```

## Test Summary
| Test | Result |
|------|--------|
| Homepage (GET /) | PASS |
| Gradio API info (/gradio_api/info) | PASS -- 7 endpoints listed |
| /mix_recog (ASR) | PASS -- returns text + SRT |
| /mix_recog_speaker (ASR+SD) | PASS -- returns text with speaker IDs |
| /mix_clip (text-based clip) | PASS -- matched segment, clipped 2.22s |
| /llm_inference (gpt-4-turbo) | PASS |

## Notes
- First startup is slow due to model downloads (~1.2GB from ModelScope)
- Models cached inside the container; restarting the container re-downloads them
- For persistent model cache, mount a volume: `-v funclip_models:/root/.cache/modelscope`
- Clip endpoints only work through the browser UI (Gradio session state manages numpy arrays)
- Default language is English (`-l en`). Change to Chinese with `-l zh` in the CMD
- Requires ~2GB RAM for model loading and inference

## Changes from Original
None. Dockerfile written from scratch. PyTorch CPU variant used (same version, different build). ImageMagick policy fix follows the developer's own README instructions.
