# ChatDBG -- Deployment Reasoning Log

## What is ChatDBG?

ChatDBG is a research tool from UMass Amherst that extends standard debuggers (Python's pdb, LLDB for C/C++, GDB) with an LLM backend. When you hit a crash, instead of manually inspecting variables and stack frames, you type `why` and an LLM reads the program state and tells you the root cause and a suggested fix.

This matters for the supply chain security research because ChatDBG injects LLM calls into the debugging workflow. The LLM can execute debugger commands (inspect memory, run expressions) via the `CHATDBG_UNSAFE=1` flag. This is a clear attack surface: a compromised LLM response could execute arbitrary debugger commands during a debug session.

---

## Step 1: What I Checked and Why

### README.md
First thing to read for any repo. Tells you what the tool does, how to install it, and what dependencies it needs. ChatDBG's README explains it supports three debuggers (pdb, lldb, gdb), requires an OpenAI API key, and has sample programs.

### Dockerfile
The repo already had a Dockerfile in the root. This is the ideal case: the authors know their own dependency chain better than we do. I checked whether it builds and runs correctly rather than writing one from scratch.

### pyproject.toml
This is the Python package definition. It tells you what `pip install` will do: what dependencies get pulled in, what entry points get created (the `chatdbg` CLI command), and what Python version is required. This is where the `chatdbg` command is registered as a console script.

### samples/ directory
The repo includes test programs with known bugs. This is valuable because it means we can test the debugger without needing real-world code. I checked what samples exist so I could use them in testing.

### src/chatdbg/ directory
The actual source code. I looked at `chatdbg_pdb.py`, `chatdbg_lldb.py`, and `chatdbg_gdb.py` to understand how the tool hooks into each debugger. This confirmed that:
- For Python: it subclasses pdb and adds the `why` command
- For LLDB/GDB: it loads via `.lldbinit`/`.gdbinit` config files
- The LLM interaction happens in the `assistant/` subdirectory

---

## Step 2: Dockerfile Decisions

### Decision: Use the existing Dockerfile as-is

**Why:** The repo's Dockerfile was comprehensive and well-structured. It installs LLVM 20, sets up all three debugger integrations, builds the bugbench C/C++ test suite, and configures the init files. Writing our own would risk missing something.

**Alternative considered: Write a minimal Dockerfile.** Rejected because ChatDBG has complex system dependencies (LLVM toolchain, clang, gdb, autoconf for bugbench builds). Getting these right from scratch would be error-prone and we would likely miss something the authors already know about.

**Alternative considered: Pin the base image.** The Dockerfile uses `FROM ubuntu` without a version tag. This means every build could use a different Ubuntu version. For reproducibility, pinning to something like `ubuntu:24.04` would be better. I noted this as a limitation but did not change it because modifying the existing Dockerfile introduces risk of breaking things, and the primary goal is a working deployment, not production hardening.

### How the Dockerfile works, line by line

1. `FROM ubuntu` -- Pulls the latest Ubuntu base image. This gives us a full Linux environment with apt package management.

2. `ARG LLVM_VERSION=20` -- Pins the LLVM toolchain version as a build argument. LLVM provides clang (the C/C++ compiler) and lldb (the debugger). Version 20 is the latest at time of writing.

3. System packages installed: `python3`, `pip`, `gdb`, `gcc`, `cmake`, `autoconf`, etc. These are needed because:
   - `python3`/`pip`: ChatDBG is a Python package
   - `gdb`: One of the three supported debuggers
   - `gcc`/`clang`/`cmake`: Needed to compile C/C++ test programs and bugbench
   - `autoconf`/`libtool`: Needed by bugbench's build system (it builds real-world C projects like libtiff)

4. LLVM install script: Downloads and runs the official LLVM install script. This adds the LLVM apt repository and installs `lldb-20`. Using the official script is better than manually adding repos because LLVM's repository structure changes between versions.

5. `pip install -e /root/ChatDBG` -- Installs ChatDBG in editable mode. The `-e` flag means Python loads the code directly from the source directory rather than copying it to site-packages. The `--break-system-packages` flag is needed because Ubuntu's pip refuses to install into the system Python without it (a safety feature to prevent breaking OS tools).

6. `.lldbinit` and `.gdbinit` configuration: These files tell lldb and gdb to load ChatDBG's extensions on startup. Without these, you would get a normal debugger without the `why` command.

7. `CHATDBG_UNSAFE=1` -- This environment variable allows the LLM to execute debugger commands. Without it, the LLM can only analyze the state it is shown. With it, the LLM can actively run commands like `print variable_name` or `frame select 3`. This is the key attack surface for supply chain security research.

8. Bugbench build: Clones and compiles a suite of C/C++ programs with known vulnerabilities (buffer overflows in libtiff, gzip, etc.). These are used as test cases for the debugger.

---

## Step 3: Build and Verification

### What happened during the build
The build completed successfully. The main time cost was:
- LLVM toolchain download and install (~1-2 minutes)
- Bugbench compilation (~1-2 minutes, builds multiple C projects from source)
- pip install of ChatDBG and dependencies (~30 seconds)

Total image size: ~3GB+. This is large because it includes the entire LLVM/Clang toolchain (which is hundreds of MB) plus compiled bugbench binaries.

---

## Step 4: Test Selection and What Each Test Validates

### Test 1: Docker build -- PASS
**What it validates:** The entire dependency chain resolves correctly. All apt packages exist in the Ubuntu repos, the LLVM install script works, pip can install ChatDBG and all its Python dependencies, and bugbench compiles.
**Why this test matters:** If the build fails, nothing else works. This is the foundation.

### Test 2: chatdbg --help -- PASS
**What it validates:** The `chatdbg` console script entry point was correctly registered by pip, and the Python package imports successfully. If this fails, it means either pip install did not create the entry point, or there is a missing Python dependency.
**Why this test matters:** Confirms the CLI tool is installed and runnable.

### Test 3: Python pdb module load -- PASS
**What it validates:** ChatDBG's custom pdb module can be imported. This is the core Python debugger integration. We ran `python -c "from chatdbg.chatdbg_pdb import ChatDBG"` to confirm the import works without errors.
**Why this test matters:** A successful import means all the Python dependencies (openai, litellm, etc.) are present and compatible.

### Test 4: Python post-mortem debugging (testme.py) -- PASS
**What it validates:** The full debugger flow: run a Python script, hit an exception (ZeroDivisionError), and enter the ChatDBG post-mortem debugger. The command was `chatdbg -c continue samples/python/testme.py`.
**Why this test matters:** This proves the debugger actually works end-to-end for Python. The `-c continue` flag tells it to run until an exception, then drop into the debugger. We verified the `(ChatDBG)` prompt appeared, meaning the custom debugger loaded correctly (not the default pdb).

### Test 5: C++ compilation + lldb load -- PASS
**What it validates:** The C/C++ toolchain works (clang++ can compile code) and lldb loads with the ChatDBG extension. We compiled `test-overflow.cpp` with AddressSanitizer (`-fsanitize=address`) and loaded it in lldb.
**Why this test matters:** Proves the LLVM toolchain is correctly installed and the `.lldbinit` file correctly loads the ChatDBG extension into lldb.

### Test 6: Bugbench build -- PASS
**What it validates:** The pre-built bugbench binaries exist and are loadable in lldb. These are real-world C programs (libtiff, gzip, etc.) with known CVEs.
**Why this test matters:** Bugbench is the research test suite. If these binaries do not exist or cannot load, the tool is not useful for vulnerability research.

### Test 7: `why` command -- PASS
**What it validates:** The LLM integration works end-to-end. With a valid API key, the `why` command sends program state to GPT-4o and receives a root cause analysis.
**Why this test matters:** This is the core feature of ChatDBG. Without this working, it is just a regular debugger. This test was done when the user provided an API key.

### Why no HTTP endpoint tests
ChatDBG is a CLI tool, not a web service. There are no HTTP endpoints to test. The interaction model is: run a program in the debugger, hit a crash, type `why`. All interaction happens through the terminal. This is why the usage doc documents CLI commands instead of API endpoints.

---

## Gotchas and Debugging Notes

### 1. Interactive terminal required
Docker must be run with `-it` flags (interactive + tty). Without these, the debugger cannot accept input and will exit immediately. This is different from web service containers that run in the background with `-d`.

### 2. CHATDBG_UNSAFE=1 default
The Dockerfile sets this to 1 by default. In a production setting this would be dangerous (the LLM can execute arbitrary debugger commands), but for research purposes it is necessary to test the full attack surface.

### 3. Unpinned base image
`FROM ubuntu` means the image is not reproducible. If Ubuntu releases a new LTS version, a rebuild could pull a different OS version and potentially break things. For a research project this is acceptable; for production it should be pinned.

### 4. Large image size
3GB+ is large but unavoidable. The LLVM toolchain alone is several hundred MB. If size were a concern, you could create separate images for Python-only debugging (much smaller, no LLVM needed) vs. C/C++ debugging.
