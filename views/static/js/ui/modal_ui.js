export function abreModal(nome) {
  document.querySelector(`.modal-${nome}`).showModal();
}

export function fechaModal(nome) {
  document.querySelector(`.modal-${nome}`).close();
}