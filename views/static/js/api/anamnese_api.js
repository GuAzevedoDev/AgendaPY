import { csrfToken } from "../utils/csrf.js";

export async function mostrarFichas() {
  const resposta = await fetch("/anamnese/mostrar", {
    method: "GET",
  });
  return await resposta.json();
}

export async function buscarFicha(id) {
  const resposta = await fetch("/anamnese/detalhes", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({ id }),
  });
  return await resposta.json();
}

export async function atualizarFicha(id, respostas) {
  const resposta = await fetch("/anamnese/atualizar", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({ id, respostas }),
  });
  return await resposta.json();
}

export async function excluirFicha(id) {
  const resposta = await fetch("/anamnese/excluir", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({ id }),
  });
  return await resposta.json();
}

export async function enviarFicha(nome, numero, respostas) {
  const resposta = await fetch("/anamnese/enviar", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({ nome, numero, respostas }),
  });
  return await resposta.json();
}
