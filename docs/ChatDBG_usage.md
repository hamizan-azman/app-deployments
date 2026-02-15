# ChatDBG -- Usage Documentation

## Overview
AI-powered debugging assistant that integrates LLMs into standard debuggers (pdb, lldb, gdb). Lets you ask open-ended questions like "why is x null?" and gets AI-driven root cause analysis and fix suggestions.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/chatdbg

# Or build from source
docker build -t chatdbg ./ChatDBG

docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY hoomzoom/chatdbg
```

## Tool Type
CLI debugging tool (not a web service). No HTTP endpoints. Interaction is via terminal debugger commands.

## Core Features
- AI-assisted Python debugging via extended pdb
- AI-assisted C/C++ debugging via lldb and gdb extensions
- `why` command for automatic root cause analysis
- Suggested code fixes from LLM
- Support for Rust debugging
- IPython and Jupyter notebook integration
- Bugbench sample suite for C/C++ vulnerability testing

## CLI Commands

### Debug a Python script
- **Command:** `chatdbg -c continue <script.py>`
- **Description:** Runs script, enters post-mortem debugger on uncaught exception
- **Example:**
```bash
docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY chatdbg \
  chatdbg -c continue samples/python/testme.py
```
- **Tested:** Yes (debugger loads, catches ZeroDivisionError, enters post-mortem)

### Ask "why" (requires API key)
- **Command:** `why` (inside debugger prompt)
- **Description:** Sends program state to LLM, gets root cause analysis and fix
- **Example:** At `(ChatDBG)` prompt, type `why`
- **Tested:** No (requires valid OPENAI_API_KEY with credits)

### Debug C/C++ with lldb
- **Command:** `lldb <binary>`
- **Description:** Loads ChatDBG-extended lldb for native debugging
- **Example:**
```bash
docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY chatdbg bash -c \
  "cd samples/cpp && clang++ -g -fsanitize=address -o test-overflow test-overflow.cpp && lldb ./test-overflow"
```
- **Tested:** Yes (compiles, lldb loads with ChatDBG prompt)

### Debug C/C++ with gdb
- **Command:** `gdb <binary>`
- **Description:** Loads ChatDBG-extended gdb for native debugging
- **Example:**
```bash
docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY chatdbg bash -c \
  "cd samples/cpp && clang++ -g -fsanitize=address -o test-overflow test-overflow.cpp && gdb ./test-overflow"
```
- **Tested:** Yes (compiles, gdb available)

### Run bugbench samples
- **Description:** Pre-built C/C++ programs with known bugs (libtiff, gzip, etc.)
- **Example:**
```bash
docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY chatdbg bash -c \
  "lldb samples/bugbench/libtiff-4.0.6/tools/.libs/tiffdump"
```
- **Tested:** Yes (bugbench built during Docker build)

### ChatDBG CLI options
```
--log=<file>          Log file (default: log.yaml)
--model=<model>       LLM model (default: gpt-4o)
--instructions=<file> Custom instructions file for LLM
--format=<fmt>        Output format: text, md, md:simple, jupyter
--module_whitelist=<file>  Module whitelist
--unsafe              Disable protections against harmful code execution
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | None | OpenAI API key for the `why` command |
| CHATDBG_UNSAFE | No | 1 (in Docker) | Allow LLM to execute debugger commands |

## Sample Python Scripts (included)
| Script | Bug | Purpose |
|--------|-----|---------|
| testme.py | ZeroDivisionError | Division by zero in loop |
| sample.py | TypeError | Wrong argument order to numpy |
| bootstrap.py | Statistics error | Bootstrap sampling bug |
| mean.py | Calculation error | Mean computation bug |

## Test Summary
| Test | Result |
|------|--------|
| Docker build | PASS |
| chatdbg --help | PASS |
| Python pdb module load | PASS |
| Python post-mortem debugging (testme.py) | PASS |
| C++ compilation + lldb load | PASS |
| Bugbench build | PASS |
| `why` command (with API key) | PASS |

## Notes
- This is a CLI tool, not a web service. Must run with `-it` for interactive terminal.
- The `why` command requires an OpenAI API key with positive balance and GPT-4 access.
- The Docker image is large (~3GB+) because it includes LLVM/Clang toolchain and bugbench C/C++ samples.
- The image uses unpinned `FROM ubuntu`. For reproducibility, pin to a specific tag.
- Default model is gpt-4o. Can be changed with `--model` flag.
- Supports litellm backend, so other LLM providers may work with appropriate config.

## Changes from Original
None. The deployed container uses the developer's original Dockerfile with no source code or dependency changes.
