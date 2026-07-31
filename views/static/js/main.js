import { abreModal, fechaModal } from "./ui/modal_ui.js";
import * as calendarioController from "./controllers/calendario_controller.js";
import * as agendaController from "./controllers/agenda_controller.js";
import * as clienteController from "./controllers/cliente_controller.js";
import * as servicoController from "./controllers/servico_controller.js";
import * as funcionarioController from "./controllers/funcionario_controller.js";
import * as anamneseController from "./controllers/anamnese_controller.js";
import * as financeiroController from "./controllers/financeiro_controller.js";
import * as mobileMenu from "./mobile/mobile_menu.js";
import * as mobileAgenda from "./mobile/mobile_agenda.js";
import * as mobileClientes from "./mobile/mobile_clientes.js";

window.abreModal = abreModal;
window.fechaModal = fechaModal;

mobileMenu.iniciarMenuMobile();

if (document.querySelector(".pagina-agenda")) {
  servicoController.iniciarServicos();
  funcionarioController.iniciarFuncionarios();
  calendarioController.iniciarCalendario();
  agendaController.iniciarAgenda();
  mobileAgenda.iniciarAgendaMobile();
}

if (document.querySelector(".pagina-clientes")) {
  clienteController.iniciarClientes();
  mobileClientes.iniciarClientesMobile();
}

if (document.querySelector(".pagina-anamnese")) {
  anamneseController.iniciarAnamnese();
}

if (document.querySelector(".pagina-financeiro")) {
  financeiroController.iniciarFinanceiro();
}
