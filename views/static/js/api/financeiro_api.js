import { csrfToken } from "../utils/csrf.js";

export async function buscarValorFuncionario(idFuncionario, mes, ano) {
  const resposta = await fetch("/agendar/valorAgendamento", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({
      idFuncionario: idFuncionario,
      mes: mes,
      ano: ano,
    }),
  });
  return await resposta.json();
}
