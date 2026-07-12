from . import db
from .base import Base

class Servicos(Base):
  __tablename__ = "servicos"

  nome = db.Column(db.String,nullable = False)
  duracao_min = db.Column(db.Integer,nullable = False)
  
  agendamento = db.relationship('servicos',back_populates = 'servicos')
        
                     

