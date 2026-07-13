from flask import Blueprint, redirect, render_template, request, url_for
from models import Agendamentos,Clientes,Funcionarios,ServicosAgendamentos,Servicos
from auth import login_required


home_bp = Blueprint("home")

@home_bp.route("/")
@login_required     #Verifica se existe um funcionario logado
def home():
    funcionarios = funcionario_service.mostrarFuncionariosWeb()
    sessaoFun = {
        "funcionario_id": session["funcionario_id"],
        "funcionario_nome": session["funcionario_nome"],
        "funcionario_cargo": session["funcionario_cargo"],
        "funcionario_funcao": session["funcionario_funcao"]
    }
    return render_template("home.html",funcionarios=funcionarios, sessaoFun = sessaoFun)