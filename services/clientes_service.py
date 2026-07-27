from exeptions import ClienteError
from repositories import ClienteRepository

repo_cliente = ClienteRepository()


#Clientes(ORM OK)

class Cliente:
  def pesquisar_cliente_web(self,nome:str,num:str) -> int:
    cliente_encontrado = repo_cliente.buscar_cliente(nome)

    if not cliente_encontrado:
      clienteCadastrado = self.cadastrar_cliente_web(nome,num)
      return clienteCadastrado
    cliente_encontrado_id = cliente_encontrado.id

    return cliente_encontrado_id

  def cadastrar_cliente_web(self,nome:str,numero:str) -> int:
    cliente = repo_cliente.cadastrar_cliente(nome,numero or "")
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

  def mostrar_clientes(self) -> list:
    clientes = repo_cliente.trazer_todos_clientes()
    clientes_totais = []
    for cliente in clientes:
      cliente_id = cliente.id
      cliente_nome = cliente.nome
      cliente_numero = cliente.numero

      clientes_totais.append({
        "id": cliente_id,
        "nome": cliente_nome,
        "numero": cliente_numero,
      })

    return clientes_totais

  def pesquisar_clientes_web(self, termo: str) -> list:
    if not termo or not termo.strip():
      return self.mostrar_clientes()
    clientes_encontrados = repo_cliente.busca_pesquisa_cliente(termo.strip())
    clientes_totais = []
    for cliente in clientes_encontrados:
      clientes_totais.append({
        "id": cliente.id,
        "nome": cliente.nome,
        "numero": cliente.numero,
      })
    return clientes_totais

  def pegar_historico(self,cliente_id:int) -> list:
    cliente_id = int(cliente_id)
    dados_cliente = repo_cliente.buscar_cliente_id(cliente_id)
    if not dados_cliente:
      raise ClienteError("Cliente nao encontrado")
    todos_agendamentos = []

    cliente_nome = dados_cliente.nome
    cliente_numero = dados_cliente.numero

    agendamentos = sorted(
      dados_cliente.agendamentos,
      key=lambda agendamento: (agendamento.data, agendamento.horario),
      reverse=True,
    )
    contador = 0
    for agendamento in agendamentos:
      servicos_totais = []
      contador += 1
      agendamento_data = agendamento.data
      data_formatada = agendamento_data.strftime("%d/%m/%Y")

      agendamento_horario = agendamento.horario
      agendamento_horario = str(agendamento_horario)

      agendamento_profissional = agendamento.funcionario.nome
      servicos = agendamento.servicos_agendamentos

      for servico in servicos:
        servicos_totais.append(servico.servico.nome)

      dados_agendamento = {
        "cliente_nome": cliente_nome,
        "cliente_numero": cliente_numero,
        "agendamento_data": data_formatada,
        "agendamento_horario": agendamento_horario,
        "agendamento_profissional": agendamento_profissional,
        "servicos": servicos_totais,
      }

      todos_agendamentos.append(dados_agendamento)
    return todos_agendamentos

  def excluir_cliente_web(self,cliente_id:int) -> None:
    cliente_id = int(cliente_id)
    cliente = repo_cliente.buscar_cliente_id(cliente_id)
    if not cliente:
      raise ClienteError("Cliente nao encontrado")

    if cliente.agendamentos or cliente.anamnese:
      raise ClienteError("Cliente possui agendamentos ou anamnese vinculados e nao pode ser excluido")

    repo_cliente.excluir_cliente(cliente)
