"""Entry point for the local AI node."""

import logging
from pathlib import Path

import yaml

from . import api_server
from .memory import Memory
from .model_infer import LocalModel

logger = logging.getLogger(__name__)


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    logging.basicConfig(level=logging.DEBUG)
    config = load_config(Path(__file__).parent / "config.yaml")
    api_server.start(
        config["api_host"],
        config["api_port"],
        Path(config["model_path"]),
        Path(config["memory_db"]),
    )


if __name__ == "__main__":
    main()
