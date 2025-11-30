"""Log export utility module.

This module provides functionality to export scan logs.
"""

import sqlite3
import os
import json
from datetime import datetime


def get_db_path():
    """Get the database path."""
    locations = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite'),
        os.path.join(os.getcwd(), 'db.sqlite'),
    ]
    
    for path in locations:
        if os.path.exists(path):
            return path
    
    return locations[0]


def export_scan_logs(format: str = "list") -> list:
    """Export scan logs from the database.
    
    Args:
        format: Output format ('list' or 'dict').
        
    Returns:
        list: Scan log records.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            if format == "dict":
                conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM scan_logs ORDER BY id DESC")
            rows = c.fetchall()
            
            if format == "dict":
                return [dict(row) for row in rows]
            return rows
    except sqlite3.OperationalError:
        return []


def export_logs_to_json(filepath: str = "scan_logs_export.json") -> str:
    """Export scan logs to a JSON file.
    
    Args:
        filepath: Output file path.
        
    Returns:
        str: Path to the exported file.
    """
    logs = export_scan_logs(format="dict")
    
    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "total_records": len(logs),
        "logs": logs
    }
    
    with open(filepath, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return filepath


def get_logs_by_risk(min_risk: int = 0) -> list:
    """Get logs filtered by minimum risk score.
    
    Args:
        min_risk: Minimum risk score to filter by.
        
    Returns:
        list: Filtered log records.
    """
    db_path = get_db_path()
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                "SELECT * FROM scan_logs WHERE risk_score >= ? ORDER BY risk_score DESC",
                (min_risk,)
            )
            return [dict(row) for row in c.fetchall()]
    except sqlite3.OperationalError:
        return []
