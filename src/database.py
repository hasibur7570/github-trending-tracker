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

    def date_exists(self, date: str) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM trending_repos WHERE date= ? LIMIT 1", (date,))
        exists = cur.fetchone() is not None
        conn.close()
        return exists
    
    def insert_repos(self, date: str, repos= List[Tuple[str, int]]):
        conn = self._connect()
        cur = conn.cursor()
        cur.executemany(
            "INSERT OR REPLACE INTO trending_repos (date, repo_name, stars) VALUES (?, ?, ?)",
            [(date, name, int(stars)) for name, stars in repos]
        )
        conn.commit()
        conn.close()



    