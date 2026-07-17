import * as funcionarioUi from "../ui/funcionario_ui.js";

export function iniciarFuncionarios() {
  const funcionarios = document.querySelectorAll(".funcionario");

  funcionarios.forEach((funcionario) => {
    if (funcionario.dataset.id == window.id_funcionario) {
      funcionarioUi.marcar_funcionario_ativo(funcionario);
    }

    funcionario.addEventListener("click", () => {
      funcionarioUi.desmarcar_funcionarios(funcionarios);

      window.id_funcionario = funcionario.dataset.id;

      funcionarioUi.marcar_funcionario_ativo(funcionario);

      const diaAtivo = document.querySelector(".dias-calendario .ativo");
      if (diaAtivo) {
        diaAtivo.click();
      }
    });
  });
}
