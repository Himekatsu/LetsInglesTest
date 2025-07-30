# models/database.py
import sqlite3
import os

class Database:
    """Handles all database connections and operations."""
    def __init__(self, db_file):
        """Initializes the database connection."""
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            raise FileNotFoundError(f"Database file not found at: {self.db_file}")
        self.conn = None

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            # This allows accessing columns by name, which is very convenient.
            self.conn.row_factory = sqlite3.Row
            return self.conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def close(self):
        """Closes the database connection if it's open."""
        if self.conn:
            self.conn.close()

