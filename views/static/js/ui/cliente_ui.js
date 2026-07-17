import * as dom from "./dom.js";

export function coloca_nome_lista(clientes, listaNomes) {
  listaNomes.innerHTML = "";
  clientes.forEach((cliente) => {
    listaNomes.innerHTML += `<li class="nome-lista" data-nome="${cliente[1]}" data-numero="${cliente[2]}">${cliente[1]}</li>`;
  });
  if (dom.inputNome.value === "") {
    listaNomes.innerHTML = "";
  }
}

export function ativa_cliente_selecionado(nomesLista) {
  nomesLista.forEach((nomeLista) => {
    nomeLista.addEventListener("click", function colocaNumero() {
      const nomeSelecionado = nomeLista.dataset.nome;
      const numeroSelecionado = nomeLista.dataset.numero;
      dom.inputNome.value = nomeSelecionado;
      dom.inputNumero.value = numeroSelecionado;
      dom.listaNomes.innerHTML = "";
    });
  });
}