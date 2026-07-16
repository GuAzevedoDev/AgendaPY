from datetime import datetime
from . import db

class Base(db.Model):
  __abstract__ = True
  id = db.Column(db.Integer,primary_key = True)
  data_de_criacao = db.Column(db.DateTime, default = datetime.now, nullable = False)
  data_de_atualizacao = db.Column(db.DateTime,default = datetime.now,onupdate = datetime.now,nullable = False)