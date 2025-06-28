"""LLM inference module using llama-cpp-python."""

import logging
from pathlib import Path

from llama_cpp import Llama

logger = logging.getLogger(__name__)


class LocalModel:
    def __init__(self, model_path: Path):
        logger.debug("Loading model from %s", model_path)
        self.llm = Llama(model_path=str(model_path), n_ctx=2048)

    def generate(self, prompt: str) -> str:
        logger.debug("Generating response for prompt: %s", prompt)
        output = self.llm(prompt, echo=False)
        text = output["choices"][0]["text"].strip()
        logger.debug("Model output: %s", text)
        return text
