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
  def selecionar_servico_web(self,nomesServicos:list) -> list:
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
        if servico.nome == nome:
          listaServicos.append(servico.id)

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
    return servico.id

  def buscarServicoWeb(self,servico:str) -> list:
    servicos_encontrados = repo_servico.busca_pesquisa_servicos(servico)
    #Retorna tudo de servicos em uma lista logo preciso de iterar e fazer uma lista so de id e nome
    nomes_servicos = []

    for servico in servicos_encontrados:
      nomes_servicos.append((servico.id,servico.nome))

    return nomes_servicos



#Agendamentos(Falta apenas mostrarAgendaWeb)

class AgendamentosService:
  @staticmethod
  def gerar_horarios() -> list:
    #Inicio a lista horarios
    horarios = []

    horaI:int = 7
    horaF:int = 23

    #Inicio no horarioI e finalizo na horaF
    for i in range(horaI,horaF + 1):
      horarios.append(datetime.strptime(f"{horaI}:00","%H:%M").time())

      #Quando for igual a horaF nao coloca o :30 na lista
      if horaF != i:
        horarios.append(datetime.strptime(f"{horaI}:30","%H:%M").time())
      horaI = horaI + 1

      #Retorno os horarios
    return horarios
  
  def marcarHorarioWeb(self,id_funcionario_logado:int,nome:str,num:str,hora:str,data:str,nomesServicos:str) -> str:
    #Selecionar data
    data = self.selecionar_data_web(data)

    #Selecionar horario
    horario_escolhido = self.selecionar_horario_web(id_funcionario_logado,data,hora)
    
    #Selecione o nome do cliente
    cliente_service = Cliente()
    cliente_escolhido_id = cliente_service.pesquisar_cliente_web(nome,num)
    
    #Selecione o servico
    servicos_service = ServicosService()
    servicos_ids = servicos_service.selecionar_servico_web(nomesServicos)
    
    #Passar para o banco
    agendamento = repo_agendamento.cadastrar_horario(cliente_escolhido_id,id_funcionario_logado,horario_escolhido,data)
    agendamento_id = agendamento.id

    #Itero a lista dos ids dos servicos escolhidos e salvo na tabela com id do mesmo agendamento
    for servico_id in servicos_ids:
      repo_agendamento  .cadastrar_servico_agendamento(servico_id,agendamento_id)
    return True

  def selecionar_horario_web(self,id_funcionario_logado:int, data:str, horario_escolhido:str) -> str:
    horarios = AgendamentosService.gerar_horarios()
    tudoHorarios = self.mostrarAgendaWeb(id_funcionario_logado,data)
    horario_escolhido = self.converter_hora(horario_escolhido)
    data = self.converter_data(data)
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
    ocupados = []
    tudoHorarios = []
    horarios = AgendamentosService.gerar_horarios()
    data = self.converter_data(data)
    horarios_dia = repo_agendamento.trazer_horarios_dias(data,id_funcionario_logado)

    for horario in horarios:
        encontrado = False

        for agendamento in horarios_dia:
            hora = agendamento.horario
            cliente = agendamento.cliente.nome
            servicos_agendamentos = agendamento.servicos_agendamentos
            servico_total = []
            for servico_agendamento in servicos_agendamentos:
              servico_total.append(servico_agendamento.servico.nome)
            status = agendamento.status
            valor_pago = agendamento.valor_pago
            forma_pagamento = agendamento.forma_pagamento

            if horario == hora:
                tudoHorarios.append({"hora":horario.strftime("%H:%M"),"status":"Ocupado","cliente":cliente,"servico":servico_total,"concluido":status,"valorPago":valor_pago,"formaPagamento":forma_pagamento})
                encontrado = True
                ocupados.append(agendamento)
                break

        if not encontrado:
            tudoHorarios.append({"hora":horario.strftime("%H:%M"),"status":"Livre"})
    return tudoHorarios
  
  def selecionar_data_web(self,data:str) -> str:
    #Pego a data atual
    dataAtual:str = datetime.now()

    #Transformo a data do usuario pro formato
    dataUsuario:str = datetime.strptime(data, "%d/%m/%Y")
    
    #Se aconteceu antes retorna None
    if dataUsuario.date() < dataAtual.date():
      raise AgendamentoError("Essa data esta no passado")
    
    #Se tiver tudo certo retorno a data
    return dataUsuario

  def excluirAgendamentoWeb(self,funcionario_id:int, data:str, hora:str) -> bool:
    # Busca o ID do agendamento para poder remover as dependências primeiro (tabela agendamentos_servicos)
    # Passar data e hora para o tipo correto
    data = self.converter_data(data)
    hora = self.converter_hora(hora)

    agendamento = repo_agendamento.buscar_agendamento(funcionario_id,data,hora)
    
    #Caso nao exista agendamento
    if not agendamento:
      raise AgendamentoError("Não existe esse agendamento")
    agendamento_id = agendamento.id

    # Remove os serviços vinculados a esse agendamento
    repo_agendamento.excluir_servicos_agendamentos(agendamento_id)

    # Remove o agendamento principal
    repo_agendamento.excluir_agendamento(agendamento)

    return True
    
  def atualizarPagoWeb(self,valor,forma_pag,funcionario_id,data,hora) -> bool:
    data = self.converter_data(data)
    hora = self.converter_hora(hora)

    status = "confirmado"
    formas_de_pag = ["pix",'debito','dinheiro','credito']
    valor_formatado = float(valor)
    
    if valor_formatado <= 0:
      raise AgendamentoError("Valor inválido")
    
    if not forma_pag in formas_de_pag:
      raise AgendamentoError("Forma de pagamento inválida")
    
    repo_agendamento.atualizar_agendamento(valor_formatado,forma_pag,status,funcionario_id,data,hora)

    return True

  def converter_hora(self,hora):
    if isinstance(hora,str):
      hora = datetime.strptime(hora,"%H:%M").time()
    elif hora is None:
      raise AgendamentoError("Nao foi possivel converter a hora")
    return hora
  
  def converter_data(self,data):
    if isinstance(data,str):
      data = datetime.strptime(data, "%d/%m/%Y").date()
    elif data is None:
      raise AgendamentoError("Nao foi possivel converter a data")
    
    return data
    


#Clientes(ORM OK)

class Cliente:
  def pesquisar_cliente_web(self,nome:str,num:str) -> int:
    cliente_encontrado = repo_cliente.buscar_cliente(nome)
    cliente_encontrado_id = cliente_encontrado.id

    if not cliente_encontrado_id:
      clienteCadastrado = self.cadastrar_cliente_web(nome,num)
      return clienteCadastrado

    return cliente_encontrado_id
  
  def cadastrar_cliente_web(self,nome:str,numero:str) -> int:
    cliente = repo_cliente.cadastrar_cliente(nome,numero)
    cliente_id = cliente.id
    if not cliente_id:
      raise ClienteError("Nao foi possivel cadastrar o cliente")
    return cliente_id

  def buscar_nome_web(self,nome:str) -> list:
    clientes_encontrados = repo_cliente.busca_pesquisa_cliente(nome)
    lista_clientes = []
    for cliente in clientes_encontrados:
      lista_clientes.append((cliente.id,cliente.nome,cliente.numero))
    return lista_clientes
