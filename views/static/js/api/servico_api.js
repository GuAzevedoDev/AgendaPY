export async function buscarServicos(nomeServico) {
  const resposta = await fetch("/agendar/buscaServico", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nomeServico: nomeServico,
    }),
  });
  return await resposta.json();
}
