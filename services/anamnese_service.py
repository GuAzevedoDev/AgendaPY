from exeptions import AnamneseError
from repositories import AnamneseRepository
from .clientes_service import Cliente

repo_anamnese = AnamneseRepository()
cliente_service = Cliente()


# Secoes preenchidas so pela equipe (ver SECOES_PROFISSIONAL em
# views/static/js/data/anamnese_perguntas.js). A ficha e considerada
# "avaliada" quando pelo menos um campo dessas secoes foi preenchido.
SECOES_AVALIACAO_PROFISSIONAL = ["avaliacao_clinica_pele", "plano_tratamento"]


def _avaliacao_concluida(respostas:dict) -> bool:
  for secao_id in SECOES_AVALIACAO_PROFISSIONAL:
    secao_respostas = (respostas or {}).get(secao_id) or {}
    if any(secao_respostas.values()):
      return True
  return False


class Anamnese:
  def enviar_ficha_web(self,nome:str,numero:str,respostas:dict) -> int:
    cliente_id = cliente_service.pesquisar_cliente_web(nome,numero)
    anamnese = repo_anamnese.criar_ou_atualizar(cliente_id,respostas)
    return anamnese.id

  def listar_fichas_web(self) -> list:
    anamneses = repo_anamnese.listar_todas()
    fichas = []
    for anamnese in anamneses:
      fichas.append({
        "id": anamnese.id,
        "cliente_id": anamnese.cliente_id,
        "nome": anamnese.cliente.nome,
        "numero": anamnese.cliente.numero,
        "data": anamnese.data_de_atualizacao.strftime("%d/%m/%Y"),
        "data_iso": anamnese.data_de_atualizacao.strftime("%Y-%m-%d"),
        "avaliacao_concluida": _avaliacao_concluida(anamnese.respostas),
      })
    return fichas

  def obter_ficha_web(self,anamnese_id:int) -> dict:
    anamnese = repo_anamnese.buscar_por_id(anamnese_id)
    if not anamnese:
      raise AnamneseError("Ficha nao encontrada")

    return {
      "id": anamnese.id,
      "cliente_id": anamnese.cliente_id,
      "nome": anamnese.cliente.nome,
      "numero": anamnese.cliente.numero,
      "respostas": anamnese.respostas,
      "data": anamnese.data_de_atualizacao.strftime("%d/%m/%Y"),
      "avaliacao_concluida": _avaliacao_concluida(anamnese.respostas),
    }

  def atualizar_ficha_web(self,anamnese_id:int,respostas:dict) -> None:
    anamnese = repo_anamnese.buscar_por_id(anamnese_id)
    if not anamnese:
      raise AnamneseError("Ficha nao encontrada")

    repo_anamnese.criar_ou_atualizar(anamnese.cliente_id,respostas)
