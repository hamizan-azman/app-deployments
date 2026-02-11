# Data-Copilot. Reasoning Log

## What Was Checked
- `requirements.txt`: 18 packages including scikit-learn==1.0, typing_extensions==4.5.0, gradio (implicit via app.py), tushare, openai==0.27.0, zhipuai==2.0.1
- `app.py`: Gradio Blocks UI with Chinese financial data examples, uses deprecated `.style()`, `gr.inputs`, `gr.outputs` APIs (Gradio 2.x/3.x only)
- `main.py`: imports tushare, tool.py (which calls `ts.pro_api()` at module level), and lab_llms_call.py (which imports zhipuai)
- `tool.py`: all financial analysis functions, reads TUSHARE_TOKEN from env, calls `ts.pro_api()` at module level
- `lab_llms_call.py`: LLM integrations for DashScope (Qwen), ZhiPu AI (GLM), and indirectly OpenAI
- `lab_gpt4_call.py`: OpenAI GPT-4 integration using openai==0.27.0 and tiktoken

## Dockerfile Strategy
Python 3.10-slim. Two-phase dependency install: first pre-install era-matched pins for packages with build/resolution issues, then install the rest from requirements.txt.

## Key Decisions

### scikit-learn version pin
The repo pins scikit-learn==1.0, which has no prebuilt wheel for Python 3.10 and tries to build from source using deprecated `numpy.distutils.msvccompiler`. This fails on modern Python. Fixed by removing the pin from requirements.txt via `sed` and pre-installing scikit-learn==1.1.3 which has a wheel.

### pydantic v1 vs v2 conflict
Gradio 3.35.2 requires pydantic v1 (its FastAPI integration uses `FieldInfo.in_` which was removed in pydantic v2). zhipuai 2.0.1 requires pydantic v2 (uses `NotGiven` type that isn't v1 compatible). These are fundamentally incompatible.

Resolution: keep pydantic v1 for Gradio compatibility. Patch `lab_llms_call.py` to make the zhipuai import a try/except, with `ZhipuAI = None` fallback. Also guard the module-level `client = ZhipuAI(...)` call. This means GLM model support is unavailable, but OpenAI and DashScope integrations work fine.

Alternative considered: install pydantic v2 + newer FastAPI. This failed because Gradio 3.35.2's `routes.py` directly uses old FastAPI patterns that don't work with pydantic v2, regardless of FastAPI version. Upgrading to Gradio 4.x would break the app because it uses `gr.inputs`, `gr.outputs`, and `.style()` which were removed.

### typing_extensions and scipy
Both had version pins in requirements.txt that caused pip resolution conflicts. typing_extensions==4.5.0 conflicted with pydantic v1's requirements. scipy==1.7.3 was fine but scikit-learn 1.0 pulled incompatible scipy. Fixed by removing from requirements.txt and pre-installing compatible versions.

### Missing transitive dependencies
Initially tried `--no-deps` for the requirements.txt install to avoid resolution conflicts. This caused a cascade of missing runtime deps: websocket-client (tushare), beautifulsoup4 (tushare), regex (tiktoken), cachetools (zhipuai). Abandoned the `--no-deps` approach in favor of installing WITH deps and fixing conflicts via pins.

### CJK fonts
The app renders Chinese text in matplotlib charts. Installed `fonts-wqy-zenhei` and `fonts-noto-cjk` system packages for CJK support. The app's original code referenced `SimHei.ttf` but the font file isn't included in the repo. the system CJK fonts serve as fallback via the matplotlib rcParams override in app.py.

### Tushare token requirement
`tool.py` calls `ts.pro_api(tushare_token)` at module level (line 30). If TUSHARE_TOKEN is not set, this raises an exception and the app crashes before Gradio even starts. With a dummy token, tushare initializes but API calls would fail at runtime. This is the original developer's design.

## Build Iterations
1. scikit-learn==1.0 build failure (no wheel, distutils.msvccompiler missing). Fixed with scikit-learn==1.1.3
2. pip backtracking on typing_extensions/pydantic/gradio. Fixed with explicit pins: pydantic<2, gradio==3.35.2, gradio-client==0.2.7, typing_extensions==4.7.1
3. --no-deps approach: missing websocket-client, beautifulsoup4, regex, cachetools at runtime. Abandoned
4. WITH deps approach: works but pydantic v2 gets installed via zhipuai dependency chain
5. Remove zhipuai from requirements, reinstall pydantic<2 after: zhipuai import fails at startup
6. Patch zhipuai import to try/except + guard client instantiation: SUCCESS

## Testing
1. **GET /**. 200 OK, Gradio web UI loads with Chinese financial query interface
2. **GET /info**. 200 OK, returns full Gradio API schema with all registered endpoints
3. **Query execution**. NOT TESTED, requires valid Tushare Pro token and OpenAI API key

## Gotchas
- The app crashes at import time without TUSHARE_TOKEN (module-level API init in tool.py)
- zhipuai v2 and gradio 3.x are fundamentally incompatible (pydantic v1 vs v2). No clean fix exists
- The app uses deprecated Gradio APIs (.style(), gr.inputs, gr.outputs) that only work in Gradio 3.x
- Chinese text appears garbled in non-UTF8 terminals but renders correctly in the web UI
