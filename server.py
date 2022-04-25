from flask import Flask, render_template

# Import routes
from routes.auth import auth
from routes.quiz.createQuiz import create_quiz
from routes.quiz.modifyQuiz import modify_quiz
from routes.quiz.deleteQuiz import delete_quiz
from routes.quiz.resultQuiz import result_quiz
from routes.quiz.quiz import quiz
from routes.user import user

app = Flask(__name__)

app.secret_key = ""

# Path for our main page
@app.route("/")
def base():
    description = "Bienvenue sur learniz, l'application qui vous permet de créer vos propres quiz et de les partager avec vos amis. Créer, apprendre, partager sont nos valeurs. N'attendez plus, inscrivez-vous et rejoingnez la communauté !"
    return render_template("home.html", title="Accueil", description=description)


# Add routes
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(create_quiz, url_prefix="/create-quiz")
app.register_blueprint(modify_quiz, url_prefix="/modify-quiz")
app.register_blueprint(delete_quiz, url_prefix="/delete-quiz")
app.register_blueprint(result_quiz, url_prefix="/quiz/")
app.register_blueprint(quiz, url_prefix="/quiz")
app.register_blueprint(user, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=False)
