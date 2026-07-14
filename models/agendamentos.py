from . import db
from .base import Base

class Agendamentos(Base):
  __tablename__ = "agendamentos"

  nome = db.Column(db.String,nullable = False)
  cliente_id = db.Column(
    db.Integer,
    db.ForeignKey("clientes.id"),
    primary_key=True
  )
  funcionario_id = db.Column(db.Integer,db.ForeignKey("funcionarios.id"),primary_key=True)
  horario = db.Column(db.String,nullable = False)
  data = db.Column(db.Date,nullable = False)
  valor_pago = db.Column(db.Integer,nullable = False)
  forma_pagamento = db.Column(db.Integer,nullable = False)
  status = db.Column(db.Enum('confirmado','cancelado','concluido',name = 'status_type'),default='confirmado')

  cliente = db.relationship('Clientes',back_populates= "agendamentos")
  funcionario = db.relationship('Funcionarios',back_populates= "agendamentos")
  servicos_agendamentos = db.relationship(
        "ServicosAgendamentos",
        back_populates="agendamento",
    )
