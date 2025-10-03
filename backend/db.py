"""
Database operations for the ESP32 control system.
This module handles all database interactions for event logging and management.
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from typing import List, Tuple, Optional

# Import configuration
from .config import DATABASE_PATH

@contextmanager
def db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db() -> None:
    """Initialize the database and create required tables."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                command TEXT NOT NULL
            )
        ''')
        conn.commit()

def log_event(command: str) -> None:
    """Log a new event to the database.
    
    Args:
        command: The command to log
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO events (timestamp, command) VALUES (?, ?)",
            (timestamp, command)
        )
        conn.commit()

def update_event(event_id: int, new_command: str) -> None:
    """Update an existing event in the database.
    
    Args:
        event_id: The ID of the event to update
        new_command: The new command value
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE events SET command = ? WHERE id = ?",
            (new_command, event_id)
        )
        conn.commit()

def delete_event(event_id: int) -> None:
    """Delete an event from the database.
    
    Args:
        event_id: The ID of the event to delete
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()

def get_events() -> List[Tuple[int, str, str]]:
    """Retrieve all events from the database.
    
    Returns:
        List of tuples containing (id, timestamp, command)
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, timestamp, command FROM events ORDER BY id DESC')
        return cursor.fetchall()

def delete_db() -> bool:
    """Delete the entire database file.
    
    Returns:
        bool: True if database was deleted, False if it didn't exist
    """
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"Base de datos '{DATABASE_PATH}' eliminada.")
        return True
    print(f"Base de datos '{DATABASE_PATH}' no existe.")
    return False
