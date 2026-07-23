function algumModalAberto() {
  return [...document.querySelectorAll(".modal-container")].some(
    (modal) => modal.open,
  );
}

function desbloquearScrollSeNecessario() {
  if (!algumModalAberto()) {
    document.documentElement.classList.remove("scroll-bloqueado");
  }
}

// Alguns modais sao fechados via dialog.close() direto no onclick (sem passar por fechaModal),
// e o ESC tambem fecha nativamente. Escutar o evento "close" cobre todos os casos.
document.querySelectorAll(".modal-container").forEach((modal) => {
  modal.addEventListener("close", desbloquearScrollSeNecessario);
});

export function abreModal(nome) {
  document.querySelector(`.modal-${nome}`).showModal();
  document.documentElement.classList.add("scroll-bloqueado");
}

export function fechaModal(nome) {
  document.querySelector(`.modal-${nome}`).close();
}