"""Persistent memory for storing interactions."""

import logging
import sqlite3
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Memory:
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
        )
        self.conn.commit()

    def add(self, role: str, message: str):
        logger.debug("Storing %s: %s", role, message)
        self.conn.execute(
            "INSERT INTO interactions (role, message) VALUES (?, ?)",
            (role, message),
        )
        self.conn.commit()

    def history(self, limit: int = 50) -> List[Tuple[str, str, str]]:
        cur = self.conn.execute(
            "SELECT role, message, timestamp FROM interactions ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return cur.fetchall()
