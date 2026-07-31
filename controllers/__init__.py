from .agendamentos_controller import agendamento_bp
from .auth_controller import auth_bp
from .home_controller import home_bp
from .clientes_controller import clientes_bp
from .anamnese_controller import anamnese_bp
from .financeiro_controller import financeiro_bp

__all__ = ['agendamento_bp','auth_bp','home_bp','clientes_bp','anamnese_bp','financeiro_bp']