from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import Clientes

__all__ = [Clientes]

