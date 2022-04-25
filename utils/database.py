import sqlite3

class Database:
    def __init__(self) -> None:
        self.database_name = './database/database.sqlite'
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def is_email_used(self, email: str) -> bool:
        self.cursor.execute(f"SELECT * FROM users WHERE lower(email)=lower(?)", (email,))
        return self.cursor.fetchone() is not None
    
    def is_pseudo_used(self, pseudo: str) -> bool:
        self.cursor.execute(f"SELECT * FROM users WHERE lower(pseudo)=lower(?)", (pseudo,))
        return self.cursor.fetchone() is not None
    
    def is_email_used_by_user(self, email: str, user_id: int) -> bool:
        self.cursor.execute(f"SELECT * FROM users WHERE lower(email)=lower(?) AND id!=?", (email, user_id))
        return self.cursor.fetchone() is not None
    def is_pseudo_used_by_user(self, pseudo: str, user_id: int) -> bool:
        self.cursor.execute(f"SELECT * FROM users WHERE lower(pseudo)=lower(?) AND id!=?", (pseudo, user_id))
        return self.cursor.fetchone() is not None


    def is_good_password(self, email: str, password: str) -> bool:
        self.cursor.execute(f"SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return self.cursor.fetchone() is not None


    def add_user(self, email: str, password: str, pseudo: str) -> None:
        self.cursor.execute(f"INSERT INTO users (email, password, pseudo) VALUES (?, ?, ?)", (email, password, pseudo))
        self.connection.commit()

    def update_user(self, user_id, email: str, pseudo: str):
        self.cursor.execute(
            "UPDATE users SET email=?, pseudo=? WHERE id=?",
            (email, pseudo, user_id)
        )
        self.connection.commit()


    # USERS FUNCTION
    def get_userid_by_email(self, email: str) -> dict:
        self.cursor.execute(f"SELECT id FROM users WHERE email=?", (email,))
        return self.cursor.fetchone()[0]

    def get_user_by_email(self, email: str) -> dict:
        self.cursor.execute(f"SELECT id, pseudo, email FROM users WHERE email=?", (email,))
        return self.cursor.fetchone()


    # quiz FUNCTION
    def add_quiz(self, owner_id:int, title: str, description: str, tag: str) -> int:
        self.cursor.execute(f"INSERT INTO quiz (owner_id, title, description, tags) VALUES (?, ?, ?,?)", (owner_id, title[0:100], description[0:250], tag[0:50]))
        self.connection.commit()
        return self.cursor.lastrowid

    def modif_quiz_infos(self, quiz_id: int, title: str, description: str) -> None:
        self.cursor.execute(f"UPDATE quiz SET title=?, description=? WHERE id=?", (title[0:100], description[0:250], quiz_id))
        self.connection.commit()

    def set_quiz_questions(self, quiz_id: int, questions: list) -> None:
        self.cursor.execute(f"DELETE FROM questions WHERE quiz_id=?", (quiz_id,))
        self.connection.commit()
        for question in questions:
            self.cursor.execute("INSERT INTO questions VALUES(?,?,?)",
            (quiz_id, question['content'][0:250], question['response'])
            )
        self.connection.commit()

    def get_user_quiz(self, user_id) -> list:
        self.cursor.execute(f"SELECT id, title FROM quiz WHERE owner_id=?", (user_id,))
        return self.cursor.fetchall()


    def get_quiz_info(self, quiz_id: int):
        self.cursor.execute(
            """SELECT title, description, tags FROM quiz WHERE id=?""",
            (quiz_id,)
        )
        return self.cursor.fetchone()
    
    def get_quiz_questions(self, quiz_id: int):
        self.cursor.execute(
            "SELECT content, response FROM questions WHERE quiz_id=?",
            (quiz_id,)
        )
        questions = self.cursor.fetchall()
        for i in range(len(questions)):
            questions[i] = questions[i] + (i,)
        return questions

    def is_quiz_owner(self, quiz_id: int, user_id: int):
        self.cursor.execute(
            "SELECT 1 FROM quiz WHERE id=? AND owner_id=?",
            (quiz_id, user_id)
        )
        return self.cursor.fetchone() is not None


    def get_quiz_list(self, tag: str) -> list:
        if tag:
            self.cursor.execute("SELECT id, title, description FROM quiz WHERE tags LIKE ? LIMIT 100", (f"%{tag}%",))
            return self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT id, title, description FROM quiz")
            return self.cursor.fetchall()

    def delete_quiz(self, quiz_id) -> list:
        self.cursor.execute("DELETE FROM quiz WHERE id=?",(quiz_id,))
        self.cursor.execute("DELETE FROM results WHERE quiz_id=?",(quiz_id,))
        self.cursor.execute("DELETE FROM questions WHERE quiz_id=?",(quiz_id,))
        self.connection.commit()


    # Score FUNCTION
    def get_user_score(self, user_id, quiz_id: int):
        self.cursor.execute(
            "SELECT result FROM results WHERE user_id=? AND quiz_id=?",
            (user_id, quiz_id)
        )
        return self.cursor.fetchone()

    def set_user_score(self, user_id, quiz_id, score: int):
        old_score = self.get_user_score(user_id, quiz_id)
        if old_score is None:
            query = "INSERT INTO results VALUES({}, {}, {})".format(quiz_id, user_id, score)
        else:
            query = "UPDATE results SET result={} WHERE user_id={} AND quiz_id={}".format(score, user_id, quiz_id)
        
        self.cursor.execute(query)
        self.connection.commit()

    
    def get_top_classement(self, quiz_id: int) -> list:
        self.cursor.execute(
            "SELECT u.pseudo, r.result FROM results as r JOIN users as u ON r.user_id = u.id WHERE r.quiz_id=? ORDER BY result DESC LIMIT 10",
            (quiz_id,)
        )
        return self.cursor.fetchall()