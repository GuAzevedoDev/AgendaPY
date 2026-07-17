import * as dom from "../ui/dom.js";
import * as agendaUI from "../ui/agenda_ui.js";
import * as agendaApi from "../api/agenda_api.js";
import { abreModal } from "../ui/modal_ui.js";

let dataPagActive = null;
let horaPagActive = null;

export function iniciarAgenda() {
  inicializarFiltro();
  atualizarTituloAgenda();
  configurarGlobalClickCloser();
  configurarFormaPagRadioListener();
  configurarBotaoAtualizarPagamento();
}

export async function carregarAgendaDoDia(diaData) {
  try {
    const agenda = await agendaApi.enviar_dia_clicado(diaData, window.id_funcionario);
    dom.agendaDiv.innerHTML = "";
    renderizaAgendamentos(agenda, diaData);
  } catch (err) {
    console.error("Erro ao carregar agenda do dia:", err);
  }
}

export function renderizaAgendamentos(agenda, diaData) {
  agendaUI.mostrar_agenda_horarios(agenda, dom.agendaDiv, diaData);

  const cards = dom.agendaDiv.querySelectorAll(".horarioTudo");
  cards.forEach((card) => {
    const status = card.querySelector(".horario").dataset.status;
    
    if (status === "Livre") {
      const botao = card.querySelector(".botaoAgenda");
      if (botao) {
        botao.addEventListener("click", () => {
          const inputHora = document.querySelector(".horaCliente");
          const inputData = document.querySelector(".dataCliente");
          if (inputHora) inputHora.value = botao.dataset.hora;
          if (inputData) inputData.value = botao.dataset.data;
          abreModal("agendamento");
        });
      }
    } else {
      configurarCardOcupadoOuConcluido(card);
    }
  });

  filtrarAgendaAtiva();
}

function configurarCardOcupadoOuConcluido(card) {
  const detalhesBotao = card.querySelector(".detalhes");
  const menu = card.querySelector(".detalhes-menu");

  if (detalhesBotao && menu) {
    detalhesBotao.addEventListener("click", (evento) => {
      evento.stopPropagation();
      document.querySelectorAll(".detalhes-menu").forEach((m) => {
        if (m !== menu) {
          m.classList.remove("ativo");
          m.parentElement.classList.remove("ativo");
        }
      });
      menu.classList.toggle("ativo");
      detalhesBotao.classList.toggle("ativo");
    });

    const opcaoPagamento = menu.querySelector(".opcao-pagamento");
    if (opcaoPagamento) {
      opcaoPagamento.addEventListener("click", (evento) => {
        evento.stopPropagation();
        menu.classList.remove("ativo");
        detalhesBotao.classList.remove("ativo");
        card.click();
      });
    }

    const opcaoExcluir = menu.querySelector(".opcao-excluir");
    if (opcaoExcluir) {
      opcaoExcluir.addEventListener("click", async (evento) => {
        evento.stopPropagation();
        menu.classList.remove("ativo");
        detalhesBotao.classList.remove("ativo");

        const dataAgendamento = card.dataset.data;
        const horaAgendamento = card.dataset.hora;

        if (confirm(`Deseja realmente excluir o agendamento de ${dataAgendamento} às ${horaAgendamento}?`)) {
          try {
            const dados = await agendaApi.excluir_horario(window.id_funcionario, dataAgendamento, horaAgendamento);
            if (dados.sucesso === true || dados.mensagem === true) {
              window.location.reload();
            } else {
              alert("Erro ao excluir horário: " + (dados.mensagem || "Erro desconhecido"));
            }
          } catch (err) {
            console.error("Erro na requisição de exclusão:", err);
            alert("Ocorreu um erro técnico ao tentar excluir o horário.");
          }
        }
      });
    }
  }

  card.addEventListener("click", () => {
    if (card.classList.contains("ativoPag")) {
      const informacoes = {
        data: card.dataset.data,
        hora: card.dataset.hora,
        servicos: card.dataset.servico,
        valorPago: card.dataset.valorpago,
        formaPagamento: card.dataset.formapag,
      };

      document.querySelector(".data-detalhes").innerHTML = informacoes.data;
      document.querySelector(".hora-detalhes").innerHTML = informacoes.hora;
      document.querySelector(".servico-detalhes").innerHTML = informacoes.servicos;
      document.querySelector(".pagamento-detalhes").innerHTML = informacoes.formaPagamento;
      document.querySelector(".valor-detalhes").innerHTML = informacoes.valorPago;

      abreModal("detalhes");
    } else {
      dataPagActive = card.dataset.data;
      horaPagActive = card.dataset.hora;
      abreModal("valor");
    }
  });
}

function configurarBotaoAtualizarPagamento() {
  const botaoEnviar = document.querySelector("#btnAtualizar");
  if (!botaoEnviar) return;

  botaoEnviar.addEventListener("click", async () => {
    const inputValor = document.querySelector(".valorAgendamento");
    const formaPagamento = document.querySelector('input[name="formaPag"]:checked');
    const avisos = document.querySelectorAll(".aviso-modal");
    const aviso = avisos[1] || avisos[0];

    if (!formaPagamento) {
      if (aviso) aviso.innerHTML = "Selecione uma forma de pagamento";
      return;
    }

    try {
      const dados = await agendaApi.adicionarPagamento(
        window.id_funcionario,
        inputValor.value,
        formaPagamento.id,
        dataPagActive,
        horaPagActive
      );

      if (dados["mensagem"] === true) {
        window.location.reload();

      } else {
        console.log(dados["mensagem"]);
      }
    } catch (err) {
      console.error("Erro ao atualizar pagamento:", err);
    }
  });
}

function configurarFormaPagRadioListener() {
  document.querySelectorAll('input[name="formaPag"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      const avisos = document.querySelectorAll(".aviso-modal");
      const aviso = avisos[1] || avisos[0];
      if (aviso) aviso.innerHTML = "";
    });
  });
}

function configurarGlobalClickCloser() {
  document.addEventListener("click", () => {
    document.querySelectorAll(".detalhes-menu").forEach((m) => {
      m.classList.remove("ativo");
    });
    document.querySelectorAll(".detalhes").forEach((d) => {
      d.classList.remove("ativo");
    });
  });
}

function inicializarFiltro() {
  const dropdown = document.querySelector(".drop-down-filtro");
  const opcoesLista = document.querySelector(".opcoes-filtro");
  if (!dropdown || !opcoesLista) return;

  const spanFiltro = dropdown.querySelector("span");

  dropdown.addEventListener("click", (evento) => {
    evento.stopPropagation();
    opcoesLista.classList.toggle("ativo");
  });

  opcoesLista.querySelectorAll("li").forEach((opcao) => {
    opcao.addEventListener("click", (evento) => {
      evento.stopPropagation();
      spanFiltro.textContent = opcao.textContent;
      dropdown.dataset.filtro = opcao.dataset.opcao;
      opcoesLista.classList.remove("ativo");
      filtrarAgendaAtiva();
    });
  });

  document.addEventListener("click", () => {
    opcoesLista.classList.remove("ativo");
  });
}

function filtrarAgendaAtiva() {
  const dropdown = document.querySelector(".drop-down-filtro");
  if (!dropdown) return;
  const filtroAtivo = dropdown.dataset.filtro || "tudo";
  agendaUI.filtrarAgenda(filtroAtivo);
}

function atualizarTituloAgenda() {
  const agendaTitulo = document.querySelector(".agenda-titulo");
  if (!agendaTitulo) return;

  const funcionarios = document.querySelectorAll(".funcionario");
  funcionarios.forEach((funcionario) => {
    if (funcionario.dataset.id == window.id_funcionario) {
      agendaUI.atualizarTituloAgenda(funcionario.dataset.nome);
    }

    funcionario.addEventListener("click", () => {
      agendaUI.atualizarTituloAgenda(funcionario.dataset.nome);
    });
  });
}