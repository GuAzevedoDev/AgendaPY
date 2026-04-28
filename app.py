from services.services import cadastrarClienteWeb,loginFuncionarioWeb
from flask import Flask, render_template, request, redirect, url_for,jsonify,session
import re
import hashlib
from auth import login_required
app = Flask(__name__)
app.secret_key = "Gugu.000"


#Login

#Pagina de login, retorna html
@app.route("/login")
def login():
    return render_template("login.html")

#Rota de login, para validacao e salvar sessao
@app.route("/loginEntrada", methods=["POST"])
def loginFuncWeb():
    #Pega os dados do JS
    dados = request.json
    usuario = dados["usuario"]
    senha = dados["senha"].encode('utf-8')
    hashSenha = hashlib.sha256(senha)
    senhaHex = hashSenha.hexdigest()

    #validacao de formulario
    if usuario and senha:
        funcionario = loginFuncionarioWeb(usuario, senhaHex)
    else:
        return jsonify({"mensagem": "Preencha todos os campos"}), 400
    
    if not funcionario:
        return jsonify({"mensagem": "O funcionario nao existe"}), 400
    
    if senhaHex != funcionario[3]:
        return jsonify({"mensagem": "Senha incorreta"}), 400
    
    # login OK
    session["funcionario_id"] = funcionario[0]

    #Caso passe por todos os retornos o login esta OK
    return jsonify({"mensagem": "Login feito com sucesso", "redirect": "/"}), 200

#Verificar se esta logado
@app.route("/verificaLogin")
def verificaLogin():
    if 'funcionario_id' in session:
        return jsonify({"logado": True})
    else:
        return jsonify({"logado": False})

#Rota de logout
@app.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logoutFunc():
    #Limpa sessao
    session.clear()
    
    #Mensagem para JS
    return jsonify({"mensagem": "Logout feito com sucesso"}), 200


#Pagina inicial,retorna html
@app.route("/")
@login_required     #Verifica se existe um funcionario logado
def home():
    return render_template("index.html")


#Cadastrar clientes
@app.route("/CadastroClientes", methods=["POST"])
@login_required     #Verifica se existe um funcionario logado
def cadastroClienteWeb():
    dados = request.json
    nome = dados["nome"]
    numero = dados["telefone"]
    telefone_limpo = re.sub(r"\D", "", numero)

    if not re.fullmatch(r"\d{11}", telefone_limpo):
        return jsonify({"mensagem": "Telefone inválido"}), 400  # ← 400 Bad Request

    if nome and telefone_limpo:
        cadastrarClienteWeb(nome, telefone_limpo)
    else:
        return jsonify({"mensagem": "Preencha todos os campos"}), 400

    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 200









# def agendar():
#     dados = request.json
#     cliente_id = dados["cliente_id"]
#     funcionario_id = dados["funcionario_id"]
#     servico_id = dados["servico_id"]
#     horario = dados["horario"]
#     data = dados["data"]

if __name__ == "__main__":
    app.run(debug=True)