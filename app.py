from services.services import AgendamentosService, ServicosService,Funcionario,Cliente
from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash
from config import DevelopmentConfig
import hashlib
from auth import login_required

servicos_service = ServicosService()
agendamento_service = AgendamentosService()
funcionario_service = Funcionario()
cliente_service = Cliente()

def create_app(config = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    return app

app = create_app()
#Login

#Pagina de login, retorna html
@app.route("/login", methods=["GET", "POST"])
def login():
    #Se estiver no metodo get ele so pega a renderiza o html
    if request.method == "GET":
        return render_template("login.html")
    
    #Se estiver no metodo POST ele pega os dados do usuario 
    elif request.method == "POST":
        #Pega dado do form HTML
        usuario = request.form["nomeUsuario"]
        #O encode transforma o utf puro pra bytes pois o hash so aceita bytes
        senha = request.form["senhaUsuario"].encode('utf-8')
        hashSenha = hashlib.sha256(senha)
        senhaHex = hashSenha.hexdigest()
       
        #validacao de formulario
        if usuario and senha:
            funcionario = funcionario_service.loginFuncionarioWeb(usuario, senhaHex)
        else:
            flash("Preencha todos os campos"), 400
            return redirect(url_for("login"))
    
        if not funcionario:
            flash("Senha ou Usuario incorretos"), 400
            return redirect(url_for("login"))
        
        # login OK
        session["funcionario_id"] = funcionario[0]
        session["funcionario_nome"] = funcionario[1]
        session["funcionario_cargo"] = funcionario[2]
        session["funcionario_funcao"] = funcionario[3]
        #Caso passe por todos os retornos o login esta OK e redireciona
        #Dentro da url_for(nome da funcao)
        return redirect(url_for("home"))
    


#Rota de logout
@app.route("/logout")
@login_required     #Verifica se existe um funcionario logado
def logoutFunc():
    #Limpa sessao
    session.clear()
    
    #Redirecionamento para funcao login
    return redirect(url_for("login"))


#Pagina inicial,retorna html
@app.route("/")
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



@app.route('/agendar', methods=["GET", "POST"])
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


if __name__ == "__main__":
    app.run(debug=True)