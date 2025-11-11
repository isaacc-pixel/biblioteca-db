import mysql.connector
from datetime import date
from database.config import USER, HOST, PORT, DATABASE, PASSWORD, SQL_BASE, SQL_INSERTS
from werkzeug.security import generate_password_hash


def connect() -> mysql.connector.MySQLConnection:
    conn = mysql.connector.connect(
        user=USER, host=HOST, port=PORT, database=DATABASE, password=PASSWORD
    )

    return conn


def initDB():
    try:
        conn = connect()
        conn.close()
    except:
        conn = mysql.connector.connect(
            user=USER, host=HOST, port=PORT, password=PASSWORD
        )

        cur = conn.cursor()
        with open(SQL_BASE, "r") as base:
            cur.execute(base.read())
        cur.close()

        conn.close()
        pswd_hash = generate_password_hash('admin')

        initBooks()
        addUser(nome='admin', email='admin@admin', senha_hash=pswd_hash, admin=True)


def initBooks():
    conn = connect()
    cur = conn.cursor()

    with open(SQL_INSERTS, "r", encoding="utf-8") as inserts:
        sql = inserts.read()

    for query in sql.split(";"):
        # print('+'*40)
        # print(query)
        # print(query.strip())
        if query.strip():
            cur.execute(query.strip())

    conn.commit()
    cur.close()
    conn.close()


def getBooks():
    query = """
        SELECT 
            l.*,
            g.nome_genero,
            a.nome_autor,
            e.nome_editora
        FROM livros l
        INNER JOIN generos g
            ON l.genero_id = g.id_genero
        INNER JOIN autores a
            ON l.autor_id = a.id_autor
        INNER JOIN editoras e
            ON l.editora_id = e.id_editora
    """
    with connect() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query)
        livros = cur.fetchall()
        cur.close()
    return livros


def addUserBook(user_id, book_id):
    user_id = int(user_id)
    book_id = int(book_id)

    data_emprestimo = date.today()

    if data_emprestimo.day + 7 > 31:
        devolucao_prevista = date(
            data_emprestimo.year,
            data_emprestimo.month + 1,
            data_emprestimo.day + 7 - 31,
        )
    else:
        devolucao_prevista = date(
            data_emprestimo.year, data_emprestimo.month, data_emprestimo.day + 7
        )

    data_emprestimo = data_emprestimo

    query = """
        INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo, data_devolucao_prevista, status_emprestimo) 
        VALUES(
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            query, (user_id, book_id, data_emprestimo, devolucao_prevista, "pendente")
        )
        conn.commit()
        cur.close()


def getUserBooks(user_id):
    query = """
        SELECT 
            l.*,
            ep.*,
            g.nome_genero,
            a.nome_autor,
            e.nome_editora
        FROM usuarios u
        INNER JOIN emprestimos ep
            ON u.id_usuario = ep.usuario_id
        INNER JOIN livros l
            ON l.id_livro = ep.livro_id

        INNER JOIN generos g
            ON l.genero_id = g.id_genero
        INNER JOIN autores a
            ON l.autor_id = a.id_autor
        INNER JOIN editoras e
            ON l.editora_id = e.id_editora
        WHERE u.id_usuario = %s
        ORDER BY FIELD(status_emprestimo, 'atrasado', 'pendente','devolvido')
    """
    with connect() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, (user_id,))
        livros = cur.fetchall()
        cur.close()
    return livros


def returnBook(emprestimo_id):
    # depois fazer adicionar na multa se estiver atrasado
    data_devolucao = date.today()

    query = """
        UPDATE emprestimos
        SET 
            status_emprestimo='devolvido',
            data_devolucao_real=%s
        WHERE id_emprestimo=%s
    """

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, (data_devolucao, emprestimo_id))
        conn.commit()
        cur.close()


def addUser(nome, email, senha_hash, numero = None, admin = False):
    conn = connect()
    cur = conn.cursor()

    adduser = """
        INSERT INTO usuarios (nome_usuario, email, numero_telefone, senha_hash, data_inscricao, admin)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = date.today()

    usuario = (nome, email, numero, senha_hash, data, admin)

    cur.execute(adduser, usuario)

    conn.commit()
    cur.close()
    conn.close()


def getUserById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM usuarios
        WHERE id_usuario = %s
    """

    cur.execute(query, (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def getUserByEmail(email):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM usuarios
        WHERE email = %s
    """

    cur.execute(query, (email,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user

def addAuthor(nome, nacionalidade, data_nascimento, biografia):
    query = '''
        INSERT INTO autores(nome_autor, nacionalidade, data_nascimento, biografia) VALUES
        (%s, %s, %s, %s)

    '''
    params = (nome, nacionalidade, data_nascimento, biografia)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()     

def getAuthors():
    query = '''SELECT * FROM autores'''

    with connect() as conn:
        cur = conn.cursor(dictionary=True)

        cur.execute(query)
        results = cur.fetchall()
        
        cur.close()     
    return results

def addBook(titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo):
    query = '''
        INSERT INTO livros(titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)

    '''
    params = (titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()

def addPublisher(nome, endereco):
    query = '''
        INSERT INTO editoras(nome_editora, endereco_editora) VALUES
        (%s, %s)

    '''
    params = (nome, endereco)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()

def getPublishers():
    query = '''SELECT * FROM editoras'''

    with connect() as conn:
        cur = conn.cursor(dictionary=True)

        cur.execute(query)
        results = cur.fetchall()
        
        cur.close()     
    return results


def getGenres():
    query = '''SELECT * FROM generos'''

    with connect() as conn:
        cur = conn.cursor(dictionary=True)

        cur.execute(query)
        results = cur.fetchall()
        
        cur.close()     
    return results

def deleteBook(id):
    query = '''
        DELETE FROM livros
        WHERE id_livro = %s
    '''

    params = (id)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()

def deleteAuthor(id):
    query = '''
        DELETE FROM autores
        WHERE id_autor = %s
    '''

    params = (id)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()

def deletePublishers(id):
    query = '''
        DELETE FROM editoras
        WHERE id_editora = %s
    '''

    params = (id)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()


def getPublisherById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM editoras
        WHERE id_editora = %s
    """

    cur.execute(query, (id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def getAuthorById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM autores
        WHERE id_autor = %s
    """

    cur.execute(query, (id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def getBookById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM livros
        WHERE id_livro = %s
    """

    cur.execute(query, (id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


# def updatePublishers(id_editora, titulo, autor_id, isbn, ano_publicacao, genero_id, editora_id, quantidade_disponivel, resumo):
#     query = '''
#         UPDATE editoras
#         SET titulo=%s, autor_id=%s, isbn=%s, ano_publicacao=%s, genero_id=%s, editora_id=%s, quantidade_disponivel=%s, resumo=%s
#         WHERE id_editora = %s
#     '''
    
#     params = (
#         titulo, 
#         autor_id, 
#         isbn, 
#         ano_publicacao, 
#         genero_id, 
#         editora_id, 
#         quantidade_disponivel, 
#         resumo, 
#         id_editora
#     )

#     antes = getPublisherById(id_editora)

#     if 

#     with connect() as conn:
#         cur = conn.cursor()
#         cur.execute(query, params)
#         conn.commit()
#         cur.close()