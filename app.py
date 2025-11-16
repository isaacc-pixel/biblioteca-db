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
from database.db import *

initDB()

app = Flask(__name__)
app.config["SECRET_KEY"] = "CHAVE SUPER SECRETA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, nome, admin):
        self.id = id
        self.nome = nome
        self.admin = admin
        # self.nome = nome

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(id):
    user = getUserById(id)
    return User(id, user["nome_usuario"], user["admin"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/livros")
def livros():
    livros = getBooks()
    nao_exibir = []
    if current_user.is_authenticated:
        livros_usuario = getUserBooks(current_user.id)

        for livro in livros_usuario:
            if livro["status_emprestimo"] != "devolvido":
                nao_exibir.append(livro["id_livro"])

    return render_template("livros/list.html", livros=livros, nao_exibir=nao_exibir)


@app.route("/livros/<livro_id>/emprestimo")
@login_required
def pegar_livro(livro_id):
    addUserBook(current_user.id, livro_id)
    flash("📚 Empréstimo realizado com sucesso!", "success")
    return redirect(url_for("livros"))


@app.route("/livros/<emprestimo_id>/devolver")
@login_required
def devolver_livro(emprestimo_id):
    returnBook(emprestimo_id)
    flash("📚 Devolução realizada com sucesso!", "success")
    return redirect(url_for("meus_emprestimos"))


@app.route("/meus-emprestimos")
@login_required
def meus_emprestimos():
    emprestimos = getUserBooks(current_user.id)

    return render_template("usuario/meus_emprestimos.html", emprestimos=emprestimos)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        if not user:
            senha_hash = generate_password_hash(senha)
            addUser(nome, email, senha_hash, telefone)
            return redirect(url_for("login"))
        else:
            flash("Este email já está cadastrado", "error")
            return redirect(url_for("cadastro"))
    return render_template("auth/cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        if user is not None:
            if check_password_hash(user["senha_hash"], senha):
                login_user(
                    User(user["id_usuario"],
                         user["nome_usuario"], user["admin"])
                )
            return redirect(url_for("index"))
        flash("Email ou senha incorreta", "error")

    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/autor/add", methods=["GET", "POST"])
@login_required
def adicionar_autor():
    if request.method == "POST":
        if current_user.admin == 1:
            nome = request.form.get("nome")
            nacionalidade = request.form.get("nacionalidade")
            data_nascimento = request.form.get("data_nascimento")
            biografia = request.form.get("biografia")
            if nome:
                print(data_nascimento)
                addAuthor(nome, nacionalidade, data_nascimento, biografia)
                flash('Autor adicionado com sucesso', 'success')
                return redirect(url_for("autores"))
            flash("Nome não pode estar vazio")

    return render_template("autores/add.html")


@app.route("/editora/add", methods=["GET", "POST"])
@login_required
def adicionar_editora():
    if request.method == "POST":
        if current_user.admin == 1:
            nome_editora = request.form.get("nome_editora")
            endereco_editora = request.form.get("endereco")
            if nome_editora:
                addPublisher(nome_editora, endereco_editora)
                flash('Editora adicionada com sucesso', 'success')

                return redirect(url_for("editoras"))
            flash("Nome não pode estar vazio")

    return render_template("/editoras/add.html")


@app.route("/livro/add", methods=["POST", "GET"])
@login_required
def adicionar_livro():
    if request.method == "POST":
        if current_user.admin == 1:
            titulo = request.form.get("titulo")
            autor_id = request.form.get("autor")
            isbn = request.form.get("isbn")
            ano_publicacao = request.form.get("ano_publicacao")
            genero_id = request.form.get("genero_id")
            editora_id = request.form.get("editora_id")
            quantidade_disponivel = request.form.get("quantidade_disponivel")
            resumo = request.form.get("resumo")

            if (
                titulo
                and autor_id
                and isbn
                and genero_id
                and editora_id
                and quantidade_disponivel
            ):
                addBook(titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo)
                flash('Livro adicionado com sucesso', 'success')

                return redirect(url_for("livros"))
            flash("Nome não pode estar vazio")
    generos = getGenres()
    editoras = getPublishers()
    autores = getAuthors()
    return render_template("livros/add.html", autores=autores, generos=generos, editoras=editoras)


@app.route("/autores")
def autores():
    autores = getAuthors()
    return render_template("autores/list.html", autores=autores)


@app.route("/editoras")
def editoras():
    editoras = getPublishers()
    return render_template("editoras/list.html", editoras=editoras)


@app.route("/autor/update/<autor_id>", methods=["GET", "POST"])
@login_required
def update_autor(autor_id):
    if request.method == "POST":
        if current_user.admin == 1:
            nome = request.form.get("nome")
            nacionalidade = request.form.get("nacionalidade")
            data_nascimento = request.form.get("data_nascimento")
            biografia = request.form.get("biografia")
            updateAuthor(autor_id, nome, nacionalidade, data_nascimento, biografia)
            flash('Autor atualizado com sucesso', 'success')

            return redirect(url_for("autores"))
    autor = getAuthorById(autor_id)
    return render_template("autores/update.html", autor=autor)


@app.route("/editora/update/<id_editora>", methods=["GET", "POST"])
@login_required
def update_editora(id_editora):
    editora = getPublisherById(id_editora)
    if request.method == "POST":
        if current_user.admin == 1:
            nome_editora = request.form.get("nome_editora")
            endereco = request.form.get("endereco")
            updatePublisher(id_editora, nome_editora, endereco)
            flash('Editora atualizada com sucesso', 'success')

            return redirect(url_for("editoras"))

    return render_template("editoras/update.html", editora=editora)


@app.route("/livro/update/<livro_id>", methods=["GET", "POST"])
@login_required
def update_livro(livro_id):
    if request.method == "POST":
        if current_user.admin == 1:
            titulo = request.form.get("titulo")
            autor_id = request.form.get("autor")
            isbn = request.form.get("isbn")
            ano_publicacao = request.form.get("ano_publicacao")
            genero_id = request.form.get("genero_id")
            editora_id = request.form.get("editora_id")
            quantidade_disponivel = request.form.get("quantidade_disponivel")
            resumo = request.form.get("resumo")

            updateBook(
                livro_id,
                titulo,
                autor_id,
                isbn,
                ano_publicacao,
                genero_id,
                editora_id,
                quantidade_disponivel,
                resumo,
            )
            flash('Livro atualizado com sucesso', 'success')
            return redirect(url_for("livros"))

    livro = getBookById(livro_id)
    autores = getAuthors()
    editoras = getPublishers()
    generos = getGenres()
    return render_template("livros/update.html", livro=livro, autores=autores, editoras=editoras, generos=generos)


@app.route("/autor/delete/<int:autor_id>", methods=["POST"])
@login_required
def delete_autor(autor_id):
    if current_user.admin == 1:
        for livro in getBooks():
            if autor_id == livro["autor_id"]:
                flash('Delete os livros relacionados antes de deletar este autor', 'error')
                return redirect(url_for("autores"))
        deleteAuthor(autor_id)
        flash('Autor deletado com sucesso', 'success')
        return redirect(url_for("autores"))
    return redirect(url_for("index"))

@app.route("/editora/delete/<int:id_editora>", methods=["POST"])
@login_required
def delete_editora(id_editora):
    if current_user.admin == 1:
        for livro in getBooks():
            if id_editora == livro["editora_id"]:
                flash('Delete os livros relacionados antes de deletar esta editora', 'error')
                return redirect(url_for("editoras"))
        deletePublisher(id_editora)
        flash('Editora deletada com sucesso', 'success')
        return redirect(url_for("editoras"))
    return redirect(url_for("index"))


@app.route("/livro/delete/<livro_id>", methods=["POST"])
@login_required
def delete_livro(livro_id):
    if current_user.admin == 1:
        deleteBook(livro_id)
        flash('Livro deletado com sucesso', 'success')
        return redirect(url_for("livros"))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
