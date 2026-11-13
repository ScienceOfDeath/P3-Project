import os
import sqlite3

DB_PATH = os.environ.get("BOARD_DB", os.path.join(os.path.dirname(__file__), "board.db"))

