import { csrfToken } from "../utils/csrf.js";

export async function buscarServicos(nomeServico) {
  const resposta = await fetch("/agendar/buscaServico", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      nomeServico: nomeServico,
    }),
  });
  return await resposta.json();
}
