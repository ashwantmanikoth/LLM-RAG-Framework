import sqlite3
from pathlib import Path

# Database file path
DB_FILE = "./feedback.db"

# Initialize the database and table
def setup_database():
    db = sqlite3.connect(DB_FILE)
    try:
        # Check if the table exists
        db.execute("SELECT * FROM history").fetchall()
    except sqlite3.OperationalError:
        # Create the table if it doesn't exist
        db.execute('''
            CREATE TABLE history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                user_input TEXT,
                output TEXT
            )
        ''')
        db.commit()
    db.close()

# Add feedback to the database
def store_feedback(model: str, user_input: str, output: str) -> bool:
    try:
        setup_database()
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO history (model, user_input, output) VALUES (?, ?, ?)", 
            (model, user_input, output)
        )
        db.commit()
        db.close()
        return True
    except Exception as e:
        return False

def format_feedback_for_table() -> list[list]:
    """
    Convert the list of dicts from retrieve_feedback() into
    a list of lists suitable for displaying in gr.DataFrame.
    """
    data = retrieve_feedback()

    # The first sub-list is used as the header row if we pass headers="first_row" to gr.DataFrame
    # table_data = [["id","Model Name", "User prompt", "LLM Response"]]
    table_data = []
    for row in data:
        table_data.append([
            row["id"],
            row["model"],
            row["user_input"],
            row["output"],
        ])
    return table_data

# Retrieve all feedback from the database
def retrieve_feedback() -> list[dict]:
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    rows = cursor.execute("SELECT id, model, user_input, output FROM history").fetchall()
    db.close()
    return [{"id": row[0], "model": row[1], "user_input": row[2],"output":row[3]} for row in rows]

# Load feedback data for initial display
def load_data():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    rows = cursor.execute("SELECT id, model, user_input, output FROM history").fetchall()
    db.close()
    return rows

def delete():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE history")
    db.commit()
    db.close()