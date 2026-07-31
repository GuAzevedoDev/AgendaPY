export function formatarValor(valor) {
  const numero = Number(valor) || 0;
  return numero.toLocaleString("pt-br", { style: "currency", currency: "BRL" });
}

export function marcarCarregando(card) {
  card.classList.remove("erro");
  card.classList.add("carregando");
  definirValoresCard(card, "Carregando...", "Carregando...", "Carregando...");
}

export function mostrarValor(card, valores) {
  card.classList.remove("carregando", "erro");
  definirValoresCard(
    card,
    formatarValor(valores.valorTotal),
    formatarValor(valores.valorPagar),
    formatarValor(valores.valorReceber),
  );
}

export function mostrarErro(card) {
  card.classList.remove("carregando");
  card.classList.add("erro");
  definirValoresCard(card, "Erro ao buscar", "Erro ao buscar", "Erro ao buscar");
}

function definirValoresCard(card, total, pagar, receber) {
  const elTotal = card.querySelector(".funcionario-financeiro-valor-total");
  const elPagar = card.querySelector(".funcionario-financeiro-valor-pagar");
  const elReceber = card.querySelector(".funcionario-financeiro-valor-receber");

  if (elTotal) elTotal.textContent = total;
  if (elPagar) elPagar.textContent = pagar;
  if (elReceber) elReceber.textContent = receber;
}

export function atualizarTotal(elTotal, total) {
  if (!elTotal) return;
  elTotal.textContent = formatarValor(total);
}

export function limparTotal(elTotal) {
  if (!elTotal) return;
  elTotal.textContent = "--";
}

export function marcarBotaoCarregando(botao, carregando) {
  if (!botao) return;
  botao.disabled = carregando;
  botao.classList.toggle("carregando", carregando);
}
