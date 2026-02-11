# BabelDOC Deployment Reasoning

## App Type
CLI tool. No web server, no port. Invoked directly via the `babeldoc` command.

## Deployment Decision
Deploy. BabelDOC has a clean Python package structure with a `pyproject.toml` and a registered console script entry point. It runs headlessly with no GUI dependencies, making it straightforward to containerise.

## Base Image
`python:3.12-slim`. BabelDOC targets Python 3.12 and has no Playwright or other dependencies that conflict with the slim variant of Debian. No reason to use the heavier bookworm image.

## System Dependencies
Three libraries are required before pip install:

- `libglib2.0-0`: GLib runtime, pulled in by OpenCV.
- `libgl1`: OpenGL library stub, also required by OpenCV for headless operation.
- `libgomp1`: GNU OpenMP runtime, required by ONNX Runtime for multi-threaded inference.

Without these, OpenCV and ONNX imports fail at runtime with missing shared library errors. They are installed via apt before pip to ensure the build succeeds cleanly.

## Install Method
`pip install --no-cache-dir .` from the repository root. BabelDOC uses a `pyproject.toml` with a `[project.scripts]` entry that registers `babeldoc` as a console script. This is the correct install path as documented upstream. No `requirements.txt` is used.

## Dependency Pinning
Not applied. BabelDOC is installed directly from source using `pip install .`. There is no standalone requirements file to pin. Pip resolves and installs all transitive dependencies at build time. The resulting image is reproducible via the Docker image digest rather than through a pinned manifest.

## Entry Point and Healthcheck
`ENTRYPOINT ["babeldoc"]` maps directly to the installed console script. The healthcheck runs `babeldoc --help`, which exercises the full import chain and confirms the binary is functional. This is the standard QC approach for CLI tools in this project.

## Non-Root User
`appuser` created at UID 1000. The container drops to this user before the entrypoint. No write access to system paths is needed at runtime.

## API Key Handling
BabelDOC accepts the API key via `--openai-api-key` CLI flag at runtime. It does not read from environment variables. This means no API key needs to be baked into the image or passed via `-e`. Users supply the key when invoking the container. This is the upstream-intended interface and consistent with the architectural fidelity rule.

## No Port
CLI tool. No `EXPOSE` directive is needed. No HTTP server is started.

## Volume Mount
Input and output PDFs must be passed via a mounted volume. The typical pattern is `-v /host/path:/data` with `--input /data/file.pdf --output /data/out.pdf`. This is standard Docker practice for CLI tools that process files.

## QC Result
`babeldoc --help` passes. Exit code 0. Usage text printed. Translation functionality is NOT TESTED as it requires a live API key and an input PDF.

## Architectural Fidelity
No changes to application logic. The Dockerfile installs the app exactly as the upstream project intends, using the same install command a developer would run locally. The only additions are the system library prerequisites and Docker housekeeping (non-root user, healthcheck).
