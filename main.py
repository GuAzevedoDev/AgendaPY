from app import app
from services import Funcionario, ServicosService, Cliente
from exeptions import AgendaPy

funcionario = Funcionario()
servico = ServicosService()
cliente = Cliente()


def cadastrar_servico():
    nome = input("Nome do servico: ").strip()
    while True:
        duracao_texto = input("Duracao (minutos): ").strip()
        try:
            duracao = int(duracao_texto)
            break
        except ValueError:
            print("Duracao invalida, digite um numero inteiro.")

    servico.cadastrarServicosWeb(nome, duracao)
    print(f"Servico '{nome}' cadastrado!")


def cadastrar_cliente():
    nome = input("Nome do cliente: ").strip()
    numero = input("Numero do cliente: ").strip()

    cliente.cadastrar_cliente_web(nome, numero)
    print(f"Cliente '{nome}' cadastrado!")


def excluir_funcionario():
    nome = input("Nome do funcionario a excluir: ").strip()
    funcionario.excluir_funcionarios(nome)
    print(f"Funcionario '{nome}' excluido!")

def mostrar_servicos() -> list:
    #Conexao segura com db
    servicosEncontrados = servico.mostrar_servicos()
  
    #Se nao exitir retorno lista vazia
    for servico in servicosEncontrados:
        print(servico)

def excluir_servico() -> list:
    #Conexao segura com db
    print("Qual nome do servico?")
    nome_servico = input()
    try:      
        servico.excluir_servico(nome_servico)
    except Exception as e:
        print(e)
    print(f"Servico {nome_servico} excluido")

OPCOES = {
    "1": ("Cadastrar funcionario", funcionario.cadastrarFuncionarios),
    "2": ("Cadastrar servico", cadastrar_servico),
    "3": ("Cadastrar cliente", cadastrar_cliente),
    "4": ("Excluir funcionario", excluir_funcionario),
    "5":("Mostrar servicos", mostrar_servicos),
    "6":("Excluir servico", excluir_servico)
}


def menu():
    print("\n--- AgendaPY: cadastros manuais ---")
    for chave, (rotulo, _) in OPCOES.items():
        print(f"{chave} - {rotulo}")
    print("0 - Sair")
    return input("Escolha uma opcao: ").strip()


if __name__ == "__main__":
    with app.app_context():
        while True:
            opcao = menu()

            if opcao == "0":
                break

            acao = OPCOES.get(opcao)
            if not acao:
                print("Opcao invalida.")
                continue

            try:
                acao[1]()
            except AgendaPy as e:
                print(f"Erro: {e}")
