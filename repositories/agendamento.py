from models import db,Agendamentos
from exeptions import AgendamentoError

class AgendamentoRepository:
  def cadastrar_horario(self,cliente_id,funcionario_id,horario,data,valor_pago,forma_pagamento,status):
    agendamento = Agendamentos(cliente_id,funcionario_id,horario,data,valor_pago,forma_pagamento,status)
    try:
      db.session.add(agendamento)
      db.commit()
    except:
      raise AgendamentoError("Falha ao adicionar o agendamento no banco")

    return cliente

  

  
