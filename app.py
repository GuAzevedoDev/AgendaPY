from services.services import cadastrarClienteWeb,loginFuncionarioWeb,mostrarAgendaWeb,mostrarFuncionariosWeb
from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash
import re
import hashlib
from auth import login_required
app = Flask(__name__)
app.secret_key = "Gugu.000"


#Login

#Pagina de login, retorna html
@app.route("/login", methods=["GET", "POST"])
def login():
    #Se estiver no metodo get ele so pega a renderiza o html
    if request.method == "GET":
        return render_template("login.html")
    
    #Se estiver no metodo POST ele pega os dados do usuario 
    elif request.method == "POST":
        #Pega dado do form HTML
        usuario = request.form["nomeUsuario"]
        #O encode transforma o utf puro pra bytes pois o hash so aceita bytes
        senha = request.form["senhaUsuario"].encode('utf-8')
        hashSenha = hashlib.sha256(senha)
        senhaHex = hashSenha.hexdigest()
       
        #validacao de formulario
        if usuario and senha:
            funcionario = loginFuncionarioWeb(usuario, senhaHex)
        else:
            flash("Preencha todos os campos"), 400
            return redirect(url_for("login"))
    
        if not funcionario:
            flash("Senha ou Usuario incorretos"), 400
            return redirect(url_for("login"))
        
        # login OK
        session["funcionario_id"] = funcionario[0]
        session["funcionario_nome"] = funcionario[1]
        session["funcionario_cargo"] = funcionario[2]
        session["funcionario_funcao"] = funcionario[3]
        #Caso passe por todos os retornos o login esta OK e redireciona
        #Dentro da url_for(nome da funcao)
        return redirect(url_for("home"))
    


#Rota de logout
@app.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logoutFunc():
    #Limpa sessao
    session.clear()
    
    #Redirecionamento para funcao login
    return redirect(url_for("login"))


#Pagina inicial,retorna html
@app.route("/")
@login_required     #Verifica se existe um funcionario logado
def home():
    funcionarios = mostrarFuncionariosWeb()
    sessaoFun = {
        "funcionario_id": session["funcionario_id"],
        "funcionario_nome": session["funcionario_nome"],
        "funcionario_cargo": session["funcionario_cargo"],
        "funcionario_funcao": session["funcionario_funcao"]
    }
    print(session["funcionario_cargo"])
    return render_template("home.html",funcionarios=funcionarios, sessaoFun = sessaoFun)



@app.route("/calendario", methods = ['POST'])
@login_required     #Verifica se existe um funcionario logado
def calendario():
    #Pego os dados do js
    dados = request.json
    dataSelecionada = dados['data']
    idFuncionario = dados['idFuncionario']
    

    #Chamo a funcao
    horarios = mostrarAgendaWeb(idFuncionario,dataSelecionada)
    return jsonify(horarios)




# #Cadastrar clientes
# @app.route("/CadastroClientes", methods=["POST"])
# @login_required     #Verifica se existe um funcionario logado
# def cadastroClienteWeb():
    # dados = request.json
    # nome = dados["nome"]
    # numero = dados["telefone"]
    # telefone_limpo = re.sub(r"\D", "", numero)

    # if not re.fullmatch(r"\d{11}", telefone_limpo):
    #     return jsonify({"mensagem": "Telefone inválido"}), 400  # ← 400 Bad Request

    # if nome and telefone_limpo:
    #     cadastrarClienteWeb(nome, telefone_limpo)
    # else:
    #     return jsonify({"mensagem": "Preencha todos os campos"}), 400

    # return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 200









# def agendar():
#     dados = request.json
#     cliente_id = dados["cliente_id"]
#     funcionario_id = dados["funcionario_id"]
#     servico_id = dados["servico_id"]
#     horario = dados["horario"]
#     data = dados["data"]

if __name__ == "__main__":
    app.run(debug=True)