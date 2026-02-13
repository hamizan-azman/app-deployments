# chemcrow-public -- Reasoning Log

## What I Checked and Why

### Repository Structure
- `setup.py`: Found Python >=3.9,<3.12 constraint. Key deps: openai==0.27.8, langchain>=0.0.234,<=0.0.275, langchain_core==0.0.1, paper-qa==1.1.1, rdkit, molbloom. The `paper-scraper` git dependency is commented out but the code still imports it.
- `chemcrow/agents/chemcrow.py`: The main ChemCrow class. Uses langchain's ChatOpenAI (old API), rmrkl's ChatZeroShotAgent, and a collection of chemistry tools.
- `chemcrow/agents/tools.py`: Tool factory function. Loads python_repl + wikipedia from langchain, then adds custom chemistry tools. Some tools are conditional on API keys.
- `chemcrow/tools/`: Individual tool modules for RDKit operations, safety checks, reaction prediction, literature search, web search, and molecular pricing.

### App Type Assessment
This is a pure Python library. No web server, no HTTP endpoints, no Streamlit app (Streamlit is a dependency for the frontend module but not the core library). The README shows usage as `from chemcrow.agents import ChemCrow`. The HuggingFace demo is hosted separately.

Per the architectural fidelity rule: "If an app is a library with no web interface, deploy it as a library (importable in container)."

### Dependency Challenges
- `openai==0.27.8`: The old pre-1.0 OpenAI Python package. Uses `openai.ChatCompletion.create()` style API.
- `langchain>=0.0.234,<=0.0.275`: Very old langchain from mid-2023.
- `langchain_core==0.0.1`: The very first release of langchain-core.
- `paper-scraper`: Commented out in setup.py (`#"paper-scraper@git+https://github.com/blackadad/paper-scraper.git"`) but `from paperscraper import get_papers_from_queries` is used in `search.py`. Must be installed separately.

## What I Decided and Why

### Base Image: python:3.11-slim
Python 3.11 is within the required range. Slim variant since no GPU or system-level chemistry libraries are needed (RDKit has a pure Python PyPI wheel now).

### Install via setup.py (editable mode)
Used `pip install -e .` from the cloned repo. This installs the exact version in the repo (0.3.24) with its pinned dependencies. The PyPI version might differ.

### Separate paper-scraper Install
Since `paper-scraper` is commented out in setup.py but imported at runtime, it must be installed as a second pip install step. Used the git URL from the commented-out line: `paper-scraper@git+https://github.com/blackadad/paper-scraper.git`.

### No Custom Web Wrapper
The library has no web interface and no HTTP server. Per architectural fidelity, I deployed it as-is: a Python library importable in the container. Users interact via `docker run -it ... python` or by running Python scripts.

### No Port Exposed
Since there's no web server, no ports are exposed. The container's CMD just verifies the import works.

## How Tests Were Chosen

### Test 1: Agent Import
`from chemcrow.agents import ChemCrow` -- verifies the main class loads, all its dependencies resolve, and the module structure is intact.

### Test 2: All Tools Import
`from chemcrow.tools import *` -- this imports all tool modules including rdkit, safety, search, reactions, chemspace. Verifies the entire tool chain loads.

### Test 3: RDKit Molecular Weight
`SMILES2Weight().run('CC(=O)Oc1ccccc1C(=O)O')` returns 180.042258736 for aspirin. This exercises the RDKit chemistry engine end-to-end: SMILES parsing, molecular graph construction, property calculation. No API key needed.

### Test 4: Functional Group Detection
`FuncGroups().run(aspirin_smiles)` returns detected functional groups (esters, ketones, carboxylic acids). Tests RDKit's substructure matching against known functional group patterns.

### Test 5: Molecular Similarity
`MolSimilarity().run('mol1.mol2')` computes Tanimoto similarity using Morgan fingerprints. Tests RDKit's fingerprint generation and comparison. Returns 0.24 for aspirin vs acetic acid (low similarity, correct).

### Test 6: Version Verification
Confirmed correct dependency versions: RDKit 2025.09.4, LangChain 0.0.275, OpenAI 0.27.8. These match the setup.py constraints.

### Tests Not Run
- Full agent query (requires OPENAI_API_KEY at runtime for GPT-4 calls)
- Literature search (requires Semantic Scholar API key)
- Web search (requires SerpAPI key)
- Reaction prediction (requires RXN4Chem API key or local GPU Docker images)
- Molecular pricing (requires Chem-Space API key)

These are all API-dependent features. The core chemistry tools (RDKit-based) work fully offline and were tested.

## Gotchas and Debugging

### paper-scraper Missing
First build failed with `ModuleNotFoundError: No module named 'paperscraper'`. The dependency is commented out in setup.py but still imported. Had to add a separate `pip install` for it from the git URL.

### Old OpenAI API
Uses `openai==0.27.8` which has a completely different API from modern openai>=1.0. The old API uses `openai.ChatCompletion.create()` instead of `client.chat.completions.create()`. This is intentional and correct for this library's era.

### RDKit Deprecation Warnings
`DEPRECATION WARNING: please use MorganGenerator` -- RDKit deprecated the old Morgan fingerprint API. The library uses the old API but it still works. These are warnings, not errors.

### Explosive Check Input Format
The `ExplosiveCheck` tool expects CAS numbers, not SMILES. Passing a SMILES string returns "Please input a valid CAS number." This is correct behavior -- the tool checks against a database of known explosives by CAS number.

### No Streamlit App
Despite `streamlit` being in the dependencies, it's only used for the HuggingFace Spaces frontend (`chemcrow/frontend/`). The main library usage is Python API, not web interface.
