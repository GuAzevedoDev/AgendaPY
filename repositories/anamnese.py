from models import db,Anamnese

class AnamneseRepository:
  def buscar_por_cliente(self,cliente_id:int) -> tuple:
    anamnese = Anamnese.query.filter_by(cliente_id = cliente_id).first()
    return anamnese

  def buscar_por_id(self,anamnese_id:int) -> tuple:
    anamnese = Anamnese.query.filter_by(id = anamnese_id).first()
    return anamnese

  def criar_ou_atualizar(self,cliente_id:int,respostas:dict) -> tuple:
    anamnese = self.buscar_por_cliente(cliente_id)

    if anamnese:
      anamnese.respostas = respostas
    else:
      anamnese = Anamnese(cliente_id = cliente_id,respostas = respostas)
      db.session.add(anamnese)

    db.session.commit()
    return anamnese

  def listar_todas(self) -> list:
    anamneses = Anamnese.query.join(Anamnese.cliente).order_by(Anamnese.data_de_atualizacao.desc()).all()
    return anamneses

  def excluir(self,anamnese:Anamnese) -> None:
    db.session.delete(anamnese)
    db.session.commit()
