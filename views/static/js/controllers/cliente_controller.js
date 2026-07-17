import * as dom from "../ui/dom.js";
import * as clienteApi from "../api/cliente_api.js";
import * as clienteUi from "../ui/cliente_ui.js";

export function iniciarClientes() {
  if (!dom.inputNome) return;

  dom.inputNome.addEventListener("input", async function pegaNome() {
    try {
      const clientes = await clienteApi.pegaNomes(dom.inputNome.value);
      clienteUi.coloca_nome_lista(clientes, dom.listaNomes);
      
      const nomesLista = document.querySelectorAll(".nome-lista");
      clienteUi.ativa_cliente_selecionado(nomesLista);
    } catch (err) {
      console.error("Erro ao obter lista de clientes:", err);
    }
  });
}
