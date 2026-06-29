import sqlite3
from pathlib import Path
from typing import Generator

from app.core.config import get_settings


def _database_path() -> str:
    url = get_settings().database_url
    if not url.startswith("sqlite:///"):
        raise ValueError("This implementation expects a sqlite:/// DATABASE_URL")
    return url.replace("sqlite:///", "", 1)


def get_connection() -> sqlite3.Connection:
    path = _database_path()
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
