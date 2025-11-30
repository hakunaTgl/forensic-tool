"""Log export module.

This module provides functionality to export scan logs from the database.
"""

import sqlite3
import os
from datetime import datetime


def get_db_path():
    """Get the database path.
    
    Returns:
        str: Absolute path to the database file.
    """
    # Try different locations
    locations = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite'),
        os.path.join(os.getcwd(), 'db.sqlite'),
    ]
    
    for path in locations:
        if os.path.exists(path):
            return path
    
    # Return default path (will be created if needed)
    return locations[0]


def export_logs(limit=100):
    """Export scan logs from the database.
    
    Args:
        limit: Maximum number of logs to retrieve (default: 100).
        
    Returns:
        list: List of log entries as tuples.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT ?", (limit,))
            logs = c.fetchall()
        return logs
    except sqlite3.OperationalError:
        # Table doesn't exist yet
        return []


def export_logs_as_dict(limit=100):
    """Export scan logs as a list of dictionaries.
    
    Args:
        limit: Maximum number of logs to retrieve.
        
    Returns:
        list: List of log entries as dictionaries.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT ?", (limit,))
            rows = c.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.OperationalError:
        return []


def get_logs_summary():
    """Get a summary of logged scans.
    
    Returns:
        dict: Summary statistics of scan logs.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            
            # Total scans
            c.execute("SELECT COUNT(*) FROM scan_logs")
            total = c.fetchone()[0]
            
            # Average risk score
            c.execute("SELECT AVG(risk_score) FROM scan_logs")
            avg_risk = c.fetchone()[0] or 0
            
            # High risk scans (score >= 5)
            c.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_score >= 5")
            high_risk = c.fetchone()[0]
            
            return {
                "total_scans": total,
                "average_risk_score": round(avg_risk, 2),
                "high_risk_scans": high_risk,
                "timestamp": datetime.utcnow().isoformat()
            }
    except sqlite3.OperationalError:
        return {
            "total_scans": 0,
            "average_risk_score": 0,
            "high_risk_scans": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
