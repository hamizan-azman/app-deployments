# readme-ai Usage Documentation

## Overview
CLI tool that automatically generates README files for software projects using LLMs. Supports OpenAI, Anthropic, and Google AI as backend providers. Also supports offline mode using local templates without an API key.

## Quick Start
```bash
docker pull hoomzoom/readme-ai
docker run --rm -e OPENAI_API_KEY=your_key hoomzoom/readme-ai \
    --repository https://github.com/user/repo \
    --output /tmp/README.md
```

## Usage

### Generate README from a remote repository
```bash
docker run --rm \
    -e OPENAI_API_KEY=your_key \
    -v $(pwd)/output:/output \
    hoomzoom/readme-ai \
    --repository https://github.com/user/repo \
    --output /output/README.md
```

### Generate README from a local directory
```bash
docker run --rm \
    -e OPENAI_API_KEY=your_key \
    -v /path/to/project:/project \
    -v $(pwd)/output:/output \
    hoomzoom/readme-ai \
    --repository /project \
    --output /output/README.md
```

### Offline mode (no API key required)
```bash
docker run --rm \
    -v $(pwd)/output:/output \
    hoomzoom/readme-ai \
    --repository https://github.com/user/repo \
    --api offline \
    --output /output/README.md
```

### View help
```bash
docker run --rm hoomzoom/readme-ai --help
```

## CLI Options (Common)
| Flag | Description |
|------|-------------|
| `--repository` | URL or local path of the repository to document |
| `--output` | Output file path for the generated README |
| `--api` | LLM provider: `openai`, `anthropic`, `google`, `offline` |
| `--model` | Model name to use (e.g. `gpt-4o`, `claude-3-5-sonnet-20241022`) |
| `--badge-style` | Badge style for shields.io badges |
| `--image` | Header image style |

Run `--help` for the full option list.

## Health Check
- **Method:** `python -c "import readmeai"`
- **Tested:** Yes (import succeeds)

## QC Test
```bash
docker run --rm hoomzoom/readme-ai --help
```
Output: Prints readmeai CLI usage and exits 0.

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | No | None | OpenAI API key |
| ANTHROPIC_API_KEY | No | None | Anthropic API key |
| GOOGLE_API_KEY | No | None | Google AI API key |

At least one API key is required unless `--api offline` is used.

## Notes
- No port exposed. This is a CLI-only tool.
- Output files must be written to a mounted volume to be accessible on the host.
- The image includes git, required for cloning remote repositories during analysis.
- The container runs as non-root user `appuser` (UID 1000).
- readmeai version: 0.6.3

## Changes from Original
- No upstream Dockerfile exists. Dockerfile written from scratch for this project.
- Installed readmeai 0.6.3 directly from PyPI.
- Added non-root user, HEALTHCHECK, and explicit ENTRYPOINT.
- Set `GIT_PYTHON_REFRESH=quiet` to suppress GitPython warnings when git metadata is absent.

## V2 Dependency Changes (Minimum Version Pinning)
Installed as a single pinned PyPI package (`readmeai==0.6.3`). No requirements file to pin. Transitive dependencies resolved by pip at install time.
