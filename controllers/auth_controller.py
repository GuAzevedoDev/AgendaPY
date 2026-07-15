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
        senha = request.form["senhaUsuario"]
       
        #validacao de formulario
        repo_funcionario = Funcionario()
        if usuario and senha:
            funcionario = repo_funcionario.loginFuncionarioWeb(usuario, senha)
        else:
            flash("Preencha todos os campos"), 400
            return redirect(url_for("auth.login"))
    
        if not funcionario:
            flash("Senha ou Usuario incorretos"), 400
            return redirect(url_for("auth.login"))
        
        # login OK
        session["funcionario_id"] = funcionario.id
        session["funcionario_nome"] = funcionario.nome
        session["funcionario_cargo"] = funcionario.cargo
        session["funcionario_funcao"] = funcionario.funcao
        #Caso passe por todos os retornos o login esta OK e redireciona
        #Dentro da url_for(nome da funcao)
        return redirect(url_for("home.home"))
    


#Rota de logout
@auth_bp.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logout():
    #Limpa sessao
    session.clear()
    
    #Redirecionamento para funcao login
    return redirect(url_for("auth.login"))


