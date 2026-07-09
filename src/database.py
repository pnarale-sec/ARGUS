import sqlite3

DB_PATH = "data/siem.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level     TEXT,
            message   TEXT,
            source    TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_log(log):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, level, message, source)
        VALUES (?, ?, ?, ?)
    """, (log["timestamp"], log["level"], log["message"], log["source"]))
    conn.commit()
    conn.close()

