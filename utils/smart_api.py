# utils/smart_api.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite')

def log_scan(apk_name, risk_score, permissions, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apk_name TEXT,
                risk_score INTEGER,
                permissions TEXT,
                timestamp TEXT
            )
        ''')
        c.execute('''
            INSERT INTO scan_logs (apk_name, risk_score, permissions, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (apk_name, risk_score, ','.join(permissions), timestamp))
        conn.commit()

