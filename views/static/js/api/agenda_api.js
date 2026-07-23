import { csrfToken } from "../utils/csrf.js";

export async function excluir_horario(id_funcionario, dataAgendamento, horaAgendamento) {
  const resposta = await fetch("/agendar/excluirHorario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      idFuncionario: id_funcionario,
      dataAgendamento: dataAgendamento,
      horaAgendamento: horaAgendamento,
    }),
  });
  return await resposta.json();
}

export async function enviar_dia_clicado(dia, id_funcionario) {
  const resposta = await fetch("/agendar/calendario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      data: dia,
      idFuncionario: id_funcionario,
    }),
  });
  return await resposta.json();
}

export async function adicionarPagamento(idFuncionario, valorAgendamento, formaPagamento, dataAgendamento, horaAgendamento) {
  const resposta = await fetch("/agendar/atualizarPg", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      idFuncionario,
      valorAgendamento,
      formaPagamento,
      dataAgendamento,
      horaAgendamento,
    }),
  });
  return await resposta.json();
}

export async function buscarDiasComAgendamento(mes, ano, idFuncionario) {
  const resposta = await fetch("/agendar/diasComAgendamento", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      mes,
      ano,
      idFuncionario,
    }),
  });
  return await resposta.json();
}

export async function agendarHorario(idFuncionario, nomesServicos, nomeCliente, numeroCliente, horaAgendamento, dataAgendamento,observacao) {
  const resposta = await fetch("/agendar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      idFuncionario,
      nomesServicos,
      nomeCliente,
      numeroCliente,
      horaAgendamento,
      dataAgendamento,
      observacao
    }),
  });
  return await resposta.json();
}
