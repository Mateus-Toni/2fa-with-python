import email
from dotenv import load_dotenv
import mysql.connector

NAME_DB = 'totp'
USER = 'root'
HOST = 'localhost'
PASSWORD = ''

def open_db(user, password, host, database):
    try:
        db = mysql.connector.connect(user=user, password=password,
                                     host=host, database=database)
        cursor = db.cursor(dictionary=True)
    except:
        return None, None
    else:
        return db, cursor
    
def create_user(nome, email, senha):
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db and cursor:
        cursor.execute(f"""insert into users values (default, '{nome}', '{email}', '{senha}');""")
        db.commit()
        db.close()
        
        
def get_password(email):
    db, cursor = open_db(USER, PASSWORD, HOST, NAME_DB)
    if db and cursor:
        cursor.execute(f"""select senha from users where email = '{email}';""")
        user = cursor.fetchall()
        for list_user in user:
            return list_user['senha']
    
def send_email(client_email, cod):
    import smtplib
    import email.message
    import os
    from dotenv import load_dotenv  
    load_dotenv()
    senha = os.environ.get('SENHA')
    corpo_email = f"""
    <h1>Ola,</h1>
    <h1>Seu código de verificação é:</h1>
    <h2>{cod}</h2>
    """

    msg = email.message.Message()
    msg['Subject'] = "Código de verificação"
    msg['From'] = 'WorkStation.box.email@gmail.com'
    msg['To'] = client_email
    password = senha
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    if password:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')


