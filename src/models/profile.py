# models/profile.py
import sqlite3

class Profile:
    """Model for the 'user_profiles' table."""
    def __init__(self, db):
        self.db = db

    def get(self, user_id):
        """Retrieves a user's profile data by their user ID."""
        sql = "SELECT * FROM user_profiles WHERE userID = ?"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()

    def create_or_update(self, user_id, profile_data):
        """
        Creates or updates a user's profile using an UPSERT operation.
        The profile_data is a dictionary with keys matching the table columns.
        """
        sql = """
            INSERT INTO user_profiles (
                userID, firstName, lastName, middleInitial, age, educationLevel,
                aboutMe, profilePicture, school, occupation, specialization, resumePath
            ) VALUES (
                :userID, :firstName, :lastName, :middleInitial, :age, :educationLevel,
                :aboutMe, :profilePicture, :school, :occupation, :specialization, :resumePath
            )
            ON CONFLICT(userID) DO UPDATE SET
                firstName = excluded.firstName,
                lastName = excluded.lastName,
                middleInitial = excluded.middleInitial,
                age = excluded.age,
                educationLevel = excluded.educationLevel,
                aboutMe = excluded.aboutMe,
                profilePicture = excluded.profilePicture,
                school = excluded.school,
                occupation = excluded.occupation,
                specialization = excluded.specialization,
                resumePath = excluded.resumePath;
        """
        try:
            # Ensure all keys exist in the dictionary to prevent errors
            defaults = {
                "firstName": None, "lastName": None, "middleInitial": None, "age": None,
                "educationLevel": None, "aboutMe": None, "profilePicture": None,
                "school": None, "occupation": None, "specialization": None, "resumePath": None
            }
            # Merge provided data with defaults
            full_data = {**defaults, **profile_data, "userID": user_id}

            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, full_data)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error updating profile: {e}")
            return False
