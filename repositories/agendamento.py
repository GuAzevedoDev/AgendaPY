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
    agendamentos_servicos = ServicosAgendamentos.query.filter_by(agendamento_id = agendamento_id).first()

    db.session.delete(agendamentos_servicos)

    db.session.commit()

  def trazer_horarios_dias(self,data:str,funcionario_id:int):
    agendamentos = Agendamentos.query.filter_by(funcionario_id = funcionario_id,data = data).all()
     
    return agendamentos

