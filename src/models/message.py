# models/message.py
import sqlite3
from datetime import datetime

class Message:
    """Model for the 'messages' table."""
    def __init__(self, db):
        self.db = db

    def create(self, sender_id, receiver_id, content):
        """Creates a new message."""
        sql = "INSERT INTO messages (senderID, receiverID, content, timestamp) VALUES (?, ?, ?, ?)"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (sender_id, receiver_id, content, timestamp))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error creating message: {e}")
            return None

    def get_conversation_partners(self, user_id):
        """Gets a list of users someone has messaged or received messages from."""
        sql = """
            SELECT DISTINCT u.userId, u.userName
            FROM user u
            JOIN messages m ON u.userId = m.senderID OR u.userId = m.receiverID
            WHERE (m.senderID = ? OR m.receiverID = ?) AND u.userId != ?
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, user_id, user_id))
            return cursor.fetchall()

    def get_conversation(self, user1_id, user2_id):
        """Gets the full message history between two users."""
        sql = """
            SELECT m.*, u_sender.userName as senderName
            FROM messages m
            JOIN user u_sender ON m.senderID = u_sender.userId
            WHERE (senderID = ? AND receiverID = ?) OR (senderID = ? AND receiverID = ?)
            ORDER BY timestamp ASC
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user1_id, user2_id, user2_id, user1_id))
            return cursor.fetchall()
