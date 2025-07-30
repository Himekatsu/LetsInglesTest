# models/practice_material.py
import sqlite3
from datetime import datetime

class PracticeMaterial:
    """Model for the 'practice_material' table."""
    def __init__(self, db):
        self.db = db

    def create(self, learner_id, instructor_id, skill_id, title, link):
        """Creates a new practice material record."""
        sql = """
            INSERT INTO practice_material (learnerID, instructorID, skillID, materialTitle, materialLink, submittedDate)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        submitted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (learner_id, instructor_id, skill_id, title, link, submitted_date))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error creating practice material: {e}")
            return None

    def get_for_learner(self, learner_id):
        """Retrieves all practice materials for a specific learner."""
        sql = """
            SELECT pm.materialTitle, pm.materialLink, pm.submittedDate, s.skillName, u.userName as instructorName
            FROM practice_material pm
            JOIN skills s ON pm.skillID = s.skillID
            JOIN user u ON pm.instructorID = u.userId
            WHERE pm.learnerID = ?
            ORDER BY pm.submittedDate DESC
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (learner_id,))
            return cursor.fetchall()
