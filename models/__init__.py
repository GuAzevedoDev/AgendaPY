from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .clientes import Clientes
from .agendamentos import Agendamentos
from .funcionarios import Funcionarios
from .servicos import Servicos
from .servicos_agendamentos import ServicosAgendamentos
from .anamnese import Anamnese

__all__ = ['db','Clientes','Agendamentos','Funcionarios','Servicos','ServicosAgendamentos','Anamnese']

