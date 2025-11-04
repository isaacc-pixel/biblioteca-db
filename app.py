from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import (
    logout_user,
    login_user,
    current_user,
    login_required,
    LoginManager,
    UserMixin,
)
from database.db import initDB, initBooks, addUser, getUserById, getUserByEmail

initDB()

#initBooks() #TODO

app = Flask(__name__)
app.config["SECRET_KEY"] = "CHAVE SUPER SECRETA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        # self.nome = nome

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(id):
    user = getUserById(id)
    return User(id, user["Nome_usuario"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        print(user)

        if not user:
            senha_hash = generate_password_hash(senha)
            addUser(nome, email, telefone, senha_hash)
        else:
            flash("Este email já está cadastrado", "error")
            return redirect(url_for("cadastro"))
        return redirect(url_for("login"))
    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        if user is not None:
            if check_password_hash(user["Senha_hash"], senha):
                login_user(User(user["ID_usuario"], user["Nome_usuario"]))

        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
