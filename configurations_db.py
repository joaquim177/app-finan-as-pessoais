import sqlite3
from sqlite3 import Error
import os


if not os.path.exists('./db'):
    os.makedirs('./db')



#connection or create database
def connection():
    path = '.\\db\\gerir_financeiro.db'
    try:
        con =  sqlite3.connect(path)
    except Error as er:
        print(str(er))

    return con


table_users = """
    CREATE TABLE users (
    user_id       INTEGER   PRIMARY KEY AUTOINCREMENT,
    user_email    TEXT (50) NOT NULL,
    user_name     TEXT (30) NOT NULL,
    user_password TEXT (12) NOT NULL
);"""

table_movimentacoes = "CREATE TABLE movimentacoes (movimentacao_id INTEGER   PRIMARY KEY AUTOINCREMENT, movimentacao_user TEXT(30) NOT NULL, movimentacao_description TEXT (30) NOT NULL,movimentacao_value  INTEGER   NOT NULL, movimentacao_type        TEXT (10) NOT NULL   DEFAULT Entrada, movimentacao_category    TEXT      NOT NULL,movimentacao_date        TEXT      NOT NULL);"

table_categorys = """
    CREATE TABLE categorys (
    caregory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT    NOT NULL
);

"""
vcon = connection()

def create_table(conect, sql):
    try:
        c = conect.cursor()
        c.execute(sql)
        print("tabela criada")
    except Error as er:
        print(er)


create_table(vcon, table_users)
create_table(vcon, table_movimentacoes)
create_table(vcon, table_categorys)


categorys = ['salario', 'aluguel', 'alimentacao', 'venda produto/servico', 'emprestimo', 'pagamento de emprestimo']


def consulta(conection, sql):
    try:

        c= conection.cursor()
        c.execute(sql)
        res = c.fetchall()
        return res
    except Error as er:
        print(er)

categorysDB = consulta(vcon, sql= 'SELECT * FROM categorys')

list_categorys =[]

for cateDB in categorysDB:
    list_categorys.append(cateDB[1])


for cate in categorys:
    if(not cate in list_categorys):
        try:
            c = vcon.cursor()
            sql = f'INSERT INTO categorys (category) VALUES ("{cate}")'
            c.execute(sql)
            vcon.commit()
        except Error as er:
            print(str(er))