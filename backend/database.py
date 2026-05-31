import sqlite3
import os

class NewsDatabase:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    date TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_news(self, title: str, date: str, summary: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO news (title, date, summary, content)
                VALUES (?, ?, ?, ?)
            ''', (title, date, summary, content))
            conn.commit()

    def delete_news(self, news_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM news WHERE id = ?', (news_id,))
            conn.commit()

    def get_all_news(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, date, summary FROM news ORDER BY date DESC')
            return [dict(row) for row in cursor.fetchall()]

    def get_news_by_id(self, news_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, date, summary, content FROM news WHERE id = ?', (news_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
if __name__ == "__main__":
    print("This module is not meant to be run directly.")
