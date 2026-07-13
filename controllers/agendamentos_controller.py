from flask import Blueprint,jsonify
from auth import login_required


agendamento_bp = Blueprint('agendamento',url_prefix="/agendar")



@app.route('/', methods=["GET", "POST"])
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

    #Validacao do formulario de agendamento
    if not nomeCliente or not numeroCliente or not nomesServicos or not dataAgendamento or not horaAgendamento:
        return jsonify({"mensagem": "Preencha todos os campos"})
    
    mensagemAgendamento = agendamento_service.marcarHorarioWeb(idFuncionario,nomeCliente,numeroCliente,horaAgendamento,dataAgendamento,nomesServicos)
    return jsonify({"mensagem": mensagemAgendamento})



@app.route('/buscaNome', methods=["GET", "POST"])
@login_required   
def buscarNome():
    dados = request.json
    nomeCliente = dados['nomeCliente']
    if request.method == "POST":
        nomesEncontrados = cliente_service.buscarNomeWeb(nomeCliente)
        return  nomesEncontrados


@app.route("/calendario", methods = ['POST'])
@login_required     #Verifica se existe um funcionario logado
def calendario():
    #Pego os dados do js
    dados = request.json
    dataSelecionada = "0"+dados['data']
    idFuncionario = dados['idFuncionario']
    

    #Chamo a funcao
    horarios = agendamento_service.mostrarAgendaWeb(idFuncionario,dataSelecionada)
    return jsonify(horarios)

  

@app.route('/buscaServico', methods=["GET", "POST"])
@login_required   
def buscarServico():
    dados = request.json
    nomeServico = dados['nomeServico']
    if request.method == "POST":
        servicosEncontrados = servicos_service.buscarServicoWeb(nomeServico)
        return servicosEncontrados



@app.route('/atualizarPg', methods=["GET", "POST"])
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
        return jsonify({"mensagem": "Preencha todos os campos"})


    mensagemPagamento = agendamento_service.atualizarPagoWeb(valorAgendamento,formaPagamento,idFuncionario,dataAgendamento,horaAgendamento)
    return jsonify({"mensagem": mensagemPagamento})



@app.route('/excluirHorario', methods=["POST"])
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
    sucesso = agendamento_service.excluirAgendamentoWeb(idFuncionario, data, hora)
    if sucesso:
        return jsonify({"mensagem": "Horário excluído com sucesso", "sucesso": True})
    else:
        return jsonify({"mensagem": "Agendamento não encontrado ou já excluído", "sucesso": False})
