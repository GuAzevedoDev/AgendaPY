from . import db
from .base import Base

class ServicosAgendamentos(Base):
  __tablename__ = 'servicos_agendamentos'

  servicos_id = db.Column(db.Integer,db.ForeignKey('servicos.id'))
  
  servicos = db.relationship('Servicos',back_populates = 'agendamentos')



