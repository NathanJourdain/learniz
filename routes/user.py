from flask import Blueprint, render_template, request, session, redirect
import re

from utils.userDatabase import UserDatabase

user = Blueprint('user', __name__)

# Accès à son profil


@user.route('/me/', methods=['GET', 'POST'])
def me():
    if 'email' not in session:
        return redirect('/auth/login/')

    description = "Accède à ton profil pour modifier tes informations ou voir tes quiz que tu as créé."

    user_db = UserDatabase()
    user = user_db.get_user(email=session['email'])

    if user is None:
        return redirect('/auth/login/')

    user_quiz = user_db.get_quizzes(user_id=user['id'])

    # GET
    if request.method == 'GET':
        return render_template('me.html', title="Mon profil", description=description, user=user, user_quiz=user_quiz)

    # POST
    else:
        if 'email' in request.form and 'pseudo' in request.form:

            if user['email'] != request.form['email']:
                if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', request.form['email']) is None:
                    return render_template('me.html', title="Mon profil",  description=description, user=user, user_quiz=user_quiz, error='L\'adresse mail n\'est pas valide')

                if user_db.is_email_used(email=request.form['email']):
                    return render_template('me.html', title="Mon profil", description=description, user=user, user_quiz=user_quiz, error="Cette adresse email est déjà utilisée.")

            if user['pseudo'] != request.form['pseudo']:
                if re.match(r'^[a-zA-Z0-9_]+$', request.form['pseudo']) is None:
                    return render_template('me.html', title="Mon profil",  description=description, user=user, user_quiz=user_quiz, error='Le pseudo n\'est pas valide')

                if user_db.is_pseudo_used(pseudo=request.form['pseudo']):
                    return render_template('me.html', title="Mon profil",  description=description, user=user, user_quiz=user_quiz, error="Ce pseudo est déjà utilisé.")

            user_db.update_infos(
                user[0], request.form['email'], request.form['pseudo'])
            session['email'] = request.form['email']
            return redirect('/user/me/')
