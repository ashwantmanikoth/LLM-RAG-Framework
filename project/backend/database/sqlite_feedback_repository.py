import sqlite3
from typing import List, Dict
from database.feedback_repository import FeedbackRepository


class SQLiteFeedbackRepository(FeedbackRepository):
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.setup_database()

    def setup_database(self):
        db = sqlite3.connect(self.db_file)
        try:
            db.execute("SELECT * FROM history").fetchall()
        except sqlite3.OperationalError:
            db.execute(
                """
                CREATE TABLE history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT,
                    user_input TEXT,
                    output TEXT
                )
            """
            )
            db.commit()
        finally:
            db.close()

    def store_feedback(self, model: str, user_input: str, output: str) -> bool:
        try:
            db = sqlite3.connect(self.db_file)
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO history (model, user_input, output) VALUES (?, ?, ?)",
                (model, user_input, output),
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Error storing feedback: {e}")
            return False
        finally:
            db.close()

    def retrieve_feedback(self) -> List[Dict]:
        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()
        rows = cursor.execute(
            "SELECT id, model, user_input, output FROM history"
        ).fetchall()
        db.close()
        return [
            {"id": row[0], "model": row[1], "user_input": row[2], "output": row[3]}
            for row in rows
        ]

    def delete_all(self):
        db = sqlite3.connect(self.db_file)
        cursor = db.cursor()
        cursor.execute("DROP TABLE history")
        db.commit()
        db.close()
