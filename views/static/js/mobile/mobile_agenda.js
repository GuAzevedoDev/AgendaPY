import * as dom from "../ui/dom.js";

const ABREVIACOES = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];

function decorarDia(dia) {
  if (dia.dataset.mobileReady) return;

  const [d, m, a] = dia.dataset.data.split("/").map(Number);
  const indice = new Date(a, m - 1, d).getDay();

  const label = document.createElement("span");
  label.className = "dia-semana-mini";
  label.textContent = ABREVIACOES[indice];
  dia.prepend(label);

  dia.dataset.mobileReady = "1";
}

function decorarDias() {
  dom.divDias.querySelectorAll(".dia").forEach(decorarDia);
}

function rolarParaAtivo() {
  const ativo = dom.divDias.querySelector(".dia.ativo");
  if (ativo) {
    ativo.scrollIntoView({ inline: "center", block: "nearest" });
  }
}

export function iniciarAgendaMobile() {
  if (!window.matchMedia("(max-width: 900px)").matches) return;

  if (dom.divDias) {
    decorarDias();
    rolarParaAtivo();

    const observer = new MutationObserver(() => {
      decorarDias();
      rolarParaAtivo();
    });
    observer.observe(dom.divDias, { childList: true });

    dom.divDias.addEventListener("click", (evento) => {
      const dia = evento.target.closest(".dia");
      if (dia) rolarParaAtivo();
    });
  }

  configurarToggleDisponiveis();
}

function configurarToggleDisponiveis() {
  const botao = document.querySelector(".btn-ver-disponiveis");
  const listaAgenda = dom.agendaDiv;
  if (!botao || !listaAgenda) return;

  botao.addEventListener("click", () => {
    const expandido = listaAgenda.classList.toggle("expandido");
    botao.textContent = expandido
      ? "Ver só agendados"
      : "Ver horários disponíveis";
  });

  // A cada troca de dia a agenda e re-renderizada; volta ao estado compacto por padrao
  const observer = new MutationObserver(() => {
    listaAgenda.classList.remove("expandido");
    botao.textContent = "Ver horários disponíveis";
  });
  observer.observe(listaAgenda, { childList: true });
}
