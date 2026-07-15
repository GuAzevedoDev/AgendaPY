from app import app 
from services.services import Funcionario

funcionario = Funcionario()

if __name__ == "__main__":
    with app.app_context():
        funcionario.cadastrarFuncionarios()