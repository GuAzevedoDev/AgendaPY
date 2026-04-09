
from core.database import conectar


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
    return clientesEncontrados
  
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
  senha = input("Digite sua senha: ")

  cursor.execute(
      "INSERT INTO funcionarios (nome, cargo, senha) VALUES (?, ?, ?)",
      (nome, cargo.lower(), senha)
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


#Mostrar os profissionais que fazem o servico
def mostrarServicos():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, duracao_min, valor FROM servicos")
  servicosEncontrados = cursor.fetchall()
  if not servicosEncontrados:
    print("Nenhum servico encontrado")
    return
  for servico in servicosEncontrados:
      idS,nomeS,duracaoS,valorS = servico
      print(f"ID:{idS} // NOME:{nomeS} // DURACAO:{duracaoS} // VALOR:{valorS}\n")

    

# def marcarHorario():
#   conexao = conectar()
#   cursor = conexao.cursor()
#   nome = input("Digite o nome do cliente que deseja marcar o horario:")
#   clienteEncontrado = pesquisarCliente(nome)
#   idEncontrado = clienteEncontrado[0]
#   nomeEncontrado = clienteEncontrado[1]
#   numeroEncontrado = clienteEncontrado[2]
#   cursor.execute("""INSERT INTO agendamentos(cliente_id,funcionario_id,servico_id,horario_id,data)""")

  