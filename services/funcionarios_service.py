import hashlib
from exeptions import FuncionarioError
from repositories import FuncionarioRepository

repo_funcionario = FuncionarioRepository()


#Funcionario(ORM OK)

class Funcionario:
  def loginFuncionarioWeb(self,nome:str,senha:str) -> tuple:
    #Transformar a senha em hash para comparação com db
    senha = senha.encode('utf-8')
    senha = hashlib.sha256(senha)
    senha = senha.hexdigest()

    #Se encontrado ele salva na variavel
    funcionario_encontrado = repo_funcionario.buscar_funcionario(nome.capitalize())
    #Se nao encontrado nao passa no if, verifico se a senha esta correta
    if not funcionario_encontrado or senha != funcionario_encontrado.senha:
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
    senha = input("Digite sua senha: ").encode('utf-8')
    hashSenha = hashlib.sha256(senha)
    senhaHex = hashSenha.hexdigest()

    repo_funcionario.cadastrar_funcionarios(nome,cargo.lower(),funcao,senhaHex)
    print(f"Funcionario {nome} adicionado!")
