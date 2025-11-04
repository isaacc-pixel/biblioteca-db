import mysql.connector 
from datetime import datetime
from database.config import USER, HOST, PORT, DATABASE, PASSWORD, SQL_BASE, SQL_INSERTS


def connect() -> mysql.connector.MySQLConnection:
    conn = mysql.connector.connect(
        user=USER, 
        host=HOST, 
        port=PORT, 
        database=DATABASE,
        password=PASSWORD
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
            port=PORT,
            password=PASSWORD
        )

        cur = conn.cursor()
        with open(SQL_BASE, 'r') as base:
            cur.execute(base.read())
        conn.commit()
        cur.close()
        conn.close()

def initBooks():
    #TODO
    '''ARRUMAR ISSO AQUI NÃO TÁ FUNCIONANDO'''
    conn = connect()
    cur = conn.cursor()
    
    with open(SQL_INSERTS, 'r') as inserts:
        cur.execute(inserts.read())
    
    conn.commit()
    cur.close()
    conn.close()

def addUser(nome, email, numero, senha_hash):
    conn = connect()
    cur = conn.cursor()

    adduser = '''
        INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    
    date = datetime.today().strftime("%Y-%m-%d")

    usuario = (nome, email, numero, senha_hash, date, 0)

    cur.execute(adduser, usuario)

    conn.commit()
    cur.close()
    conn.close()


def getUserById(id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = '''
        SELECT Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual
        FROM Usuarios
        WHERE ID_usuario = %s
    '''

    cur.execute(query, (id,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user


def getUserByEmail(email):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    query = '''
        SELECT *
        FROM Usuarios
        WHERE Email = %s
    '''
    

    cur.execute(query, (email,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user
