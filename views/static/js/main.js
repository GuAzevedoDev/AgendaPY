import { abreModal, fechaModal } from "./ui/modal_ui.js";
import * as calendarioController from "./controllers/calendario_controller.js";
import * as agendaController from "./controllers/agenda_controller.js";
import * as clienteController from "./controllers/cliente_controller.js";
import * as servicoController from "./controllers/servico_controller.js";
import * as funcionarioController from "./controllers/funcionario_controller.js";

window.abreModal = abreModal;
window.fechaModal = fechaModal;

if (document.querySelector(".pagina-agenda")) {
  servicoController.iniciarServicos();
  funcionarioController.iniciarFuncionarios();
  calendarioController.iniciarCalendario();
  agendaController.iniciarAgenda();
}

if (document.querySelector(".pagina-clientes")) {
  clienteController.iniciarClientes();
}
