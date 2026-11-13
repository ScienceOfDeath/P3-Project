import os
import sqlite3

DB_PATH = os.environ.get("BOARD_DB", os.path.join(os.path.dirname(__file__), "board.db"))


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()
    connection.execute(
        """CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )"""
    )
    connection.commit()
    connection.close()


def add_comment(name, message):
    connection = get_db()
    connection.execute("INSERT INTO comments (name, message) VALUES (?, ?)", (name, message))
    connection.commit()
    connection.close()


def get_all_comments():
    connection = get_db()
    rows = connection.execute("SELECT id, name, message FROM comments ORDER BY id DESC").fetchall()
    connection.close()
    return rows