from models import db,Clientes
from exeptions import ClienteError

class ClienteRepository:
  def buscar_cliente(self,nome:str) -> tuple:
    cliente = Clientes.query.filter_by(nome == nome).first()
    return cliente

  def cadastrar_cliente(self,nome:str,numero:str) -> tuple:
    cliente = Clientes(nome,numero)
    db.session.add(cliente)
    db.session.commit()
    return cliente

  def busca_pesquisa_cliente(self,nome:str) -> list:
    #ilike faz a pesquisa sem comparar maiusculas e minusculas, mas existe tambem o like(ele compara)
    clientes = Clientes.query.ilike(f"%{nome}%").all()

    return clientes
