import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import archives

cod = random.randint(10000, 99999)

def enviar_email_verificacao(email):
    remetente_email = archives.remetente_email
    senha_app = archives.senha_app

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()


        servidor.login(remetente_email, senha_app)

        mensagem = MIMEMultipart()
        mensagem['From'] = remetente_email
        mensagem['To'] = email
        mensagem['Subject'] = 'codigo de Verificaçao'

        corpo_email = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Teste</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
    <h2 style="text-align: center">Codigo de verificação.</h2>

    <p style="text-align: center">Seu codigo de verificação é {cod}.</p>
</body>
</html>
"""
        mensagem.attach(MIMEText(corpo_email, 'html'))

        servidor.send_message(mensagem)
        return cod
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticaçao.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        servidor.quit()



def verify_my_codd(cod_user, cod):
    if(cod_user == cod):
        print("true")
        return True
    else:
        print("false")
        return False
