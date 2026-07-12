from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import Clientes
from . import Agendamentos
from . import Funcionarios

__all__ = ['Clientes','Agendamentos','Funcionarios']

