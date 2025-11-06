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
        cur.close()
        conn.close()

        initBooks()

def initBooks():
    conn = connect()
    cur = conn.cursor()

    with open(SQL_INSERTS, 'r', encoding='utf-8') as inserts:
        sql = inserts.read()

    # divide o script em statements e executa um a um
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    for stmt in statements:
        try:
            cur.execute(stmt)
        except Exception:
            # ignora statements vazios ou que já foram aplicados
            pass

    conn.commit()
    cur.close()
    conn.close()
    # conn = connect()
    # cur = conn.cursor()
    
    # with open(SQL_INSERTS, 'r') as inserts:
    #     cur.execute(inserts.read())
    
    # conn.commit()
    # cur.close()
    # conn.close()

def getBooks():
    with connect() as conn:
        cur = conn.cursor(dictionary=True)

        query = '''
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
        '''

        cur.execute(query)
        livros = cur.fetchall()
        cur.close()
    return livros

def addUser(nome, email, numero, senha_hash):
    conn = connect()
    cur = conn.cursor()

    adduser = '''
        INSERT INTO usuarios (nome_usuario, email, numero_telefone, senha_hash, data_inscricao, multa_atual)
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
        SELECT *
        FROM usuarios
        WHERE id_usuario = %s
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
        FROM usuarios
        WHERE email = %s
    '''
    

    cur.execute(query, (email,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user
