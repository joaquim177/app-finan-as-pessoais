import customtkinter as c
import tkinter as tk
from datetime import date
from tkinter import messagebox, simpledialog
import db
from verify_email import enviar_email_verificacao,verify_my_codd

jan = c.CTk()
jan.geometry('800x600')
jan.title('Gestão financeira Pessoal')
jan.configure(bg='#2F4F4F')
jan.resizable(False, False)
user_logado = ()
## FUNCTIONS
def limpar_janela():
    for widget in jan.winfo_children():
        widget.destroy()


def ADD_MOVIMENTACAO():
    global user_logado
    add = c.CTkToplevel(jan)
    add.geometry('500x500')
    add.resizable(False, False)
    add.title('Add Movimentacão')
    add.configure(bg='#2F4F4F')  
    #ficar sobreposta 
    add.transient(jan)
    add.grab_set()
    add.focus_set()
    font = ('calibri bold', 17)

    c.CTkLabel(add, text='Adicionar Movimentação', font=('calibri bold', 20)).pack(pady=5)

    description = c.CTkEntry(add, width=400, height=40, font=font, placeholder_text='Descrição')
    description.pack(pady=5)
    value = c.CTkEntry(add, width=400, height=40, font=font, placeholder_text='Value: 1000 R$')
    value.pack(pady=5)

    c.CTkLabel(add, text='Type', font=font).pack()
    type = c.CTkOptionMenu(add, values=['Entrada', 'Saida'], width=400, height=40)
    type.pack( padx=2, pady=3)    


    categorys = ['Venda Produdo/Serviço','Salario', 'Emprestimo', 'Pagamento De Emprestimo', 'Aluguel', 'Outros']
    c.CTkLabel(add, text='Category', font=font).pack(side='top') 
    category = c.CTkOptionMenu(add, values=categorys, width=400, height=40)
    category.pack()

    frame_date = c.CTkFrame(add, width=400, height=120)
    frame_date.propagate(False)
    frame_date.pack(pady=10)
    
    frame_labbels = c.CTkFrame(frame_date, width=400, height=60)
    frame_labbels.propagate(False)
    frame_labbels.pack()

    c.CTkLabel(frame_labbels, text='Days', font=('calibri bold', 20)).pack(pady=5,padx=40, side='left')
    c.CTkLabel(frame_labbels, text='Mouths', font=('calibri bold', 20)).pack(pady=5,padx=40, side='left')
    c.CTkLabel(frame_labbels, text='Years', font=('calibri bold', 20)).pack(pady=5,padx=40, side='left')

    frame_buttons = c.CTkFrame(frame_date, width=400, height=60)
    frame_buttons.propagate(False)
    frame_buttons.pack()
    #################################################################################################    
    list_days = [str(i) for i in range(1, 32)]
    list_months = [str(i) for i in range(1, 13)]
    list_years = [str(i) for i in range(date.today().year, 2017, -1 )]   

    def reset_option_menu(option_menu, values):
        option_menu.configure(values=values)
        option_menu.set(values[0])

    def alterar_days(mes):
        global list_days
        if mes == '2':
            list_days = [str(i) for i in range(1, 29)]  # Considerando fevereiro com 28 dias
        elif mes in ['4', '6', '9', '11']:
            list_days = [str(i) for i in range(1, 31)]  # Meses com 30 dias
        else:
            list_days = [str(i) for i in range(1, 32)]  # Meses com 31 dias
        reset_option_menu(days, list_days)

    days = c.CTkOptionMenu(frame_buttons, values=list_days)
    months = c.CTkOptionMenu(frame_buttons, values=list_months, command=alterar_days)
    years = c.CTkOptionMenu(frame_buttons, values=list_years)

    days.pack(pady=5,padx=3, side='left')
    months.pack(pady=5,padx=3, side='left')
    years.pack(pady=5,padx=3, side='left')
##############################################################################################
    def add_movimentacao():
        day, month, year = days.get(), months.get(), years.get()
        
        dates = [day, month]
        for i in range(len(dates)):
            if(len(dates[i]) == 1):
                dates[i] =f'0{dates[i]}'


        data  = f'{dates[0]}/{dates[1]}/{year}'
        print(data)
        res = db.add_movimentacao_with_date(user_logado[2], [
            description.get(),
            value.get(),
            type.get(),
            category.get(),
            data
        ])
        if(res == 'Preencha todos campos'):
            return messagebox.showerror('Movimentacao invalida', res)
        
        messagebox.showinfo('Movimentação concluida', f'Movimentação de {value.get()} na data {data} feita com sucesso.')
        limpar_janela()
        HOME()

    c.CTkButton(add, text='Adicionar', width=400, height=40,command=add_movimentacao,  font=('calibri bold', 20)).pack()
    

def VERIFY_EMAIL(email, user):
    verify_email = c.CTkToplevel(jan)
    verify_email.geometry('500x200')
    verify_email.resizable(False, False)
    verify_email.title('Gestão financeira Pessoal')
    verify_email.configure(bg='#2F4F4F')  
    #ficar sobreposta 
    verify_email.transient(jan)
    verify_email.grab_set()
    verify_email.focus_set()
    font = ('calibri bold', 18)

    c.CTkLabel(verify_email, text='Foi enviado um email com codigo de verificação em seu email.', font=font).pack(pady=10)
    input_cod = c.CTkEntry(verify_email,width=300, height=40,font=font, placeholder_text='Codigo:')
    input_cod.pack(pady=10)

    try:
        cod =enviar_email_verificacao(email)
    except:
        print("erro")



    def cad():

        res =db.cadastrar_conta(user)

        if(res == False):
            return messagebox.showerror('Credenciais invalida!','Falha ao fazer cadastro.')
        elif(res == 'email ja existe'):
            return messagebox.showerror('Credenciais invalida!','Email ja cadastrado.')
        elif(res == 'email invalido'):
            return messagebox.showerror('Credenciais invalida!','Email invalido.')
        elif(res == 'username ja existe'):
            return messagebox.showerror('Credenciais invalida!','Username ja cadastrado.')
        
        messagebox.showinfo('Cadastro', 'Usuario cadastrado com sucesso!!')
        LOGIN()

    def verify_my_cod():
        cod_user = input_cod.get()
       
        if(not verify_my_codd(int(cod_user), int(cod))):
            return messagebox.showerror('Codigo invalido', 'Codigo invalido, vc tem mais uma tentativa.')
        
        cad()
    c.CTkButton(verify_email, text='Enviar',font=font, width=300, command=verify_my_cod).pack(pady=10)

def barra_lateral():
    frame_barra_lateral = c.CTkFrame(jan, width=200, height=1080, corner_radius=0)
    frame_barra_lateral.propagate(False)
    frame_barra_lateral.place(x=0, y=0)
   
    #########
    frame_intro_barra = c.CTkFrame(frame_barra_lateral, width=200, height=50, corner_radius=0)
    frame_intro_barra.propagate(False)
    frame_intro_barra.pack(side='top')

    def fechar():
        frame_barra_lateral.destroy()
        

    c.CTkLabel(frame_intro_barra, text='MENU', font=('calibri bold', 20)).pack(side='left', padx=10)
    c.CTkButton(frame_intro_barra, text='X', command=fechar, width=50, font=('calibri bold', 20)).pack(side='right', padx=4)
    ############################################################################
    c.CTkButton(frame_barra_lateral, text='Movimentações', command=MOVIMENTACOES,  width=180, font=('calibri', 17)).pack(side='top', padx=4, pady=7)
    c.CTkButton(frame_barra_lateral, text='Add Movimentacão', command=ADD_MOVIMENTACAO,  width=180, font=('calibri', 17)).pack(side='top', padx=4, pady=7)


# PAGES 
def LOGIN():
    global user_logado
    limpar_janela()
    jan.geometry('600x400')
    jan.config(background='#2F4F4F')
    frame_top_login = c.CTkFrame(jan, width=700, height=50, corner_radius=0, fg_color='#2F4F4F')
    frame_top_login.propagate(False)
    frame_top_login.pack()
    c.CTkLabel(frame_top_login, text='GESTÃO FINANCEIRA', text_color='white', font=('calibri bold', 25)).pack(side='left', padx=10)
    c.CTkButton(frame_top_login, text='Cadastre-se', command=CADASTRO, text_color='white', font=('calibri', 20)).pack(side='right', padx=10)
    email = c.CTkEntry(jan, placeholder_text='Email',bg_color='#2F4F4F', width=400, height=40, font=('calibri', 20))
    email.pack(pady=(40,0))

    password = c.CTkEntry(jan, placeholder_text='Password',show='*',bg_color='#2F4F4F', width=400, height=40, font=('calibri', 20))
    password.pack(pady=10)

    def logar():
        global user_logado
        user  = [email.get(), password.get()]
        if(len(user[0])<= 0 or len(user[1]) <=0 ):
            return messagebox.showerror('Credenciais invalida!','Preencha seus dados corretamente.')
        res = db.login(user)
        if(not res):
            return messagebox.showerror('Credenciais invalida!','Preencha seus dados corretamente.')
        
        user_logado = res
        HOME()



    c.CTkButton(jan, text='entrar', command=logar, width=400,bg_color='#2F4F4F',font=('calibri', 22)).pack(pady=5)

def CADASTRO():
    global user_logado
    limpar_janela()
    jan.geometry('600x400')
    jan.config(background='#2F4F4F')
    frame_top_login = c.CTkFrame(jan, width=700, height=50, corner_radius=0, fg_color='#2F4F4F')
    frame_top_login.propagate(False)
    frame_top_login.pack()
    c.CTkLabel(frame_top_login, text='GESTÃO FINANCEIRA', text_color='white', font=('calibri bold', 25)).pack(side='left', padx=10)
    c.CTkButton(frame_top_login, text='Entre',command=LOGIN, text_color='white', font=('calibri', 20)).pack(side='right', padx=10)
    name = c.CTkEntry(jan, placeholder_text='Name',bg_color='#2F4F4F', width=400, height=40, font=('calibri', 20))
    name.pack(pady=(20,5))
    email = c.CTkEntry(jan, placeholder_text='Email',bg_color='#2F4F4F', width=400, height=40, font=('calibri', 20))
    email.pack(pady=10)

    password = c.CTkEntry(jan, placeholder_text='Password',show='*',bg_color='#2F4F4F', width=400, height=40, font=('calibri', 20))
    password.pack(pady=10)


    def cadastrar():
        print(password.get())
        if(len(name.get()) <= 0 or len(email.get()) <=0 or len(password.get()) <= 0):
            return messagebox.showerror('Credenciais invalida!','Preencha seus dados corretamente.')
        user = [name.get(), email.get(), password.get()]

        
        VERIFY_EMAIL(email.get(), user= user)



        
    c.CTkButton(jan, text='Cadastrar', width=400,bg_color='#2F4F4F',font=('calibri', 22), command=cadastrar).pack(pady=5)



    
def HOME():
    global user_logado
    limpar_janela()
    jan.geometry('1024x600')
    ###################################################################################################
   
    frame_top_home = c.CTkFrame(jan, width=1024, height=50, corner_radius=0, fg_color='#2F4F4F')
    frame_top_home.propagate(False)
    frame_top_home.pack()
        #c.CTkImage colocar image
    c.CTkButton(frame_top_home, text='☰', width=20,command=barra_lateral,fg_color='#2F4F4F', font=('calibri bold', 21)).pack(side='left', padx=4)
    c.CTkLabel(frame_top_home, text='GESTÃO FINANCEIRA', text_color='white', font=('calibri bold', 25)).pack(side='left', padx=10)
     
    c.CTkButton(frame_top_home, text='sair', command=LOGIN, width=50).pack(side='right', padx=(0,20))

    name_user = c.StringVar(value=user_logado[2])

    name = c.CTkLabel(frame_top_home, textvariable=name_user, text_color='white', font=('calibri bold', 20))
    name.pack(side='right', padx=10)


    frame_mid_home =  c.CTkFrame(jan, width=1024, height=150, corner_radius=0, fg_color='#2F4F4F')
    frame_mid_home.propagate(False)
    frame_mid_home.pack(pady=10)

        ##############################
    frame_saldo = c.CTkFrame(frame_mid_home, width=230, height=140, fg_color='#4169E1')
    frame_saldo.propagate(False)
    frame_saldo.pack(side='left', padx=(20,10))

    
    money_month = db.calcular_movimentacao_mounth(user_logado[2])
    print(money_month)

    saldo = c.CTkLabel(frame_saldo, text='Saldo Mensal💰', font=('calibri bold', 20), text_color='white')
    value = c.CTkLabel(frame_saldo, text=money_month['entradas'] - money_month['saidas'], font=('calibri bold', 20), text_color='white')
    saldo.pack(side='top', pady=(10))
    value.pack(side='bottom', pady=30)


    frame_receitas = c.CTkFrame(frame_mid_home, width=230, height=140, fg_color='#32CD32')
    frame_receitas.propagate(False)
    frame_receitas.pack(side='left', padx=10)

    receitas = c.CTkLabel(frame_receitas, text='Receita Mensal 💵', font=('calibri bold', 20), text_color='white')
    receitas_value = c.CTkLabel(frame_receitas, text=money_month['entradas'], font=('calibri bold', 20), text_color='white')
    receitas.pack(side='top', pady=10)
    receitas_value.pack(side='bottom', pady=30)    


    frame_despesas = c.CTkFrame(frame_mid_home, width=230, height=140, fg_color='#B22222')
    frame_despesas.propagate(False)
    frame_despesas.pack(side='left', padx=10)

    despesas = c.CTkLabel(frame_despesas, text='Despesas Mensal', font=('calibri bold', 20), text_color='white')
    despesas_value = c.CTkLabel(frame_despesas, text=money_month['saidas'], font=('calibri bold', 20), text_color='white')
    despesas.pack(side='top', pady=10)
    despesas_value.pack(side='bottom', pady=30)    


    frame_emprestimos = c.CTkFrame(frame_mid_home, width=230, height=140, fg_color='#DAA520')
    frame_emprestimos.propagate(False)
    frame_emprestimos.pack(side='left', padx=10)

    emprestimos = c.CTkLabel(frame_emprestimos, text='Emprestimos Mensal', font=('calibri bold', 20), text_color='white')
    emprestimos_value = c.CTkLabel(frame_emprestimos, text=money_month['emprestimos'], font=('calibri bold', 20), text_color='white')
    emprestimos.pack(side='top', pady=10)
    emprestimos_value.pack(side='bottom', pady=30)   
##############################################################################################################################

    frame_add_home =  c.CTkFrame(jan, width=1024, height=130, corner_radius=0,fg_color='#2F4F4F' )
    frame_add_home.propagate(False)
    frame_add_home.pack_propagate(False)
    frame_add_home.pack()
    ################
    font =('calibri bold', 20)

    frame_description = c.CTkFrame(frame_add_home, width=230, height=100)
    frame_description.propagate(False)
    frame_description.pack(side='left', padx=(20,10))

    c.CTkLabel(frame_description, text='Description', font=font).pack(side='top')
    
    description_home = c.CTkEntry(frame_description, width=180, font=font, placeholder_text='Descrição')
    description_home.pack(side='bottom', padx=2, pady=20)
    #############
    frame_value = c.CTkFrame(frame_add_home, width=230, height=100)
    frame_value.propagate(False)
    frame_value.pack(side='left', padx=10)

    c.CTkLabel(frame_value, text='Value', font=font).pack(side='top')
    value_home = c.CTkEntry(frame_value, width=180, font=font, placeholder_text='1000 R$')
    value_home.pack(side='bottom', padx=2, pady=20)
    #############
    frame_type = c.CTkFrame(frame_add_home, width=230, height=100)
    frame_type.propagate(False)
    frame_type.pack(side='left', padx=10)

    c.CTkLabel(frame_type, text='Type', font=font).pack(side='top')
    type_home = c.CTkOptionMenu(frame_type, values=['Entrada', 'Saida'], width=180)
    type_home.pack(side='bottom', padx=2, pady=20)
    #############
    frame_category = c.CTkFrame(frame_add_home, width=230, height=100)
    frame_category.propagate(False)
    frame_category.pack(side='left', padx=10)

    categorys = ['Venda Produdo/Serviço','Salario', 'Emprestimo', 'Pagamento De Emprestimo', 'Aluguel', 'Outros']

    c.CTkLabel(frame_category, text='Category', font=font).pack(side='top') 
    category_home = c.CTkOptionMenu(frame_category, values=categorys, width=180)
    category_home.pack(side='bottom', padx=2, pady=20)
    ######################################################################################################################
    def add():
        new_movi = [description_home.get(), value_home.get(), type_home.get(), category_home.get()]

        if(len(description_home.get()) <=0 or len(value_home.get()) <=0 ):
            return messagebox.showerror('Dados invalido!', 'Preencha todos campos.')
        
        res = db.add_movimentacao(user_logado[2],new_movi)

        if(res and res == 'Preencha todos campos'):
            return messagebox.showerror('Dados invalido!', 'Preencha todos campos.')
        
        limpar_janela()
        HOME()

    btn = c.CTkButton(jan, text='Adicionar', width=1000,height=30,
                       font=font,
                         corner_radius=0,
                           fg_color='#32CD32',
                           hover_color='#228B22',
                           command= add
                           )
    btn.pack(pady=3)

    ######################################################################################################################

    frame_movements = c.CTkFrame(jan, width=1024, height=300, fg_color='#2F4F4F', corner_radius=0)
    frame_movements.propagate(False)
    frame_movements.pack()

    c.CTkLabel(frame_movements, text='As ultimas movimentações', text_color='white', font=font).pack()
    movi = db.return_movimentacoes(user_logado[2])
    if(len(movi) == 0):
        c.CTkLabel(frame_movements, text='Sem nenhuma movimentação feita ainda.', text_color='white', font=('calibri', 18)).pack(pady=(20,0))
    elif(len(movi) > 3):
        movi = movi[len(movi) -3: ]
    for mo in movi:
        title_frame = f'frame{mo[0]}'
        title_frame = c.CTkFrame(frame_movements, width=900, height=40)
        title_frame.propagate(False)
        title_frame.pack(padx=30, pady=2)

        description = c.CTkLabel(title_frame, text=mo[2], width=150).pack(side='left', padx=2)
        value = c.CTkLabel(title_frame, text=mo[3], width=150).pack(side='left', padx=2)
        type = c.CTkLabel(title_frame, text=mo[4], width=150).pack(side='left', padx=2)
        category = c.CTkLabel(title_frame, text=mo[5], width=150).pack(side='left', padx=2)
        date = c.CTkLabel(title_frame, text=mo[6], width=150).pack(side='left', padx=2)
        def remove():
            db.exluir_movimentacao(mo[0])
            limpar_janela()
            HOME()

        c.CTkButton(title_frame, text='Remove', width=150, command=remove).pack(side='left', padx=2)


def MOVIMENTACOES():
    global user_logado
    limpar_janela()
    jan.geometry('1024x600')    


    money = db.calcular_money(user_logado[2])

    ###################################################################################################
   
    frame_top_home = c.CTkFrame(jan, width=1024, height=50, corner_radius=0, fg_color='#2F4F4F')
    frame_top_home.propagate(False)
    frame_top_home.pack()
        #c.CTkImage colocar image
    c.CTkButton(frame_top_home, text='☰', width=20,command=barra_lateral,fg_color='#2F4F4F', font=('calibri bold', 21)).pack(side='left', padx=4)
    c.CTkLabel(frame_top_home, text='GESTÃO FINANCEIRA', text_color='white', font=('calibri bold', 25)).pack(side='left', padx=10)
     
    c.CTkButton(frame_top_home, text='Voltar', command=HOME, width=50).pack(side='right', padx=(0,20))
    name_user = c.StringVar(value=user_logado[2])
    name = c.CTkLabel(frame_top_home, textvariable=name_user, text_color='white', font=('calibri bold', 20))
    name.pack(side='right', padx=10)

    #################################
    frame_mid_home =  c.CTkFrame(jan, width=1024, height=150, corner_radius=0, fg_color='#2F4F4F')
    frame_mid_home.propagate(False)
    frame_mid_home.pack(pady=10)

        ##############################
    frame_saldo = c.CTkFrame(frame_mid_home, width=230, height=100, fg_color='#4169E1')
    frame_saldo.propagate(False)
    frame_saldo.pack(side='left', padx=(20,10))

    saldo = c.CTkLabel(frame_saldo, text='SALDO TOTAL', font=('calibri bold', 20), text_color='white')
    value = c.CTkLabel(frame_saldo, text=money['entradas'] - money['saidas'], font=('calibri bold', 20), text_color='white')
    saldo.pack(side='top')
    value.pack(side='bottom', pady=10)


    frame_receitas = c.CTkFrame(frame_mid_home, width=230, height=100, fg_color='#32CD32')
    frame_receitas.propagate(False)
    frame_receitas.pack(side='left', padx=10)

    receitas = c.CTkLabel(frame_receitas, text='RECEITA TOTAL', font=('calibri bold', 20), text_color='white')
    receitas_value = c.CTkLabel(frame_receitas, text=money['entradas'], font=('calibri bold', 20), text_color='white')
    receitas.pack(side='top')
    receitas_value.pack(side='bottom', pady=10)    


    frame_despesas = c.CTkFrame(frame_mid_home, width=230, height=100, fg_color='#B22222')
    frame_despesas.propagate(False)
    frame_despesas.pack(side='left', padx=10)

    despesas = c.CTkLabel(frame_despesas, text='DESPESAS TOTAL', font=('calibri bold', 20), text_color='white')
    despesas_value = c.CTkLabel(frame_despesas, text=money['saidas'], font=('calibri bold', 20), text_color='white')
    despesas.pack(side='top')
    despesas_value.pack(side='bottom', pady=10)    


    frame_emprestimos = c.CTkFrame(frame_mid_home, width=230, height=100, fg_color='#DAA520')
    frame_emprestimos.propagate(False)
    frame_emprestimos.pack(side='left', padx=10)

    emprestimos = c.CTkLabel(frame_emprestimos, text='EMPRESTIMOS TOTAL', font=('calibri bold', 20), text_color='white')
    emprestimos_value = c.CTkLabel(frame_emprestimos, text=money['emprestimos'], font=('calibri bold', 20), text_color='white')
    emprestimos.pack(side='top')
    emprestimos_value.pack(side='bottom', pady=10)
    ######################################################################################################################


    


    ###########################################
    frame_list = c.CTkFrame(jan, width=1024, height=600)
    frame_list.propagate(False)
    frame_list.pack()

    canvas = tk.Canvas(frame_list, width=900)
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = c.CTkScrollbar(frame_list, command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = c.CTkFrame(canvas, corner_radius=0, width=900)
    scrollable_frame.pack()

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    scrollable_frame.bind('<Configure>', update_scroll_region)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    
    c.CTkLabel(scrollable_frame, text='MOVIMENTAÇÕES', width=1000, font=('calibri bold', 20)).pack( pady=5)
    movi = db.return_movimentacoes(user_logado[2])
    def moviment():
        if(len(movi) == 0):
            c.CTkLabel(scrollable_frame, text='Sem nenhuma movimentação feita ainda.', width=1000, font=('calibri', 18)).pack(pady=(20,0))
        for mo in movi:
            title_frame = c.CTkFrame(scrollable_frame, width=900, height=40)
            title_frame.propagate(False)
            title_frame.pack(padx=30, pady=4)

            description = c.CTkLabel(title_frame, text=mo[2], width=150)
            description.pack(side='left', padx=2)
            
            value = c.CTkLabel(title_frame, text=mo[3], width=150)
            value.pack(side='left', padx=2)
            
            type_label = c.CTkLabel(title_frame, text=mo[4], width=150)
            type_label.pack(side='left', padx=2)
            
            category = c.CTkLabel(title_frame, text=mo[5], width=150)
            category.pack(side='left', padx=2)
            
            date = c.CTkLabel(title_frame, text=mo[6], width=150)
            date.pack(side='left', padx=2)
            def remove():
                db.exluir_movimentacao(mo[0])
                limpar_janela()
                MOVIMENTACOES()

            remove_button = c.CTkButton(title_frame, text='Remove', width=150, command=remove)
            remove_button.pack(side='left', padx=2)
    moviment()

LOGIN()



jan.mainloop()