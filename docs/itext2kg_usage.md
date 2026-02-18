# itext2kg -- Local Install Guide

## Overview
itext2kg (now called ATOM) is a Python library for incremental construction of Temporal Knowledge Graphs from unstructured text. It uses LangChain-compatible LLMs to extract entities, relations, and temporal facts, and optionally stores results in Neo4j.

## Why Not Dockerized
itext2kg is a pure Python library with no web server, no CLI entrypoint, and no standalone application. It is imported and called from user Python code or Jupyter notebooks. Deploying it as a Docker service would require writing a custom API wrapper, which violates the architectural fidelity rule for this project. It is documented here as a library to be used locally.

## Requirements
- OS: Any (Windows, macOS, Linux)
- Python 3.9+
- A LangChain-compatible LLM (e.g., OpenAI GPT-4, Ollama, etc.)
- A LangChain-compatible embeddings model (e.g., OpenAI text-embedding-3-small)
- Neo4j (optional, for graph visualization)
- OpenAI API key or equivalent

## Installation

```bash
# Install from PyPI
pip install itext2kg

# Or install the latest version
pip install --upgrade itext2kg
```

Dependencies include `langchain`, `langchain-openai`, `pydantic`, and `neo4j` (optional).

## Usage

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from itext2kg import iText2KG

# Initialize with your LLM and embeddings model
llm = ChatOpenAI(model="gpt-4o", api_key="your-key-here")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key="your-key-here")

kg_builder = iText2KG(llm=llm, embeddings=embeddings)

# Build a knowledge graph from a list of text documents
documents = [
    "Marie Curie discovered polonium in 1898.",
    "Polonium is a radioactive element.",
]

graph = kg_builder.build_graph(
    sections=documents,
    observation_date="1898-01-01"
)

print(graph)
```

### With Neo4j visualization

```python
from itext2kg import iText2KG
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

kg_builder = iText2KG(llm=llm, embeddings=embeddings, neo4j_driver=driver)
graph = kg_builder.build_graph(sections=documents, observation_date="2024-01-01")
```

### Example notebooks

The repo provides runnable examples in the `examples/` directory:

```bash
git clone https://github.com/AuvaLab/itext2kg.git
cd itext2kg/examples
jupyter notebook
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes (if using OpenAI) | None | Passed directly to LangChain OpenAI client |

## Notes
- itext2kg works with any LangChain-supported LLM, not just OpenAI. Substitute with `ChatOllama`, `ChatAnthropic`, etc.
- The Neo4j integration requires a running Neo4j instance. Start one with: `docker run -p 7474:7474 -p 7687:7687 neo4j:latest`
- The library name on PyPI is `itext2kg`; the internal module/API may refer to the newer name "ATOM".
- GitHub: https://github.com/AuvaLab/itext2kg
