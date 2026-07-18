import * as dom from "./dom.js";

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
          data-nome="${cliente[1]}"
          data-numero="${cliente[2]}"
          tabindex="-1">
          ${cliente[1]}
        </li>
      `
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