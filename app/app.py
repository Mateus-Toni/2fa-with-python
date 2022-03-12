
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import dao

app = Flask(__name__)
app.secret_key = 'mateus'

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/codigo")
def codigo():
    import random
    cod = random.randint(111111, 999999) 
    dao.send_email(session['usuario_logado'], cod)
    return render_template("codigo.html", cod_back=cod)

@app.route("/user_logado")
def usuario_logado():
    return render_template("usuario_logado.html")

@app.route("/autenticar" , methods=['POST'])
def autenticar():
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    email = request.form['email']
    senha = request.form['senha']
    db_user = dao.get_password(email)
    if db_user == senha:
        session['usuario_logado'] = email
        return redirect(url_for('codigo'))
    else:
        return redirect(url_for('login'))
        
@app.route("/verifica_codigo", methods=['POST'])
def verifica_codigo():
    cod_user = request.form['cod_user']
    cod_back = request.form['cod_back']
    
    if cod_user == cod_back:
        return redirect(url_for('usuario_logado'))
    else:
        return redirect(url_for('login'))
    
@app.route("/criar", methods=['POST'])
def cria_user():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    dao.create_user(nome, email, senha)
    
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)