# Paper2Poster -- Usage Documentation

## Overview
Multi-agent system that converts academic papers (PDFs) into professional posters (PPTX). Uses a top-down, visual-in-the-loop pipeline: Parser extracts structured assets, Planner creates binary-tree layout, Painter-Commentor loop refines panels. Published at NeurIPS 2025.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/paper2poster

# Or build from source
docker build -t paper2poster ./Paper2Poster

docker run --rm hoomzoom/paper2poster python -m PosterAgent.new_pipeline --help
```

## Dockerfile Modifications
- Changed base image from `nvidia/cuda:12.6.0-devel-ubuntu24.04` to `ubuntu:24.04` (CPU-only, same supply chain)
- Added pip upgrade step with `PIP_BUILD_CONSTRAINT` to fix setuptools/pkg_resources issue in build isolation
- Pinned `docling_parse==4.0.0` (repo vendors older docling code expecting `pdf_parser_v2` API)

## CLI Commands

### Generate Poster (Main Pipeline)
```bash
# Run without --rm so output can be extracted via docker cp
MSYS_NO_PATHCONV=1 docker run \
  --name paper2poster_run \
  -e OPENAI_API_KEY=<your_key> \
  paper2poster \
  python -m PosterAgent.new_pipeline \
    --poster_path="/app/assets/poster_data/Test/nips-2011-001/nips-2011-001.pdf" \
    --model_name_t=4o \
    --model_name_v=4o \
    --poster_width_inches=48 \
    --poster_height_inches=36 \
    --max_workers=1

# Extract output (angle brackets in path are illegal on Windows)
docker start paper2poster_run
docker cp "paper2poster_run:/app/<4o_4o>_generated_posters/app/assets/poster_data/Test/nips-2011-001/nips-2011-001.pdf/poster.png" ./poster.png
docker cp "paper2poster_run:/app/<4o_4o>_generated_posters/app/assets/poster_data/Test/nips-2011-001/nips-2011-001.pdf/nips-2011-001.pptx" ./nips-2011-001.pptx
docker stop paper2poster_run && docker rm paper2poster_run
```

### CLI Flags
| Flag | Description |
|------|-------------|
| `--poster_path` | Path to input paper PDF |
| `--model_name_t` | LLM model name (e.g., `4o`, `vllm_qwen`) |
| `--model_name_v` | VLM model name (e.g., `4o`, `vllm_qwen_vl`) |
| `--poster_width_inches` | Poster width in inches (default: 48) |
| `--poster_height_inches` | Poster height in inches (default: 36) |
| `--max_workers` | Parallel section generation workers |
| `--no_blank_detection` | Disable blank detection (use when overflow is severe) |
| `--conference_venue` | Conference name for auto logo search (e.g., "NeurIPS") |
| `--institution_logo_path` | Custom institution logo path |
| `--conference_logo_path` | Custom conference logo path |
| `--use_google_search` | Use Google Custom Search for logos (requires API keys) |
| `--estimate_chars` | Estimate character counts |
| `--ablation_no_tree_layout` | Ablation: disable tree layout |
| `--ablation_no_commenter` | Ablation: disable commenter |
| `--ablation_no_example` | Ablation: disable example |

### Download Evaluation Dataset
```bash
docker run --rm -v "$(pwd)/data:/app/Paper2Poster-data" paper2poster \
  python -m PosterAgent.create_dataset
```

### Evaluate with PaperQuiz
```bash
docker run --rm \
  -e OPENAI_API_KEY=<your_key> \
  -v "$(pwd)/data:/app/Paper2Poster-data" \
  paper2poster \
  python -m Paper2Poster-eval.eval_poster_pipeline \
    --paper_name="<paper_name>" \
    --poster_method="4o_4o_generated_posters" \
    --metric=qa
```

### Evaluate with VLM-as-Judge
```bash
docker run --rm \
  -e OPENAI_API_KEY=<your_key> \
  -v "$(pwd)/data:/app/Paper2Poster-data" \
  paper2poster \
  python -m Paper2Poster-eval.eval_poster_pipeline \
    --paper_name="<paper_name>" \
    --poster_method="4o_4o_generated_posters" \
    --metric=judge
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for GPT-4o |
| GOOGLE_SEARCH_API_KEY | No | None | Google Custom Search API key (for logo search) |
| GOOGLE_SEARCH_ENGINE_ID | No | None | Google Custom Search Engine ID |

## Gradio Demo
The repo includes a Gradio demo at `demo/app.py` for the HuggingFace Spaces deployment. The `gradio` package is not included in the Docker image requirements. The demo is designed for the hosted HuggingFace Space.

## Test Results
| Test | Result |
|------|--------|
| `docker build` | PASS |
| `python -m PosterAgent.new_pipeline --help` | PASS |
| `import PosterAgent` | PASS |
| `libreoffice --version` | PASS (24.2.7.2) |
| `pdftoppm -v` | PASS (24.02.0) |
| Full pipeline (paper to poster) | PASS (nips-2011-001, gpt-4o, 569s, output: poster.png + .pptx) |
| Evaluation pipeline | NOT TESTED (requires OPENAI_API_KEY) |
| Gradio demo | NOT TESTED (gradio not in requirements.txt) |

## Notes
- Image is large (~6GB) due to 576 pip packages including PyTorch, vLLM, LibreOffice, and Java.
- The repo vendors its own `docling/` directory that shadows the pip-installed docling package. Requires `docling_parse==4.0.0` for API compatibility.
- Full pipeline requires an OpenAI API key and a paper PDF. Without these, only infrastructure tests can be run.
- Output path uses angle brackets (e.g. `<4o_4o>_generated_posters/`), which are illegal on Windows. Use `docker cp` from a non-`--rm` container instead of volume mounts.
- On Git Bash for Windows, set `MSYS_NO_PATHCONV=1` before `docker run` to prevent `/app` paths being mangled to `C:/Program Files/Git/app`.
- With a 30k TPM OpenAI tier, use `--max_workers=1` to avoid rate limit errors during content generation.
- Supports local models via vLLM (e.g., Qwen-2.5-7B-Instruct) as alternative to OpenAI API.
- YAML style customization available via `config/poster.yaml` or per-poster `poster.yaml` next to `paper.pdf`.
