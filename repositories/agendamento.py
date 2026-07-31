from models import db,Agendamentos,ServicosAgendamentos

class AgendamentoRepository:
  def cadastrar_horario(self,cliente_id:int,funcionario_id:int,horario:str,data:str,observacao:str):
    agendamento = Agendamentos(cliente_id = cliente_id,funcionario_id = funcionario_id,horario = horario,data = data,observacao = observacao)

    db.session.add(agendamento)
    db.session.commit()


    return agendamento

  def cadastrar_servico_agendamento(self,servico_id:int,agendamento_id:int):
    servico_agendamento = ServicosAgendamentos(servico_id = servico_id,agendamento_id = agendamento_id)
    db.session.add(servico_agendamento)
    db.session.commit()

    return servico_agendamento
  
  def buscar_agendamento(self,funcionario_id:int,data:str,hora:str):
    agendamento = Agendamentos.query.filter_by(funcionario_id = funcionario_id , data = data , horario = hora).first()
    return agendamento

  def atualizar_agendamento(self,valor_formatado:int,forma_pagamento:str,status:str,funcionario_id:int,data:str,hora:str):
    agendamento = self.buscar_agendamento(funcionario_id= funcionario_id,data = data,hora = hora)

    agendamento.valor_pago = valor_formatado
    agendamento.forma_pagamento = forma_pagamento
    agendamento.status = status

    db.session.commit()

  def excluir_agendamento(self,agendamento:tuple):
    db.session.delete(agendamento)
    db.session.commit()

  def excluir_servicos_agendamentos(self,agendamento_id:int):
    #Um agendamento pode ter varios servicos vinculados, entao precisa apagar todos
    agendamentos_servicos = ServicosAgendamentos.query.filter_by(agendamento_id = agendamento_id).all()

    for agendamento_servico in agendamentos_servicos:
      db.session.delete(agendamento_servico)

    db.session.commit()

  def trazer_horarios_dias(self,data:str,funcionario_id:int):
    agendamentos = Agendamentos.query.filter_by(funcionario_id = funcionario_id,data = data).all()

    return agendamentos

  def trazer_agendamentos_do_mes(self,funcionario_id:int,primeiro_dia,ultimo_dia) -> list:
    agendamentos = Agendamentos.query.filter(
      Agendamentos.funcionario_id == funcionario_id,
      Agendamentos.data >= primeiro_dia,
      Agendamentos.data <= ultimo_dia,
    ).all()

    return agendamentos

  def somar_valor_pago_do_mes(self,funcionario_id:int,primeiro_dia,ultimo_dia) -> int:
    total = db.session.query(db.func.coalesce(db.func.sum(Agendamentos.valor_pago),0)).filter(
      Agendamentos.funcionario_id == funcionario_id,
      Agendamentos.status == 'confirmado',
      Agendamentos.data >= primeiro_dia,
      Agendamentos.data <= ultimo_dia,
    ).scalar()

    return total

  def somar_valor_pago_por_servicos(
    self,
    funcionario_id: int,
    primeiro_dia,
    ultimo_dia,
    servicos_ids: list[int],
):
    # 1º: pega os IDs dos agendamentos que têm pelo menos um dos serviços buscados
    subquery = db.session.query(Agendamentos.id).join(
        ServicosAgendamentos, ServicosAgendamentos.agendamento_id == Agendamentos.id
    ).filter(
        Agendamentos.funcionario_id == funcionario_id,
        Agendamentos.status == 'confirmado',
        Agendamentos.data >= primeiro_dia,
        Agendamentos.data <= ultimo_dia,
        ServicosAgendamentos.servico_id.in_(servicos_ids),
    ).distinct().subquery()

    # 2º: soma o valor_pago desses agendamentos, cada um contado uma única vez
    total = db.session.query(
        db.func.coalesce(db.func.sum(Agendamentos.valor_pago), 0)
    ).filter(
        Agendamentos.id.in_(subquery)
    ).scalar()

    return total
