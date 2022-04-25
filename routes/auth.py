from flask import Blueprint, session, redirect, request, render_template
from flask_hashing import Hashing
import re

from utils.userDatabase import UserDatabase

auth = Blueprint('auth', __name__)

description = "Bienvenue sur learniz, l'application qui vous permet de créer vos propres quiz et de les partager avec vos amis. Créer, apprendre, partager sont nos valeurs. N'attendez plus, inscrivez-vous et rejoingnez la communauté !"

@auth.route('/login/', methods=['GET', 'POST'])
def sign_in():
    title = "Connexion"
    
    if request.method == 'GET':
        # GET 
        return render_template('login.html', title=title, description=description)
    else:
        # POST
        form = request.form
        if 'email' in form and 'password' in form:
            email = form['email']
            password = form['password']
            
            if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email) is not None:
                # Check if password is correct
                hasher = Hashing()
                hashed_password = hasher.hash_value(password)
                user_db = UserDatabase()
                if user_db.is_good_password(email, hashed_password):
                    session['email'] = email
                    if 'redirect' in request.args:
                        return redirect(request.args['redirect'])
                    else:
                        return redirect('/')
            
            # Password is incorrect or email is not valid
            return render_template('login.html', title=title, description=description, error='Adresse mail ou mot de passe incorrect')
    

@auth.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    title = "Inscription"

    if request.method == 'GET':
        # GET
        return render_template('sign-up.html', title=title, description=description)
    else:
        # POST
        form = request.form
        
        if 'pseudo' in form and 'email' in form and 'password' in form and 'confirm_password' in form:

            pseudo = form['pseudo']
            email = form['email']
            password = form['password']
            confirm_password = form['confirm_password']

            # Verify data for sign up form
            if re.match(r'^[a-zA-Z0-9_]+$', pseudo) is None:
                return render_template('sign-up.html', title=title, description=description, error='Le pseudo n\'est pas valide')
            elif re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
                return render_template('sign-up.html', title=title, description=description, error='L\'adresse mail n\'est pas valide')
            elif re.match(r'^\S*(?=\S{6,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])(?=\S*[!@#$%^&*?])\S*$', password) is None:
                return render_template('sign-up.html', title=title, description=description, error='Le mot de passe n\'est pas valide')
            elif password != confirm_password:
                return render_template('sign-up.html', title=title,  description=description,error='Les mots de passe ne correspondent pas')


            # Check if email is already used
            user_db = UserDatabase()
            if user_db.is_email_used(email):
                return render_template('sign-up.html', title=title, description=description, error='Cet email est déjà utilisé')
            
            # Check if pseudo is already used
            if user_db.is_pseudo_used(pseudo):
                return render_template('sign-up.html', title=title, description=description, error='Ce pseudo est déjà utilisé')

            # Hash password
            hasher = Hashing()
            hashed_password = hasher.hash_value(password)

            # Add user to database
            user_db.insert_user(email=email, password=hashed_password, pseudo=pseudo)
            session['email'] = email

            return redirect('/')

        else:
            return render_template('sign-up.html', title=title, description=description, error='Veuillez remplir tous les champs')


            


@auth.route('/logout/', methods=['GET'])
def logout():
    del session['email']
    return redirect("/")
