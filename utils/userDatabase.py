from flask import session
import sqlite3


class UserDatabase:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('./database/database.sqlite')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def is_email_used(self, email: str) -> bool:
        """Check if an email is already used"""
        self.cursor.execute(
            f"SELECT * FROM users WHERE lower(email)=lower(?)", (email,))
        return self.cursor.fetchone() is not None

    def is_pseudo_used(self, pseudo: str) -> bool:
        """Check if an email is already used"""
        self.cursor.execute(
            f"SELECT * FROM users WHERE lower(pseudo)=lower(?)", (pseudo,))
        return self.cursor.fetchone() is not None

    def is_good_password(self, email: str, password: str) -> bool:
        """Check if email and password are correct"""
        self.cursor.execute(
            f"SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return self.cursor.fetchone() is not None

    def get_user(self, email: str = "", user_id: int = None) -> sqlite3.Row:
        """Get user by email"""
        self.cursor.execute(
            f"SELECT id, pseudo, email FROM users WHERE email=? OR id = ?", (email,user_id))
        return self.cursor.fetchone()

    def insert_user(self, email: str, password: str, pseudo: str) -> None:
        """Insert a new user"""
        self.cursor.execute(
            f"INSERT INTO users (email, password, pseudo) VALUES (?, ?, ?)", (email, password, pseudo))
        self.connection.commit()

    def update_infos(self, user_id, email: str, pseudo: str):
        """Update user infos"""
        self.cursor.execute(
            "UPDATE users SET email=?, pseudo=? WHERE id=?", (email, pseudo, user_id))
        self.connection.commit()

    def update_password(self, user_id, password: str):
        """Update user password"""
        self.cursor.execute(
            "UPDATE users SET password=? WHERE id=?", (password, user_id))
        self.connection.commit()

    def get_quizzes(self, user_id: int) -> list:
        """Get quizzes by user id"""
        self.cursor.execute(
            f"SELECT * FROM quiz WHERE owner_id=?", (user_id,))
        return self.cursor.fetchall()

    def set_score(self, user_id: int, quiz_id: int, score: int) -> None:
        """Set the score of a user for a quiz"""
        if self.get_score(user_id=user_id, quiz_id=quiz_id) is None:
            self.cursor.execute(
                f"INSERT INTO results (user_id, quiz_id, result) VALUES (?, ?, ?)", (user_id, quiz_id, score))
        else:
            self.cursor.execute(
                f"UPDATE results SET result=? WHERE user_id=? AND quiz_id=?", (score, user_id, quiz_id))
        self.connection.commit()
    
    def get_score(self, user_id: int, quiz_id: int) -> int:
        """Get the score of a user for a quiz"""
        self.cursor.execute(
            f"SELECT result FROM results WHERE user_id=? AND quiz_id=?", (user_id, quiz_id))
        return self.cursor.fetchone()

    def is_connected(self):
        """Check if user is connected"""
        if 'email' not in session:
            return False
        user = self.get_user(email=session['email'])
        if user is None:
            return False
        return True
