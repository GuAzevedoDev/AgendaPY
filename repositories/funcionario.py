from models import db,Funcionarios

class FuncionarioRepository:
  def buscar_funcionario(self,nome:str) -> tuple:
    #ilike sem wildcard faz comparacao exata ignorando maiusculas/minusculas
    funcionario_encontrado = Funcionarios.query.filter(Funcionarios.nome.ilike(nome)).first()
    return funcionario_encontrado

  def mostrar_funcionarios(self) -> list:
    funcionarios = Funcionarios.query.all()
    return funcionarios
  
  def cadastrar_funcionarios(self,nome:str,cargo:str,funcao:str,senha:str):
    funcionario = Funcionarios(nome = nome,cargo = cargo,funcao = funcao,senha = senha)
    db.session.add(funcionario)
    db.session.commit()
    return funcionario

  def excluir_funcionairos(self,funcionario:Funcionarios):
    db.session.delete(funcionario)
    db.session.commit()