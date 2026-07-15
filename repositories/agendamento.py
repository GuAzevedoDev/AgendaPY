from models import db,Agendamentos,ServicosAgendamentos
from exeptions import AgendamentoError

class AgendamentoRepository:
  def cadastrar_horario(self,cliente_id:int,funcionario_id:int,horario:str,data:str,valor_pago:int,forma_pagamento:str,status:str):
    agendamento = Agendamentos(cliente_id,funcionario_id,horario,data,valor_pago,forma_pagamento,status)
    try:
      db.session.add(agendamento)
      db.session.commit()
    except:
      raise AgendamentoError("Falha ao adicionar o agendamento no banco")

    return agendamento

  def cadastrar_servico_agendamento(self,servico_id:int,agendamento_id:int):
    servico_agendamento = ServicosAgendamentos(servico_id,agendamento_id)
    db.session.add(servico_agendamento)
    db.session.commit()

    return servico_agendamento
  
  def buscar_agendamento(self,funcionario_id:int,data:str,hora:str):
    agendamento = Agendamentos.query.filter_by(funcionario_id == funcionario_id and data == data and horario == hora).first()
    return agendamento

  def atualizar_agendamento(self,valor_formatado:int,forma_pagamento:str,status:str,funcionario_id:int,data:str,hora:str):
    agendamento = self.buscar_agendamento(funcionario_id,data,hora)

    agendamento.valor_pago = valor_formatado
    agendamento.forma_pagamento = forma_pagamento
    agendamento.status = status

    db.session.commit()

  def excluir_agendamento(self,agendamento:tuple):
    db.session.delete(agendamento)
    db.session.commit()

  def excluir_servicos_agendamentos(self,agendamento_id:int):
    agendamentos_servicos = ServicosAgendamentos.query.filter_by(agendamento_id == agendamento_id).first()

    db.session.delete(agendamentos_servicos)

    db.session.commit()


