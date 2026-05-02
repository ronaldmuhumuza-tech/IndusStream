import sqlite3
from pathlib import Path
from datetime import datetime

from config.settings import DATA_DIR, DB_FILE_PREFIX


def get_today_db_path() -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    return DATA_DIR / f"{DB_FILE_PREFIX}_{today}.db"


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