from . import db
from .base import Base

class Clientes(Base):
  __tablename__ = "clientes"

  nome = db.Column(db.String,nullable = False)
  numero = db.Column(db.String,nullable = False)

  agendamentos = db.relationship('Agendamentos',back_populates = 'cliente')
  anamnese = db.relationship('Anamnese',back_populates = 'cliente',uselist = False)
