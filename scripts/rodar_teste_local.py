"""
Sobe a aplicacao localmente para testes rapidos, sem precisar do Docker/Postgres.

Usa um banco SQLite local (dev.db, na raiz do projeto — ja esta no .gitignore)
em vez do Postgres de producao. Cria as tabelas automaticamente e garante um
funcionario de teste para poder logar.

Como rodar (a partir da raiz do projeto):
    venv\\Scripts\\python.exe scripts\\rodar_teste_local.py

Depois e so acessar http://127.0.0.1:5055
Login de teste: usuario "mali", senha "123456"

Para recomecar do zero, apague o arquivo dev.db e rode de novo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DevelopmentConfig

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dev.db")


class ConfigTesteLocal(DevelopmentConfig):
    SECRET_KEY = "dev-teste-local"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH


from app import create_app
from models import db, Funcionarios
from werkzeug.security import generate_password_hash

app = create_app(ConfigTesteLocal)

with app.app_context():
    db.create_all()
    if not Funcionarios.query.filter_by(nome="mali").first():
        db.session.add(Funcionarios(
            nome="mali",
            cargo="dono",
            funcao="esteticista",
            senha=generate_password_hash("123456"),
        ))
        db.session.commit()
        print("Funcionario de teste criado: usuario 'mali', senha '123456'")

print(f"Banco local: {DB_PATH}")
print("Rodando em http://127.0.0.1:5055")
app.run(host="127.0.0.1", port=5055, debug=True)
