from models import db,Clientes

class ClienteRepository:
  def buscar_cliente(self,nome:str) -> tuple:
    cliente = Clientes.query.filter_by(nome = nome).first()
    return cliente

  def cadastrar_cliente(self,nome:str,numero:str) -> tuple:
    cliente = Clientes(nome = nome,numero = numero)
    db.session.add(cliente)
    db.session.commit()
    return cliente

  def busca_pesquisa_cliente(self,nome:str) -> list:
    #ilike faz a pesquisa sem comparar maiusculas e minusculas, mas existe tambem o like(ele compara)
    clientes = Clientes.query.filter(Clientes.nome.ilike(f"%{nome}%")).all()

    return clientes

  def trazer_todos_clientes(self) -> list:
    clientes = Clientes.query.all()
    return clientes
  
  def buscar_cliente_id(self,id) -> tuple:
    cliente = Clientes.query.filter_by(id = id).first()
    
    return cliente