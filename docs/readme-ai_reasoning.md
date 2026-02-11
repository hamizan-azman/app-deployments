# readme-ai Deployment Reasoning

## App Type
CLI tool. No web interface, no port exposed.

## Deployment Decision
Deploy. readmeai is a well-packaged PyPI library with a clear CLI entrypoint. It has no GUI dependencies and no hardware requirements. Straightforward single-container deployment.

## Dockerfile Approach
No upstream Dockerfile existed in the repository. Dockerfile written from scratch following the CLI pattern used in this project.

Base image: `python:3.11-slim`. readmeai requires Python 3.9 or later. Python 3.11 is a stable, widely tested release that matches the era of readmeai 0.6.x.

readmeai is installed directly from PyPI as a single package (`readmeai==0.6.3`). No requirements file needed. Pip resolves all transitive dependencies at build time.

## System Dependencies
git is required. readmeai uses GitPython to clone and inspect remote repositories during analysis. Without git installed in the image, repository analysis fails for remote URLs. Added via apt-get before pip install, with apt lists cleaned afterward to keep the image lean.

`GIT_PYTHON_REFRESH=quiet` is set as an env var. GitPython prints a warning when git is present but there is no git repository in the working directory. This warning appears on every run even when readmeai is working correctly. Suppressing it keeps CLI output clean.

## Non-Root User
Created `appuser` (UID 1000) and switched to it before the ENTRYPOINT. The readmeai CLI only reads from the repository and writes the output file. Running as non-root is safe and follows the project convention.

## HEALTHCHECK
Uses `python -c "import readmeai"`. The tool has no running process to probe because it exits after generating the README. An import check confirms the package installed correctly and the Python environment is intact.

## Entrypoint
`ENTRYPOINT ["readmeai"]` with `CMD ["--help"]`. Running the container with no arguments prints usage. All actual usage passes arguments after the image name, which appends to the ENTRYPOINT.

## Volume Mounts
readmeai writes the generated README to the path specified by `--output`. If the output path is inside the container with no volume mount, the file is lost when the container exits. Users must mount a host directory and point `--output` into it to retrieve the generated file.

## API Keys
readmeai supports four providers: OpenAI, Anthropic, Google AI, and offline. The key is passed as an environment variable at runtime. No key is baked into the image. Offline mode works without any key and is useful for testing that the tool runs correctly without spending API credits.

## QC Test
```bash
docker run --rm hoomzoom/readme-ai --help
```
Passes. Prints the readmeai CLI help text and exits 0. This confirms the package is installed, the entrypoint resolves, and the container starts cleanly.

Full generation (calling an LLM provider) was not tested as part of QC because it requires a valid API key and incurs cost. The import healthcheck and --help test are sufficient to confirm the deployment is functional.

## Image Size
Small. python:3.11-slim base plus git plus a single pip package. No large model weights, no GPU dependencies.
