from datetime import datetime

class Base(db.Model):
  __abstract__ = True
  id = db.Column(db.Integer,primary_key = True)
  data_de_criação = db.Column(db.Datetime, default = datetime.now, nullable = False)