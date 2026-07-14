from models import db,Agendamentos,ServicosAgendamentos
from exeptions import AgendamentoError

class AgendamentoRepository:
  def cadastrar_horario(self,cliente_id,funcionario_id,horario,data,valor_pago,forma_pagamento,status):
    agendamento = Agendamentos(cliente_id,funcionario_id,horario,data,valor_pago,forma_pagamento,status)
    try:
      db.session.add(agendamento)
      db.session.commit()
    except:
      raise AgendamentoError("Falha ao adicionar o agendamento no banco")

    return cliente

  def buscar_agendamento(self,funcionario_id,data,hora):
    agendamento = Agendamentos.query.filter_by(funcionario_id == funcionario_id and data == data and horario == hora).first()
    return agendamento

  def atualizar_agendamento(self,valor_formatado,forma_de_pag,status,funcionario_id,data,hora):
    agendamento = self.buscar_agendamento(funcionario_id,data,hora)

    agendamento.valor_pago = valor_formatado
    agendamento.forma_pagamento = forma_pagamento
    agendamento.status = status

    db.session.commit()

  def excluir_agendamento(self,agendamento):
    db.session.delete(agendamento)
    db.session.commit()

  def excluir_servicos_agendamentos(agendamento_id):
    agendamentos_servicos = ServicosAgendamentos.query.filter_by(agendamento_id == agendamento_id).first()

    db.session.delete(agendamentos_servicos)

    db.session.commit()


