
from core.database import conectar
import hashlib
from datetime import datetime

#Funcionario

def cadastrarFuncionarios():
  conexao = conectar()
  cursor = conexao.cursor()

  while True:
    nome = input("Digite seu nome: ")

    cursor.execute("SELECT nome FROM funcionarios WHERE nome = ?", (nome,))
    funcionarioExistente = cursor.fetchone()

    if funcionarioExistente is None:
      break
        
    print(f"Funcionario '{nome}' ja existe, tente outro nome.")

  cargo = input("Digite seu cargo [dono] // [profissional]: ")
  funcao = input("Digite sua funcao: ")
  senha = input("Digite sua senha: ").encode('utf-8')
  hashSenha = hashlib.sha256(senha)
  senhaHex = hashSenha.hexdigest()

  cursor.execute(
      "INSERT INTO funcionarios (nome, cargo, funcao, senha) VALUES (?, ?, ?, ?)",
      (nome, cargo.lower(),funcao, senhaHex)
    )
  conexao.commit()
  print(f"Funcionario {nome} adicionado!")


def mostrarFuncionarios():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, cargo FROM funcionarios")
  funcionariosEncontrados = cursor.fetchall()
  for funcionario in funcionariosEncontrados:
      idF,nomeF,cargoF = funcionario
      print(f"ID:{idF} // NOME:{nomeF} // CARGO:{cargoF}\n")


def loginFuncionario():
  conexao = conectar()
  cursor = conexao.cursor()
  nome = input("Digite seu nome: ")
  cursor.execute("SELECT id, nome, cargo, senha FROM funcionarios WHERE nome = ?",
    (nome,))
  funcionarioEncontrado = cursor.fetchone()
  if funcionarioEncontrado:
    senha = input("Digite sua senha: ")
    print(funcionarioEncontrado)
    if senha == funcionarioEncontrado[3]:
      print("Login feito com sucesso!")
      return funcionarioEncontrado
    else:
      print("Senha incorreta!")
      return None
    
  else:
    print("Usuario nao encontrado")
    return None


#Servicos


def cadastrarServicos():
  conexao = conectar()
  cursor = conexao.cursor()
  nomeS = input("Digite o nome do servico: ")
  duracaoS = int(input("Digite a duracao do servico em minutos: "))
  cursor.execute("INSERT INTO servicos(nome,duracao_min)VALUES(?,?,?)",(nomeS,duracaoS))
  conexao.commit()
  print(f"{nomeS} adicionado(a) com sucesso!")


def relacionarServico(idServico,funcionarioLogin):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("INSERT OR IGNORE INTO servicos_funcionarios(funcionario_id,servico_id)VALUES(?,?)",(funcionarioLogin[0],idServico))
  conexao.commit()
  cursor.rowcount
  linhas = cursor.rowcount
  if linhas == 0:
    print('Ja estava relacionado')
  elif linhas == 1:
    print('Relacionado com sucesso!')


def mostrarServicos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, duracao_min FROM servicos")
    servicosEncontrados = cursor.fetchall()

    if not servicosEncontrados:
        print("Nenhum servico encontrado")
        return []

    for servico in servicosEncontrados:
        idS, nomeS, duracaoS = servico

        print(f"ID:{idS} // NOME:{nomeS} // DURACAO:{duracaoS} // VALOR:{valorS}")

        cursor.execute("""
            SELECT f.nome
            FROM funcionarios f
            JOIN servicos_funcionarios sf
            ON f.id = sf.funcionario_id
            WHERE sf.servico_id = ?
        """, (idS,))

        funcionarios = cursor.fetchall()

        if funcionarios:
            nomes = [f[0] for f in funcionarios]
            print("Profissionais:", ", ".join(nomes))
        else:
            print("Profissionais: Nenhum")

        print()

    return servicosEncontrados



#Agendamentos
def gerarHorarios():
   horarios = [
    "07:00", "07:30",
    "08:00", "08:30",
    "09:00", "09:30",
    "10:00", "10:30",
    "11:00", "11:30",
    "12:00", "12:30",
    "13:00", "13:30",
    "14:00", "14:30",
    "15:00", "15:30",
    "16:00", "16:30",
    "17:00", "17:30",
    "18:00", "18:30",
    "19:00", "19:30",
    "20:00", "20:30",
    "21:00", "21:30",
    "22:00", "22:30",
    "23:00"
]
   return horarios


def selecionarData():
  print("Digite a data que ira fazer o agendamento: [XX/XX/XXXX]")
  entrada = input()
  return entrada


#Funcoes Web

def loginFuncionarioWeb(nome,senha):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, cargo, funcao, senha FROM funcionarios WHERE nome = ?",
    (nome.capitalize(),))
  funcionarioEncontrado = cursor.fetchone()
  if funcionarioEncontrado:
    if senha == funcionarioEncontrado[4]:
      return funcionarioEncontrado
    else:
      return None
    
  else:
    return None


def marcarHorarioWeb(idFuncionarioLogado,nome,num,hora,data,nomesServicos):
  #Selecionar data
  dataEscolhida = selecionarDataWeb(data)
  if not dataEscolhida:
    return "Data invalida"

  #Selecionar horario
  horarioEscolhido = selecionarHorarioWeb(idFuncionarioLogado,dataEscolhida,hora)

  if hora != horarioEscolhido:
    return horarioEscolhido
  
  #Selecione o nome do cliente
  clienteEscolhido = pesquisarClienteWeb(nome,num)

  if not clienteEscolhido:
    return clienteEscolhido
  
  #Selecione o servico
  servicos_ids = selecionarServicoWeb(nomesServicos)
  if not servicos_ids:
    return "Sem servicos cadastrados"
  
  #Passar para o banco
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("""INSERT INTO agendamentos(cliente_id,funcionario_id,horario,data)VALUES(?,?,?,?)""",(clienteEscolhido,idFuncionarioLogado,horarioEscolhido,dataEscolhida))
  conexao.commit()
  
  #Pego id do agendamento cadastrado e salvo em uma variavel
  agendamento_id = cursor.lastrowid

  #Itero a lista dos ids dos servicos escolhidos e salvo na tabela com id do mesmo agendamento
  for servico_id in servicos_ids:
    cursor.execute("INSERT INTO agendamentos_servicos (servicos_id,agendamentos_id) VALUES (?,?)", (servico_id,agendamento_id))

  conexao.commit()
  conexao.close()
  return True


def selecionarHorarioWeb(funcionarioLogado, data, horarioEscolhido):
  horarios = gerarHorarios()
  tudoHorarios = mostrarAgendaWeb(funcionarioLogado,data)
  ocupados = []
  for horario in tudoHorarios:
    if horario['status'] == 'Ocupado':
      ocupados.append(horario['hora'])
  
  if horarioEscolhido not in horarios:
    return "Esse horario não é válido"
  
  if horarioEscolhido in ocupados:
    return "Esse horario já está ocupado"
  
  return horarioEscolhido
  

def mostrarAgendaWeb(funcionarioLogado, data):
    conexao = conectar()
    cursor = conexao.cursor()
    ocupados = []
    tudoHorarios = []
    horarios = gerarHorarios()
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
    livres = [h for h in horarios if h not in ocupados]
    return tudoHorarios


def selecionarDataWeb(data):
  dataAtual = datetime.now()
  dataUsuario = datetime.strptime(data, "%d/%m/%Y")
  if dataUsuario.date() < dataAtual.date():
    return
  return data


def pesquisarClienteWeb(nome,num):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id FROM clientes WHERE nome = ?;",
    (nome,))
  clientesEncontrados = cursor.fetchone()

  if not clientesEncontrados:
    clienteCadastrado = cadastrarClienteWeb(nome,num)
    return clienteCadastrado

  if clientesEncontrados:
    return clientesEncontrados[0]
  




def selecionarServicoWeb(nomesServicos):
  servicos = mostrarServicosWeb()
  listaServicos = []
  if not servicos:
    return 

  for servico in servicos:
    for nome in nomesServicos:
      if servico[1] == nome:
        listaServicos.append(servico[0])
  
  return listaServicos


def mostrarServicosWeb():
  conexao = conectar()
  cursor = conexao.cursor()

  cursor.execute("SELECT id,nome FROM servicos")
  servicosEncontrados = cursor.fetchall()

  if not servicosEncontrados:
    return "Sem servicos cadastrados"

  return servicosEncontrados


def cadastrarClienteWeb(nome,numero):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute( "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
    (nome, numero))
  conexao.commit()
  cliente_id = cursor.lastrowid
  return cliente_id

def mostrarFuncionariosWeb():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, cargo, funcao FROM funcionarios")
  funcionariosEncontrados = cursor.fetchall()
  return funcionariosEncontrados


def buscarNomeWeb(nome):
  conexao = conectar()
  cursor = conexao.cursor()
  nomeTotal = "%" + nome + "%" 
  cursor.execute("SELECT id, nome, telefone FROM clientes WHERE nome LIKE ?;",
    (nomeTotal,))
  clientesEncontrados = cursor.fetchall()
  return clientesEncontrados


def buscarServicoWeb(servico):
  conexao = conectar()
  cursor = conexao.cursor()
  servicoTotal = "%" + servico + "%" 
  cursor.execute("SELECT id, nome, duracao_min FROM servicos WHERE nome LIKE ?;",
    (servicoTotal,))
  servicosEncontrados = cursor.fetchall()
  return servicosEncontrados

def atualizarPagoWeb(valor,formaPag,funcionarioId,data,hora):
  conexao = conectar()
  cursor = conexao.cursor()
  status = "confirmado"
  formasDePag = ["pix",'debito','dinheiro','credito']
  valorFormatado = float(valor)
  
  if valorFormatado <= 0:
    return "Valor inválido"
  
  if not formaPag in formasDePag:
    return "Forma de pagamento inválida"
  
  cursor.execute("""UPDATE agendamentos
                 SET valor_pago = ?,forma_pagamento = ?,status = ?
                 WHERE funcionario_id = ? AND data = ? AND horario = ?;""",(valorFormatado,formaPag,status,funcionarioId,data,hora))
  conexao.commit()

  return True

def excluirHorarioWeb(idFuncionario, data, hora):
  # Estabelece conexão com o banco de dados
  conexao = conectar()
  cursor = conexao.cursor()
  
  # Busca o ID do agendamento para poder remover as dependências primeiro (tabela agendamentos_servicos)
  cursor.execute("SELECT id FROM agendamentos WHERE funcionario_id = ? AND data = ? AND horario = ?;", (idFuncionario, data, hora))
  agendamento = cursor.fetchone()
  
  if agendamento:
    agendamento_id = agendamento[0]
    # Remove os serviços vinculados a esse agendamento
    cursor.execute("DELETE FROM agendamentos_servicos WHERE agendamentos_id = ?;", (agendamento_id,))
    # Remove o agendamento principal
    cursor.execute("DELETE FROM agendamentos WHERE id = ?;", (agendamento_id,))
    conexao.commit()
    conexao.close()
    return True
  
  conexao.close()
  return False
