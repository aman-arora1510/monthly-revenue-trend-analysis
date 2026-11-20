"""
src/db.py
---------
SQLite database connection context manager enforcing foreign keys and read optimization.
"""

import sqlite3
from contextlib import contextmanager
from src.config import DB_PATH

@contextmanager
def get_db_connection():
    """
    Yields an active SQLite database connection with row factory enabled
    and foreign key constraints enforced.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: tuple = ()) -> list:
    """
    Executes a SELECT query and returns a list of dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
