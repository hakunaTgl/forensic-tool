"""Smart API module.

This module provides database operations for logging scan results.
"""

import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_db_path():
    """Get the database path.
    
    Returns:
        str: Path to the SQLite database.
    """
    # Try finding db.sqlite in various locations
    locations = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite'),
        os.path.join(os.getcwd(), 'db.sqlite'),
    ]
    
    for path in locations:
        if os.path.exists(path):
            return path
    
    return locations[0]


def init_database():
    """Initialize the database with required tables.
    
    Creates the scan_logs table if it doesn't exist.
    """
    db_path = get_db_path()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apk_name TEXT NOT NULL,
                risk_score INTEGER DEFAULT 0,
                permissions TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
    
    logger.info(f"Database initialized at {db_path}")


def log_scan(apk_name: str, risk_score: int, permissions: list, timestamp: str = None):
    """Log a scan result to the database.
    
    Args:
        apk_name: Name of the scanned APK file.
        risk_score: Calculated risk score.
        permissions: List of permissions found.
        timestamp: ISO format timestamp (optional).
    """
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()
    
    db_path = get_db_path()
    
    # Ensure table exists
    init_database()
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            
            # Convert permissions list to string
            if isinstance(permissions, list):
                permissions_str = ','.join(permissions)
            else:
                permissions_str = str(permissions) if permissions else ''
            
            c.execute('''
                INSERT INTO scan_logs (apk_name, risk_score, permissions, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (apk_name, risk_score, permissions_str, timestamp))
            conn.commit()
            
        logger.info(f"Logged scan for {apk_name} with risk score {risk_score}")
    except Exception as e:
        logger.error(f"Failed to log scan: {e}")
        raise


def get_recent_scans(limit: int = 10) -> list:
    """Get recent scan logs.
    
    Args:
        limit: Maximum number of records to return.
        
    Returns:
        list: List of recent scan records.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                "SELECT * FROM scan_logs ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in c.fetchall()]
    except sqlite3.OperationalError:
        return []


def clear_old_logs(days: int = 30):
    """Clear logs older than specified days.
    
    Args:
        days: Number of days to keep logs.
    """
    db_path = get_db_path()
    cutoff = datetime.utcnow()
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "DELETE FROM scan_logs WHERE timestamp < datetime('now', '-? days')",
                (days,)
            )
            conn.commit()
            logger.info(f"Cleared logs older than {days} days")
    except Exception as e:
        logger.error(f"Failed to clear old logs: {e}")
