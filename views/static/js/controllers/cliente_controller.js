import * as dom from "../ui/dom.js";
import * as clienteApi from "../api/cliente_api.js";
import * as clienteUi from "../ui/cliente_ui.js";
import { fechaModal } from "../ui/modal_ui.js";

const ehMobile = () => window.matchMedia("(max-width: 900px)").matches;

let clienteSelecionadoId = null;

export async function iniciarClientes() {
  await mostrarClientes();
  mostraHistoricoCliente();
  configurarPesquisa();
  configurarNovoCliente();
  configurarExcluirCliente();
  selecionarClienteDesktop();
}

export async function mostrarClientes() {
  let clientes = await clienteApi.mostrarClientes();
  clienteUi.mostrarClientes(clientes, dom.clientesLista);
}

export async function mostraHistoricoCliente() {
  let clientesItens = document.querySelectorAll(".cliente-item");
  clientesItens.forEach((item) => {
    item.addEventListener("click", async () => {
      clienteSelecionadoId = item.dataset.id;
      clienteUi.marcaClicado(item, clientesItens);
      clienteUi.inserirHistoricoCima(item.dataset.nome, item.dataset.numero);
      clienteUi.limparHistorico();
      let dadosCliente = await clienteApi.pegaDadosCliente(item.dataset.id);
      dadosCliente = dadosCliente || [];
      clienteUi.atualizarMetricas(
        dadosCliente.length,
        dadosCliente[0]?.agendamento_data,
      );
      dadosCliente.forEach((dado) => {
        clienteUi.inserirHistorico(dado);
      });
    });
  });
}

// Mantem sempre um cliente selecionado no desktop; no mobile a lista fica livre
function selecionarClienteDesktop(itemAlvo) {
  if (ehMobile()) return;

  const alvo = itemAlvo || dom.clientesLista.querySelector(".cliente-item");
  if (alvo) {
    alvo.click();
  } else {
    clienteSelecionadoId = null;
    clienteUi.limparDetalhesCliente();
  }
}

export function configurarExcluirCliente() {
  const botaoExcluir = document.querySelector(".btn-excluir-cliente");
  if (!botaoExcluir) return;

  botaoExcluir.addEventListener("click", async () => {
    if (!clienteSelecionadoId) return;

    const nome = dom.nomeCliente.textContent;
    if (!confirm(`Deseja realmente excluir o cliente ${nome}?`)) return;

    try {
      const dados = await clienteApi.excluirCliente(clienteSelecionadoId);
      if (dados.sucesso === true) {
        clienteSelecionadoId = null;
        await mostrarClientes();
        mostraHistoricoCliente();
        selecionarClienteDesktop();
      } else {
        alert(dados.mensagem || "Nao foi possivel excluir o cliente");
      }
    } catch (err) {
      console.error("Erro ao excluir cliente:", err);
    }
  });
}

export function configurarPesquisa() {
  if (!dom.inputPesquisaCliente) return;

  const realizarPesquisa = async () => {
    let termo = dom.inputPesquisaCliente.value;
    let clientes = await clienteApi.pesquisarClientes(termo);
    clienteUi.mostrarClientes(clientes, dom.clientesLista);
    mostraHistoricoCliente();
    selecionarClienteDesktop();
  };

  dom.inputPesquisaCliente.addEventListener("input", realizarPesquisa);

  if (dom.btnPesquisaCliente) {
    dom.btnPesquisaCliente.addEventListener("click", (e) => {
      e.preventDefault();
      realizarPesquisa();
    });
  }
}

export function configurarNovoCliente() {
  const botaoCadastrar = document.querySelector("#btnCadastrarCliente");
  const form = document.querySelector("#formNovoCliente");
  const inputNome = document.querySelector(".nomeNovoCliente");
  const inputNumero = document.querySelector(".numeroNovoCliente");

  if (!botaoCadastrar || !form || !inputNome || !inputNumero) return;

  botaoCadastrar.addEventListener("click", async (event) => {
    event.preventDefault();

    const avisoModal = document.querySelector(".modal-cliente .aviso-modal");
    if (avisoModal) avisoModal.innerHTML = "";

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    try {
      const dados = await clienteApi.cadastrarCliente(
        inputNome.value.trim(),
        inputNumero.value.trim(),
      );

      if (dados["sucesso"] === true) {
        form.reset();
        fechaModal("cliente");
        await mostrarClientes();
        mostraHistoricoCliente();

        const novoItem = dados.cliente
          ? dom.clientesLista.querySelector(
              `.cliente-item[data-id="${dados.cliente.id}"]`,
            )
          : null;
        selecionarClienteDesktop(novoItem);
      } else if (avisoModal && dados["mensagem"]) {
        avisoModal.innerHTML = dados["mensagem"];
      }
    } catch (err) {
      console.error("Erro ao cadastrar cliente:", err);
    }
  });
}
