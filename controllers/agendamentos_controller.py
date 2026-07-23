from flask import Blueprint,jsonify,request
from auth import login_required
from services import AgendamentosService,Cliente,ServicosService
from exeptions import AgendaPy

agendamento_bp = Blueprint('agendamento',__name__,url_prefix="/agendar")
agendamento_service = AgendamentosService()
repo_cliente = Cliente()
repo_servico = ServicosService()

@agendamento_bp.route('/', methods=["POST"])
@login_required     #Verifica se existe um funcionario logado
def agendar():
    #Pego do JS
    dados = request.get_json(silent=True) or {}
    #Salvo em variaveis
    idFuncionario = dados.get("idFuncionario")
    nomeCliente = dados.get("nomeCliente")
    numeroCliente = dados.get("numeroCliente")
    nomesServicos = dados.get("nomesServicos")
    dataAgendamento = dados.get("dataAgendamento")
    horaAgendamento = dados.get("horaAgendamento")
    observacaoAgendamento = dados.get("observacao")

    #Validacao do formulario de agendamento
    if not nomeCliente or not numeroCliente or not nomesServicos or not dataAgendamento or not horaAgendamento:
        return jsonify({
            "sucesso": False,
            "mensagem": "Preencha todos os campos"
            }),400
    
    try:
        agendamento_service.marcarHorarioWeb(idFuncionario,nomeCliente,numeroCliente,horaAgendamento,dataAgendamento,nomesServicos,observacaoAgendamento)
        return jsonify({
            "sucesso": True,
            }),201
    except AgendaPy as e:
        return jsonify({
            "sucesso": False,
            "mensagem": str(e)
            }),400


@agendamento_bp.route('/buscaNome', methods=["GET", "POST"])
@login_required   
def buscarNome():
    dados = request.get_json(silent=True) or {}
    nomeCliente = dados.get('nomeCliente', '')
    if request.method == "POST":
        nomesEncontrados = repo_cliente.buscar_nome_web(nomeCliente)
        return  nomesEncontrados


@agendamento_bp.route("/calendario", methods = ['POST'])
@login_required     #Verifica se existe um funcionario logado
def calendario():
    #Pego os dados do js
    dados = request.get_json(silent=True) or {}
    dataSelecionada = dados.get('data')
    idFuncionario = dados.get('idFuncionario')

    if not dataSelecionada or not idFuncionario:
        return jsonify({"sucesso": False, "mensagem": "Dados incompletos"}), 400

    #Chamo a funcao
    try:
        horarios = agendamento_service.mostrarAgendaWeb(idFuncionario,dataSelecionada)
        return jsonify({
            "sucesso": True,
            "mensagem":horarios
            }),200
    except AgendaPy as e:
        return jsonify({
            "sucesso": False,
            "mensagem":str(e)
            }),400

  

@agendamento_bp.route("/diasComAgendamento", methods=["POST"])
@login_required
def dias_com_agendamento():
    dados = request.get_json(silent=True) or {}
    idFuncionario = dados.get("idFuncionario")
    mes = dados.get("mes")
    ano = dados.get("ano")

    if not idFuncionario or not mes or not ano:
        return jsonify({"sucesso": False, "mensagem": "Dados incompletos"}), 400

    try:
        dias = agendamento_service.diasComAgendamentoWeb(int(idFuncionario), int(mes), int(ano))
        return jsonify({"sucesso": True, "dias": dias}), 200
    except AgendaPy as e:
        return jsonify({"sucesso": False, "mensagem": str(e)}), 400


@agendamento_bp.route('/buscaServico', methods=["GET", "POST"])
@login_required   
def buscarServico():
    dados = request.get_json(silent=True) or {}
    nome_servico = dados.get('nomeServico', '')
    if request.method == "POST":
        servicos_encontrados = repo_servico.buscarServicoWeb(nome_servico)
        return servicos_encontrados



@agendamento_bp.route('/atualizarPg', methods=["GET", "POST"])
@login_required   
def atualizarPg():
    #Pego do JS
    dados = request.get_json(silent=True) or {}

    #Salvo em variaveis
    idFuncionario = dados.get("idFuncionario")
    valorAgendamento = dados.get("valorAgendamento")
    formaPagamento = dados.get("formaPagamento")
    dataAgendamento = dados.get("dataAgendamento")
    horaAgendamento = dados.get("horaAgendamento")
    #Validacao do formulario de agendamento
    if not valorAgendamento or not formaPagamento or not dataAgendamento or not horaAgendamento:
        return jsonify({
            "sucesso": False,
            "mensagem": "Preencha todos os campos"
            }),400

    try:
        mensagemPagamento = agendamento_service.atualizarPagoWeb(valorAgendamento,formaPagamento,idFuncionario,dataAgendamento,horaAgendamento)
        return jsonify({
            "sucesso": True,
            })
    except AgendaPy as e:
        return jsonify({
            "sucesso": False,
            "mensagem": str(e)
            }),400



@agendamento_bp.route('/excluirHorario', methods=["POST"])
@login_required   
def excluirHorario():
    # Pega os dados enviados pelo JavaScript (fetch)
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"mensagem": "Dados inválidos", "sucesso": False}), 400

    idFuncionario = dados.get("idFuncionario")
    data = dados.get("dataAgendamento")
    hora = dados.get("horaAgendamento")

    # Validação necessária para os campos obrigatórios
    if not idFuncionario or not data or not hora:
        return jsonify({"mensagem": "Dados incompletos para exclusão", "sucesso": False}), 400

    # Tenta excluir o agendamento no banco
    try:
        sucesso = agendamento_service.excluirAgendamentoWeb(idFuncionario, data, hora)
        if sucesso:
            return jsonify({"mensagem": "Horário excluído com sucesso", "sucesso": True}),200
    except AgendaPy as e:
            return jsonify({"mensagem": str(e), "sucesso": False}),400
