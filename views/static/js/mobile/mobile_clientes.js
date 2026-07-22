import * as dom from "../ui/dom.js";

export function iniciarClientesMobile() {
  if (!window.matchMedia("(max-width: 900px)").matches) return;

  const painel = document.querySelector(".cliente-detalhes-secao");
  const botaoVoltar = document.querySelector(".btn-voltar-cliente");
  if (!painel || !dom.clientesLista) return;

  dom.clientesLista.addEventListener("click", (evento) => {
    if (evento.target.closest(".cliente-item")) {
      painel.classList.add("painel-aberto");
    }
  });

  if (botaoVoltar) {
    botaoVoltar.addEventListener("click", () => {
      painel.classList.remove("painel-aberto");
    });
  }
}
