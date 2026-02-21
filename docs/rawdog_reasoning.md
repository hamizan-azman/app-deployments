# Rawdog. Reasoning Log

Covers every decision made for the Rawdog deployment, including alternatives considered and why they were rejected.

## 1) Clarify The Product Type
**What I checked**
- `README.md` to see how users run the project.

**What I saw**
- Usage examples: `rawdog "prompt"` and interactive prompt mode.

**Decision**
- This is a **CLI tool**, not a web server.

**Why this matters**
- No HTTP endpoints, so “endpoints” become CLI commands.
- No port exposure needed in Docker.

**Alternatives I considered**
- Treat as web app (would be incorrect because no server is described).

## 2) Identify The True Entry Point
**What I checked**
- `pyproject.toml` for `[project.scripts]`.
- `src/rawdog/__main__.py` for CLI behavior.

**What I saw**
- `rawdog = "rawdog.__main__:main"`

**Decision**
- The Docker image must run `pip install .` so `rawdog` exists in PATH.

**Why**
- Matches how the package is meant to be used.
- Avoids having to use `python -m rawdog`.

**Alternative**
- Use `python -m rawdog` without installing. Rejected because it diverges from README usage.

## 3) Enumerate CLI Flags For Documentation
**What I checked**
- `src/rawdog/__main__.py`
- `src/rawdog/config.py`

**What I saw**
- Flags: `--leash`, `--retries`, `--dry-run` (deprecated), plus config fields exposed via CLI.

**Decision**
- Include all relevant flags in usage doc.

**Why**
- The project workflow requires extracting all commands/endpoints.

## 4) Dockerfile Design. Base Image
**Decision**
- Use `python:3.11.8-slim`.

**Why**
- Project requires Python >=3.8. Python 3.11 is stable and broadly compatible.
- Slim keeps image smaller.

**Alternatives**
- `python:3.10-slim`: viable but slightly older.
- `python:3.12-slim`: newer, but higher risk of library incompatibilities.

## 5) Dockerfile Design. System Packages
**Decision**
- Install `git`.

**Why**
- Code references `git log` in `rawdog/utils.py` to read metadata.
- Avoid runtime failures if git is not present.

**Alternative**
- Skip `git` to reduce size. Rejected because it risks breaking runtime behavior.

## 6) Dockerfile Design. Copy and Install Strategy
**Decision**
- Copy `pyproject.toml`, `README.md`, `src/`.
- Run `pip install .`.

**Why**
- Only necessary files for package install.
- Creates CLI entrypoint.

**Alternative**
- Copy entire repo. Rejected because it’s unnecessary and larger.

## 7) Dockerfile Design. ENTRYPOINT
**Decision**
- `ENTRYPOINT ["rawdog"]`.

**Why**
- Makes `docker run rawdog "prompt"` behave exactly like the CLI.

**Alternative**
- Use `CMD ["rawdog"]`. Rejected because ENTRYPOINT is more direct for CLI tools.

## 8) Build Verification
**Decision**
- Run `docker build` to verify image builds.

**Why**
- Required by the project workflow (Step 3: build and verify).

## 9) Test Strategy
**Test A: `rawdog --help`**
- **Why**: Validates CLI is installed without needing API keys.
- **Outcome**: Pass.

**Test B: `rawdog "Hello"` without key**
- **Why**: Confirm expected failure behavior when no API key provided.
- **Outcome**: Authentication error (expected).

**Test C: `rawdog "RAWDOG_OK"` with key**
- **Why**: Real usage test to confirm functionality.
- **Outcome**: Pass (user confirmed).

## 10) Usage Documentation Decisions
**Base URL**
- Set to `N/A`, because this is a CLI tool.

**Commands listed as “Endpoints”**
- Direct prompt execution.
- Interactive conversation.
- `--help`.
- Flag usage (`--leash`, `--retries`).

**Environment variables**
- `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` included because README and code mention them.

**Testing status**
- Marked `--help` as tested.
- Marked direct prompt as tested only after user confirmed.

## 11) Notes Captured
- Config is written to `~/.rawdog/config.yaml` on first run.
- Internet access required to reach LLM providers.

## 12) What I Did NOT Do (And Why)
- Did not run interactive mode in Docker: not necessary for a basic functional test.
- Did not add extra dependencies: only git was required to avoid runtime issues.

## Final Outputs
- Dockerfile created.
- Usage doc created and updated with test results.
- Tests: `--help` and prompt execution with key passed.
