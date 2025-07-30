# models/session.py
import sqlite3

class Session:
    """Model for the 'session' table."""
    def __init__(self, db):
        self.db = db

    def create(self, request_id, instructor_id, learner_id, session_date):
        """Creates a new session record, linking a request to an instructor."""
        sql = "INSERT INTO session (requestID, instructorID, learnerID, sessionDate) VALUES (?, ?, ?, ?)"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (request_id, instructor_id, learner_id, session_date))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error creating session: {e}")
            return None

    def get_by_instructor(self, instructor_id):
        """Retrieves all sessions for a specific instructor, including learner and skill info."""
        sql = """
            SELECT s.sessionID, s.sessionDate, s.status, u.userName as learnerName, r.reqSkills, s.learnerID
            FROM session s
            JOIN user u ON s.learnerID = u.userId
            JOIN request r ON s.requestID = r.reqId
            WHERE s.instructorID = ?
            ORDER BY s.sessionDate DESC
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (instructor_id,))
            return cursor.fetchall()

    def get_by_learner(self, learner_id):
        """Retrieves all sessions for a specific learner, including instructor info."""
        sql = """
            SELECT s.sessionID, s.sessionDate, s.status, u.userName as instructorName, r.reqSkills
            FROM session s
            JOIN user u ON s.instructorID = u.userId
            JOIN request r ON s.requestID = r.reqId
            WHERE s.learnerID = ?
            ORDER BY s.sessionDate DESC
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (learner_id,))
            return cursor.fetchall()

    def update_status(self, session_id, status):
        """Updates the status of a session (e.g., 'approved', 'completed')."""
        sql = "UPDATE session SET status = ? WHERE sessionID = ?"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (status, session_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error updating session status: {e}")
            return False
