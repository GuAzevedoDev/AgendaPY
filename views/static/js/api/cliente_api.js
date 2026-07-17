export async function pegaNomes(nomeCliente) {
  const resposta = await fetch("/agendar/buscaNome", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nomeCliente: nomeCliente,
    }),
  });
  return await resposta.json();
}
