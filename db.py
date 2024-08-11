
from configurations_db import vcon
from sqlite3 import Error
from datetime import datetime
from datetime import date
import pytz
from validate_email import validate_email




def verify_email(email):
    try:
        c = vcon.cursor()
        sql = f'SELECT * FROM users WHERE user_email = "{email}"'
        c.execute(sql)
        res = c.fetchall()
    except Error as er:
        print(str(er))
    
    return res
   

def verify_name(name):
    try:
        c = vcon.cursor()
        sql = f'SELECT * FROM users WHERE user_name = "{name}"'
        c.execute(sql)
        res = c.fetchall()
    except Error as er:
        print(str(er))
    return res


def cadastrar_conta(user):
    name, email, password = user
    if(len(name) <=0 or len(email) <=0 or len(password) <= 0):
            return False
    if(not validate_email(email)):
        return 'email invalido'
    if(verify_name(name)):
        return 'username ja existe'
    if(verify_email(email)):
        return 'email ja existe'
    

    
    
    #verificar name existe
    #verificar email existe
    try:
        c = vcon.cursor()
        sql=f'INSERT INTO users (user_name, user_email, user_password) VALUES ("{name}", "{email}", "{password}")'
        c.execute(sql)
        vcon.commit()
    except Error as er:
        print(str(er))

def login(user):
    email, password = user
    try:
        c= vcon.cursor()
        sql = f'SELECT * FROM users WHERE (user_email, user_password) = ("{email}","{password}")'
        c.execute(sql)
        res = c.fetchall()

    except Error as er:
        print(str(er))
    if(res):
        return res[0][:-1]
    return False
    

def add_movimentacao(username, movimentacao):
    name = username
    if not name: return
    description, value, type, category = movimentacao

    if(len(description) <= 0 or len(value) <=0 or len(type) <= 0 or len(category) <= 0):
        return 'Preencha todos campos'

    timezone = pytz.timezone('America/Sao_Paulo')
    brasilia_now = datetime.now(timezone)
    formatted_date = brasilia_now.strftime('%d/%m/%Y')

    try:
        c = vcon.cursor()
        sql=f'INSERT INTO movimentacoes (movimentacao_user, movimentacao_description, movimentacao_value, movimentacao_type, movimentacao_category, movimentacao_date) VALUES ("{name}","{description}","{value}","{type}","{category}","{formatted_date}")'
        c.execute(sql)
        vcon.commit()

    except Error as er:
        print(str(er))

def add_movimentacao_with_date(username, movimentacao):
    name = username
    if not name: return
    description, value, type, category, date = movimentacao

    if(len(description) <= 0 or len(value) <=0 or len(type) <= 0 or len(category) <= 0 or len(date) <= 0):
        return 'Preencha todos campos'


    try:
        c = vcon.cursor()
        sql=f'INSERT INTO movimentacoes (movimentacao_user, movimentacao_description, movimentacao_value, movimentacao_type, movimentacao_category, movimentacao_date) VALUES ("{name}","{description}","{value}","{type}","{category}","{date}")'
        c.execute(sql)
        vcon.commit()

    except Error as er:
        print(str(er))


def return_movimentacoes(username):
    name = username
    try:
        c = vcon.cursor()
        sql = f'SELECT * FROM movimentacoes WHERE movimentacao_user = "{name}"'
        c.execute(sql)
        res = c.fetchall()
    except Error as er:
        print(str(er))
    return res
 

def return_movimentacoes_time(username):
    month = date.today().month
    year = date.today().year
    data = f'{month}/{year}'
    all  = return_movimentacoes(username)

    movimentacoes_in_month = []    
    for movi in all:
        if((movi[6][4:]) == (data)):
            movimentacoes_in_month.append(movi)
    
    
    return movimentacoes_in_month

def calcular_movimentacao_mounth(username):
    movimentacoes = return_movimentacoes_time(username)
    saidas = 0
    entradas = 0
    emprestimos = 0
    for mo in movimentacoes:
        if(mo[5].lower() == 'emprestimo'):
            emprestimos+= float(mo[3])
        elif(mo[5].lower() == 'pagamento de emprestimo'):
            emprestimos-= float(mo[3])
            saidas+= float(mo[3])
        elif(mo[4].lower() ==  'entrada'):
            entradas+= float(mo[3])
        else:
            saidas+= float(mo[3]) 

    return {'saidas': saidas, 'entradas': entradas, 'emprestimos': emprestimos }          


def calcular_money(username):
    movimentacoes = return_movimentacoes(username)
    saidas = 0
    entradas = 0
    emprestimos = 0
    for mo in movimentacoes:
        if(mo[5].lower() == 'emprestimo'):
            emprestimos+= float(mo[3])
        elif(mo[5].lower() == 'pagamento de emprestimo'):
            emprestimos-= float(mo[3])
        elif(mo[4].lower() ==  'entrada'):
            entradas+= float(mo[3])
        else:
            saidas+= float(mo[3]) 
    

    return {'saidas': saidas, 'entradas': entradas, 'emprestimos': emprestimos }           
def exluir_movimentacao(id):
    try:
        c = vcon.cursor()
        sql = f'DELETE FROM movimentacoes WHERE movimentacao_id = "{id}"'
        c.execute(sql)
        vcon.commit()
    except Error as er:
        print(str(er))



#exluir_movimentacao(3)        
#print(return_movimentacoes('santos'))
    
#add_movimentacao('pedro', ['banco', 600, 'Entrada', 'emprestimo'])
#cadastrar_conta(['joaquim132', 'joaquimmanoel2002@gmail.com', '123'])




