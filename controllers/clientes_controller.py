from flask import Blueprint, render_template, session,jsonify,request
from auth import login_required
from services import Cliente

cliente_service = Cliente()

clientes_bp = Blueprint("clientes", __name__,url_prefix="/clientes")

@clientes_bp.route("/")
@login_required
def clientes():
    sessaoFun = {
        "funcionario_id": session.get("funcionario_id"),
        "funcionario_nome": session.get("funcionario_nome"),
        "funcionario_cargo": session.get("funcionario_cargo"),
        "funcionario_funcao": session.get("funcionario_funcao")
    }
    return render_template("clientes.html", sessaoFun=sessaoFun)

@clientes_bp.route("/mostrar",methods = ['GET','POST'])
@login_required
def mostrar_clientes():
    clientes = cliente_service.mostrar_clientes()
    return jsonify(clientes)

@clientes_bp.route("/historico",methods = ['GET','POST'])
@login_required
def mostar_historico():
    dados = request.json
    id = dados["id"]
    historico = cliente_service.pegar_historico(id)
    return jsonify(historico)

@clientes_bp.route("/pesquisar", methods=['GET', 'POST'])
@login_required
def pesquisar_clientes():
    dados = request.json or {}
    termo = dados.get("termo", "")
    clientes = cliente_service.pesquisar_clientes_web(termo)
    return jsonify(clientes)