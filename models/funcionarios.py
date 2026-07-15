from . import db
from .base import Base

class Funcionarios(Base):
  __tablename__ = "funcionarios"

  nome = db.Column(db.String,nullable = False)
  cargo = db.Column(db.String,db.Enum('dono','profissional', name = 'cargo_types'))
  funcao = db.Column(db.String,nullable = False)
  senha = db.Column(db.String,nullable = False)

  agendamentos = db.relationship('Agendamentos',back_populates= 'funcionario')
