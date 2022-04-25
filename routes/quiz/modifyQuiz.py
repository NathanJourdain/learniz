from flask import Blueprint, session, redirect, render_template, request
import json

from utils.quizDatabase import QuizDatabase
from utils.userDatabase import UserDatabase

modify_quiz = Blueprint('modify-quiz', __name__)



@modify_quiz.route('/<int:quiz_id>', methods=['GET', 'POST'])
def create_quiz_home(quiz_id: int):
    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/modify-quiz/' + str(quiz_id))

    user_id = user_db.get_user(email=session['email'])['id']
    title = "Modifier le quiz"
    description = ""

    quiz_db = QuizDatabase()

    if request.method == 'GET':
        if not quiz_db.is_quiz_owner(quiz_id=quiz_id, user_id=user_id):
            return 'You are not the owner of this quiz'
        
        quiz_info = quiz_db.get_quiz(quiz_id=quiz_id)
        if not quiz_info:
            return 'This quiz does not exist'
            
        quiz_questions = quiz_db.get_questions(quiz_id=quiz_id)
        return render_template('modify.html', title=title, quiz_info=quiz_info, quiz_questions=quiz_questions, description=description)

    else:
        datas: dict = json.loads(request.data)
        
        keys = datas.keys()

        if not quiz_db.is_quiz_owner(quiz_id=quiz_id, user_id=user_id):
            return 'You are not the owner of this quiz'

        if 'title' in keys and 'description' in keys and 'questions' in keys:
            if type(datas['title']) == str and type(datas['description']) == str and type(datas['questions']) == list and len(datas['questions']) > 0:
                
                for question in datas['questions']:
                    if question['content'] == '' or question['response'] not in ('true', 'false'):
                        return '', 400

                quiz_db.modif_infos(quiz_id=quiz_id, title=datas['title'], description=datas['description']);
                quiz_db.set_questions(quiz_id=quiz_id, questions=datas['questions'])
                return json.dumps({'quiz_id': quiz_id})

        return 'error', 400