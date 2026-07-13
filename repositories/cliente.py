from models import db,Clientes
from exeptions import ClienteError

class ClienteRepository:
  def buscar_cliente(self,nome):
    cliente = Clientes.query.filter_by(nome == nome).first()
    return cliente

  def cadastrar_cliente(self,nome,numero):
    cliente = Clientes(nome,numero)

    db.session.add(cliente)
    db.commit()
    return cliente

  def busca_pesquisa_cliente(self,nome):
    #ilike faz a pesquisa sem comparar maiusculas e minusculas, mas existe tambem o like(ele compara)
    clientes = Clientes.query().ilike(f"%{nome}%").all()

    return clientes
