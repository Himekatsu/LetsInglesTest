# models/feedback.py
import sqlite3
from datetime import datetime

class Feedback:
    """Model for the 'feedback' table."""
    def __init__(self, db):
        self.db = db

    def create(self, session_id, learner_id, rating, comment):
        """Creates a new feedback record for a completed session."""
        sql = "INSERT INTO feedback (sessionID, learnerID, rating, comment, feedbackDate) VALUES (?, ?, ?, ?, ?)"
        feedback_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (session_id, learner_id, rating, comment, feedback_date))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error creating feedback: {e}")
            return None

    def check_exists(self, session_id):
        """Checks if feedback already exists for a given session."""
        sql = "SELECT feedbackID FROM feedback WHERE sessionID = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (session_id,))
            return cursor.fetchone() is not None
