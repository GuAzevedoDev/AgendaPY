from flask import Blueprint, render_template, session, jsonify, request
from auth import login_required
from services import Anamnese
from exeptions import AgendaPy

anamnese_service = Anamnese()

anamnese_bp = Blueprint("anamnese", __name__, url_prefix="/anamnese")


# --- Rotas publicas: o cliente preenche sem precisar logar ---

@anamnese_bp.route("/responder")
def responder():
    return render_template("anamnese_form.html")

@anamnese_bp.route("/enviar", methods=['POST'])
def enviar_ficha():
    dados = request.get_json(silent=True) or {}
    nome = dados.get("nome", "").strip()
    numero = dados.get("numero", "").strip()
    respostas = dados.get("respostas")

    if not nome or not numero or not respostas or not isinstance(respostas, dict):
        return jsonify({
            "sucesso": False,
            "mensagem": "Preencha todos os campos obrigatorios"
            }), 400

    try:
        anamnese_service.enviar_ficha_web(nome, numero, respostas)
        return jsonify({"sucesso": True}), 201
    except AgendaPy as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400


# --- Rotas protegidas: uso da equipe ---

@anamnese_bp.route("/")
@login_required
def anamnese():
    sessaoFun = {
        "funcionario_id": session.get("funcionario_id"),
        "funcionario_nome": session.get("funcionario_nome"),
        "funcionario_cargo": session.get("funcionario_cargo"),
        "funcionario_funcao": session.get("funcionario_funcao")
    }
    return render_template("anamnese.html", sessaoFun=sessaoFun)

@anamnese_bp.route("/mostrar", methods=['GET', 'POST'])
@login_required
def mostrar_fichas():
    fichas = anamnese_service.listar_fichas_web()
    return jsonify(fichas)

@anamnese_bp.route("/detalhes", methods=['POST'])
@login_required
def detalhes_ficha():
    dados = request.get_json(silent=True) or {}
    anamnese_id = dados.get("id")
    if not anamnese_id:
        return jsonify({"sucesso": False, "mensagem": "Ficha nao informada"}), 400

    try:
        ficha = anamnese_service.obter_ficha_web(anamnese_id)
        return jsonify(ficha)
    except AgendaPy as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400

@anamnese_bp.route("/atualizar", methods=['POST'])
@login_required
def atualizar_ficha():
    dados = request.get_json(silent=True) or {}
    anamnese_id = dados.get("id")
    respostas = dados.get("respostas")

    if not anamnese_id or not respostas or not isinstance(respostas, dict):
        return jsonify({
            "sucesso": False,
            "mensagem": "Preencha todos os campos obrigatorios"
            }), 400

    try:
        anamnese_service.atualizar_ficha_web(anamnese_id, respostas)
        return jsonify({"sucesso": True}), 200
    except AgendaPy as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400
