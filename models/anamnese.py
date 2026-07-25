from . import db
from .base import Base

class Anamnese(Base):
  __tablename__ = "anamneses"

  cliente_id = db.Column(db.Integer,db.ForeignKey("clientes.id"),nullable = False,unique = True)
  respostas = db.Column(db.JSON,nullable = False)

  cliente = db.relationship('Clientes',back_populates = 'anamnese')
