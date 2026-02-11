# slide-deck-ai. Reasoning Log

Covers every decision made for the slide-deck-ai deployment, including alternatives considered and why they were rejected.

## 1) Clarify The Product Type
What I checked
- `README.md` to understand how the project is used.
- `pyproject.toml` to see if there is a CLI entrypoint.

What I saw
- The project provides a Streamlit UI and a CLI (`slidedeckai`).

Decision
- Build a Docker image that runs Streamlit by default, but also supports CLI commands.

Why it matters
- Users can either run the UI (`streamlit run app.py`) or use the CLI for generation.

## 2) Identify Entrypoints
What I checked
- `pyproject.toml` shows `[project.scripts] slidedeckai = "slidedeckai.cli:main"`.

Decision
- The Docker image must run `pip install .` so the CLI exists in PATH.

Why
- Without installing the package, `slidedeckai` is not found when running `docker run ... slidedeckai`.

## 3) Review Dependencies And Size Risks
What I checked
- `requirements.txt` includes `torch`, `transformers`, `scikit-learn`, etc.

Decision
- Accept that the image will be very large. do not attempt to remove deps.

Why
- Removing dependencies may break functionality or diverge from upstream.
- The project requires working builds, not optimized size.

## 4) Dockerfile Design Decisions
Base image
- `python:3.11.9-slim` pinned.
- Why: project supports Python 3.10+, 3.11 is stable and common.

System packages
- Install `git`.
- Why: repo references Git LFS and templates may need git tooling.

Install strategy
- `pip install -r requirements.txt` then `pip install .`.
- Why: installs dependencies and registers CLI entrypoint.

Default command
- `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`.
- Why: makes container behave like the UI by default.

Port
- `EXPOSE 8501` for Streamlit.

## 5) Handle Git LFS Templates
What I checked
- `src/slidedeckai/pptx_templates` contained very small `.pptx` files.

Decision
- Add a note in usage doc about `git lfs pull`.

Why
- Without LFS, templates are pointers and PPTX generation fails.

## 6) Build Verification
Decision
- Build the Docker image to verify dependencies resolve.

Observation
- Build is extremely heavy due to GPU torch wheels (~GBs).

Conclusion
- Build succeeded but image is large. This is expected given deps.

## 7) CLI Test Strategy
Test chosen
- `slidedeckai --list-models`.

Why
- Works without API keys and validates CLI path.

First attempt result
- Failed because CLI was not installed in PATH.

Fix
- Added `pip install .` to Dockerfile.
- Rebuilt.

Second attempt result
- CLI worked, but downloaded a Hugging Face model and printed warnings.

Notes
- Warning about missing `PEXEL_API_KEY` is expected.
- HF model loading is expected at first run.

## 8) Usage Documentation Decisions
Base URL
- Set to `http://localhost:8501`.

Endpoints
- UI launch via Streamlit.
- CLI list models.
- CLI generate.

Tested status
- `--list-models` marked as tested.
- UI and generation marked untested (require API keys / browser).

Environment variables
- Added all provider keys based on `global_config.py`.
- Added `PEXEL_API_KEY` and `RUN_IN_OFFLINE_MODE`.

## 9) What I Did NOT Do (And Why)
- Did not test `slidedeckai generate` because no API key was provided.
- Did not launch Streamlit UI in browser.
- Did not attempt to slim the image, to avoid breaking upstream dependencies.

## Final Outputs
- Dockerfile created and updated to install CLI.
- Usage doc created.
- CLI list models tested successfully.
