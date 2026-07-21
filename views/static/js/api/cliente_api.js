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

export async function mostrarClientes() {
  const resposta = await fetch("/clientes/mostrar", {
    method: "GET",
  });
  return await resposta.json();
}

export async function pegaDadosCliente(idCliente) {
  const resposta = await fetch("/clientes/historico", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: idCliente,
    }),
  });
  return await resposta.json();
}

export async function pesquisarClientes(termo) {
  const resposta = await fetch("/clientes/pesquisar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      termo: termo,
    }),
  });
  return await resposta.json();
}