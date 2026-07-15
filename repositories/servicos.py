from models import db,Servicos
from exeptions import ServicoError

class ServicoRepository:
  def mostrar_servicos(self) -> list:
    servicos = Servicos.query.all()
    return servicos
  
  def cadastrar_servico(nome:str,duracao:int) -> tuple:
    servico = Servicos(nome = nome,duracao = duracao)
    db.session.add(servico)
    db.session.commit()
    return servico
  
  def busca_pesquisa_cliente(servico:str) -> list:
    servicos = Servicos.query.ilike(f"%{servico}%").all()
    return servicos