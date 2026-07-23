import * as funcionarioUi from "../ui/funcionario_ui.js";
import * as clienteUi from "../ui/cliente_ui.js";
import * as clienteApi from "../api/cliente_api.js";
import * as dom from "../ui/dom.js";
import { carregarMarcadoresAgendamento } from "./calendario_controller.js";

export function iniciarFuncionarios() {
  const funcionarios = document.querySelectorAll(".funcionario");

  funcionarios.forEach((funcionario) => {
    if (funcionario.dataset.id == window.id_funcionario) {
      funcionarioUi.marcar_funcionario_ativo(funcionario);
    }

    funcionario.addEventListener("click", () => {
      funcionarioUi.desmarcar_funcionarios(funcionarios);

      window.id_funcionario = funcionario.dataset.id;

      funcionarioUi.marcar_funcionario_ativo(funcionario);

      const diaAtivo = document.querySelector(".dias-calendario .ativo");
      if (diaAtivo) {
        diaAtivo.click();
      }

      carregarMarcadoresAgendamento();
    });
  });
  if (!dom.inputNome) return;
  dom.inputNome.addEventListener("input", async function pegaNome() {
    try {
      const clientes = await clienteApi.pegaNomes(dom.inputNome.value);
      clienteUi.coloca_nome_lista(clientes, dom.listaNomes);

      const nomesLista = document.querySelectorAll(".nome-lista");
      clienteUi.ativa_cliente_selecionado();
    } catch (err) {
      console.error("Erro ao obter lista de clientes:", err);
    }
  });
}
