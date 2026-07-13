from . import db
from .base import Base

class Clientes(Base):
  __tablename__ = "clientes"

  nome = db.Column(db.String,nullable = False)
  numero = db.Column(db.String,nullable = False)

  agendamentos = db.relationship('Agendamentos',back_populates = 'cliente')



# """
#         PRAGMA foreign_keys = ON;

#         -- funcionarios
#         CREATE TABLE IF NOT EXISTS funcionarios (
#             id       INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome     TEXT NOT NULL UNIQUE,
#             cargo    TEXT NOT NULL CHECK(cargo IN ('dono', 'profissional')),
#             funcao   TEXT NOT NULL,
#             senha    TEXT NOT NULL
#         );

#         -- clientes
#         CREATE TABLE IF NOT EXISTS clientes (
#             id        INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome      TEXT NOT NULL,
#             telefone  TEXT
#         );

#         -- servicos
#         CREATE TABLE IF NOT EXISTS servicos (
#             id           INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome         TEXT NOT NULL,
#             duracao_min  INTEGER NOT NULL
#         );
        
                     
#         -- servicos e funcionarios
#         CREATE TABLE IF NOT EXISTS servicos_funcionarios (
#             funcionario_id INTEGER NOT NULL,
#             servico_id     INTEGER NOT NULL,
#             PRIMARY KEY (funcionario_id, servico_id),
#             FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE,
#             FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE
#         );
                     

#         -- agendamentos
#         CREATE TABLE IF NOT EXISTS agendamentos (
#             id              INTEGER PRIMARY KEY AUTOINCREMENT,
#             cliente_id      INTEGER NOT NULL,
#             funcionario_id  INTEGER NOT NULL,
#             horario         TEXT NOT NULL,
#             data            TEXT NOT NULL,
#             valor_pago      REAL,
#             forma_pagamento TEXT CHECK(forma_pagamento IN ('pix', 'dinheiro', 'débito', 'crédito')),
#             status          TEXT NOT NULL DEFAULT 'confirmado'
#                             CHECK(status IN ('confirmado', 'cancelado', 'concluido')),
#             criado_em       TEXT NOT NULL DEFAULT (datetime('now')),

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