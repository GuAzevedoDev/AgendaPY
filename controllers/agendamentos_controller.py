from flask import Blueprint,jsonify,request
from auth import login_required
from services.services import AgendamentosService,Cliente,ServicosService
from exeptions import AgendaPy,AgendamentoError,ClienteError,FuncionarioError,ServicoError

agendamento_bp = Blueprint('agendamento',__name__,url_prefix="/agendar")
agendamento_service = AgendamentosService()
repo_cliente = Cliente()
repo_servico = ServicosService()

@agendamento_bp.route('/', methods=["POST"])
@login_required     #Verifica se existe um funcionario logado
def agendar():
    #Pego do JS
    dados = request.json
    #Salvo em variaveis
    idFuncionario = dados["idFuncionario"]
    nomeCliente = dados["nomeCliente"]
    numeroCliente = dados["numeroCliente"]
    nomesServicos = dados["nomesServicos"]
    dataAgendamento = dados["dataAgendamento"]
    horaAgendamento = dados["horaAgendamento"]
    observacaoAgendamento = dados["observacao"]

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
    dados = request.json
    nomeCliente = dados['nomeCliente']
    if request.method == "POST":
        nomesEncontrados = repo_cliente.buscar_nome_web(nomeCliente)
        return  nomesEncontrados


@agendamento_bp.route("/calendario", methods = ['POST'])
@login_required     #Verifica se existe um funcionario logado
def calendario():
    #Pego os dados do js
    dados = request.json
    dataSelecionada = dados['data']
    idFuncionario = dados['idFuncionario']
    

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

  

@agendamento_bp.route('/buscaServico', methods=["GET", "POST"])
@login_required   
def buscarServico():
    dados = request.json
    nome_servico = dados['nomeServico']
    if request.method == "POST":
        servicos_encontrados = repo_servico.buscarServicoWeb(nome_servico)
        return servicos_encontrados



@agendamento_bp.route('/atualizarPg', methods=["GET", "POST"])
@login_required   
def atualizarPg():
    #Pego do JS
    dados = request.json

    #Salvo em variaveis
    idFuncionario = dados["idFuncionario"]
    valorAgendamento = dados["valorAgendamento"]
    formaPagamento = dados["formaPagamento"]
    dataAgendamento = dados["dataAgendamento"]
    horaAgendamento = dados["horaAgendamento"]
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
    dados = request.json
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
