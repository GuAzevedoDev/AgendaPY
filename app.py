from services.services import cadastrarClienteWeb,loginFuncionarioWeb
from flask import Flask, render_template, request, redirect, url_for,jsonify
import re

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginEntrada", methods=["POST"])
def loginFuncWeb():
    dados = request.json
    usuario = dados["usuario"]
    senha = dados["senha"]

    if usuario and senha:
        funcionario = loginFuncionarioWeb(usuario, senha)
    else:
        return jsonify({"mensagem": "Preencha todos os campos"}), 400
    
    if not funcionario:
        return jsonify({"mensagem": "Login ou senha incorretos"}), 400
    

    return jsonify({"mensagem": "Login efetuado com sucesso"}), 200



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/CadastroClientes", methods=["POST"])
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