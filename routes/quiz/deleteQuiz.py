from flask import Blueprint, session, redirect, render_template, request

from utils.quizDatabase import QuizDatabase
from utils.userDatabase import UserDatabase

delete_quiz = Blueprint('delete-quiz', __name__)



@delete_quiz.route('/<int:quiz_id>', methods=['GET'])
def create_quiz_home(quiz_id: int):
    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/delete-quiz/' + str(quiz_id))

    user_id = user_db.get_user(email=session['email'])['id']
    quiz_db = QuizDatabase()

    if not quiz_db.is_quiz_owner(quiz_id=quiz_id, user_id=user_id):
        return render_template('404.html', title="La page n'existe pas"), 404
    else:
        quiz_db.delete_quiz(quiz_id=quiz_id)
        return redirect('/quiz/')
