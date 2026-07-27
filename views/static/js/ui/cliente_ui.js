import * as dom from "./dom.js";
import * as cliente_api from "../api/cliente_api.js";
import { escapeHtml } from "../utils/html.js";

let indiceSelecionado = -1;

function selecionarCliente(item) {
  dom.inputNome.value = item.dataset.nome;
  dom.inputNumero.value = item.dataset.numero;
  dom.listaNomes.innerHTML = "";
  indiceSelecionado = -1;
}

function atualizarSelecao() {
  const itens = dom.listaNomes.querySelectorAll(".nome-lista");

  itens.forEach((item, index) => {
    item.classList.toggle("ativo", index === indiceSelecionado);
  });

  if (indiceSelecionado >= 0) {
    itens[indiceSelecionado].scrollIntoView({
      block: "nearest",
    });
  }
}

export function coloca_nome_lista(clientes, listaNomes) {
  if (dom.inputNome.value.trim() === "") {
    listaNomes.innerHTML = "";
    indiceSelecionado = -1;
    return;
  }

  listaNomes.innerHTML = clientes
    .map(
      (cliente) => `
        <li
          class="nome-lista"
          data-nome="${escapeHtml(cliente[1])}"
          data-numero="${escapeHtml(cliente[2])}"
          tabindex="-1">
          ${escapeHtml(cliente[1])}
        </li>
      `,
    )
    .join("");

  indiceSelecionado = -1;
}

export function ativa_cliente_selecionado() {
  // Clique na lista
  dom.listaNomes.addEventListener("click", (e) => {
    const item = e.target.closest(".nome-lista");

    if (!item) return;

    selecionarCliente(item);
  });

  // Navegação por teclado
  dom.inputNome.addEventListener("keydown", (e) => {
    const itens = [...dom.listaNomes.querySelectorAll(".nome-lista")];

    if (!itens.length) return;

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        indiceSelecionado = Math.min(indiceSelecionado + 1, itens.length - 1);
        atualizarSelecao();
        break;

      case "ArrowUp":
        e.preventDefault();
        indiceSelecionado = Math.max(indiceSelecionado - 1, 0);
        atualizarSelecao();
        break;

      case "Enter":
      case "Tab":
        if (indiceSelecionado >= 0) {
          e.preventDefault();
          selecionarCliente(itens[indiceSelecionado]);
        }
        break;

      case "Escape":
        dom.listaNomes.innerHTML = "";
        indiceSelecionado = -1;
        break;
    }
  });
}

export function mostrarClientes(clientes, listaClientes) {
  listaClientes.innerHTML = "";
  clientes.forEach((cliente) => {
    let dados = {
      id: cliente["id"],
      nome: cliente["nome"],
      numero: cliente["numero"],
    };
    listaClientes.innerHTML += `<li class="cliente-item" data-id = "${dados.id}" data-nome = "${escapeHtml(dados.nome)}" data-numero = "${escapeHtml(dados.numero)}">
              <div class="cliente-inicial">${escapeHtml(dados.nome[0].toUpperCase())}</div>
              <div class="cliente-info">
                <h3>${escapeHtml(dados.nome)}</h3>
                <span class="cor-3">${escapeHtml(dados.numero)}</span>
              </div>
            </li>`;
  });
}

export function marcaClicado(clienteClicado, clientesItens) {
  //Tirar todos marcados
  clientesItens.forEach((item) => {
    item.classList.remove("ativo");
  });
  clienteClicado.classList.add("ativo");
}

export function inserirHistoricoCima(nome, numero) {
  dom.nomeCliente.textContent = nome;
  dom.numeroCliente.textContent = numero;
  let inicial = document.querySelector(
    ".cliente-detalhes-header .cliente-inicial",
  );
  if (inicial && nome) {
    inicial.innerText = nome[0].toUpperCase();
  }
}

export function atualizarMetricas(totalAgendamentos, ultimoAtendimento) {
  dom.metricaTotalAgendamentos.innerHTML = totalAgendamentos;
  dom.metricaUltimoAgendamento.innerHTML = ultimoAtendimento || "-";
}

export function inserirHistorico(historico) {
  let dados = {
    agendamento_data: historico["agendamento_data"],
    agendamento_horario: historico["agendamento_horario"],
    agendamento_profissional: historico["agendamento_profissional"],
    cliente_nome: historico["cliente_nome"],
    cliente_numero: historico["cliente_numero"],
    servicos: historico["servicos"],
  };
  dom.listaUltimosAgendamentos.innerHTML += `<div class="agendamento-historico-card">
              <div class="agendamento-tempo">
                <span class="cor-2 data">${dados.agendamento_data}</span>
                <span class="cor-3 hora">${dados.agendamento_horario}</span>
              </div>
              <div class="agendamento-info">
                <h4 class="cor-2 servico">${dados.servicos.map((item) => item).join(" + ")}</h4>
                <span class="cor-3 profissional">Profissional: ${dados.agendamento_profissional}</span>
              </div>
            </div>`;
}

export function limparHistorico() {
  let listaHistoricoAgendamentos = document.querySelector(
    ".agendamentos-historico-lista",
  );
  listaHistoricoAgendamentos.innerHTML = "";
}

export function limparDetalhesCliente() {
  dom.nomeCliente.innerHTML = "Selecione um cliente";
  dom.numeroCliente.innerHTML = "";
  let inicial = document.querySelector(
    ".cliente-detalhes-header .cliente-inicial",
  );
  if (inicial) inicial.innerText = "-";
  atualizarMetricas(0, null);
  limparHistorico();
}
