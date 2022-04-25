import sqlite3


class QuizDatabase:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('./database/database.sqlite')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_quiz(self, quiz_id) -> sqlite3.Row:
        """Get quiz by id"""
        self.cursor.execute(
            "SELECT * FROM quiz WHERE id=?", (quiz_id,))
        return self.cursor.fetchone()

    def get_all_quizzes(self, tag:str, page:int) -> list:
        """Get all quizzes with a tag"""
        if tag is None:
            self.cursor.execute(
                """SELECT * FROM quiz 
                ORDER BY id DESC 
                LIMIT 20 OFFSET ?""",
                (page*20,)
            )
        else:
            self.cursor.execute(
                """SELECT * FROM quiz 
                WHERE tags LIKE ? 
                ORDER BY id DESC 
                LIMIT 20 OFFSET ?""",
                (f"%{tag}%", page*20)
            )

        return self.cursor.fetchall()

    def get_questions(self, quiz_id) -> list:
        """Get questions by quiz id"""
        self.cursor.execute(
            "SELECT * FROM questions WHERE quiz_id=?", (quiz_id,))
        return self.cursor.fetchall()

    def insert_quiz(self, owner_id: int, title: str, description: str, tags: str) -> int:
        """Insert a new quiz"""
        self.cursor.execute(
            "INSERT INTO quiz (owner_id, title, description, tags) VALUES (?, ?, ?, ?)",
            (owner_id, title[0:100], description[0:250], tags[0:50]))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def set_questions(self, quiz_id: int, questions: list) -> None:
        """Set the questions of a quiz"""
        self.cursor.execute(
            "DELETE FROM questions WHERE quiz_id=?", (quiz_id,))

        for question in questions:
            self.cursor.execute(
                "INSERT INTO questions (quiz_id, content, response) VALUES (?, ?, ?)",
                (quiz_id, question['content'][0:250], question['response']))
        self.connection.commit()

    def modif_infos(self, quiz_id: int, title: str, description: str) -> None:
        """Modify the infos of a quiz"""
        self.cursor.execute(f"UPDATE quiz SET title=?, description=? WHERE id=?", (title[0:100], description[0:250], quiz_id))
        self.connection.commit()

    def is_quiz_owner(self, quiz_id: int, user_id: int) -> bool:
        """Check if the user is the owner of the quiz"""
        self.cursor.execute(
            "SELECT 1 FROM quiz WHERE id=? AND owner_id=?",
            (quiz_id, user_id))
        return self.cursor.fetchone() is not None
    
    def delete_quiz(self, quiz_id) -> list:
        self.cursor.execute("DELETE FROM questions WHERE quiz_id=?",(quiz_id,))
        self.cursor.execute("DELETE FROM results WHERE quiz_id=?",(quiz_id,))
        self.cursor.execute("DELETE FROM quiz WHERE id=?",(quiz_id,))
        self.connection.commit()

    def get_top_classement(self, quiz_id: int) -> list:
        self.cursor.execute(
            """SELECT pseudo, result 
            FROM results as r JOIN users as u ON r.user_id = u.id 
            WHERE quiz_id=? 
            ORDER BY result DESC 
            LIMIT 10""",
            (quiz_id,)
        )
        return self.cursor.fetchall()
