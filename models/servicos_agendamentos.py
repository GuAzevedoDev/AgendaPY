from . import db
from .base import Base

class ServicosAgendamentos(Base):
  __tablename__ = 'servicos_agendamentos'
  agendamento_id = db.Column(db.Integer,db.ForeignKey('agendamentos.id'))
  servico_id = db.Column(db.Integer,db.ForeignKey('servicos.id'))

  agendamento = db.relationship(
      "Agendamentos",
      back_populates="servicos_agendamentos"
  )

  servico = db.relationship(
      "Servicos",
      back_populates="servicos_agendamentos"
  )


