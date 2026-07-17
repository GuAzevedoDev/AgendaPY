export function desmarcar_funcionarios(funcionarios) {
  funcionarios.forEach((funcionario) => {
    funcionario.classList.remove("ativo");
  });
}

export function marcar_funcionario_ativo(funcionario) {
  if (window.id_funcionario == funcionario.dataset.id) {
    funcionario.classList.add("ativo");
  }
}
