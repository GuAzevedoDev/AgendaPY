export function mostrar_agenda_horarios(dados, agendaDiv, dataDiaAtivo) {
  dados.forEach((horario) => {
    switch (horario.status) {
      case "Livre":
        criar_card_livre(horario, agendaDiv, dataDiaAtivo);
        break;
      case "ocupado":
        criar_card_ocupado(horario, agendaDiv, dataDiaAtivo);
        break;
      case "confirmado":
        criar_card_concluido(horario, agendaDiv, dataDiaAtivo);
        break;
    }
  });
}

function criar_card_livre(horario, agendaDiv, dataDiaAtivo) {
  const agenda = {
    status: horario.status,
    horario: horario.hora,
    dia: horario.dia,
  };
  agendaDiv.innerHTML += `<div class="horarioTudo">
      <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">${agenda.horario}</div>
      <div class="status" >
        <span>Horário livre</span>
        <button class ="botaoAgenda" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">+</button>
      </div>
    </div>`;
}

function criar_card_ocupado(horario, agendaDiv, dataDiaAtivo) {
  const agenda = {
    concluido: horario.status,
    status: horario.status,
    horario: horario.hora,
    servico: horario.servico,
    cliente: horario.cliente,
    profissional: horario.profissional,
  };

  agendaDiv.innerHTML += `<div class="horarioTudo ${agenda.status}" data-data="${dataDiaAtivo}" data-hora="${agenda.horario}">
        <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
          <div class="status">
            <div class="cliente" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.cliente}</div>
            <div class="servico" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.servico}</div>
            <div class="detalhes">
            <svg width="4" height="13" viewBox="0 0 4 13" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M1.66667 9.91667C2.58717 9.91667 3.33333 10.5509 3.33333 11.3333C3.33333 12.1157 2.58717 12.75 1.66667 12.75C0.746167 12.75 0 12.1157 0 11.3333C0 10.5509 0.746167 9.91667 1.66667 9.91667Z" />
<path d="M1.66667 4.95832C2.58717 4.95832 3.33333 5.59256 3.33333 6.37499C3.33333 7.15741 2.58717 7.79166 1.66667 7.79166C0.746167 7.79166 0 7.15741 0 6.37499C0 5.59256 0.746167 4.95832 1.66667 4.95832Z" />
<path d="M1.66667 1.00136e-05C2.58717 1.00136e-05 3.33333 0.634252 3.33333 1.41668C3.33333 2.1991 2.58717 2.83334 1.66667 2.83334C0.746167 2.83334 0 2.1991 0 1.41668C0 0.634252 0.746167 1.00136e-05 1.66667 1.00136e-05Z"/>
</svg>
            <!-- Menu de opções adicionado dentro do botão de detalhes -->
            <ul class="detalhes-menu">
              <li class="opcao-pagamento">Adicionar forma de pagamento</li>
              <li class="opcao-excluir">Excluir horário</li>
            </ul>
</div>

          </div>  
        </div>`;
}

function criar_card_concluido(horario, agendaDiv, dataDiaAtivo) {
  const agenda = {
    concluido: horario.status,
    valorPago: horario.valorPago,
    formaPagamento: horario.formaPagamento,
    status: horario.status,
    horario: horario.hora,
    servico: horario.servico,
    cliente: horario.cliente,
    profissional: horario.profissional,
  };
  agendaDiv.innerHTML += `<div class="horarioTudo ${agenda.status} ativoPag" data-data="${dataDiaAtivo}" data-hora="${agenda.horario}" data-valorPago="${agenda.valorPago}" data-formaPag="${agenda.formaPagamento}" data-nomeCliente="${agenda.cliente}" data-servico="${agenda.servico}">
        <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
          <div class="status">       
            <div class="cliente" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.cliente}</div>
            <div class="servico" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.servico}</div>
            <div class="detalhes">
            <svg width="4" height="13" viewBox="0 0 4 13" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M1.66667 9.91667C2.58717 9.91667 3.33333 10.5509 3.33333 11.3333C3.33333 12.1157 2.58717 12.75 1.66667 12.75C0.746167 12.75 0 12.1157 0 11.3333C0 10.5509 0.746167 9.91667 1.66667 9.91667Z"/>
<path d="M1.66667 4.95832C2.58717 4.95832 3.33333 5.59256 3.33333 6.37499C3.33333 7.15741 2.58717 7.79166 1.66667 7.79166C0.746167 7.79166 0 7.15741 0 6.37499C0 5.59256 0.746167 4.95832 1.66667 4.95832Z"/>
<path d="M1.66667 1.00136e-05C2.58717 1.00136e-05 3.33333 0.634252 3.33333 1.41668C3.33333 2.1991 2.58717 2.83334 1.66667 2.83334C0.746167 2.83334 0 2.1991 0 1.41668C0 0.634252 0.746167 1.00136e-05 1.66667 1.00136e-05Z"/>
</svg>
            <!-- Menu de opções adicionado dentro do botão de detalhes -->
            <ul class="detalhes-menu">
              <li class="opcao-pagamento">Adicionar forma de pagamento</li>
              <li class="opcao-excluir">Excluir horário</li>
            </ul>
</div>

          </div>
        </div>`;
}

export function obterPeriodo(horario) {
  const hora = parseInt(horario.split(":")[0], 10);
  if (hora < 12) {
    return "manha";
  } else if (hora < 18) {
    return "tarde";
  } else {
    return "noite";
  }
}

export function filtrarAgenda(filtroAtivo) {
  const horarios = document.querySelectorAll(".horarioTudo");
  horarios.forEach((bloco) => {
    const elementoHora = bloco.querySelector(".horario");
    if (!elementoHora) return;
    const horaTexto =
      elementoHora.dataset.hora || elementoHora.textContent.trim();
    const periodo = obterPeriodo(horaTexto);
    if (filtroAtivo === "tudo" || periodo === filtroAtivo) {
      bloco.style.display = "";
    } else {
      bloco.style.display = "none";
    }
  });
}

export function atualizarTituloAgenda(nomeFuncionario) {
  const agendaTitulo = document.querySelector(".agenda-titulo");
  if (agendaTitulo) {
    agendaTitulo.textContent = `Agenda de ${nomeFuncionario}`;
  }
}
