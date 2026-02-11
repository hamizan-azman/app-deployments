# Paper2Poster. Deployment Reasoning Log

## What is Paper2Poster?

Paper2Poster is a multi-agent system from NeurIPS 2025 that automatically converts academic papers (PDFs) into professional conference posters (PPTX/PNG). The pipeline works in stages: parse the paper into structured content, plan a poster layout using a binary-tree algorithm, generate text content for each panel via LLM, render panels as PowerPoint slides with an iterative overflow-correction loop, and composite the final poster with logos.

For supply chain security research, this tool is interesting because:
- It uses multiple LLM providers (OpenAI, Anthropic, Mistral, Cohere) via a bundled `camel/` framework
- It vendors its own copy of the `docling` library, creating a shadow dependency
- It has 576 pip dependencies, creating a massive attack surface
- The LLM generates PowerPoint code that is executed to create slides (code execution from LLM output)

---

## Step 1: What I Checked and Why

### README.md
Comprehensive documentation covering the pipeline architecture, CLI usage, and evaluation metrics. Told me:
- The tool is CLI-based (no web server in normal mode)
- It requires an OpenAI API key for GPT-4o
- It has a Gradio demo designed for HuggingFace Spaces
- The main entry point is `python -m PosterAgent.new_pipeline`

### Existing Dockerfile
The repo had a Dockerfile. I read it to check:
- Base image: `nvidia/cuda:12.6.0-devel-ubuntu24.04` (GPU-focused, CUDA development image)
- Dependencies: installs system packages + 576 pip packages
- Entry point structure

### requirements.txt
576 packages. This is enormous. Key observations:
- Includes GPU libraries: `torch`, `vllm`, `transformers` (for local model support)
- Includes a forked `python-pptx` from GitHub (custom PowerPoint modifications)
- Includes `docling_core`, `docling_parse`, `docling_ibm_models` (PDF parsing)
- Includes multiple LLM SDKs: `openai`, `anthropic`, `mistralai`, `cohere`
- Every line in requirements.txt matters because changing any one line invalidates Docker's build cache for the entire pip install layer (~10 minute rebuild)

### docling/ vendored directory
This is a copy of the `docling` Python library checked into the repo. This is the critical insight that caused the most debugging:

**The problem:** pip installs `docling` from PyPI (the official published version). But the repo also has a `docling/` directory in its root. Python's import system finds local directories first. So when the code does `import docling`, it gets the vendored copy, not the pip-installed one.

**Why this matters:** The vendored copy is older. It expects `docling_parse` to have a `pdf_parser_v2` API. But newer versions of `docling_parse` renamed this. So we need to pin `docling_parse==4.0.0` which is the last version that has the old API the vendored code expects.

**How I discovered this:** The build succeeded but the pipeline crashed at runtime with an `AttributeError` about a missing `pdf_parser_v2` attribute. I traced the import chain and found the vendored `docling/` was being loaded instead of the pip package. Then I checked which version of `docling_parse` the vendored code expected.

### PosterAgent/new_pipeline.py
The main pipeline script. I read this to understand:
- What CLI arguments it accepts
- What the output path pattern is (turned out to be `<{model_t}_{model_v}>_generated_posters/`)
- How it calls the LLM (through the bundled `camel/` framework)
- What files it generates (PPTX, PNG, log.json)

### PosterAgent/gen_poster_content.py
The content generation module. I checked this for the `max_workers` parameter, which controls how many poster sections are generated in parallel. This was critical for the rate limit issue.

### config/ directory
YAML configuration files for poster styling (fonts, colors, sizes). The tool uses these to customize the poster appearance. Not critical for deployment but good to know about.

---

## Step 2: Dockerfile Decisions

### Decision: Change base image from CUDA to plain Ubuntu

**Original:** `nvidia/cuda:12.6.0-devel-ubuntu24.04`
**Changed to:** `ubuntu:24.04`

**Why:** We are deploying on a machine without an NVIDIA GPU. The CUDA base image adds ~4GB to the image for GPU libraries we cannot use. The `devel` variant is even larger because it includes CUDA compilers.

**Why this is safe:** The tool supports both GPU (via vLLM for local models) and CPU (via OpenAI API). Since we are using the OpenAI API, no GPU is needed. PyTorch will install CPU-only automatically when CUDA is not available.

**Alternative considered: Keep the CUDA image.** Rejected because it triples the image size for no benefit. We cannot use GPU features without an NVIDIA GPU and the nvidia-docker runtime.

**Alternative considered: Use `python:3.12-slim`.** Rejected because Ubuntu gives us `apt-get` access to system packages (LibreOffice, Java, poppler) that the tool needs for PDF/PPTX processing. While a Python slim image would work, we would need to add these system packages anyway, and Ubuntu 24.04's default Python 3.12 is compatible.

**Supply chain note:** Switching from `nvidia/cuda` to `ubuntu:24.04` changes the supply chain. The CUDA image is published by NVIDIA and is built on Ubuntu. By using `ubuntu:24.04` directly, we remove NVIDIA from the trust chain. For supply chain security research, this is worth documenting: same OS, different publisher.

### Decision: Add PIP_BUILD_CONSTRAINT for setuptools

```dockerfile
RUN echo "setuptools<71" > /tmp/build-constraints.txt
ENV PIP_BUILD_CONSTRAINT=/tmp/build-constraints.txt
```

**Why:** Several packages in the 576-package requirements.txt use `pkg_resources` in their `setup.py` files. `pkg_resources` was part of `setuptools` but was removed in version 71. When pip builds these packages in an isolated environment, it downloads the latest setuptools (which is 71+), and the build fails because `import pkg_resources` no longer works.

**How this fix works:** `PIP_BUILD_CONSTRAINT` tells pip to constrain packages in build isolation environments. By setting `setuptools<71`, pip will use setuptools 70.x when building packages, which still has `pkg_resources`. This only affects build isolation, not the final installed setuptools version.

**Alternative considered: Pin setuptools globally.** Rejected because some packages might need newer setuptools features. The constraint file approach is more surgical: it only affects the build environment.

**How I discovered this:** The pip install step failed with `ModuleNotFoundError: No module named 'pkg_resources'` during the build of one of the 576 packages. I traced it to setuptools 71 removing the module.

### Decision: Pin docling_parse==4.0.0

**Why:** The repo vendors an older version of the `docling` library in its `docling/` directory. This vendored copy calls `docling_parse`'s `pdf_parser_v2` API. In `docling_parse` versions after 4.0.0, this API was renamed or removed. Pinning to 4.0.0 ensures the vendored code works.

**How this relates to the repo's behavior:** When Python encounters `import docling`, it checks the local directory first. Since `docling/` exists in the repo root (which is `/app` in the container), Python loads the vendored version, not the pip-installed one. The vendored version is written against an older `docling_parse` API. So even though pip installs the latest `docling_parse`, the code that actually runs is the older vendored code that needs the older API.

**Alternative considered: Delete the vendored docling/ directory.** Rejected because the vendored version contains modifications specific to Paper2Poster (custom PDF parsing logic for academic papers). The authors vendored it intentionally.

**Alternative considered: Install the exact docling version the vendors copy came from.** Rejected because we could not determine which exact version it was cloned from, and the vendored copy has local modifications.

### Decision: Install LibreOffice and Java

**Why:** The pipeline uses LibreOffice to convert PPTX to images (the `soffice` command) and Java is required by some PDF processing libraries. Without LibreOffice, the final poster rendering step fails. Without Java, some of the PDF/table extraction tools fail.

### Decision: Create an entrypoint script that writes .env file

```dockerfile
RUN echo '#!/bin/bash\necho "OPENAI_API_KEY=$OPENAI_API_KEY" > /app/.env\ncd /app\nexport PYTHONPATH=/app:$PYTHONPATH\nexec "$@"' > /entrypoint.sh
```

**Why:** The `camel/` framework (the bundled LLM interaction library) reads API keys from a `.env` file in the working directory. Docker passes environment variables via `-e`, but camel expects a file. The entrypoint script bridges this gap by writing the Docker env var into a `.env` file at startup.

**How `exec "$@"` works:** This replaces the shell process with whatever command was passed to the container. So `docker run paper2poster python -m PosterAgent.new_pipeline` first writes the .env file, then becomes the Python process. This ensures signals (like Ctrl+C) are forwarded correctly to Python.

---

## Step 3: Build and Verification

### Build issues encountered

**Issue 1: setuptools/pkg_resources**
- Symptom: pip install fails with `ModuleNotFoundError: No module named 'pkg_resources'`
- Root cause: setuptools 71+ removed pkg_resources. old packages still import it during build
- Fix: PIP_BUILD_CONSTRAINT with setuptools<71

**Issue 2: docling_parse API mismatch**
- Symptom: Runtime crash with `AttributeError: pdf_parser_v2`
- Root cause: Vendored docling/ expects old docling_parse API
- Fix: Pin docling_parse==4.0.0

**Build time:** ~10-15 minutes due to 576 pip packages. This is the slowest build of all three apps. Any change to requirements.txt invalidates the pip cache layer and triggers a full reinstall.

**Image size:** ~6GB. The largest of the three apps. This is because of:
- PyTorch (~2GB, even CPU-only)
- LibreOffice (~500MB)
- 576 pip packages with their transitive dependencies
- Java runtime (~200MB)

---

## Step 4: Test Selection and What Each Test Validates

### Test 1: docker build. PASS
**What it validates:** All 576 pip packages install without conflicts, system packages (LibreOffice, Java, poppler) install correctly, the setuptools constraint works.
**Why this test matters:** With 576 dependencies, there are thousands of potential version conflicts. A successful build means the entire dependency graph resolved.

### Test 2: python -m PosterAgent.new_pipeline --help. PASS
**What it validates:** The main pipeline module imports successfully, all its dependencies (camel, docling, sklearn, pptx, etc.) load without errors, and the argparse CLI works.
**Why this test matters:** This exercises the import chain through the entire codebase. If the vendored docling or the pinned docling_parse were wrong, this would fail.

### Test 3: import PosterAgent. PASS
**What it validates:** The Python package is importable as a module. Tested with `python -c "import PosterAgent"`.
**Why this test matters:** Quick smoke test that the package structure is correct and PYTHONPATH includes /app.

### Test 4: libreoffice --version. PASS (24.2.7.2)
**What it validates:** LibreOffice is installed and runnable. The version number confirms we have a specific, known version.
**Why this test matters:** LibreOffice is used to convert PPTX to PNG in the final rendering step. Without it, the pipeline completes but cannot produce poster images.

### Test 5: pdftoppm -v. PASS (24.02.0)
**What it validates:** The poppler-utils PDF tools are installed. pdftoppm converts PDF pages to images, used during paper parsing.
**Why this test matters:** Paper parsing requires converting PDF pages to images for OCR and figure extraction. Without poppler, the parser cannot process input papers.

### Test 6: Full pipeline (paper to poster). PASS
**What it validates:** The entire end-to-end pipeline works: PDF parsing with docling, institution detection, logo matching, outline generation via LLM, panel layout optimization, content generation via LLM with overflow correction, style application, PowerPoint rendering, and PNG export.
**Why this test matters:** This is the real test. All infrastructure tests can pass while the actual pipeline fails (wrong API format, missing model weights, incorrect file paths, etc.). Only running the full pipeline proves the tool actually works.

**Test details:**
- Input: Bundled sample paper `nips-2011-001` (Image Parsing via Stochastic Scene Grammar)
- Model: GPT-4o (text and vision)
- Max workers: 1 (to avoid rate limits)
- Time: 569 seconds
- Output: poster.png (2.1MB) + nips-2011-001.pptx (2.3MB) + log.json + detail_log.json

### Tests NOT run and why

**Evaluation pipeline:** Requires downloading additional datasets and running more LLM calls. The infrastructure for evaluation is separate from poster generation. Marked NOT TESTED because we validated the core functionality.

**Gradio demo:** The `gradio` package is not in requirements.txt. The demo is designed for HuggingFace Spaces (a hosted platform) and is not part of the Docker deployment.

---

## Step 5: Full Pipeline Debugging (The Hard Part)

Running the full pipeline required solving three problems in sequence. This section explains each one and how to recognize similar issues.

### Problem 1: MSYS path mangling

**Symptom:** `FileNotFoundError: No such file or directory: 'C:/Program Files/Git/app/assets/poster_data/Test/nips-2011-001/nips-2011-001.pdf'`

**What happened:** On Windows with Git Bash, the MSYS compatibility layer automatically converts paths that look like Unix paths. When Docker sees `--poster_path="/app/assets/..."`, MSYS intercepts it before Docker does and converts `/app` to `C:/Program Files/Git/app` (because MSYS thinks `/app` is a relative path under the Git install directory).

**Fix:** Set `MSYS_NO_PATHCONV=1` before the docker command. This disables MSYS path conversion for that command.

**How to recognize this in the future:** If you see Windows paths inside a Docker container (like `C:/Program Files/...`), it is almost certainly MSYS path mangling. The fix is always `MSYS_NO_PATHCONV=1`.

### Problem 2: OpenAI rate limits (429 errors)

**Symptom:** `openai.RateLimitError: Rate limit reached for gpt-4o ... Limit 30000 TPM`

**What happened:** The pipeline generates content for each poster section in parallel using `max_workers=10` (default). Each section involves multiple LLM calls (generate content, check overflow, modify, re-render, repeat). With 10 workers, the total tokens per minute exceeded the 30,000 TPM limit on the user's OpenAI tier.

**First fix attempt:** `--max_workers=2`. Still failed because even 2 workers can generate enough calls during the overflow correction loop to exceed 30k TPM.

**Alternative tried:** Using `gpt-4o-mini` instead. Failed with a different error: `AttributeError: 'list' object has no attribute 'items'`. The mini model returned a JSON list where the code expected a dict. This is a common issue with smaller models: they follow output format instructions less reliably.

**Final fix:** `--max_workers=1`. Fully serializes all LLM calls. Each section is processed one at a time, so the TPM stays well under 30k.

**How to recognize this in the future:** 429 errors from OpenAI always mean rate limiting. Check three things: (1) your TPM tier at platform.openai.com, (2) the concurrency of your application, (3) the size of each request. Reduce whichever one you can control.

### Problem 3: Angle brackets in output path

**Symptom:** Output directory is empty after pipeline completes, even with a volume mount.

**What happened:** The pipeline writes output to `<4o_4o>_generated_posters/`. The angle brackets `<>` are literal characters in the directory name (generated from the model name template `<{model_t}_{model_v}>_generated_posters`). On Linux (inside Docker), this is a valid directory name. On Windows, `<>` are illegal filename characters.

When we mounted `-v "C:/SMU/app-deployments/paper2poster_output:/app/4o_4o_generated_posters"` (without angle brackets), the mount point did not match the actual output path (with angle brackets). The container wrote to `<4o_4o>_generated_posters/` which was a different directory, not the mounted volume.

**Fix:** Do not use `--rm` flag. Let the container persist after exit, then use `docker cp` to extract files:
```
docker start paper2poster_run
docker cp "paper2poster_run:/app/<4o_4o>_generated_posters/.../poster.png" ./poster.png
```

`docker cp` runs inside Docker's Linux filesystem where angle brackets are valid. It copies the file to Windows where it gets a clean filename.

**How to recognize this in the future:** If a volume mount appears to work (no errors) but the output directory is empty, check for special characters in the container's output path. Use `docker exec` to `ls` the actual output location inside the container and compare it to your mount point.

---

## Key Architectural Observations

### The vendored dependency pattern
Paper2Poster vendors its own copy of `docling` rather than depending on the pip package. This is a deliberate choice by the authors to freeze the parsing behavior. But it creates a maintenance burden: the vendored code and the pip-installed dependencies must stay in sync. If `docling_parse` gets updated and changes its API, the vendored code breaks.

This pattern appears in many ML research repos. Authors copy a library, modify it for their needs, and check it into the repo. The result is a "shadow dependency" that pip does not know about and cannot manage. For supply chain security, this is noteworthy because:
- Vulnerability scanners only check pip-installed packages, not vendored copies
- The vendored code may have known vulnerabilities that are invisible to automated tools
- Updates to the pip package do not update the vendored copy

### The 576-package supply chain
Paper2Poster has the largest dependency tree of the three apps. Every one of those 576 packages is a potential supply chain attack vector. The requirements.txt pins some packages to specific versions and leaves others unpinned. The forked `python-pptx` from a personal GitHub account is particularly notable: it pulls code from `github.com/Force1ess/python-pptx`, which is an individual's fork, not the official package.

### LLM-generated code execution
The pipeline uses LLMs to generate Python code for PowerPoint slide creation. This code is then `exec()`'d to produce the slides. This is a direct code execution from LLM output, which is a significant attack surface. A poisoned model or compromised API response could inject arbitrary code into the poster generation process.
