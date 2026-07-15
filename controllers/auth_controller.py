from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash,Blueprint
import hashlib
from auth import login_required
from services.services import Funcionario

auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
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
        repo_funcionario = Funcionario()
        if usuario and senha:
            funcionario = repo_funcionario.loginFuncionarioWeb(usuario, senhaHex)
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
@auth_bp.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logoutFunc():
    #Limpa sessao
    session.clear()
    
    #Redirecionamento para funcao login
    return redirect(url_for("login"))


