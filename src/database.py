import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id        SERIAL PRIMARY KEY,
            timestamp TEXT,
            level     TEXT,
            message   TEXT,
            source    TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("PostgreSQL database initialized.")

def insert_log(log):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, level, message, source)
        VALUES (%s, %s, %s, %s)
    """, (log["timestamp"], log["level"], log["message"], log["source"]))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, level, message, source FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    logs = []
    for row in rows:
        logs.append({
            "id":        row[0],
            "timestamp": row[1],
            "level":     row[2],
            "message":   row[3],
            "source":    row[4]
        })
    return logs

def get_logs_by_level(level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, level, message, source
        FROM logs WHERE level = %s ORDER BY id DESC
    """, (level,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    logs = []
    for row in rows:
        logs.append({
            "id":        row[0],
            "timestamp": row[1],
            "level":     row[2],
            "message":   row[3],
            "source":    row[4]
        })
    return logs