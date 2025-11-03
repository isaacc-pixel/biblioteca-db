import mysql.connector 
from datetime import datetime
from database.config import USER, HOST, PORT, DATABASE, SQL_BASE


def connect() -> mysql.connector.MySQLConnection:
    conn = mysql.connector.connect(
        user=USER, 
        host=HOST, 
        port=PORT, 
        database=DATABASE
    )

    return conn 


def initDB():
    try:
        conn = connect()
        conn.close()
    except:
        conn = mysql.connector.connect(
            user=USER, 
            host=HOST, 
            port=PORT
        )
        cur = conn.cursor()

        with open(SQL_BASE, 'r') as base:
            cur.execute(base.read())

        cur.close()
        conn.close()


def addUser(nome, email, numero, senha_hash):
    conn = connect()
    cur = conn.cursor()

    adduser = (
        "INSERT INTO Usuarios"
        "(Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    date = datetime.today().strftime("%Y-%m-%d")

    usuario = (nome, email, numero, senha_hash, date, 0)

    cur.execute(adduser, usuario)

    conn.commit()
    cur.close()
    conn.close()


def getUserById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = (
        "SELECT Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual"
        "WHERE ID_usuario = %s"
    )

    cur.execute(query, (id,))
    data = cur.fetchone()

    user = {
        "Nome_usuario": data["Nome_usuario"],
        "Email": data["Email"],
        "Numero_telefone": data["Numero_telefone"],
        "Senha_hash": data["Senha_hash"],
        "Data_inscricao": data["Data_inscricao"],
        "Multa_atual": data["Multa_atual"],
    }
    cur.close()
    conn.close()
    return user


def getUserByEmail(email):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = (
        "SELECT Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual",
        "WHERE Email = %s",
    )

    cur.execute(query, (email,))
    data = cur.fetchone()

    user = {
        "Nome_usuario": data["Nome_usuario"],
        "Email": data["Email"],
        "Numero_telefone": data["Numero_telefone"],
        "Senha_hash": data["Senha_hash"],
        "Data_inscricao": data["Data_inscricao"],
        "Multa_atual": data["Multa_atual"],
    }
    cur.close()
    conn.close()
    return user