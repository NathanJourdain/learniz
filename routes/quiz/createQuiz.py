from flask import Blueprint, session, redirect, render_template, request, jsonify
import json

from utils.userDatabase import UserDatabase
from utils.quizDatabase import QuizDatabase


create_quiz = Blueprint('create-quiz', __name__)



@create_quiz.route('/', methods=['GET', 'POST'])
def create_quiz_home():

    user_db = UserDatabase()
    if not user_db.is_connected():
        return redirect('/auth/login?redirect=/create-quiz/')

    title = "Créer un quiz"
    description = "Créer tes propres quiz grâce à une interface simple et intuitive qui te permettra de créer n'importe quel quiz facilement et rapidement !"

    if request.method == 'GET':
        return render_template('create.html', title=title, description=description)

    else:
 
        datas: dict = json.loads(request.data)

        keys = datas.keys()

        if 'title' in keys and 'description' in keys and 'questions' in keys:
            if type(datas['title']) == str and type(datas['description']) == str and type(datas['questions']) == list and datas['title'] != '' and datas['description'] != '' and len(datas['questions']) > 0:
                
                for question in datas['questions']:
                   
                    if question['content'] == '' or question['response'] not in ('true', 'false'):
                        return '', 400

                quiz_db = QuizDatabase()

                user_id = user_db.get_user(email=session['email'])['id']
                
                if not user_id:
                    return redirect('/auth/login?redirect=/create-quiz/')

                if 'tag' in keys:
                    if type(datas['tag']) == str and datas['tag'] != '':
                        tag = datas['tag']
                    else: tag = ""

                quiz_id = quiz_db.insert_quiz(owner_id=user_id, title=datas['title'], description=datas['description'], tags=tag);
                
                quiz_db.set_questions(quiz_id=quiz_id, questions=datas['questions'])
                return jsonify({'quiz_id': quiz_id})

        return jsonify({'error': 'Veuillez remplir tout les champs'}), 400