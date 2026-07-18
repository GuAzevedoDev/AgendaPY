export async function excluir_horario(id_funcionario, dataAgendamento, horaAgendamento) {
  const resposta = await fetch("/agendar/excluirHorario", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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

export async function agendarHorario(idFuncionario, nomesServicos, nomeCliente, numeroCliente, horaAgendamento, dataAgendamento,observacao) {
  const resposta = await fetch("/agendar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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