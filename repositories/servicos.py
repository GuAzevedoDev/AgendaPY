from models import db,Servicos

class ServicoRepository:
  def mostrar_servicos(self) -> list:
    servicos = Servicos.query.all()
    return servicos
  
  def cadastrar_servico(self,nome:str,duracao:int) -> tuple:
    servico = Servicos(nome = nome,duracao_min = duracao)
    db.session.add(servico)
    db.session.commit()
    return servico
  
  def busca_pesquisa_servicos(self,servico:str) -> list:
    servicos = Servicos.query.filter(Servicos.nome.ilike(f"%{servico}%")).all()
    return servicos

  def excluir_servico(self,nome):
    servico = Servicos.query.filter_by(nome = nome).first()
    if not servico:
      raise Exception("Nao existe esse servico")

    db.session.delete(servico)
    db.session.commit()
    return servico