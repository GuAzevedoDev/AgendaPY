
from core.database import conectar
import hashlib

#Clientes

def pesquisarCliente(nome):
  conexao = conectar()
  cursor = conexao.cursor()
  nomeTotal = "%" + nome + "%" 
  cursor.execute("SELECT id, nome, telefone FROM clientes WHERE nome LIKE ?;",
    (nomeTotal,))
  clientesEncontrados = cursor.fetchall()
  if len(clientesEncontrados) == 0:
    print("Nenhum cliente encontrado\n")
    entrada = input("Deseja cadastrar ? (s/n)\n")
    if entrada.lower() == "s":
      numero = input("Digite o numero do cliente:")
      cadastrarCliente(nome,numero)
    else:
       print("Voltando para o menu")

  if len(clientesEncontrados) == 1:
    return clientesEncontrados[0]
  
  elif len(clientesEncontrados) > 1:
    print("Foram encontrados esses clientes:\n")

    for cliente in clientesEncontrados:
      idCliente,nomeCliente,numero = cliente
      print(f"ID:{idCliente} // NOME:{nomeCliente} // NUMERO:{numero}\n")
    idProucurado = int(input("Digite o id do cliente desejado:"))
    
    for cliente in clientesEncontrados:
      if cliente[0] == idProucurado:
        return cliente
      
    print("Nenhum cliente encontrado\n")
    entrada = input("Deseja cadastrar ? (s/n)\n")
    if entrada.lower() == "s":
      numero = input("Digite o numero do cliente:")
      cadastrarCliente(nome,numero)
      return pesquisarCliente(nome)
    else:
      print("Voltando para o menu...")
      return None


def cadastrarCliente(nome,numero):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute( "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
    (nome, numero))
  conexao.commit()
  print(f"Cliente {nome} adicionado!")


def mostrarClientes():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, telefone FROM clientes")
  clientesEncontrados = cursor.fetchall()
  for cliente in clientesEncontrados:
      idCliente,nomeCliente,numero = cliente
      print(f"ID:{idCliente} // NOME:{nomeCliente} // NUMERO:{numero}\n")


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
  valorS = float(input("Digite o valor do servico: "))
  cursor.execute("INSERT INTO servicos(nome,duracao_min,valor)VALUES(?,?,?)",(nomeS,duracaoS,valorS))
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

    cursor.execute("SELECT id, nome, duracao_min, valor FROM servicos")
    servicosEncontrados = cursor.fetchall()

    if not servicosEncontrados:
        print("Nenhum servico encontrado")
        return []

    for servico in servicosEncontrados:
        idS, nomeS, duracaoS, valorS = servico

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


def selecionarServico():
  servicos = mostrarServicos()
  if not servicos:
    return None
  entrada = input("Digite o id do servico: ")
  try: 
    entrada = int(entrada)
  except:
     print("Entrada invalida")

  for servico in servicos:
    if servico[0] == entrada:
      return servico
    
  print("Servico nao encontrado")

  entrada2 = input("Deseja cadastrar ? (s/n)")
  if entrada2.lower() == "s":
    return cadastrarServicos()
  else:
    return None
  

#Agendamentos
def gerarHorarios():
   horarios = [
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


def mostrarAgenda(funcionario_id, data):
    conexao = conectar()
    cursor = conexao.cursor()
    ocupados = []
    horarios = gerarHorarios()
    cursor.execute("""
        SELECT horario, cliente_id, servico_id
        FROM agendamentos
        WHERE funcionario_id = ?
        AND data = ?
    """, (funcionario_id, data))

    horariosDia = cursor.fetchall()

    for horario in horarios:
        encontrado = False

        for agendamento in horariosDia:
            hora, cliente, servico = agendamento

            if horario == hora:
                print(f"{horario} ocupado (cliente {cliente}, servico {servico})")
                encontrado = True
                ocupados.append(hora)
                break

        if not encontrado:
            print(f"{horario} livre")
    return ocupados


def selecionarHorario(funcionario_id, data):
  horarios = gerarHorarios()
  ocupados = mostrarAgenda(funcionario_id,data)
  
  horarioEscolhido = input("Digite o horario de deseja marcar: ")
  if horarioEscolhido not in horarios:
     print("Esse horario nao e valido")
     return None
  if horarioEscolhido in ocupados:
    print("Esse horario ja esta ocupado")
    return None
  else:
     return horarioEscolhido
  

def marcarHorario(idfuncionarioLogado):

  #Selecionar data
  dataEscolhida = selecionarData()

  #Selecionar horario
  horarioEscolhido = selecionarHorario(idfuncionarioLogado,dataEscolhida)

  if not horarioEscolhido:
    return
  
  #Selecione o nome do cliente
  nome = input("Digite o nome do cliente: ")
  clienteEscolhido = pesquisarCliente(nome)

  if not clienteEscolhido:
    return
  
  #Selecione o servico
  servicoEscolhido = selecionarServico()
  if not servicoEscolhido:
    return

  #Passar para o banco
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("""INSERT INTO agendamentos(cliente_id,funcionario_id,servico_id,horario,data)VALUES(?,?,?,?,?)""",(clienteEscolhido[0],idfuncionarioLogado,servicoEscolhido[0],horarioEscolhido,dataEscolhida))
  conexao.commit()

  print("Agendamento realizado com sucesso!")


#Funcoes Web

def loginFuncionarioWeb(nome,senha):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, cargo, funcao, senha FROM funcionarios WHERE nome = ?",
    (nome.capitalize(),))
  funcionarioEncontrado = cursor.fetchone()
  if funcionarioEncontrado:
    if senha == funcionarioEncontrado[4]:
      # print("Login feito com sucesso!")
      return funcionarioEncontrado
    else:
      return None
    
  else:
    return None


def marcarHorarioWeb(funcionarioLogado,nome,hora,data):
  #Selecionar data
  dataEscolhida = selecionarData(data)

  #Selecionar horario
  horarioEscolhido = selecionarHorarioWeb(funcionarioLogado,dataEscolhida,hora)

  if not horarioEscolhido:
    return
  
  #Selecione o nome do cliente
  clienteEscolhido = pesquisarClienteWeb(nome)

  if not clienteEscolhido:
    return
  
  #Selecione o servico
  servicoEscolhido = selecionarServico()
  if not servicoEscolhido:
    return

  #Passar para o banco
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("""INSERT INTO agendamentos(cliente_id,funcionario_id,servico_id,horario,data)VALUES(?,?,?,?,?)""",(clienteEscolhido[0],funcionarioLogado[0],servicoEscolhido[0],horarioEscolhido,dataEscolhida))
  conexao.commit()

  #print("Agendamento realizado com sucesso!")


def selecionarHorarioWeb(funcionarioLogado, data, horarioEscolhido):
  horarios = gerarHorarios()
  ocupados = mostrarAgendaWeb(funcionarioLogado[0],data)
  if horarioEscolhido not in horarios:
     print("Esse horario nao e valido")
     return None
  if horarioEscolhido in ocupados:
    print("Esse horario ja esta ocupado")
    return None
  else:
     return horarioEscolhido
  

def mostrarAgendaWeb(funcionarioLogado, data):
    conexao = conectar()
    cursor = conexao.cursor()
    ocupados = []
    tudoHorarios = []
    horarios = gerarHorarios()
    # cursor.execute("""
    #     SELECT horario, cliente_id, servico_id
    #     FROM agendamentos
    #     WHERE funcionario_id = ?
    #     AND data = ?
    # """, (funcionarioLogado, data))
    cursor.execute("""
          SELECT horario, clientes.nome, servicos.nome
          FROM agendamentos
          INNER JOIN clientes ON agendamentos.cliente_id = clientes.id
          INNER JOIN servicos ON agendamentos.servico_id = servicos.id
          WHERE funcionario_id = ?
          AND data = ?
    """, (funcionarioLogado, data))

    horariosDia = cursor.fetchall()

    for horario in horarios:
        encontrado = False

        for agendamento in horariosDia:
            hora, cliente, servico = agendamento

            if horario == hora:
                print(f"{horario} ocupado (cliente {cliente}, servico {servico})")
                tudoHorarios.append({"hora":horario,"status":"Ocupado","cliente":cliente,"servico":servico})
                encontrado = True
                ocupados.append(agendamento)
                break

        if not encontrado:
            tudoHorarios.append({"hora":horario,"status":"Livre"})
    livres = [h for h in horarios if h not in ocupados]
    return tudoHorarios


def selecionarDataWeb(data):
  #print("Digite a data que ira fazer o agendamento: [XX/XX/XXXX]")
  return data


def pesquisarClienteWeb(nome,idProucurado):
  conexao = conectar()
  cursor = conexao.cursor()
  nomeTotal = "%" + nome + "%" 
  cursor.execute("SELECT id, nome, telefone FROM clientes WHERE nome LIKE ?;",
    (nomeTotal,))
  clientesEncontrados = cursor.fetchall()
  if len(clientesEncontrados) == 0:
    #print("Nenhum cliente encontrado\n")
    entrada = input("Deseja cadastrar ? (s/n)\n")
    if entrada.lower() == "s":
      numero = input("Digite o numero do cliente:")
      cadastrarCliente(nome,numero)
    else:
       #print("Voltando para o menu")
       completar

  if len(clientesEncontrados) == 1:
    return clientesEncontrados[0]
  
  elif len(clientesEncontrados) > 1:
    #print("Foram encontrados esses clientes:\n")

    for cliente in clientesEncontrados:
      idCliente,nomeCliente,numero = cliente
      #print(f"ID:{idCliente} // NOME:{nomeCliente} // NUMERO:{numero}\n")
    
    
    for cliente in clientesEncontrados:
      if cliente[0] == idProucurado:
        return cliente
      
    # print("Nenhum cliente encontrado\n")
    # entrada = input("Deseja cadastrar ? (s/n)\n")
    # if entrada.lower() == "s":
    #   numero = input("Digite o numero do cliente:")
    #   cadastrarCliente(nome,numero)
    #   return pesquisarCliente(nome)
    # else:
    #   print("Voltando para o menu...")
    #   return None


def selecionarServicoWeb(entrada):
  servicos = mostrarServicos()
  if not servicos:
    return None
  #entrada = input("Digite o id do servico: ")
  try: 
    entrada = int(entrada)
  except:
     print("Entrada invalida")

  for servico in servicos:
    if servico[0] == entrada:
      return servico
    
  print("Servico nao encontrado")

  # entrada2 = input("Deseja cadastrar ? (s/n)")
  # if entrada2.lower() == "s":
  #   return cadastrarServicos()
  # else:
  #   return None
  

def mostrarServicosWeb():
  conexao = conectar()
  cursor = conexao.cursor()

  cursor.execute("SELECT id, nome, duracao_min, valor FROM servicos")
  servicosEncontrados = cursor.fetchall()

  if not servicosEncontrados:
    #print("Nenhum servico encontrado")
    return []

  for servico in servicosEncontrados:
      idS, nomeS, duracaoS, valorS = servico

      #print(f"ID:{idS} // NOME:{nomeS} // DURACAO:{duracaoS} // VALOR:{valorS}")

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
          #print("Profissionais:", ", ".join(nomes))
      else:
          #print("Profissionais: Nenhum")
          todos
      #print()

  return servicosEncontrados


def cadastrarClienteWeb(nome,numero):
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute( "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
    (nome, numero))
  conexao.commit()

def mostrarFuncionariosWeb():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, cargo, funcao FROM funcionarios")
  funcionariosEncontrados = cursor.fetchall()
  return funcionariosEncontrados