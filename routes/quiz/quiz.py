from flask import Blueprint, render_template, request, session, redirect

from utils.quizDatabase import QuizDatabase
from utils.userDatabase import UserDatabase

quiz = Blueprint('quiz', __name__)


# Accès à la liste des quiz
@quiz.route('/', methods=['GET'])
def quiz_list():
    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/quiz/')

    page = int(request.args.get('page', 0))
    tag = request.args.get('tag', None)

    quiz_db = QuizDatabase()
    quiz_list = quiz_db.get_all_quizzes(tag=tag, page=page)
    title = "Liste des quiz"
    description = "Bienvenue sur learniz, l'application qui vous permet de créer vos propres quiz et de les partager avec vos amis. Créer, apprendre, partager sont nos valeurs. N'attendez plus, inscrivez-vous et rejoingnez la communauté !"
    
    return render_template('list.html', connected= 'email' in session, title=title, description=description, quiz_list=quiz_list, page=page)


# Accès à la page d'un quiz
@quiz.route('/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_view(quiz_id):
    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/quiz/' + str(quiz_id))

    quiz_db = QuizDatabase()
    quiz_info = quiz_db.get_quiz(quiz_id=quiz_id)

    if not quiz_info:
        return render_template('404.html', title="La page n'existe pas", description=""), 404

    quiz_questions = quiz_db.get_questions(quiz_id=quiz_id)
    user_id = user_db.get_user(email=session['email'])['id']

    if request.method == 'GET':
        is_owner = quiz_db.is_quiz_owner(quiz_id=quiz_id, user_id=user_id)

        if quiz_info and quiz_questions:
            return render_template('quiz.html', title=quiz_info['title'], description=quiz_info['description'], quiz_id=quiz_id, quiz_info=quiz_info, quiz_questions=quiz_questions, is_owner=is_owner)
        else:
            return render_template('404.html', title="La page n'existe pas", description=""), 404

    else:
        # POST
        if len(quiz_questions) != len(request.form):
            return "Une erreur est survenue", 400
        else:
            score = 0
            user_responses = list(request.form.items())
            for i in range(len(quiz_questions)):
                if len(user_responses[i]) != 2:
                    return "Une erreur est survenue", 400
                else:
                    if str(quiz_questions[i]['response']).lower() == str(user_responses[i][1]).lower():
                        score += 1

            user_db.set_score(user_id=user_id, quiz_id=quiz_id, score=score)
            return redirect('/quiz/' + str(quiz_id) + '/result')
