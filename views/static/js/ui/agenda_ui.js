export function mostrar_agenda_horarios(dados, agendaDiv,dataDiaAtivo) {
  dados.forEach((horario, i) => {
    switch (horario.status) {
      case "Livre":
        criar_card_livre(horario, agendaDiv,dataDiaAtivo);
      case "Ocupado":
        criar_card_ocupado(horario, agendaDiv,dataDiaAtivo);
      case "Concluido":
        criar_card_concluido(horario, agendaDiv,dataDiaAtivo);
    }
  });
}

function criar_card_livre(horario, agendaDiv) {
  agenda = {
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

function criar_card_ocupado(horario, agendaDiv) {
  agenda = {
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

function criar_card_concluido(horario,agendaDiv){
  agenda = {
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

export function pega_ocupados(){
  let ocupados = document.querySelectorAll(".horarioTudo.Ocupado");
  return ocupados
}

function mostrarAgenda(dados) {
//   let dataDiaAtivo = document.querySelector(".dia.ativo").dataset.data;
//   dados.forEach((dado, i) => {
//     if (dado.status == "Livre") {
//       agenda = {
//         status: dado.status,
//         horario: dado.hora,
//         dia: dado.dia,
//       };
//       agendaDiv.innerHTML += `<div class="horarioTudo">
//       <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">${agenda.horario}</div>
//       <div class="status" >
//         <span>Horário livre</span>
//         <button class ="botaoAgenda" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">+</button>
//       </div>
//     </div>`;
//     } else {
//       agenda = {
//         concluido: dado.status,
//         valorPago: dado.valorPago,
//         formaPagamento: dado.formaPagamento,
//         status: dado.status,
//         horario: dado.hora,
//         servico: dado.servico,
//         cliente: dado.cliente,
//         profissional: dado.profissional,
//       };
//       if (agenda.valorPago && agenda.formaPagamento) {
//         agendaDiv.innerHTML += `<div class="horarioTudo ${agenda.status} ativoPag" data-data="${dataDiaAtivo}" data-hora="${agenda.horario}" data-valorPago="${agenda.valorPago}" data-formaPag="${agenda.formaPagamento}" data-nomeCliente="${agenda.cliente}" data-servico="${agenda.servico}">
//         <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
//           <div class="status">       
//             <div class="cliente" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.cliente}</div>
//             <div class="servico" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.servico}</div>
//             <div class="detalhes">
//             <svg width="4" height="13" viewBox="0 0 4 13" fill="none" xmlns="http://www.w3.org/2000/svg">
// <path d="M1.66667 9.91667C2.58717 9.91667 3.33333 10.5509 3.33333 11.3333C3.33333 12.1157 2.58717 12.75 1.66667 12.75C0.746167 12.75 0 12.1157 0 11.3333C0 10.5509 0.746167 9.91667 1.66667 9.91667Z"/>
// <path d="M1.66667 4.95832C2.58717 4.95832 3.33333 5.59256 3.33333 6.37499C3.33333 7.15741 2.58717 7.79166 1.66667 7.79166C0.746167 7.79166 0 7.15741 0 6.37499C0 5.59256 0.746167 4.95832 1.66667 4.95832Z"/>
// <path d="M1.66667 1.00136e-05C2.58717 1.00136e-05 3.33333 0.634252 3.33333 1.41668C3.33333 2.1991 2.58717 2.83334 1.66667 2.83334C0.746167 2.83334 0 2.1991 0 1.41668C0 0.634252 0.746167 1.00136e-05 1.66667 1.00136e-05Z"/>
// </svg>
//             <!-- Menu de opções adicionado dentro do botão de detalhes -->
//             <ul class="detalhes-menu">
//               <li class="opcao-pagamento">Adicionar forma de pagamento</li>
//               <li class="opcao-excluir">Excluir horário</li>
//             </ul>
// </div>

//           </div>
//         </div>`;
//       } else {
//         agendaDiv.innerHTML += `<div class="horarioTudo ${agenda.status}" data-data="${dataDiaAtivo}" data-hora="${agenda.horario}">
//         <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
//           <div class="status">
//             <div class="cliente" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.cliente}</div>
//             <div class="servico" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.servico}</div>
//             <div class="detalhes">
//             <svg width="4" height="13" viewBox="0 0 4 13" fill="none" xmlns="http://www.w3.org/2000/svg">
// <path d="M1.66667 9.91667C2.58717 9.91667 3.33333 10.5509 3.33333 11.3333C3.33333 12.1157 2.58717 12.75 1.66667 12.75C0.746167 12.75 0 12.1157 0 11.3333C0 10.5509 0.746167 9.91667 1.66667 9.91667Z" />
// <path d="M1.66667 4.95832C2.58717 4.95832 3.33333 5.59256 3.33333 6.37499C3.33333 7.15741 2.58717 7.79166 1.66667 7.79166C0.746167 7.79166 0 7.15741 0 6.37499C0 5.59256 0.746167 4.95832 1.66667 4.95832Z" />
// <path d="M1.66667 1.00136e-05C2.58717 1.00136e-05 3.33333 0.634252 3.33333 1.41668C3.33333 2.1991 2.58717 2.83334 1.66667 2.83334C0.746167 2.83334 0 2.1991 0 1.41668C0 0.634252 0.746167 1.00136e-05 1.66667 1.00136e-05Z"/>
// </svg>
//             <!-- Menu de opções adicionado dentro do botão de detalhes -->
//             <ul class="detalhes-menu">
//               <li class="opcao-pagamento">Adicionar forma de pagamento</li>
//               <li class="opcao-excluir">Excluir horário</li>
//             </ul>
// </div>

//           </div>  
//         </div>`;
//       }
//     }
//   });
  let ocupados = document.querySelectorAll(".horarioTudo.Ocupado");
  atualizarPag(ocupados);

  // === CONFIGURAÇÃO DO MENU DOS TRÊS PONTOS (DETALHES) ===
  ocupados.forEach((ocupado) => {
    // Localiza o botão de três pontos (.detalhes) dentro do card ocupado
    let detalhesBotao = ocupado.querySelector(".detalhes");
    // Localiza o respectivo menu de opções
    let menu = ocupado.querySelector(".detalhes-menu");

    if (detalhesBotao && menu) {
      // 1. Ouvinte para abrir/fechar o menu ao clicar nos três pontos
      detalhesBotao.addEventListener("click", function (evento) {
        // MUITO IMPORTANTE: Impede a propagação do clique para o container pai ocupado (.horarioTudo.Ocupado),
        // evitando que o modal de pagamento/detalhes seja aberto acidentalmente ao clicar nas opções!
        evento.stopPropagation();

        // Fecha todos os outros menus que porventura estejam abertos
        document.querySelectorAll(".detalhes-menu").forEach((m) => {
          if (m !== menu) {
            m.classList.remove("ativo");
            m.parentElement.classList.remove("ativo");
          }
        });

        // Alterna o estado ativo do menu atual e o botão
        menu.classList.toggle("ativo");
        detalhesBotao.classList.toggle("ativo");
      });

      // 2. Ouvinte para a opção de "Adicionar forma de pagamento"
      let opcaoPagamento = menu.querySelector(".opcao-pagamento");
      if (opcaoPagamento) {
        opcaoPagamento.addEventListener("click", function (evento) {
          // Impede propagação para não dar conflito
          evento.stopPropagation();

          // Fecha o menu atual
          menu.classList.remove("ativo");
          detalhesBotao.classList.remove("ativo");

          // Simula programaticamente um clique no container ocupado principal
          // Isso chama automaticamente a função original formaPg(), abrindo o modal correto
          ocupado.click();
        });
      }

      // 3. Ouvinte para a opção de "Excluir horário"
      let opcaoExcluir = menu.querySelector(".opcao-excluir");
      if (opcaoExcluir) {
        opcaoExcluir.addEventListener("click", function (evento) {
          // Impede propagação para que o clique não abra o modal de pagamento
          evento.stopPropagation();

          // Fecha o menu atual
          menu.classList.remove("ativo");
          detalhesBotao.classList.remove("ativo");

          // Captura a data e a hora do agendamento a partir do container principal (.horarioTudo)
          const dataAgendamento = ocupado.dataset.data;
          const horaAgendamento = ocupado.dataset.hora;

          // Caixa de diálogo nativa para confirmar a exclusão com o usuário
          if (
            confirm(
              `Deseja realmente excluir o agendamento de ${dataAgendamento} às ${horaAgendamento}?`,
            )
          ) {
            // Realiza a chamada fetch post para a rota Flask que criamos no backend
            fetch("/agendar/excluirHorario", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                idFuncionario: id_funcionario,
                dataAgendamento: dataAgendamento,
                horaAgendamento: horaAgendamento,
              }),
            })
              .then((resposta) => resposta.json()) // Converte a resposta do Flask em JSON
              .then((dados) => {
                // Verifica se a exclusão foi bem sucedida
                if (dados.sucesso === true || dados.mensagem === true) {
                  // Recarrega a página para atualizar a agenda na tela de forma limpa
                  window.location.reload();
                } else {
                  // Caso contrário, mostra a mensagem de erro retornada pelo servidor
                  alert(
                    "Erro ao excluir horário: " +
                      (dados.mensagem || "Erro desconhecido"),
                  );
                }
              })
              .catch((erro) => {
                console.error("Erro na requisição de exclusão:", erro);
                alert("Ocorreu um erro técnico ao tentar excluir o horário.");
              });
          }
        });
      }
    }
  });

  // Ouvinte global para fechar o menu caso o usuário clique em qualquer outro lugar fora do menu
  document.addEventListener("click", function () {
    document.querySelectorAll(".detalhes-menu").forEach((m) => {
      m.classList.remove("ativo");
    });
    document.querySelectorAll(".detalhes").forEach((d) => {
      d.classList.remove("ativo");
    });
  });

  let botoesAgenda = document.querySelectorAll(".botaoAgenda");
  botoesAgenda.forEach((botao) => {
    botao.addEventListener("click", function pegaData() {
      let horaAgenda = botao.dataset.hora;
      let dataAgenda = botao.dataset.data;
      let inputHora = document.querySelector(".horaCliente");
      let inputData = document.querySelector(".dataCliente");
      abreModal("agendamento");
      inputHora.value = horaAgenda;
      inputData.value = dataAgenda;
    });
  });
}
