from . import db
from .base import Base

class Agendamentos(Base):
  __tablename__ = "agendamentos"

  cliente_id = db.Column(
    db.Integer,
    db.ForeignKey("clientes.id"),
  )
  funcionario_id = db.Column(db.Integer,db.ForeignKey("funcionarios.id"))
  horario = db.Column(db.Time,nullable = False)
  data = db.Column(db.Date,nullable = False)
  valor_pago = db.Column(db.Integer,nullable = True )
  forma_pagamento = db.Column(db.Integer,nullable = True)
  status = db.Column(db.Enum('confirmado','cancelado','concluido',name = 'status_type'),default='confirmado')

  cliente = db.relationship('Clientes',back_populates= "agendamentos")
  funcionario = db.relationship('Funcionarios',back_populates= "agendamentos")

  servicos_agendamentos = db.relationship(
    "ServicosAgendamentos", 
    back_populates="agendamento"
  )
  