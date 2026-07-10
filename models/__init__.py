from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import clientes

__all__ = ['Clientes',]

