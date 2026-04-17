from services.services import cadastrarClienteWeb
from flask import Flask, render_template, request, redirect, url_for,jsonify
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/CadastroClientes",methods=["POST"])
def cadastroClienteWeb():
    dados = request.json
    nome = dados["nome"]
    numero = dados["telefone"]
    telefone_limpo = re.sub(r"\D", "", numero)

    if not re.fullmatch(r"\d{11}", telefone_limpo):
        return jsonify({"mensagem": "telefone invalido"})
    
    if nome and telefone_limpo:
        cadastrarClienteWeb(nome,telefone_limpo)
    else:
        return
    return jsonify({"mensagem": "Cliente cadastrado com sucesso"})

# def agendar():
#     dados = request.json
#     cliente_id = dados["cliente_id"]
#     funcionario_id = dados["funcionario_id"]
#     servico_id = dados["servico_id"]
#     horario = dados["horario"]
#     data = dados["data"]

if __name__ == "__main__":
    app.run(debug=True)