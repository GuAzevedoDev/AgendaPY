from . import db
from .base import Base

class Servicos(Base):
  __tablename__ = "servicos"

  nome = db.Column(db.String,nullable = False)
  duracao_min = db.Column(db.Integer,nullable = False)

  servicos_agendamentos = db.relationship(
    "ServicosAgendamentos",
    back_populates="servico"
  )

  def __repr__(self):
    return f"{self.id} - {self.nome} ({self.duracao_min} min)"

