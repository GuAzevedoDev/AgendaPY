from app import app 
from services.services import Funcionario,ServicosService,AgendamentosService,Cliente
from repositories import AgendamentoRepository
from datetime import datetime

funcionario = Funcionario()
servico = ServicosService()
agendamento = AgendamentosService()
cliente = Cliente()

repo_agendamento = AgendamentoRepository()

data = datetime.strptime("21/07/2026", "%d/%m/%Y").date()
hora = datetime.strptime("10:30","%H:%M").time()

if __name__ == "__main__":
    with app.app_context():
        # funcionario = funcionario.cadastrarFuncionarios()
        agendamento = agendamento.mostrarAgendaWeb(1,data)
        servico = servico.cadastrarServicosWeb("Escova",180)
        cliente = cliente.cadastrar_cliente_web("Dona Geralda","31980257381")
        agendamento = repo_agendamento.cadastrar_horario(1,1,hora,data)
        agendamento_servico = repo_agendamento.cadastrar_servico_agendamento(1,1)

