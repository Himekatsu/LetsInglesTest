# models/assignment.py
import sqlite3
from datetime import datetime

class Assignment:
    """Model for the 'assignments' and 'submissions' tables."""
    def __init__(self, db):
        self.db = db

    def create(self, instructor_id, skill_id, title, description, due_date):
        """Creates a new assignment."""
        sql = "INSERT INTO assignments (instructorID, skillID, title, description, dueDate) VALUES (?, ?, ?, ?, ?)"
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (instructor_id, skill_id, title, description, due_date))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error creating assignment: {e}")
            return None

    def get_all(self):
        """Retrieves all assignments for learners to view."""
        sql = """
            SELECT a.assignmentID, a.title, a.description, a.dueDate, s.skillName, u.userName as instructorName
            FROM assignments a
            JOIN skills s ON a.skillID = s.skillID
            JOIN user u ON a.instructorID = u.userId
            ORDER BY a.dueDate DESC
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def submit(self, assignment_id, learner_id):
        """Creates a submission record for a learner."""
        sql = "INSERT INTO submissions (assignmentID, learnerID, submissionDate) VALUES (?, ?, ?)"
        sub_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (assignment_id, learner_id, sub_date))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error creating submission: {e}")
            return False

    def get_submissions_by_learner(self, learner_id):
        """Checks which assignments a learner has submitted."""
        sql = "SELECT assignmentID FROM submissions WHERE learnerID = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (learner_id,))
            return [row['assignmentID'] for row in cursor.fetchall()]

