# bilingual_book_maker -- Reasoning Log

Covers every decision made for the bilingual_book_maker deployment, including alternatives considered and why they were rejected.

## 0) Quick Assessment Of Rawdog Log
Rawdog log is already complete and does not need changes.

## 1) Clarify The Product Type
What I checked
- `README.md` for usage patterns and outputs.
- `book_maker/cli.py` to confirm real CLI args.

What I saw
- The project is a file-processing CLI that reads a book file and writes output files.
- Many flags and multiple providers.

Decision
- Treat as a CLI tool, not a server.

Why it matters
- No HTTP endpoints or ports.
- Tests are CLI commands, not curl.

## 2) Locate The True Contract For Flags
What I checked
- `book_maker/cli.py` to see authoritative flags, defaults, and constraints.

What I saw
- Flags such as `--test`, `--test_num`, `--translate-tags`, `--block_size`.
- Hidden constraints: `--block_size` requires `--single_translate`.
- API key selection logic differs by provider.

Decision
- Document flags based on `cli.py`, not just README.

Why
- README can lag behind code. CLI file is ground truth.

## 3) Review The Existing Dockerfile
What I checked
- `Dockerfile` in repo.

What I saw
- Minimal Dockerfile using `python:3.10-slim`.
- No pinning, no extra system packages, no PyMuPDF.

Decision
- Update Dockerfile to be more deterministic and to fix runtime dependency gaps.

Why
- The project workflow requires pinned base image and a working container.

## 4) Fix Runtime Dependency Gaps
What I checked
- `book_maker/loader/pdf_loader.py` imports `fitz`.
- `requirements.txt` did not include PyMuPDF.

Decision
- Add `PyMuPDF` to Dockerfile install step.

Why
- Without it, `--help` failed because import happens at module load.

Alternative
- Add PyMuPDF to `requirements.txt`. Rejected to avoid modifying upstream dependency list.

## 5) Dockerfile Design Decisions
Base image
- `python:3.10.14-slim` pinned.
- Why: Python 3.10 is supported, pinning avoids drift.

System packages
- Installed `git`.
- Why: safe for repos that use LFS or git metadata and consistent with other builds.

Install strategy
- Install from `requirements.txt`, then `PyMuPDF==1.24.2`.
- Why: ensures PDF loader works.

Entrypoint
- Keep `python3 make_book.py` as default.
- Why: aligns with README usage.

## 6) Build Verification
Decision
- Build image to ensure dependencies resolve in container.

Why
- Required by the project workflow (Step 3: build and verify).

## 7) Testing Strategy
Goal
- Verify core CLI paths with minimal cost and time.

Core rules
- Use `--test --test_num 1` to avoid full book translation.
- Run commands that exercise different code paths.

Test matrix I selected
- `--help` for basic CLI.
- Base translation with OpenAI key.
- `--single_translate`.
- `--translate-tags`.
- `--prompt` with txt and json template.
- `--parallel-workers`.
- `--use_context` and `--context_paragraph_limit`.
- `--batch_size` and `--block_size` on TXT.
- `--model openai --model_list ...`.
- `--resume` and interrupted run.
- `--exclude_filelist` and `--only_filelist`.
- `--allow_navigable_strings`.
- `--temperature --accumulated_num --translation_style`.
- `--retranslate`.

Why this mix
- It covers input control, output control, prompt control, parallelism, and resume.
- It avoids non-OpenAI providers because you requested OpenAI only.

## 8) Handling The `--retranslate` Failure
What I checked
- Whether `index_split_002.html` exists inside the EPUB.

What I saw
- The bilingual EPUB had only `index_split_000.html`.

Decision
- Retest retranslate using `index_split_000.html`.

Outcome
- It failed with `ValueError: Element has no parent, so 'after' has no meaning.`

Conclusion
- Mark `--retranslate` as failed and note the error in usage doc.

## 9) Handling Interrupted Tests
What happened
- `--temperature --accumulated_num --translation_style` run was interrupted.

Decision
- Mark it as pass per your request, but note that it was interrupted in logs.

Why
- You explicitly asked to count it as pass.

## 10) Usage Documentation Decisions
Base URL
- Set to `N/A` because this is CLI.

Command list
- Converted all flags into CLI “endpoints”.

Tested markers
- Updated each section based on real execution results.
- Marked non-OpenAI providers as untested.

Notes
- Added PyMuPDF note.
- Added retranslate failure note and error message.

## 11) What I Did NOT Do (And Why)
- Did not test non-OpenAI providers because you requested OpenAI only.
- Did not modify upstream requirements file to add PyMuPDF.
- Did not test Streamlit or UI because none exists.

## Final Outputs
- Updated Dockerfile for deterministic builds and PDF support.
- Created and updated usage doc with real test status.
- Ran an extensive OpenAI-only test suite and logged failures.
