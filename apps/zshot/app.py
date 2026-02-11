"""Zshot REST API -- zero-shot named entity recognition."""
from typing import List, Optional

import spacy
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from zshot import PipelineConfig, displacy
from zshot.linker import LinkerRegen
from zshot.mentions_extractor import MentionsExtractorSpacy
from zshot.utils.data_models import Entity

app = FastAPI(title="Zshot NER API")

# Default entities (from README example)
DEFAULT_ENTITIES = [
    Entity(name="Paris", description="Paris is located in northern central France, in a north-bending arc of the river Seine"),
    Entity(name="IBM", description="International Business Machines Corporation (IBM) is an American multinational technology corporation headquartered in Armonk, New York"),
    Entity(name="New York", description="New York is a city in U.S. state"),
    Entity(name="Florida", description="southeasternmost U.S. state"),
    Entity(name="American", description="American, something of, from, or related to the United States of America"),
    Entity(name="Armonk", description="Armonk is a hamlet and census-designated place in the town of North Castle, located in Westchester County, New York, United States."),
]

nlp = spacy.load("en_core_web_sm")
nlp_config = PipelineConfig(
    mentions_extractor=MentionsExtractorSpacy(),
    linker=LinkerRegen(),
    entities=DEFAULT_ENTITIES,
)
nlp.add_pipe("zshot", config=nlp_config, last=True)


class EntityDef(BaseModel):
    name: str
    description: str


class ExtractRequest(BaseModel):
    text: str
    entities: Optional[List[EntityDef]] = None


class ExtractedEntity(BaseModel):
    text: str
    label: str
    start: int
    end: int


class ExtractResponse(BaseModel):
    text: str
    entities: List[ExtractedEntity]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    """Extract named entities from text using zero-shot NER."""
    zshot_pipe = nlp.get_pipe("zshot")
    if req.entities:
        custom = [Entity(name=e.name, description=e.description) for e in req.entities]
        zshot_pipe.entities = custom
        zshot_pipe.linker.set_kg(custom)
    doc = nlp(req.text)
    if req.entities:
        zshot_pipe.entities = DEFAULT_ENTITIES
        zshot_pipe.linker.set_kg(DEFAULT_ENTITIES)
    ents = [
        ExtractedEntity(text=ent.text, label=ent.label_, start=ent.start_char, end=ent.end_char)
        for ent in doc.ents
    ]
    return ExtractResponse(text=req.text, entities=ents)


@app.post("/visualize", response_class=HTMLResponse)
def visualize(req: ExtractRequest):
    """Return displacy HTML visualization of extracted entities."""
    zshot_pipe = nlp.get_pipe("zshot")
    if req.entities:
        custom = [Entity(name=e.name, description=e.description) for e in req.entities]
        zshot_pipe.entities = custom
        zshot_pipe.linker.set_kg(custom)
    doc = nlp(req.text)
    if req.entities:
        zshot_pipe.entities = DEFAULT_ENTITIES
        zshot_pipe.linker.set_kg(DEFAULT_ENTITIES)
    html = displacy.render(doc, style="ent")
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
