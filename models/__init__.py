from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .clientes import Clientes
from .agendamentos import Agendamentos
from .funcionarios import Funcionarios
from .servicos import Servicos
from .servicos_agendamentos import ServicosAgendamentos

__all__ = ['db','Clientes','Agendamentos','Funcionarios','Servicos','ServicosAgendamentos']

