# models/user.py
import sqlite3
import hashlib

class User:
    """Model for the 'user' table."""
    def __init__(self, db):
        self.db = db

    @staticmethod
    def _hash_password(password):
        """Hashes the password using SHA256 for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self, user_role, user_name, user_pass, user_email, user_lat=None, user_long=None):
        """Creates a new user in the database."""
        hashed_pass = self._hash_password(user_pass)
        sql = '''INSERT INTO user(userRole, userName, userPass, userEmail, userLat, userLong)
                 VALUES(?,?,?,?,?,?)'''
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (user_role, user_name, hashed_pass, user_email, user_lat, user_long))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return "Error: Username or email already exists."
        except sqlite3.Error as e:
            return f"Database error: {e}"

    def authenticate(self, user_name, password):
        """Authenticates a user by checking username and hashed password."""
        user = self.get_by_username(user_name)
        if user and user['userPass'] == self._hash_password(password):
            return user
        return None

    def get_by_username(self, user_name):
        """Retrieves a single user by their username."""
        sql = "SELECT * FROM user WHERE userName = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_name,))
            return cursor.fetchone()

    def check_username(self, user_name):
        """Checks if a username already exists. Returns True if it exists, False otherwise."""
        sql = "SELECT 1 FROM user WHERE userName = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_name,))
            return cursor.fetchone() is not None

    def get_all_instructors(self):
        """Retrieves all users with the 'instructor' role."""
        sql = "SELECT * FROM user WHERE userRole = 'instructor'"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def get_instructor_availability(self, instructor_id):
        """Gets the weekly availability for a specific instructor."""
        sql = "SELECT day, startTime, endTime FROM instructor_availability WHERE instructorID = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (instructor_id,))
            return cursor.fetchall()

    def get_instructor_skills(self, instructor_id):
        """Gets the skill IDs for a specific instructor."""
        sql = "SELECT skillID FROM instructor_skills WHERE instructorID = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            return [row['skillID'] for row in cursor.fetchall()]
