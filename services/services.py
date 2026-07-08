from core.database import conectar
import hashlib
from datetime import datetime
from contextlib import contextmanager



#Classes para erros
class AgendaPy(Exception):
  pass

class AgendamentoError(AgendaPy):
  pass

class ClienteError(AgendaPy):
  pass

class FuncionarioError(AgendaPy):
  pass

class ServicoError(AgendaPy):
  pass



#Conexao com banco
@contextmanager
def get_db():
    conexao = conectar()
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()



#Funcionario

class Funcionario:
  def loginFuncionarioWeb(self,nome:str,senha:str) -> tuple:
  #Conectar com banco de forma segura
    with get_db() as db:
      cursor = db.cursor()
      cursor.execute("SELECT id, nome, cargo, funcao, senha FROM funcionarios WHERE nome = ?",
        (nome.capitalize(),))
      
      #Se encontrado ele salva na variavel
      funcionarioEncontrado = cursor.fetchone()

      #Se nao encontrado nao passa no if, verifico se a senha esta correta
      if not funcionarioEncontrado or senha != funcionarioEncontrado[4]:
        raise FuncionarioError("Credenciais invalidas")
      
      #Se nao retorno none
      return funcionarioEncontrado
  
  def mostrarFuncionariosWeb(self) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cargo, funcao FROM funcionarios")
    funcionariosEncontrados = cursor.fetchall()
    return funcionariosEncontrados

  def cadastrarFuncionarios(self):
    with get_db() as db:
      cursor = db.cursor()
      while True:
        nome = input("Digite seu nome: ")

        db.execute("SELECT nome FROM funcionarios WHERE nome = ?", (nome,))
        funcionarioExistente = cursor.fetchone()

        if funcionarioExistente is None:
          break
            
        print(f"Funcionario '{nome}' ja existe, tente outro nome.")

      cargo = input("Digite seu cargo [dono] // [profissional]: ")
      funcao = input("Digite sua funcao: ")
      senha = input("Digite sua senha: ").encode('utf-8')
      hashSenha = hashlib.sha256(senha)
      senhaHex = hashSenha.hexdigest()

      db.execute(
          "INSERT INTO funcionarios (nome, cargo, funcao, senha) VALUES (?, ?, ?, ?)",
          (nome, cargo.lower(),funcao, senhaHex)
        )
      print(f"Funcionario {nome} adicionado!")



#Servicos

class ServicosService:
  def selecionarServicoWeb(self,nomesServicos:list) -> list:
    #Pego todos os servicos
    servicos = self.mostrarServicosWeb()

    #Inicio uma lista vazia
    listaServicos = []

    #Se nao tiver servicos cadastrados
    if not servicos:
      raise("Sem servicos cadastrados")
    
    #Passo por todos se bater com o nome digitado retorno a lista com os servicos selecionados
    for servico in servicos:
      for nome in nomesServicos:
        if servico[1] == nome:
          listaServicos.append(servico[0])

    #Retorno a lista com os servicos selecionados
    return listaServicos
  
  def mostrarServicosWeb(self)-> list:
    #Conexao segura com db
    with get_db() as db:
      cursor = db.cursor()

      #Seleciono todos
      cursor.execute("SELECT id,nome FROM servicos")
      servicosEncontrados = cursor.fetchall()

      #Se nao exitir retorno lista vazia
      if not servicosEncontrados:
        return []
      #Se exitir retorno lista com todos
      return servicosEncontrados
  
  def cadastrarServicosWeb(self,nome:str, duracao:int) -> int:
    #Conexao segura com db
    with get_db() as db:
      cursor = db.cursor()
      #Insiro no bd as informacoes passadas nos parametros
      cursor.execute("INSERT INTO servicos(nome,duracao_min) VALUES(?,?)",(nome,duracao))

      #Retorno id gerado
      return cursor.lastrowid

  def relacionarServico(self,idServico:int,idFuncionarioLogado:int) -> bool:
    #Conexao segura
    with get_db() as db:
      cursor = db.cursor()

      #Insiro se nao existir, se existir nao lanca erro
      cursor.execute("INSERT OR IGNORE INTO servicos_funcionarios(funcionario_id,servico_id)VALUES(?,?)",(idFuncionarioLogado,idServico))

      #Pego se alinha retornar 1
      linhas = db.rowcount
      if linhas == 0:
        return False
      return True

  def buscarServicoWeb(self,servico:str)-> list:
    #Estabeleco conexao segura
    with get_db() as db:
      cursor = db.cursor()

      #Concateno para fazer a pesquisa com like
      servicoTotal = "%" + servico + "%"

      #Pego tudo todos com like
      cursor.execute("SELECT id, nome, duracao_min FROM servicos WHERE nome LIKE ?;",
        (servicoTotal,))
      servicosEncontrados = cursor.fetchall()

      #Retorno a lista
      return servicosEncontrados



#Agendamentos

class AgendamentosService:
  @staticmethod
  def gerarHorarios()-> list:
    #Inicio a lista horarios
    horarios = []

    horaI:int = 7
    horaF:int = 23

    #Inicio no horarioI e finalizo na horaF
    for i in range(horaI,horaF + 1):
      horarios.append(f"{horaI}:00")

      #Quando for igual a horaF nao coloca o :30 na lista
      if horaF != i:
        horarios.append(f"{horaI}:30")
      horaI = horaI + 1

      #Retorno os horarios
    return horarios
  
  def marcarHorarioWeb(self,idFuncionarioLogado:int,nome:str,num:str,hora:str,data:str,nomesServicos:str) -> str:
    #Selecionar data
    data = self.selecionarDataWeb(data)

    #Selecionar horario
    horarioEscolhido = self.selecionarHorarioWeb(idFuncionarioLogado,data,hora)
    
    #Selecione o nome do cliente
    cliente_service = Cliente()
    clienteEscolhido = cliente_service.pesquisarClienteWeb(nome,num)
    
    #Selecione o servico
    servicos_service = ServicosService()
    servicos_ids = servicos_service.selecionarServicoWeb(nomesServicos)
    
    #Passar para o banco
    with get_db() as db:
      cursor = db.cursor()
      cursor.execute("""INSERT INTO agendamentos(cliente_id,funcionario_id,horario,data)VALUES(?,?,?,?)""",(clienteEscolhido,idFuncionarioLogado,horarioEscolhido,data))

      #Pego id do agendamento cadastrado e salvo em uma variavel
      agendamento_id = cursor.lastrowid

      #Itero a lista dos ids dos servicos escolhidos e salvo na tabela com id do mesmo agendamento
      for servico_id in servicos_ids:
        cursor.execute("INSERT INTO agendamentos_servicos (servicos_id,agendamentos_id) VALUES (?,?)", (servico_id,agendamento_id))
    return True

  def selecionarHorarioWeb(self,funcionarioLogado, data, horarioEscolhido) -> str:
    horarios = AgendamentosService.gerarHorarios()
    tudoHorarios = self.mostrarAgendaWeb(funcionarioLogado,data)
    ocupados = []
    for horario in tudoHorarios:
      if horario['status'] == 'Ocupado':
        ocupados.append(horario['hora'])
    
    if horarioEscolhido not in horarios:
      raise AgendamentoError("Esse horario não é válido")
    
    if horarioEscolhido in ocupados:
      raise AgendamentoError("Esse horario já está ocupado")
    
    return horarioEscolhido

  def mostrarAgendaWeb(self,funcionarioLogado, data) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    ocupados = []
    tudoHorarios = []
    horarios = AgendamentosService.gerarHorarios()
    cursor.execute("""
          SELECT horario, clientes.nome, servicos.nome, status,valor_pago,forma_pagamento
          FROM agendamentos
          INNER JOIN agendamentos_servicos ON agendamentos.id = agendamentos_servicos.agendamentos_id
          INNER JOIN servicos ON agendamentos_servicos.servicos_id = servicos.id
          INNER JOIN clientes ON agendamentos.cliente_id = clientes.id
          WHERE funcionario_id = ?
          AND data = ?
    """, (funcionarioLogado, data))

    horariosDia = cursor.fetchall()

    for horario in horarios:
        encontrado = False

        for agendamento in horariosDia:
            hora, cliente, servico, status, valorPago,formaPagamento = agendamento

            if horario == hora:
                tudoHorarios.append({"hora":horario,"status":"Ocupado","cliente":cliente,"servico":servico,"concluido":status,"valorPago":valorPago,"formaPagamento":formaPagamento})
                encontrado = True
                ocupados.append(agendamento)
                break

        if not encontrado:
            tudoHorarios.append({"hora":horario,"status":"Livre"})
    return tudoHorarios
  
  def selecionarDataWeb(self,data:str) -> str:
    #Pego a data atual
    dataAtual:str = datetime.now()

    #Transformo a data do usuario pro formato
    dataUsuario:str = datetime.strptime(data, "%d/%m/%Y")
    
    #Se aconteceu antes retorna None
    if dataUsuario.date() < dataAtual.date():
      raise AgendamentoError("Essa data esta no passado")
    
    #Se tiver tudo certo retorno a data
    return data

  def excluirAgendamentoWeb(self,idFuncionario, data, hora) -> bool:
    # Estabelece conexão com o banco de dados
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Busca o ID do agendamento para poder remover as dependências primeiro (tabela agendamentos_servicos)
    cursor.execute("SELECT id FROM agendamentos WHERE funcionario_id = ? AND data = ? AND horario = ?;", (idFuncionario, data, hora))
    agendamento = cursor.fetchone()
    
    #Caso nao exista agendamento
    if not agendamento:
      raise AgendamentoError("Não existe esse agendamento")
    agendamento_id = agendamento[0]

    # Remove os serviços vinculados a esse agendamento
    cursor.execute("DELETE FROM agendamentos_servicos WHERE agendamentos_id = ?;", (agendamento_id,))

    # Remove o agendamento principal
    cursor.execute("DELETE FROM agendamentos WHERE id = ?;", (agendamento_id,))
    conexao.commit()
    conexao.close()
    return True
    
  def atualizarPagoWeb(self,valor,formaPag,funcionarioId,data,hora) -> bool:
    conexao = conectar()
    cursor = conexao.cursor()
    status = "confirmado"
    formasDePag = ["pix",'debito','dinheiro','credito']
    valorFormatado = float(valor)
    
    if valorFormatado <= 0:
      raise AgendamentoError("Valor inválido")
    
    if not formaPag in formasDePag:
      raise AgendamentoError("Forma de pagamento inválida")
    
    cursor.execute("""UPDATE agendamentos
                  SET valor_pago = ?,forma_pagamento = ?,status = ?
                  WHERE funcionario_id = ? AND data = ? AND horario = ?;""",(valorFormatado,formaPag,status,funcionarioId,data,hora))
    conexao.commit()

    return True



#Clientes

class Cliente:
  def pesquisarClienteWeb(self,nome,num) -> int:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM clientes WHERE nome = ?;",
      (nome,))
    clientesEncontrados = cursor.fetchone()

    if not clientesEncontrados:
      clienteCadastrado = self.cadastrarClienteWeb(nome,num)
      return clienteCadastrado

    if clientesEncontrados:
      return clientesEncontrados[0]
  
  def cadastrarClienteWeb(self,nome,numero) -> int:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute( "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
      (nome, numero))
    conexao.commit()
    cliente_id = cursor.lastrowid
    if not cliente_id:
      raise ClienteError("nao foi possivel cadastrar o cliente")
    return cliente_id

  def buscarNomeWeb(self,nome) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    nomeTotal = "%" + nome + "%" 
    cursor.execute("SELECT id, nome, telefone FROM clientes WHERE nome LIKE ?;",
      (nomeTotal,))
    clientesEncontrados = cursor.fetchall()
    return clientesEncontrados
