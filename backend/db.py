def update_event(event_id, new_command):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET command = ? WHERE id = ?", (new_command, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
def delete_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Base de datos '{DB_FILE}' eliminada.")
    else:
        print(f"Base de datos '{DB_FILE}' no existe.")
import sqlite3
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "data", "events.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            command TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_event(command):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO events (timestamp, command) VALUES (?, ?)", (timestamp, command))
    conn.commit()
    conn.close()

def get_events():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, command FROM events ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows
