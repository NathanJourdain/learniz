from flask import Blueprint, session, redirect, render_template, request

from utils.userDatabase import UserDatabase
from utils.quizDatabase import QuizDatabase

result_quiz = Blueprint('result-quiz', __name__)

@result_quiz.route('/<int:quiz_id>/result', methods=['GET'])
def result_quiz_view(quiz_id):
    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/result-quiz/' + str(quiz_id))

    title = "Résultat du quiz"

    quiz_db = QuizDatabase()
    quiz_info = quiz_db.get_quiz(quiz_id=quiz_id)
    nb_questions = len(quiz_db.get_questions(quiz_id=quiz_id))

    user = user_db.get_user(email=session['email'])
    score = user_db.get_score(user_id=user['id'], quiz_id=quiz_id)

    if score is not None:
        score = score['result']
        top_classement = quiz_db.get_top_classement(quiz_id=quiz_id)
        return render_template('result.html', title=title, description=quiz_info['description'], quiz_info=quiz_info, score=score, top_classement=top_classement, nb_questions=nb_questions)
    else:
        return redirect('/quiz/' + str(quiz_id))

