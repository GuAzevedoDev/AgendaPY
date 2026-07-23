from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash,Blueprint
from auth import login_required
from exeptions import AgendaPy
from services import Funcionario
from extensions import limiter

service_funcionario = Funcionario()
auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    #Se estiver no metodo get ele so pega a renderiza o html
    if request.method == "GET":
        return render_template("login.html")
    
    #Se estiver no metodo POST ele pega os dados do usuario 

    #Pega dado do form HTML
    usuario = request.form.get("nomeUsuario", "")
    #O encode transforma o utf puro pra bytes pois o hash so aceita bytes
    senha = request.form.get("senhaUsuario", "")
       
    #validacao de formulario
    

    if not usuario or not senha:
        flash("Preencha todos os campos"), 400
        return redirect(url_for("auth.login"))
    try:
        funcionario = service_funcionario.loginFuncionarioWeb(usuario, senha)
        # login OK
        session.permanent = True  # ativa o PERMANENT_SESSION_LIFETIME (expira em 30min de inatividade)
        session["funcionario_id"] = funcionario.id
        session["funcionario_nome"] = funcionario.nome
        session["funcionario_cargo"] = funcionario.cargo
        session["funcionario_funcao"] = funcionario.funcao

        #Caso passe por todos o s retornos o login esta OK e redireciona
        #Dentro da url_for(nome da funcao)
        return redirect(url_for("home.home"))
    except AgendaPy as e:
        flash(str(e), "erro")
        return redirect(url_for("auth.login"))
        
       
    


#Rota de logout
@auth_bp.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logout():
    #Limpa sessao
    session.clear()
    
    #Redirecionamento para funcao login
    return redirect(url_for("auth.login"))


