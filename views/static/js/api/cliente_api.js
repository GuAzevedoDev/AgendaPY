import { csrfToken } from "../utils/csrf.js";

export async function pegaNomes(nomeCliente) {
  const resposta = await fetch("/agendar/buscaNome", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
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
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({
      id: idCliente,
    }),
  });
  return await resposta.json();
}

export async function pesquisarClientes(termo) {
  const resposta = await fetch("/clientes/pesquisar", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({
      termo: termo,
    }),
  });
  return await resposta.json();
}

export async function cadastrarCliente(nome, numero) {
  const resposta = await fetch("/clientes/cadastrar", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({
      nome: nome,
      numero: numero,
    }),
  });
  return await resposta.json();
}
