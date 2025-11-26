from typing import List, Dict
import sqlite3
from pathlib import Path

def init_sqlite_db(db_path: str):
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_path TEXT,
            normalized_path TEXT,
            content_hash TEXT,
            dupe_group_id TEXT,
            text TEXT
        )
        """
    )
    conn.commit()
    return conn

def index_documents_sqlite(db_path: str, docs: List[Dict]):
    conn = init_sqlite_db(db_path)
    cur = conn.cursor()

    for d in docs:
        cur.execute(
            """
            INSERT INTO documents (source_path, normalized_path, content_hash, dupe_group_id, text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                d.get("source_path"),
                d.get("normalized_path"),
                d.get("content_hash"),
                d.get("dupe_group_id"),
                d.get("text", ""),
            ),
        )

    conn.commit()
    conn.close()