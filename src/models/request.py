# models/request.py
import sqlite3

class Request:
    """Model for the 'request' table."""
    def __init__(self, db):
        self.db = db

    def create(self, user_id, req_skills, request_date):
        """Creates a new session request with 'pending' status."""
        sql = "INSERT INTO request(userId, reqSkills, requestDate, fulfilled) VALUES(?,?,?,?)"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (user_id, req_skills, request_date, 'pending'))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            return f"Database error creating request: {e}"

    def get_pending(self):
        """Retrieves all requests that are pending a match."""
        sql = """
            SELECT r.reqId, r.userId, r.reqSkills, r.requestDate, u.userName, u.userLat, u.userLong
            FROM request r
            JOIN user u ON r.userId = u.userId
            WHERE r.fulfilled = 'pending'
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def update_status(self, req_id, status):
        """Updates the status of a request (e.g., 'matched', 'cancelled')."""
        sql = "UPDATE request SET fulfilled = ? WHERE reqId = ?"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (status, req_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating request status: {e}")
            return False
