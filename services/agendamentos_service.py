import calendar
from datetime import datetime, timedelta
from exeptions import AgendamentoError
from repositories import AgendamentoRepository
from .clientes_service import Cliente
from .servicos_service import ServicosService

repo_agendamento = AgendamentoRepository()


#Agendamentos(Falta apenas mostrarAgendaWeb)

class AgendamentosService:
  @staticmethod
  def gerar_horarios() -> list:
    #Inicio a lista horarios
    horarios = []

    horaI:int = 7
    horaF:int = 23

    #Inicio no horarioI e finalizo na horaF, de 15 em 15 minutos
    atual = datetime.strptime(f"{horaI}:00","%H:%M")
    fim = datetime.strptime(f"{horaF}:00","%H:%M")

    while atual <= fim:
      horarios.append(atual.time())
      atual += timedelta(minutes=15)

      #Retorno os horarios
    return horarios

  def marcarHorarioWeb(self,id_funcionario_logado:int,nome:str,num:str,hora:str,data:str,nomesServicos:str,observacao:str) -> str:
    #Selecionar data
    data = self.selecionar_data_web(data)

    #Selecionar horario
    horario_escolhido = self.selecionar_horario_web(id_funcionario_logado,data,hora)

    self.validar_data_hora(id_funcionario_logado,data,horario_escolhido)

    #Selecione o nome do cliente
    cliente_service = Cliente()
    cliente_escolhido_id = cliente_service.pesquisar_cliente_web(nome,num)

    #Selecione o servico
    servicos_service = ServicosService()
    servicos_ids = servicos_service.selecionar_servico_web(nomesServicos)

    #Passar para o banco
    agendamento = repo_agendamento.cadastrar_horario(cliente_escolhido_id,id_funcionario_logado,horario_escolhido,data,observacao)
    agendamento_id = agendamento.id

    #Itero a lista dos ids dos servicos escolhidos e salvo na tabela com id do mesmo agendamento
    for servico_id in servicos_ids:
      repo_agendamento.cadastrar_servico_agendamento(servico_id,agendamento_id)
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
            observacao = agendamento.observacao

            if horario == hora:
                tudoHorarios.append({"hora":horario.strftime("%H:%M"),"status":"Ocupado","cliente":cliente,"servico":servico_total,"status":status,"valorPago":valor_pago,"formaPagamento":forma_pagamento,"observacao":observacao})
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
    # if dataUsuario.date() < dataAtual.date():
    #   raise AgendamentoError("Essa data esta no passado")


    #Se tiver tudo certo retorno a data
    return dataUsuario

  def diasComAgendamentoWeb(self,id_funcionario_logado:int,mes:int,ano:int) -> list:
    primeiro_dia = datetime(ano,mes,1).date()
    ultimo_dia_numero = calendar.monthrange(ano,mes)[1]
    ultimo_dia = datetime(ano,mes,ultimo_dia_numero).date()

    agendamentos = repo_agendamento.trazer_agendamentos_do_mes(id_funcionario_logado,primeiro_dia,ultimo_dia)

    dias_nao_confirmados = set()
    dias_confirmados = set()

    for agendamento in agendamentos:
      if agendamento.status == "ocupado":
        dias_nao_confirmados.add(agendamento.data.day)
      elif agendamento.status == "confirmado":
        dias_confirmados.add(agendamento.data.day)

    #Um dia so fica "confirmado" (bolinha verde) se TODOS os agendamentos dele estiverem confirmados
    dias_confirmados -= dias_nao_confirmados

    return {"dias_nao_confirmados":sorted(dias_nao_confirmados),"dias_confirmados":sorted(dias_confirmados)}


  def valorFaturadoWeb(self,id_funcionario:int,mes:int,ano:int) -> int:
    primeiro_dia = datetime(ano,mes,1).date()
    ultimo_dia_numero = calendar.monthrange(ano,mes)[1]
    ultimo_dia = datetime(ano,mes,ultimo_dia_numero).date()

    valor_total = repo_agendamento.somar_valor_pago_do_mes(id_funcionario,primeiro_dia,ultimo_dia)
    valor_total_pagar = 0
    valor_total_liquido = valor_total

    if id_funcionario == 4:
      valor_total_pagar = valor_total * 0.20
      valor_total_liquido = valor_total - valor_total_pagar

    elif id_funcionario == 3:
      valor_quimica = repo_agendamento.somar_valor_pago_por_servicos(id_funcionario,primeiro_dia,ultimo_dia,[17,16,21,19])

      valor_nao_quimica = valor_total - valor_quimica

      valor_total_pagar = (valor_quimica * 0.60) + (valor_nao_quimica * 0.50)

      valor_total_liquido = valor_total - valor_total_pagar
    return {"valor_total":valor_total,"valor_total_receber":valor_total_liquido,"valor_total_pagar":valor_total_pagar}

  def validar_horario_nao_passado(self,data:datetime,horario_escolhido) -> None:
    agora = datetime.now()

    #Se a data escolhida for hoje, o horario tambem precisa ser validado
    if data.date() == agora.date() and horario_escolhido <= agora.time():
      raise AgendamentoError("Esse horario ja passou")

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

  def validar_data_hora(self,funcionario_id:int,data:datetime,hora:str):
    agendamento_mesma_data = repo_agendamento.buscar_agendamento(funcionario_id,data.date(),hora)

    if agendamento_mesma_data:
      raise AgendamentoError("Ja existe um agendamento nessa data")

  def atualizarPagoWeb(self,valor,forma_pag,funcionario_id,data,hora) -> bool:
    data = self.converter_data(data)
    hora = self.converter_hora(hora)

    valor = valor.replace(",","")
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
