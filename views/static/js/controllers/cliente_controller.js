import * as dom from "../ui/dom.js";
import * as clienteApi from "../api/cliente_api.js";
import * as clienteUi from "../ui/cliente_ui.js";

export async function iniciarClientes() {
  await mostrarClientes();
  mostraHistoricoCliente();
}

export async function mostrarClientes() {
  let clientes = await clienteApi.mostrarClientes();
  clienteUi.mostrarClientes(clientes, dom.clientesLista);
}

export async function mostraHistoricoCliente() {
  let clientesItens = document.querySelectorAll(".cliente-item");
  clientesItens.forEach((item) => {
    item.addEventListener("click", async () => {
      clienteUi.marcaClicado(item, clientesItens);
      let dadosCliente = await clienteApi.pegaDadosCliente(item.dataset.id)
      console.log(dadosCliente)
    });
  });
}
