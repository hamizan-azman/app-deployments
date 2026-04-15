# Aider. Reasoning Log

## App Classification
CLI tool. No web server by default. Runs interactively in the terminal against a mounted code repository. Optional `--browser` flag launches a Streamlit-based UI on port 8501, but this is not the primary interface.

## Why PyPI Install Instead of Source

The upstream aider repo uses setuptools-scm to derive its version from git tags. When the repo is cloned as a git submodule (as in this project), it has no tags. setuptools-scm fails with a version detection error and the build aborts.
This was annoying to debug. The error message just said "tag not found" which was misleading since the real issue was the submodule .git reference not having full history.

The official aider documentation lists `pip install aider-chat` as the standard install method. The PyPI package is identical to a source install at runtime. There is no loss of functionality. This is not a workaround, it is the documented install path.

## Base Image Choice

`python:3.12-slim-bookworm` is used instead of `python:3.12-slim`. The default `slim` tag tracks Debian trixie (unstable), which has caused system dependency breakage on other apps in this project. Pinning to bookworm gives a stable, well-understood base.

Python 3.12 was chosen because aider-chat supports it and it is the most recent stable Python version with broad library compatibility in 2025.

## Virtual Environment

A virtual environment at `/venv` is created before installing aider. This keeps the install isolated from the system Python and avoids any potential conflict with system packages. The `PATH` is prepended with `/venv/bin` so all subsequent commands use the venv by default.

## Git Configuration

`git config --system safe.directory /app` is set during the build. Without this, git refuses to operate on a directory owned by a different UID (the host user vs the container's `appuser`). This is a common issue when mounting host directories into Docker containers that run as non-root users.

## Non-Root User

The container runs as `appuser` (UID 1000). This is the standard hardening practice for this project. The `/app`, `/venv`, and `/home/appuser` directories are all chowned to `appuser` before the USER directive.

## HOME Directory

`ENV HOME=/app` is set so aider writes its `.aider` cache directory into the mounted project volume rather than into the container filesystem. This means cache data persists across container runs as long as the same directory is mounted. It also avoids permission issues with writing to `/home/appuser` after ownership is set.

## Volume Mount Requirement

Aider requires a git repository to function. The container has no code of its own to edit. The `-v $(pwd):/app` mount is mandatory. This is documented in the usage doc. The Dockerfile design reflects this: `/app` is the working directory and the entrypoint launches aider directly, expecting files to already be present.

## Healthcheck

The healthcheck runs `aider --help`. This is the correct approach for a CLI tool with no HTTP endpoint. It validates that the binary is present, the venv is intact, and all imports succeed. The `--help` flag exits 0 on a working install.

## System Dependencies

Four system packages are installed.

- `build-essential`: Required for compiling certain Python packages with C extensions during `pip install aider-chat`.
- `git`: Required by aider at runtime to stage and commit changes to the mounted repository.
- `libportaudio2`: Required by the `sounddevice` package, which is a transitive dependency of aider for voice input features.
- `pandoc`: Required by aider for document conversion features.

Without git, aider will not start. Without libportaudio2, the import of sounddevice fails at startup. The other deps are needed for optional features but are declared as hard dependencies in the aider-chat package.

## Port Strategy

No EXPOSE directive is added to the Dockerfile because the default mode is a pure CLI with no listening socket. Users who want browser mode can pass `-p 8501:8501` manually. Exposing port 8501 unconditionally would misrepresent the app's primary interface.

## QC Test Result

`docker run --rm hoomzoom/aider --help` exits 0 and prints the aider help text. This confirms the install is complete and the entrypoint works. API-dependent features (actual code editing with an LLM) are NOT TESTED in this deployment.

## What Was Not Done

No attempt was made to pin `aider-chat` to a specific version. The package has a large and tightly coupled dependency tree. The PyPI resolver handles this correctly when installing the latest release. Pinning would require resolving hundreds of transitive dependencies across a complex dependency graph, which is outside the scope of this deployment and would provide little research value.
