import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialise la base de données SQLite et crée la table si elle n'existe pas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            passed_count INTEGER NOT NULL,
            failed_count INTEGER NOT NULL,
            latency_avg REAL NOT NULL,
            latency_p95 REAL NOT NULL,
            success_rate REAL NOT NULL,
            details TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_run(timestamp, passed_count, failed_count, latency_avg, latency_p95, success_rate, details):
    """Enregistre un run de tests dans la base de données."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # details est une liste/dict Python, on le sérialise en JSON string
    details_str = json.dumps(details)
    
    cursor.execute("""
        INSERT INTO runs (timestamp, passed_count, failed_count, latency_avg, latency_p95, success_rate, details)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, passed_count, failed_count, latency_avg, latency_p95, success_rate, details_str))
    
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_runs(limit=100):
    """Récupère l'historique complet des runs (trié du plus récent au plus ancien)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, passed_count, failed_count, latency_avg, latency_p95, success_rate, details
        FROM runs
        ORDER BY timestamp DESC, id DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    runs = []
    for row in rows:
        runs.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "passed_count": row["passed_count"],
            "failed_count": row["failed_count"],
            "latency_avg": round(row["latency_avg"], 1),
            "latency_p95": round(row["latency_p95"], 1),
            "success_rate": round(row["success_rate"], 1),
            "details": json.loads(row["details"])
        })
    return runs

def get_latest_run():
    """Récupère le tout dernier run enregistré."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, passed_count, failed_count, latency_avg, latency_p95, success_rate, details
        FROM runs
        ORDER BY timestamp DESC, id DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "id": row["id"],
        "timestamp": row["timestamp"],
        "passed_count": row["passed_count"],
        "failed_count": row["failed_count"],
        "latency_avg": round(row["latency_avg"], 1),
        "latency_p95": round(row["latency_p95"], 1),
        "success_rate": round(row["success_rate"], 1),
        "details": json.loads(row["details"])
    }

def clear_db():
    """Vide l'historique de la base de données."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runs")
    conn.commit()
    conn.close()
