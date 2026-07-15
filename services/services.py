import hashlib
from datetime import datetime
from contextlib import contextmanager
from exeptions import AgendamentoError,ClienteError,FuncionarioError,ServicoError
from repositories import AgendamentoRepository,ClienteRepository,FuncionarioRepository,ServicoRepository

repo_agendamento = AgendamentoRepository()
repo_cliente = ClienteRepository()
repo_funcionario = FuncionarioRepository()
repo_servico = ServicoRepository()


#Funcionario(ORM OK)

class Funcionario:
  def loginFuncionarioWeb(self,nome:str,senha:str) -> tuple:
    #Transformar a senha em hash para comparação com db
    senha = senha.encode('utf-8')
    senha = hashlib.sha256(senha)
    senha = senha.hexdigest()

    #Se encontrado ele salva na variavel
    funcionario_encontrado = repo_funcionario.buscar_funcionario(nome.capitalize())
    #Se nao encontrado nao passa no if, verifico se a senha esta correta
    if not funcionario_encontrado or senha != funcionario_encontrado.senha:
      raise FuncionarioError("Credenciais invalidas")

    #Se tudo ok retorno funcionario_encontrado
    return funcionario_encontrado
  
  def mostrarFuncionariosWeb(self) -> list:
    funcionariosEncontrados = repo_funcionario.mostrar_funcionarios()
    return funcionariosEncontrados

  def cadastrarFuncionarios(self):
    while True:
      nome = input("Digite seu nome: ")
      funcionarioExistente = repo_funcionario.buscar_funcionario(nome)

      if funcionarioExistente is None:
        break
            
      print(f"Funcionario '{nome}' ja existe, tente outro nome.")

    cargo = input("Digite seu cargo [dono] // [profissional]: ")
    funcao = input("Digite sua funcao: ")
    senha = input("Digite sua senha: ").encode('utf-8')
    hashSenha = hashlib.sha256(senha)
    senhaHex = hashSenha.hexdigest()

    repo_funcionario.cadastrar_funcionarios(nome,cargo.lower(),funcao,senhaHex)
    print(f"Funcionario {nome} adicionado!")



#Servicos (ORM OK)

class ServicosService:
  def selecionarServicoWeb(self,nomesServicos:list) -> list:
    #Pego todos os servicos
    servicos = self.mostrarServicosWeb()

    #Inicio uma lista vazia
    listaServicos = []

    #Se nao tiver servicos cadastrados
    if not servicos:
      raise("Sem servicos cadastrados")
    
    #Passo por todos se bater com o nome digitado retorno a lista com os servicos selecionados
    for servico in servicos:
      for nome in nomesServicos:
        if servico[1] == nome:
          listaServicos.append(servico[0])

    #Retorno a lista com os servicos selecionados
    return listaServicos
  
  def mostrarServicosWeb(self) -> list:
    #Conexao segura com db
    servicosEncontrados = repo_servico.mostrar_servicos()

    #Se nao exitir retorno lista vazia
    if not servicosEncontrados:
      return []
    
    #Se exitir retorno lista com todos
    return servicosEncontrados
  
  def cadastrarServicosWeb(self,nome:str, duracao:int) -> int:
    #Insiro no bd as informacoes passadas nos parametros
    servico = repo_servico.cadastrar_servico(nome,duracao)
    return servico[0]

  def buscarServicoWeb(self,servico:str) -> list:
    servicosEncontrados = repo_funcionario.busca_pesquisa_cliente(servico)

    return servicosEncontrados



#Agendamentos(Falta apenas mostrarAgendaWeb)

class AgendamentosService:
  @staticmethod
  def gerarHorarios() -> list:
    #Inicio a lista horarios
    horarios = []

    horaI:int = 7
    horaF:int = 23

    #Inicio no horarioI e finalizo na horaF
    for i in range(horaI,horaF + 1):
      horarios.append(f"{horaI}:00")

      #Quando for igual a horaF nao coloca o :30 na lista
      if horaF != i:
        horarios.append(f"{horaI}:30")
      horaI = horaI + 1

      #Retorno os horarios
    return horarios
  
  def marcarHorarioWeb(self,id_funcionario_logado:int,nome:str,num:str,hora:str,data:str,nomesServicos:str) -> str:
    #Selecionar data
    data = self.selecionarDataWeb(data)

    #Selecionar horario
    horario_escolhido = self.selecionarHorarioWeb(id_funcionario_logado,data,hora)
    
    #Selecione o nome do cliente
    cliente_service = Cliente()
    cliente_escolhido_id = cliente_service.pesquisarClienteWeb(nome,num)
    
    #Selecione o servico
    servicos_service = ServicosService()
    servicos_ids = servicos_service.selecionarServicoWeb(nomesServicos)
    
    #Passar para o banco
    agendamento = repo_agendamento.cadastrar_horario(cliente_escolhido_id,id_funcionario_logado,horario_escolhido,data)
    agendamento_id = agendamento[0]

    #Itero a lista dos ids dos servicos escolhidos e salvo na tabela com id do mesmo agendamento
    for servico_id in servicos_ids:
      AgendamentoRepository.cadastrar_servico_agendamento(servico_id,agendamento_id)
    return True

  def selecionarHorarioWeb(self,id_funcionario_logado:int, data:str, horario_escolhido:str) -> str:
    horarios = AgendamentosService.gerarHorarios()
    tudoHorarios = self.mostrarAgendaWeb(id_funcionario_logado,data)
    ocupados = []
    for horario in tudoHorarios:
      if horario['status'] == 'Ocupado':
        ocupados.append(horario['hora'])
    
    if horario_escolhido not in horarios:
      raise AgendamentoError("Esse horario não é válido")
    
    if horario_escolhido in ocupados:
      raise AgendamentoError("Esse horario já está ocupado")
    
    return horario_escolhido

  def mostrarAgendaWeb(self,id_funcionario_logado:int, data:str) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    ocupados = []
    tudoHorarios = []
    horarios = AgendamentosService.gerarHorarios()
    cursor.execute("""
          SELECT horario, clientes.nome, servicos.nome, status,valor_pago,forma_pagamento
          FROM agendamentos
          INNER JOIN agendamentos_servicos ON agendamentos.id = agendamentos_servicos.agendamentos_id
          INNER JOIN servicos ON agendamentos_servicos.servicos_id = servicos.id
          INNER JOIN clientes ON agendamentos.cliente_id = clientes.id
          WHERE funcionario_id = ?
          AND data = ?
    """, (id_funcionario_logado, data))

    horariosDia = cursor.fetchall()

    for horario in horarios:
        encontrado = False

        for agendamento in horariosDia:
            hora, cliente, servico, status, valorPago,formaPagamento = agendamento

            if horario == hora:
                tudoHorarios.append({"hora":horario,"status":"Ocupado","cliente":cliente,"servico":servico,"concluido":status,"valorPago":valorPago,"formaPagamento":formaPagamento})
                encontrado = True
                ocupados.append(agendamento)
                break

        if not encontrado:
            tudoHorarios.append({"hora":horario,"status":"Livre"})
    return tudoHorarios
  
  def selecionarDataWeb(self,data:str) -> str:
    #Pego a data atual
    dataAtual:str = datetime.now()

    #Transformo a data do usuario pro formato
    dataUsuario:str = datetime.strptime(data, "%d/%m/%Y")
    
    #Se aconteceu antes retorna None
    if dataUsuario.date() < dataAtual.date():
      raise AgendamentoError("Essa data esta no passado")
    
    #Se tiver tudo certo retorno a data
    return data

  def excluirAgendamentoWeb(self,funcionario_id, data, hora) -> bool:
    # Busca o ID do agendamento para poder remover as dependências primeiro (tabela agendamentos_servicos)
    agendamento = AgendamentoRepository.buscar_agendamento(funcionario_id,data,hora)
    
    #Caso nao exista agendamento
    if not agendamento:
      raise AgendamentoError("Não existe esse agendamento")
    agendamento_id = agendamento[0]

    # Remove os serviços vinculados a esse agendamento
    AgendamentoRepository.excluir_servicos_agendamentos(agendamento_id)

    # Remove o agendamento principal
    AgendamentoRepository.excluir_agendamento(agendamento)

    return True
    
  def atualizarPagoWeb(self,valor,forma_pag,funcionario_id,data,hora) -> bool:
    status = "confirmado"
    formas_de_pag = ["pix",'debito','dinheiro','credito']
    valor_formatado = float(valor)
    
    if valor_formatado <= 0:
      raise AgendamentoError("Valor inválido")
    
    if not forma_pag in formas_de_pag:
      raise AgendamentoError("Forma de pagamento inválida")
    
    AgendamentoRepository.atualizar_agendamento(valor_formatado,forma_pag,status,funcionario_id,data,hora)

    return True



#Clientes(ORM OK)

class Cliente:
  def pesquisarClienteWeb(self,nome,num) -> int:
    cliente_encontrado = repo_cliente.buscar_cliente(nome)
    cliente_encontrado_id = cliente_encontrado[0]

    if not cliente_encontrado_id:
      clienteCadastrado = self.cadastrarClienteWeb(nome,num)
      return clienteCadastrado

    return cliente_encontrado_id
  
  def cadastrarClienteWeb(self,nome,numero) -> int:
    cliente = repo_cliente.cadastrar_cliente(nome,numero)
    cliente_id = cliente[0]
    if not cliente_id:
      raise ClienteError("Nao foi possivel cadastrar o cliente")
    return cliente_id

  def buscarNomeWeb(self,nome) -> list:
    clientes_encontrados = repo_cliente.busca_pesquisa_cliente(nome)
    return clientes_encontrados
