from exeptions import ServicoError
from repositories import ServicoRepository

repo_servico = ServicoRepository()


#Servicos (ORM OK)

class ServicosService:
  def selecionar_servico_web(self,nomesServicos:list) -> list:
    #Pego todos os servicos
    servicos = self.mostrarServicosWeb()

    #Inicio uma lista vazia
    listaServicos = []

    #Se nao tiver servicos cadastrados
    if not servicos:
      raise ServicoError("Sem servicos cadastrados")

    #Passo por todos se bater com o nome digitado retorno a lista com os servicos selecionados
    for servico in servicos:
      for nome in nomesServicos:
        if servico.nome == nome:
          listaServicos.append(servico.id)

    #Retorno a lista com os servicos selecionados
    return listaServicos

  def mostrarServicosWeb(self) -> list:
    #Conexao segura com db
    servicosEncontrados = repo_servico.mostrar_servicos()

    #Se nao exitir retorno lista vazia
    if not servicosEncontrados:
      return []

    #Se exitir retorno lista com todos
    return servicosEncontrados

  def cadastrarServicosWeb(self,nome:str, duracao:int) -> int:
    #Insiro no bd as informacoes passadas nos parametros
    servico = repo_servico.cadastrar_servico(nome,duracao)
    return servico.id

  def buscarServicoWeb(self,servico:str) -> list:
    servicos_encontrados = repo_servico.busca_pesquisa_servicos(servico)
    #Retorna tudo de servicos em uma lista logo preciso de iterar e fazer uma lista so de id e nome
    nomes_servicos = []

    for servico in servicos_encontrados:
      nomes_servicos.append((servico.id,servico.nome))

    return nomes_servicos

  def excluirServicoWeb(self,nome_servico:str) -> list:
    servico_excluido = repo_servico.excluir_servico(nome_servico)
  
    return servico_excluido

