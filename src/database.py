import sqlite3
import os
from typing import List, Tuple
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        parent = os.path.dirname(os.path.abspath(db_path))
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        self._create_table()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def _create_table(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS trending_repos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    repo_name TEXT NOT NULL,
                    stars INTEGER DEFAULT 0,
                    UNIQUE(date, repo_name)
                    )
                """)
        conn.commit()
        conn.close()


    