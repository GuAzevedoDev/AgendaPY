import * as dom from "../ui/dom.js";
import * as clienteApi from "../api/cliente_api.js";
import * as clienteUi from "../ui/cliente_ui.js";

export async function iniciarClientes() {
  await mostrarClientes();
  mostraHistoricoCliente();
  configurarPesquisa();
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
      clienteUi.inserirHistoricoCima(item.dataset.nome, item.dataset.numero);
      clienteUi.limparHistorico();
      let dadosCliente = await clienteApi.pegaDadosCliente(item.dataset.id);
      if (dadosCliente) {
        dadosCliente.forEach((dado) => {
          clienteUi.inserirHistorico(dado, dadosCliente.length);
        });
      }
    });
  });
}

export function configurarPesquisa() {
  if (!dom.inputPesquisaCliente) return;

  const realizarPesquisa = async () => {
    let termo = dom.inputPesquisaCliente.value;
    let clientes = await clienteApi.pesquisarClientes(termo);
    clienteUi.mostrarClientes(clientes, dom.clientesLista);
    mostraHistoricoCliente();
  };

  dom.inputPesquisaCliente.addEventListener("input", realizarPesquisa);

  if (dom.btnPesquisaCliente) {
    dom.btnPesquisaCliente.addEventListener("click", (e) => {
      e.preventDefault();
      realizarPesquisa();
    });
  }
}
