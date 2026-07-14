from . import db
from .base import Base

class ServicosAgendamentos(Base):
  __tablename__ = 'servicos_agendamentos'
  agendamento_id = db.Column(db.Integer,db.ForeignKey('agendamento.id'),primary_key=True)
  servico_id = db.Column(db.Integer,db.ForeignKey('servicos.id'),primary_key=True)

  agendamento = db.relationship(
      "Agendamentos",
      back_populates="servicos_agendamentos"
  )

  servico = db.relationship(
      "Servicos",
      back_populates="servicos_agendamentos"
  )


