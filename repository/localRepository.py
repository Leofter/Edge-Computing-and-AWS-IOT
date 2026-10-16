import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# Diretório para imagens pendentes de upload
LOCAL_IMAGE_DIR = Path("./pending_images")
LOCAL_IMAGE_DIR.mkdir(exist_ok=True)

DB_PATH = "inference_queue.db"


def get_connection() -> sqlite3.Connection:

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # conn.row_factory = sqlite3.Row  
    # conn.execute("PRAGMA journal_mode=WAL")
    # conn.execute("PRAGMA synchronous=NORMAL") 
    return conn


def init_queue(conn: sqlite3.Connection) -> None:

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inference_queue (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            inference_id        TEXT    NOT NULL UNIQUE,
            device_id           TEXT    NOT NULL,
            inference_timestamp INTEGER NOT NULL,
            date_time           TEXT    NOT NULL,
            ocr_data            TEXT    NOT NULL,
            local_image_path    TEXT    NOT NULL,
            s3_uri              TEXT,
            s3_status           TEXT    NOT NULL DEFAULT 'pending',
            mqtt_status         TEXT    NOT NULL DEFAULT 'pending',
            retry_count         INTEGER NOT NULL DEFAULT 0,
            created_at          REAL    NOT NULL,
            sent_at             REAL
        )
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pending
        ON inference_queue (mqtt_status, s3_status, id ASC)
    """)

    conn.commit()
    print("[Queue] Banco local inicializado.")
