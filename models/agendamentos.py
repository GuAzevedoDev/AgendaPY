from . import db
from .base import Base

class Agendamentos(Base):
  __tablename__ = "agendamentos"

  nome = db.Column(db.String,nullable = False)
  cliente_id = db.Column(
    db.Integer,
    db.ForeignKey("clientes.id")
  )
  funcionario_id = db.Column(db.Integer,db.ForeignKey("funcionarios.id"))
  horario = db.Column(db.String,nullable = False)
  data = db.Column(db.Date,nullable = False)
  valor_pago = db.Column(db.Integer,nullable = False)
  forma_pagamento = db.Column(db.Integer,nullable = False)
  status = db.Column(db.Enum('confirmado','cancelado','concluido',name = 'status_type'),default='confirmado')

  cliente = db.relationship('Clientes',back_populates= "agendamentos")
  funcionario = db.relationship('Funcionarios',back_populates= "agendamentos")

        
                     
#         -- servicos e funcionarios
#         CREATE TABLE IF NOT EXISTS servicos_funcionarios (
#             funcionario_id INTEGER NOT NULL,
#             servico_id     INTEGER NOT NULL,
#             PRIMARY KEY (funcionario_id, servico_id),
#             FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE,
#             FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE
#         );
                     

#         -- agendamentos
#             FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
#             FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
#         );
                     
#         -- agendamento x servico
#         CREATE TABLE IF NOT EXISTS agendamentos_servicos (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             servicos_id        INTEGER NOT NULL,
#             agendamentos_id  INTEGER NOT NULL,
#             FOREIGN KEY (servicos_id) REFERENCES servicos(id) ON DELETE CASCADE,
#             FOREIGN KEY (agendamentos_id) REFERENCES agendamentos(id) ON DELETE CASCADE
#         );
                     
#         -- índice para evitar conflito de horário
#         CREATE UNIQUE INDEX IF NOT EXISTS idx_sem_conflito
#         ON agendamentos(funcionario_id, data, horario)
#         WHERE status = 'confirmado';
#         """