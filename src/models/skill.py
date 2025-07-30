# models/skill.py
import sqlite3

class Skill:
    """Model for the 'skills' table."""
    def __init__(self, db):
        self.db = db

    def get_all(self):
        """Retrieves all available skills."""
        sql = "SELECT * FROM skills ORDER BY skillName"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
