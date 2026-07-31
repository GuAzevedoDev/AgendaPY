import * as financeiroApi from "../api/financeiro_api.js";
import * as financeiroUi from "../ui/financeiro_ui.js";

const meses = [
  "Janeiro",
  "Fevereiro",
  "Março",
  "Abril",
  "Maio",
  "Junho",
  "Julho",
  "Agosto",
  "Setembro",
  "Outubro",
  "Novembro",
  "Dezembro",
];

const ANOS_PARA_TRAS = 4;

const hoje = new Date();
let mesSelecionado = hoje.getMonth() + 1;
let anoSelecionado = hoje.getFullYear();

export function iniciarFinanceiro() {
  const dropdownMes = document.querySelector(".financeiro-filtro-mes");
  const dropdownAno = document.querySelector(".financeiro-filtro-ano");
  const btnAtualizar = document.querySelector(".btn-atualizar-financeiro");

  if (dropdownMes) {
    configurarDropdown(dropdownMes, ".financeiro-mes-nome", ".financeiro-opcoes-mes", opcoesMes(), mesSelecionado, (valor) => {
      mesSelecionado = valor;
      buscarValores(btnAtualizar);
    });
  }

  if (dropdownAno) {
    configurarDropdown(dropdownAno, ".financeiro-ano-numero", ".financeiro-opcoes-ano", opcoesAno(), anoSelecionado, (valor) => {
      anoSelecionado = valor;
      buscarValores(btnAtualizar);
    });
  }

  if (btnAtualizar) {
    btnAtualizar.addEventListener("click", () => {
      buscarValores(btnAtualizar);
    });
  }

  buscarValores(btnAtualizar);
}

function opcoesMes() {
  return meses.map((nome, indice) => ({ valor: indice + 1, texto: nome }));
}

function opcoesAno() {
  const opcoes = [];
  for (let ano = hoje.getFullYear(); ano >= hoje.getFullYear() - ANOS_PARA_TRAS; ano--) {
    opcoes.push({ valor: ano, texto: String(ano) });
  }
  return opcoes;
}

function configurarDropdown(dropdown, seletorRotulo, seletorLista, opcoes, valorSelecionado, aoSelecionar) {
  const rotulo = dropdown.querySelector(seletorRotulo);
  const listaOpcoes = dropdown.querySelector(seletorLista);
  if (!rotulo || !listaOpcoes) return;

  opcoes.forEach((opcao) => {
    const item = document.createElement("li");
    item.textContent = opcao.texto;
    item.dataset.valor = opcao.valor;
    if (opcao.valor === valorSelecionado) rotulo.textContent = opcao.texto;
    listaOpcoes.appendChild(item);
  });

  dropdown.addEventListener("click", (evento) => {
    evento.stopPropagation();
    listaOpcoes.classList.toggle("ativo");
  });

  listaOpcoes.querySelectorAll("li").forEach((item) => {
    item.addEventListener("click", (evento) => {
      evento.stopPropagation();
      rotulo.textContent = item.textContent;
      listaOpcoes.classList.remove("ativo");
      aoSelecionar(Number(item.dataset.valor));
    });
  });

  document.addEventListener("click", () => {
    listaOpcoes.classList.remove("ativo");
  });
}

async function buscarValores(botaoAtualizar) {
  const cards = document.querySelectorAll(".funcionario-financeiro-card");
  const elTotal = document.querySelector(".financeiro-total-valor");

  financeiroUi.marcarBotaoCarregando(botaoAtualizar, true);
  cards.forEach((card) => financeiroUi.marcarCarregando(card));

  let total = 0;
  let algumaFalha = false;

  await Promise.all(
    Array.from(cards).map(async (card) => {
      try {
        const dados = await financeiroApi.buscarValorFuncionario(
          card.dataset.id,
          mesSelecionado,
          anoSelecionado,
        );

        if (dados && dados.sucesso) {
          const valores = {
            valorTotal: Number(dados.valorTotal) || 0,
            valorPagar: Number(dados.valorPagar) || 0,
            valorReceber: Number(dados.valorReceber) || 0,
          };
          total += valores.valorTotal;
          financeiroUi.mostrarValor(card, valores);
        } else {
          algumaFalha = true;
          financeiroUi.mostrarErro(card);
        }
      } catch (err) {
        console.error("Erro ao buscar valor do funcionario:", err);
        algumaFalha = true;
        financeiroUi.mostrarErro(card);
      }
    }),
  );

  if (algumaFalha) {
    financeiroUi.limparTotal(elTotal);
  } else {
    financeiroUi.atualizarTotal(elTotal, total);
  }

  financeiroUi.marcarBotaoCarregando(botaoAtualizar, false);
}
