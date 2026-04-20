# Deployment Failure Analysis

Covers the 23 of 102 applications in the benchmark set that were classified as not containerisable during Tasks 1, 2, and 3. Each failure is categorised by its concrete technical blocker. Per-app install notes are linked under each entry.

## 1. Summary

| Figure | Count |
|---|---|
| Applications evaluated | 102 |
| Deployed successfully (Docker image on Docker Hub under `hoomzoom/`) | 79 |
| Not containerised ("fail") | 23 |
| Skip rate | 22.5% |

Of the 79 successful deployments, 53 are server-type apps (HTTP endpoint on Streamlit, Gradio, FastAPI, Flask, Next.js, Django, Node, or a compose stack) and 26 are CLI-type apps (command-line tools, libraries with a `python -m <pkg>` entry point, or one-shot scripts).

## 2. Failure distribution

![Failure reasons pie chart](benchmark/failure_reasons_pie.png)

| # | Category | Apps | Share of fails |
|---|---|---:|---:|
| 1 | Desktop-bound (GUI or RPA) | 8 | 34.8% |
| 2 | Requires specific host resource (audio, mobile, non-headless browser) | 5 | 21.7% |
| 3 | GPU or VRAM ceiling (no CPU fallback) | 4 | 17.4% |
| 4 | Library only (no runnable entry point) | 4 | 17.4% |
| 5 | Not standalone (plugin or deprecated model) | 2 | 8.7% |
| Total |   | 23 | 100% |

Source data. `benchmark/failure_breakdown.csv`. Vector figure for paper inclusion. `benchmark/failure_reasons_pie.pdf`.

## 3. Classification criteria

An application was classified as a deployment failure ("skipped") when any of the following held after reviewing the repository and attempting a clean Docker build.

1. The project requires a live desktop display (X, Quartz, DirectX, Wayland) to render a GUI or to satisfy a toolkit (Tkinter, CustomTkinter, PyQt5, PyQt6, Flet desktop).
2. The project requires synthetic input to the host's physical input devices (pyautogui, pynput, pydirectinput, Win32 `SendInput`).
3. The project requires a hardware device not available inside a container (microphone, speaker, camera, Android phone via ADB, iOS device, game controller, Home Assistant host integration).
4. The project requires Windows-only APIs (pywin32, pywinauto, Windows UI Automation, DirectX capture) that cannot be provided by a Linux container or by Docker Desktop's Windows containers in a reproducible way.
5. The project requires GPU VRAM above the ceiling allowed by the benchmark's target machines (16 GB VRAM or no CPU fallback documented upstream).
6. The project is a library with no web interface, no CLI, no long-running entry point, and no authored containerisable service on top of it.
7. The project's advertised containerisation path is broken (missing directories or files referenced by `docker-compose.yml`) and no upstream fix exists.
8. The project targets a deprecated dependency that the research scope does not support (a retired OpenAI model, for example).

Where an app failed more than one criterion, it was placed in the most specific bucket.

## 4. Per-category analysis

### 4.1 Desktop-bound, GUI or RPA (8 apps, 34.8%)

The largest class. The app is built around a desktop window or around active control of the host's input devices. It cannot run without a display server and, for the RPA subset, a real keyboard and mouse. Docker containers have neither.

Split roughly half and half between pure GUI apps (4) that render a window and accept user input through it, and RPA or Windows-automation apps (4) that go further by synthesising mouse and keyboard events on the host.

| App | Blocker | Doc |
|---|---|---|
| AiNiee | PyQt5 and PyQt-Fluent-Widgets desktop tool for bulk translation. File selection and translation control happen through the window. | [AiNiee_usage.md](AiNiee_usage.md) |
| AI_NovelGenerator | CustomTkinter novel-writing app. `main.py` constructs a `customtkinter.CTk()` root and runs `mainloop()`. No CLI mode. | [AI_NovelGenerator_usage.md](AI_NovelGenerator_usage.md) |
| VideoCaptioner | PyQt5 desktop subtitling app. Window handles file import, caption editing, and video export. | [VideoCaptioner_usage.md](VideoCaptioner_usage.md) |
| Open-Interface | Tkinter tray app that controls host mouse and keyboard via `pyautogui` and screenshots via `mss`. macOS-focused dependency set. | [Open-Interface_usage.md](Open-Interface_usage.md) |
| autoMate | OmniParser-based RPA. `pyautogui` and `pynput` simulate input. Reads the desktop via an OCR pipeline. The web UI at port 7888 configures only. The automation target is the host desktop. | [autoMate_usage.md](autoMate_usage.md) |
| UFO | Uses `pywinauto`, `pywin32`, and the Windows UI Automation API to read the element tree and dispatch input. Requires a visible desktop. | [UFO_usage.md](UFO_usage.md) |
| Windrecorder | Continuously records the Windows screen with `mss` and DirectX capture, OCRs frames, and indexes them for search. No meaning inside a headless container. | [windrecorder_usage.md](windrecorder_usage.md) |
| Cradle | Multi-target agent. Games on Windows desktop plus mobile apps over ADB. The desktop runner needs RDR2 or similar running on the host. Screen capture via DirectX. | [Cradle_usage.md](Cradle_usage.md) |

### 4.2 Requires specific host resource (5 apps, 21.7%)

Apps that need a particular resource the container does not have. The resource is narrower than "a desktop" but just as unavailable. Microphone and speaker access, a physically-connected Android device reachable by ADB, or a visible non-headless browser.

| App | Resource needed | Doc |
|---|---|---|
| whispering | Microphone. Live-transcription overlay. No file-input fallback. | [whispering_usage.md](whispering_usage.md) |
| GLaDOS | Microphone and speaker. Local voice assistant (STT, LLM, TTS loop). No text-only mode. | [GLaDOS_usage.md](GLaDOS_usage.md) |
| AppAgent | Android device via ADB. `adb shell uiautomator dump`, `adb exec-out screencap`, `adb shell input`. Removing the device removes the only I/O surface. | [AppAgent_usage.md](AppAgent_usage.md) |
| droidrun | Android device via ADB. Optional iOS support. No standalone mode. | [droidrun_usage.md](droidrun_usage.md) |
| wiseflow | Visible non-headless Chrome. Upstream README documents that headless Chrome breaks most target sites (captcha walls, UA-sniffing redirects). No Dockerfile shipped. | [wiseflow_usage.md](wiseflow_usage.md) |

### 4.3 GPU or VRAM ceiling (4 apps, 17.4%)

Projects that hard-depend on a CUDA-capable GPU. They either refuse to run on CPU or are unusably slow. Upstream does not ship a CPU configuration. All four exceed the 16 GB VRAM ceiling the benchmark targets.

| App | Blocker | Doc |
|---|---|---|
| TaskMatrix | Orchestrates Visual ChatGPT plus Stable Diffusion, Grounding DINO, and SAM. Needs 16 GB or more VRAM across concurrent models. | [TaskMatrix_usage.md](TaskMatrix_usage.md) |
| MedRAX | Medical-imaging multi-modal agent. Loads several CheXagent, BioMedCLIP, and MedSAM checkpoints at the same time. Upstream quotes 12 to 16 GB VRAM minimum. | [MedRAX_usage.md](MedRAX_usage.md) |
| functionary | Serves the Functionary LLM weights through vLLM or SGLang. Both backends are GPU-only. Smallest supported quantisation still needs 24 GB or more VRAM. | [functionary_usage.md](functionary_usage.md) |
| Linly-Talker | SadTalker, Wav2Lip, and optional GFPGAN for talking-head video synthesis. Pipeline requires GPU throughout. CPU path is not wired up. | [Linly-Talker_usage.md](Linly-Talker_usage.md) |

### 4.4 Library only (4 apps, 17.4%)

Pure Python libraries consumed as a dependency from another application. No HTTP server, no CLI, no runnable entry point. Containerising a library in isolation produces an image with no process to run.

| App | Blocker | Doc |
|---|---|---|
| pandas-ai | `docker-compose.yml` references `./server` and `./client` directories that are not present in the public repo (they belong to the closed-source "PandaBI Platform"). The library itself has no CLI or server. | [pandas-ai_usage.md](pandas-ai_usage.md) |
| itext2kg | Pure library (`from itext2kg import iText2KG`). No CLI, no server, no examples with a runnable main. | [itext2kg_usage.md](itext2kg_usage.md) |
| ExtractThinker | Pure library exposing `Extractor` and `Contract` classes for document extraction. No authored service. | [ExtractThinker_usage.md](ExtractThinker_usage.md) |
| contextgem | Pure library for LLM document analysis. Imported as a dependency inside other applications. | [contextgem_usage.md](contextgem_usage.md) |

### 4.5 Not standalone (2 apps, 8.7%)

Not deployable applications in isolation. Each exists only as part of a larger product, or targets a retired dependency.

| App | Blocker | Doc |
|---|---|---|
| home-llm | Home Assistant custom integration. Installed via HACS into an existing Home Assistant instance. No standalone mode and nothing to `docker run`. | [home-llm_usage.md](home-llm_usage.md) |
| Codex-CLI | Bash, Zsh, and PowerShell hook that completes command lines using the original OpenAI Codex model. Codex was deprecated by OpenAI in 2023. No HTTP interface and no current-model replacement in this repo. | [Codex-CLI_usage.md](Codex-CLI_usage.md) |

## 5. What was attempted before skipping

For every app placed in a fail bucket, the following were checked in order.

1. Read the upstream README, `Dockerfile`, and `docker-compose.yml` (if any).
2. Read the `requirements.txt`, `pyproject.toml`, and `package.json` for dependencies that preclude a headless Linux container (PyQt5 full build, pywinauto, pyobjc, pyautogui on its own, sounddevice).
3. Look for a `--headless`, `--server`, `--api`, `--daemon`, `serve`, or equivalent CLI flag or subcommand in the entry points.
4. Search issues and discussions for "Docker" and "headless" to see whether the upstream project or community provides a supported container path.
5. For compose stacks, attempt a dry-run `docker compose config` to check that all referenced build contexts exist.
6. Where a GPU wall was suspected, check for an explicit "CPU mode", a `device=cpu` config path, or an `if torch.cuda.is_available()` fallback that does not raise.

Where any of those paths would produce a runnable container, the app was moved to success with a note in its `_reasoning.md` document. Only when every path failed was the app placed in the skip list.

## 6. Cross-references

- Full per-app status table. `../task2_status.md` (repo root).
- Lark tracker (external). `Total_Task_84` sheet columns `status` and `remark` match this document.
- Raw failure data for the pie chart. `benchmark/failure_breakdown.csv`.
- Vector figure for paper inclusion. `benchmark/failure_reasons_pie.pdf`.
- Individual `*_usage.md` skip docs linked in the per-category tables above.
