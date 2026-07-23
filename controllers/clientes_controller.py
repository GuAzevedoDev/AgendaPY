from flask import Blueprint, render_template, session,jsonify,request
from auth import login_required
from services import Cliente
from exeptions import AgendaPy

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
    dados = request.get_json(silent=True) or {}
    cliente_id = dados.get("id")
    if not cliente_id:
        return jsonify({"sucesso": False, "mensagem": "Cliente nao informado"}), 400

    try:
        historico = cliente_service.pegar_historico(cliente_id)
        return jsonify(historico)
    except AgendaPy as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400

@clientes_bp.route("/pesquisar", methods=['GET', 'POST'])
@login_required
def pesquisar_clientes():
    dados = request.get_json(silent=True) or {}
    termo = dados.get("termo", "")
    clientes = cliente_service.pesquisar_clientes_web(termo)
    return jsonify(clientes)

@clientes_bp.route("/cadastrar", methods=['POST'])
@login_required
def cadastrar_cliente():
    dados = request.get_json(silent=True) or {}
    nome = dados.get("nome", "").strip()
    numero = dados.get("numero", "").strip()

    if not nome or not numero:
        return jsonify({
            "sucesso": False,
            "mensagem": "Preencha todos os campos"
            }), 400

    try:
        cliente_id = cliente_service.cadastrar_cliente_web(nome, numero)
        return jsonify({
            "sucesso": True,
            "cliente": {"id": cliente_id, "nome": nome, "numero": numero}
            }), 201
    except AgendaPy as e:
        return jsonify({
            "sucesso": False,
            "mensagem": str(e)
            }), 400