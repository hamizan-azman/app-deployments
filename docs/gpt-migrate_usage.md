# gpt-migrate -- Usage Documentation

## Overview
CLI tool that uses LLMs to migrate codebases between languages/frameworks. Generates Dockerfiles, migrates code, creates and runs tests automatically. Requires Docker socket access since it builds and runs Docker containers internally.

## Quick Start
```bash
docker pull hoomzoom/gpt-migrate:latest
```

## Docker Run
```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/your/source:/source \
  -e OPENAI_API_KEY=your-key \
  hoomzoom/gpt-migrate:latest \
  --model gpt-4 \
  --sourcelang python \
  --targetlang nodejs \
  --sourcedir /source \
  --targetdir /tmp/target \
  --sourceentry app.py
```

## CLI Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--model` | TEXT | openrouter/openai/gpt-4-32k | LLM model name |
| `--temperature` | FLOAT | 0 | AI temperature |
| `--sourcedir` | TEXT | ../benchmarks/flask-nodejs/source | Source code directory |
| `--sourcelang` | TEXT | (auto-detect) | Source language |
| `--sourceentry` | TEXT | app.py | Entrypoint file |
| `--targetdir` | TEXT | ../benchmarks/flask-nodejs/target | Output directory |
| `--targetlang` | TEXT | nodejs | Target language |
| `--operating-system` | TEXT | linux | OS for generated Dockerfile |
| `--testfiles` | TEXT | app.py | Comma-separated test files |
| `--sourceport` | INT | None | Source app port (for validation) |
| `--targetport` | INT | 8080 | Target app port |
| `--guidelines` | TEXT | "" | Custom migration guidelines |
| `--step` | TEXT | all | Step to run: setup, migrate, test, all |

## Bundled Benchmark
The container includes a flask-nodejs benchmark at `/app/benchmarks/flask-nodejs/source`. Test with:
```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e OPENAI_API_KEY=your-key \
  hoomzoom/gpt-migrate:latest \
  --model gpt-4 \
  --sourcelang python \
  --targetlang nodejs
```

## Steps
1. **setup**: Creates a Dockerfile for the target framework
2. **migrate**: Recursively migrates source files, resolves dependencies
3. **test**: Builds Docker image, creates test files, validates against source, runs tests
4. **all**: Runs all steps sequentially

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key |
| OPENROUTER_API_KEY | No | None | OpenRouter API key (for default model) |

## Model Compatibility
Uses litellm 0.1.213 (mid-2023). Recognized model names:
- `gpt-3.5-turbo` (4096 max tokens -- too small, will fail)
- `gpt-4` (8192 max tokens -- may fail on large prompts)
- `gpt-4-32k` (32768 max tokens -- recommended)
- `openrouter/*` prefix for OpenRouter models (requires OPENROUTER_API_KEY)

Note: Newer model names (gpt-4o, gpt-4-turbo, gpt-4o-mini) are NOT recognized by this version of litellm.

## Test Results
| # | Test | Result |
|---|------|--------|
| 1 | Container build | PASS |
| 2 | CLI help/options | PASS |
| 3 | Source directory parsing | PASS |
| 4 | Docker socket access | PASS |
| 5 | OpenAI API connectivity | PASS |
| 6 | Full migration run | NOT TESTED (requires gpt-4-32k access) |

## Notes
- Interactive CLI: requires `-it` flag for Docker run
- Docker-in-Docker: requires `-v /var/run/docker.sock:/var/run/docker.sock`
- The tool generates Dockerfiles, builds images, and runs containers internally
- Hardcoded `max_tokens=10000` means only models with >10k output token support work
- The default model `openrouter/openai/gpt-4-32k` requires an OpenRouter API key
- **Security: executes arbitrary code.** gpt-migrate generates and runs code as part of migration. Do not run with access to sensitive data or networks. High-value target for code injection research.

## Changes from Original
**Category: Dependencies only.** Source code untouched.

- 6 era-matched pins added: openai==0.27.8, langchain==0.0.238, typer==0.9.0, click==8.1.7, yaspin==2.5.0, tree-sitter==0.20.4. All fall within the developer's `pyproject.toml` version ranges. Without these, the app crashes on import.

## V2 Dependency Changes (Minimum Version Pinning)
Minimum version pinning applied (all `>=`/`~=`/`^` changed to `==`). No dependency bumps were needed — all minimum versions resolved successfully.
