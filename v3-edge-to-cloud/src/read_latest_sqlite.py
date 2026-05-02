import sqlite3
from pathlib import Path
from datetime import datetime

from src.config.settings import V2_DB_PATH


def get_today_db_path():
    return V2_DB_PATH


def read_latest_reading():
    db_path = get_today_db_path()

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM raw_readings
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        conn.close()