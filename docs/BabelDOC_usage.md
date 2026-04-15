# BabelDOC. Usage Documentation

## Overview
Command-line PDF document translator powered by an OpenAI-compatible API. Translates academic papers and documents while preserving layout, formatting, and structure. Outputs bilingual or translated-only PDFs.

## Quick Start
```bash
docker pull hoomzoom/babeldoc
docker run --rm hoomzoom/babeldoc --help
```

## Running a Translation
BabelDOC is a CLI tool. Pass the input file and translation options at runtime.

```bash
docker run --rm \
  -v /path/to/your/pdfs:/data \
  hoomzoom/babeldoc \
  --openai-api-key YOUR_API_KEY \
  --input /data/paper.pdf \
  --output /data/paper_translated.pdf \
  --target-lang zh
```

On Windows with Git Bash, prefix docker run with `MSYS_NO_PATHCONV=1` to prevent path mangling.

## Entry Point
`babeldoc` (installed as a console script via pip)

## No Exposed Port
BabelDOC is a CLI-only tool. No HTTP server, no port, no web interface.

## Common Flags
| Flag | Description |
|------|-------------|
| `--openai-api-key KEY` | API key for the OpenAI-compatible backend |
| `--openai-base-url URL` | Base URL for an OpenAI-compatible endpoint (optional) |
| `--input FILE` | Path to the input PDF |
| `--output FILE` | Path for the translated output PDF |
| `--target-lang LANG` | Target language code (e.g. zh, ja, fr, de) |
| `--help` | Print usage and exit |

Run `babeldoc --help` for the full list of flags.

## Health Check
The container healthcheck runs `babeldoc --help`. If the binary is missing or broken, the check fails.

To verify manually:
```bash
docker run --rm hoomzoom/babeldoc --help
```
Expected: usage text printed, exit code 0.

## Environment Variables
BabelDOC does not read API keys from environment variables. Pass the key via `--openai-api-key` at runtime.

| Variable | Required | Description |
|----------|----------|-------------|
| None | N/A | No environment variables required |

## API Key Note
An OpenAI-compatible API key is required for actual translation. Without it, `--help` and other informational commands work but translation jobs will fail. The key is passed as a CLI flag, not an environment variable.

## Notes
- The container runs as non-root user `appuser` (UID 1000).
- No persistent storage required. Mount a local directory with `-v` to pass input files and receive output.
- BabelDOC is installed from source via `pip install .` using the upstream `pyproject.toml`.
- System libraries `libglib2.0-0`, `libgl1`, and `libgomp1` are installed for OpenCV and ONNX runtime support.

## V2 Dependency Changes (Minimum Version Pinning)
BabelDOC is installed via `pip install .` from `pyproject.toml`. Dependencies are resolved at build time by pip. No manual requirements file is used, so explicit version pinning is not applied. The build pins transitively through pip's resolver at the versions available at build time.
