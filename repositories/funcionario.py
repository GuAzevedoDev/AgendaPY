from models import db,Funcionarios
from exeptions import FuncionarioError

class FuncionarioRepository:
  def buscar_funcionario(self,nome:str) -> tuple:
    funcionario_encontrado = Funcionarios.query.filter_by(nome == nome).first()
    return funcionario_encontrado

  def mostrar_funcionarios(self) -> list:
    funcionarios = Funcionarios.query.all()
    return funcionarios
  
  def cadastrar_funcionarios(self,nome:str,cargo:str,funcao:str,senha:str):
    funcionario = Funcionarios(nome,cargo,funcao,senha)
    db.session.add(funcionario)
    db.session.commit()
    return funcionario
