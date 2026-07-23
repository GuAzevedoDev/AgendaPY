from exeptions import FuncionarioError
from repositories import FuncionarioRepository
from werkzeug.security import generate_password_hash, check_password_hash

repo_funcionario = FuncionarioRepository()


#Funcionario(ORM OK)

class Funcionario:
  def loginFuncionarioWeb(self,nome:str,senha:str) -> tuple:
    #Se encontrado ele salva na variavel
    funcionario_encontrado = repo_funcionario.buscar_funcionario(nome)

    #Se nao encontrado nao passa no if, verifico se a senha esta correta
    if not funcionario_encontrado or not check_password_hash(funcionario_encontrado.senha,senha):
      raise FuncionarioError("Credenciais invalidas")

    #Se tudo ok retorno funcionario_encontrado
    return funcionario_encontrado

  def mostrarFuncionariosWeb(self) -> list:
    funcionariosEncontrados = repo_funcionario.mostrar_funcionarios()
    return funcionariosEncontrados

  def cadastrarFuncionarios(self):
    while True:
      nome = input("Digite seu nome: ")
      funcionarioExistente = repo_funcionario.buscar_funcionario(nome)

      if funcionarioExistente is None:
        break

      print(f"Funcionario '{nome}' ja existe, tente outro nome.")

    cargo = input("Digite seu cargo [dono] // [profissional]: ")
    funcao = input("Digite sua funcao: ")
    senha = input("Digite sua senha: ")
    senhaHex = generate_password_hash(senha)

    repo_funcionario.cadastrar_funcionarios(nome,cargo.lower(),funcao,senhaHex)
    print(f"Funcionario {nome} adicionado!")

  def excluir_funcionarios(self,nome:str):
    funcionario_encontrado = repo_funcionario.buscar_funcionario(nome)

    if not funcionario_encontrado:
      raise FuncionarioError("Funcionario nao encontrado")

    repo_funcionario.excluir_funcionairos(funcionario_encontrado)