# models/learner_stats.py
import sqlite3

class LearnerStats:
    """Model for the 'learner_stats' table."""
    def __init__(self, db):
        self.db = db

    def get_stats(self, learner_id):
        """Retrieves all learning statistics for a given learner."""
        sql = """
            SELECT s.skillName, ls.proficiencyScore, ls.sessionsCompleted
            FROM learner_stats ls
            JOIN skills s ON ls.skillID = s.skillID
            WHERE ls.learnerID = ?
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (learner_id,))
            return cursor.fetchall()

    def update_on_completion(self, learner_id, skill_id):
        """Increments the proficiency and session count for a learner and skill upon session completion."""
        sql = """
            INSERT INTO learner_stats (learnerID, skillID, proficiencyScore, sessionsCompleted)
            VALUES (?, ?, 1, 1)
            ON CONFLICT(learnerID, skillID) DO UPDATE SET
                proficiencyScore = proficiencyScore + 1,
                sessionsCompleted = sessionsCompleted + 1;
        """
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (learner_id, skill_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error updating stats: {e}")
            return False
