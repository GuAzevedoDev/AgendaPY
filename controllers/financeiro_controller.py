from flask import render_template,Blueprint,session
from auth import login_required
from services import Funcionario

funcionario_service = Funcionario()

financeiro_bp = Blueprint("financeiro",__name__,url_prefix="/financeiro")


@financeiro_bp.route("/")
@login_required
def financeiro():
  sessaoFun = {
      "funcionario_id": session.get("funcionario_id"),
      "funcionario_nome": session.get("funcionario_nome"),
      "funcionario_cargo": session.get("funcionario_cargo"),
      "funcionario_funcao": session.get("funcionario_funcao")
  }

  todosFuncionarios = funcionario_service.mostrarFuncionariosWeb()

  if sessaoFun["funcionario_id"] == 1:
    funcionarios = todosFuncionarios
  else:
    funcionarios = [f for f in todosFuncionarios if f.id == sessaoFun["funcionario_id"]]

  return render_template("financeiro.html",sessaoFun = sessaoFun,funcionarios = funcionarios)
