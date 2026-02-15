# chemcrow-public -- Usage Documentation

## Overview
Python library for reasoning-intensive chemical tasks using LLM agents. Combines LangChain with chemistry tools including RDKit (molecular analysis), PubChem, Chem-Space, paper-qa (literature search), and reaction prediction. Uses GPT-4 as the reasoning engine.

## Quick Start
```bash
# Pull from Docker Hub (recommended)
docker pull hoomzoom/chemcrow

# Or build from source
docker build -t chemcrow apps/chemcrow-public/

docker run -it -e OPENAI_API_KEY=your-key hoomzoom/chemcrow python
```

## Type
Library (no web interface). Use via Python import inside the container.

## Core Features
- LLM-powered chemistry agent with specialized tools
- Molecular weight, similarity, functional group analysis (RDKit, offline)
- Explosive/controlled substance safety checks (offline)
- Patent lookup via PubChem
- Literature search via paper-qa + Semantic Scholar
- Reaction prediction and retrosynthesis (via RXN4Chem API or local Docker)
- Web search via SerpAPI or DuckDuckGo
- Molecular pricing via Chem-Space

## Python API

### Full Agent (requires OpenAI API key)
```python
from chemcrow.agents import ChemCrow

chem = ChemCrow(model="gpt-4-0613", temp=0.1, streaming=False)
result = chem.run("What is the molecular weight of tylenol?")
print(result)
```

### With Local Reaction Prediction (requires GPU Docker images)
```python
chem = ChemCrow(model="gpt-4-0613", temp=0.1, streaming=False, local_rxn=True)
result = chem.run("What is the product of the reaction between styrene and dibromine?")
```

### Individual Tools (no API key needed for RDKit tools)
```python
from chemcrow.tools.rdkit import SMILES2Weight, MolSimilarity, FuncGroups

# Molecular weight
mw = SMILES2Weight()
mw.run("CC(=O)Oc1ccccc1C(=O)O")  # Returns: 180.042258736

# Functional groups
fg = FuncGroups()
fg.run("CC(=O)Oc1ccccc1C(=O)O")  # Returns: esters, ketones, carboxylic acids...

# Molecular similarity (Tanimoto)
sim = MolSimilarity()
sim.run("CC(=O)Oc1ccccc1C(=O)O.CC(=O)O")  # Returns: 0.24
```

## Commands (inside container)

### Interactive Python
```bash
docker run -it -e OPENAI_API_KEY=your-key chemcrow python
```

### Run a Query
```bash
docker run -e OPENAI_API_KEY=your-key chemcrow python -c "
from chemcrow.agents import ChemCrow
chem = ChemCrow(model='gpt-4-0613', temp=0.1, streaming=False)
print(chem.run('What is the molecular weight of aspirin?'))
"
```

## Tested Functionality
| Test | Result |
|------|--------|
| Import chemcrow.agents.ChemCrow | PASS |
| Import all tools | PASS |
| RDKit molecular weight (aspirin SMILES) | PASS -- returned 180.042258736 |
| RDKit functional groups (aspirin SMILES) | PASS -- identified esters, ketones, carboxylic acids |
| Molecular similarity (Tanimoto) | PASS -- returned 0.24 for aspirin vs acetic acid |
| Explosive check tool | PASS -- tool loaded (needs CAS number input) |
| RDKit version | 2025.09.4 |
| LangChain version | 0.0.275 |
| OpenAI version | 0.27.8 |
| Full agent query | NOT TESTED -- requires OpenAI API key at runtime |

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (for agent) | None | OpenAI API key for GPT-4 reasoning |
| SERP_API_KEY | No | None | SerpAPI key for web search tool |
| RXN4CHEM_API_KEY | No | None | IBM RXN4Chem key for reaction prediction |
| CHEMSPACE_API_KEY | No | None | Chem-Space key for molecular pricing |
| SEMANTIC_SCHOLAR_API_KEY | No | None | Semantic Scholar key for literature search |

## Notes
- Uses old OpenAI API (v0.27.8, pre-1.0). Compatible with current OpenAI API keys.
- Uses old LangChain (v0.0.275). Do not upgrade.
- RDKit tools work fully offline without any API keys.
- Safety tools (explosive check, controlled substance check) work offline using local databases.
- Paper-qa requires Semantic Scholar API for best results.
- The `paperscraper` dependency is installed from git (commented out in setup.py but required at runtime).
- Optional self-hosted reaction prediction requires GPU Docker images: `doncamilom/rxnpred:latest` and `doncamilom/retrosynthesis:latest`.
