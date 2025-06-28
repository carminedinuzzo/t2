"""FastAPI server exposing endpoints for the clone."""

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .memory import Memory
from .model_infer import LocalModel

logger = logging.getLogger(__name__)

app = FastAPI()
memory: Memory
model: LocalModel


class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    logger.debug("Received query: %s", query.message)
    memory.add("user", query.message)
    try:
        response = model.generate(query.message)
    except Exception as e:
        logger.exception("Model generation failed")
        raise HTTPException(status_code=500, detail=str(e))
    memory.add("assistant", response)
    return {"response": response}


@app.get("/history")
async def history():
    return {"history": memory.history()}


def start(api_host: str, api_port: int, model_path: Path, db_path: Path):
    """Initialize components and run the server."""
    global memory, model
    logging.basicConfig(level=logging.DEBUG)
    memory = Memory(db_path)
    model = LocalModel(model_path)
    import uvicorn

    uvicorn.run(app, host=api_host, port=api_port)
