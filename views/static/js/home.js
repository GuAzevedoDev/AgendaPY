let mostraDiaSemana = document.querySelector(".mostraDiaSemana");

let divDias = document.querySelector(".dias-calendario");

let diaSemana = document.querySelector(".dia-semana");

let diaCima = document.querySelector(".mostraDia");

let mesCima = document.querySelector(".mostraMes");

let anoCima = document.querySelector(".mostraAno");

let anoCalendario = document.querySelector(".anoCalendario");

let agendaDiv = document.querySelector(".agenda-horarios");

let diaAgenda = document.querySelector(".dia-agenda");

let meses = [
  "Janeiro",
  "Fevereiro",
  "Março",
  "Abril",
  "Maio",
  "Junho",
  "Julho",
  "Agosto",
  "Setembro",
  "Outubro",
  "Novembro",
  "Dezembro",
];

let diasSemana = [
  "Domingo",
  "Segunda-feira",
  "Terça-feira",
  "Quarta-feira",
  "Quinta-feira",
  "Sexta-feira",
  "Sábado",
];

let diasAtivos = document.querySelectorAll(".dia");

//Pego a data atual sem formatar
const data = new Date();
let datas = {
  //Uso a data atual e pego o dia
  diaAtual: String(data.getDate()).padStart(2, "0"),

  //Esse nao altero no calendario(Usado para condicoes)
  mesAtual: data.getMonth() + 1,

  //Esse nao altero no calendario(Usado para condicoes)
  anoAtual: data.getFullYear(),

  //Uso a data atual e pego o mes
  //Somo um no mes pois ele comeca do 0 (janeiro = 0)
  mes: data.getMonth() + 1,
  //Uso a data atual e pego o ano
  ano: data.getFullYear(),
};

//Adiciona os dias no html
function mostraDias(diaX) {
  //Pego o ultimo dia do mes
  //Zero do proximo mes e o ultimo dia do anterior
  let ultimoDia = new Date(datas.ano, datas.mes, 0).getDate();

  //pego a data e o get day retorna o dia da semana(0 = domingo)
  let primeiroDia = new Date(datas.ano, datas.mes - 1, 1).getDay();

  //Mostra os dias do mes
  for (let i = 1; i <= primeiroDia; i++) {
    divDias.innerHTML += `<div class = "diaVazio"></div>`;
  }
  for (let i = 1; i <= ultimoDia; i++) {
    divDias.innerHTML += `<div class="dia" data-data="${i}/${String(datas.mes).padStart(2, "0")}/${datas.ano}" data-dia = "${i}">${i} </div>`;
  }

  //Atualiza dados em cima do calendario
  mesCima.innerHTML = meses[datas.mes - 1];
  mesCima.dataset.mesCima = meses[datas.mes - 1];

  anoCima.innerHTML = datas.ano;
  anoCima.dataset.anoCima = datas.ano;
  anoCalendario.innerHTML = `${meses[datas.mes - 1]} ${datas.ano}`;
  //Atualizo a lista dos dias dos meses
  diasAtivos = document.querySelectorAll(".dia");

  //Se o calendario estiver no mes e ano atual marco o dia atual
  if (
    datas.mesAtual - 1 == meses.indexOf(mesCima.dataset.mesCima) &&
    anoCima.dataset.anoCima == datas.anoAtual
  ) {
    diaCima.textContent = diaX;
    diaCima.dataset.diaCima = diaX;
  }
  //Senao dia 1
  else {
    diaCima.textContent = 1;
    diaCima.dataset.diaCima = "01";
  }

  //Percorro todos para pegar o clicado
  diasAtivos.forEach((dia) => {
    //Quando chegar no dia atual coloca ele ativo

    if ("0" + dia.dataset.dia === diaCima.dataset.diaCima) {
      dia.classList.add("ativo");
    }

    //Quando clicado tiro a classe de todos
    dia.addEventListener("click", () => {
      diasAtivos.forEach((diaRemove) => {
        diaRemove.classList.remove("ativo");
      });

      //Atualizo o dia em cima para o texto do clicado
      diaCima.innerHTML = dia.dataset.dia;
      diaCima.dataset.diaCima = dia.dataset.dia;

      //Me retorna o dia da semana atual
      let diaSemanaAtual = new Date(
        datas.ano,
        datas.mes - 1,
        dia.dataset.dia,
      ).getDay();

      mostraDiaSemana.innerHTML = diasSemana[diaSemanaAtual];
      diaSemana.innerHTML = `${diasSemana[diaSemanaAtual]}, ${dia.dataset.dia} de ${mesCima.dataset.mesCima}`;

      //Envio o dia clicado para o back
      fetch("/agendar/calendario", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: dia.dataset.data,
          idFuncionario: idFuncionario,
        }),
      })
        .then((resposta) => resposta.json()) // converte para JSON
        .then((dados) => {
          agendaDiv.innerHTML = "";
          mostrarAgenda(dados);
        });

      //Adiciono apenas no clicado
      dia.classList.add("ativo");
    });
  });
}

function somaSubtrai(sinal) {
  //Se o mes for 12 e o usuario pedir para somar um ano volta para mes 1
  if (sinal === -1 && datas.mes === 1) {
    datas.mes = 12;
    datas.ano -= 1;
  } else if (sinal === +1 && datas.mes === 12) {
    datas.mes = 1;
    datas.ano += 1;
  } else {
    datas.mes += sinal;
  }
  //Limpo a div dias
  divDias.innerHTML = "";

  //Mostro o mes atualizado na tela
  mostraDias(datas.diaAtual);

  document.querySelector(".dias-calendario .ativo").click();
}

function hoje() {
  datas.ano = datas.anoAtual;
  datas.mes = datas.mesAtual;
  divDias.innerHTML = "";
  mostraDias(datas.diaAtual);
  document.querySelector(".dias-calendario .ativo").click();
}

function mostrarAgenda(dados) {
  let dataDiaAtivo = document.querySelector(".dia.ativo").dataset.data;
  dados.forEach((dado, i) => {
    if (dado.status == "Livre") {
      agenda = {
        status: dado.status,
        horario: dado.hora,
        dia: dado.dia,
      };
      agendaDiv.innerHTML += `<div class="horarioTudo">
      <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">${agenda.horario}</div>
      <div class="status" >
        <span>Horário livre</span>
        <button class ="botaoAgenda" data-hora="${agenda.horario}" data-status = "${agenda.status}" data-data = "${dataDiaAtivo}">+</button>
      </div>
    </div>`;
    } else {
      agenda = {
        concluido: dado.status,
        valorPago: dado.valorPago,
        formaPagamento: dado.formaPagamento,
        status: dado.status,
        horario: dado.hora,
        servico: dado.servico,
        cliente: dado.cliente,
        profissional: dado.profissional,
      };
      if (agenda.valorPago && agenda.formaPagamento) {
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
      } else {
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
    }
  });
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
                idFuncionario: idFuncionario,
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

function funcionarioId() {
  //Pego a lista de funcionarios
  let funcionarios = document.querySelectorAll(".funcionario");

  //Percorro para deixar ativado o funcionario atual
  funcionarios.forEach((funcionario) => {
    if (idFuncionario == funcionario.dataset.id) {
      funcionario.classList.add("ativo");
    }
  });

  //Pego o elemento clicado
  funcionarios.forEach((funcionario) => {
    funcionario.addEventListener("click", function pegaId() {
      //Quando clicado removo a classe ativo de todos
      funcionarios.forEach((funcionario) => {
        funcionario.classList.remove("ativo");
      });

      //Atualizo o idFuncionario para o clicado
      idFuncionario = funcionario.dataset.id;

      //Coloco a classe ativo no clicado
      funcionario.classList.add("ativo");

      //Simulo o click para atualizar
      document.querySelector(".dias-calendario .ativo").click();
    });
  });
}

function abreModal(nome) {
  document.querySelector(`.modal-${nome}`).showModal();
}

function fechaModal(nome) {
  document.querySelector(`.modal-${nome}`).close();
}

function buscarNome() {
  let inputNome = document.querySelector(".nomeCliente");
  let inputNumero = document.querySelector(".numeroCliente");
  let listaNomes = document.querySelector(".lista-nomes");
  let nomesLista = document.querySelectorAll(".nome-lista");

  inputNome.addEventListener("input", function pegaNome() {
    fetch("/agendar/buscaNome", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nomeCliente: inputNome.value,
      }),
    })
      .then((resposta) => resposta.json()) // converte para JSON
      .then((clientes) => {
        listaNomes.innerHTML = "";
        clientes.forEach((cliente) => {
          listaNomes.innerHTML += `<li class="nome-lista" data-nome="${cliente[1]}" data-numero="${cliente[2]}">${cliente[1]}</li>`;
        });
        if (inputNome.value == "") {
          listaNomes.innerHTML = "";
        }
        nomesLista = document.querySelectorAll(".nome-lista");
        nomesLista.forEach((nomeLista) => {
          nomeLista.addEventListener("click", function colocaNumero() {
            nomeSelecionado = nomeLista.dataset.nome;
            numeroSelecionado = nomeLista.dataset.numero;
            inputNome.value = nomeSelecionado;
            inputNumero.value = numeroSelecionado;
            listaNomes.innerHTML = "";
          });
        });
      });
  });
}

function buscarServico() {
  let inputServico = document.querySelector(".servicoCliente");
  let listaServicos = document.querySelector(".lista-servicos");
  let servicosLista = document.querySelectorAll(".servico-lista");
  let listaServicosSelecionados = document.querySelector(
    ".servicos-selecionados",
  );

  inputServico.addEventListener("input", function pegaServico() {
    fetch("/agendar/buscaServico", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nomeServico: inputServico.value,
      }),
    })
      .then((resposta) => resposta.json()) // converte para JSON
      .then((servicos) => {
        console.log(servicos)
        listaServicos.innerHTML = "";
        servicos.forEach((servico) => {
          listaServicos.innerHTML += `<li class="servico-lista" data-servico="${servico[1]}"> ${servico[1]} </li>`;
        });
        if (inputServico.value == "") {
          listaServicos.innerHTML = "";
        }
        servicosLista = document.querySelectorAll(".servico-lista");
        servicosLista.forEach((servicoLista) => {
          servicoLista.addEventListener("click", function colocaServico() {
            servicoSelecionado = servicoLista.dataset.servico;
            valorServicoSelecionado = servicoLista.dataset.servicovalor;
            listaServicosSelecionados.innerHTML += `<li class="servico-lista-ativo" data-servicoSelecionado="${servicoSelecionado}">
  <span>${servicoSelecionado}</span>
    <div data-servicoSelecionado="${servicoSelecionado}" class="btn-servicos">
    <svg width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0.338429 0.338429C0.789667 -0.11281 1.52129 -0.11281 1.97248 0.338429L5.00708 3.37307L8.04168 0.338459C8.49293 -0.112779 9.22443 -0.112779 9.67568 0.338459C10.1269 0.789698 10.1269 1.52132 9.67568 1.97263L6.64123 5.00708L9.67568 8.04152C10.1269 8.49277 10.1269 9.22443 9.67568 9.67568C9.22443 10.1269 8.49277 10.1269 8.04152 9.67568L5.00708 6.64123L1.97263 9.67568C1.52132 10.1269 0.789698 10.1269 0.338459 9.67568C-0.112779 9.22443 -0.112779 8.49293 0.338459 8.04168L3.37307 5.00708L0.338429 1.97248C-0.11281 1.52129 -0.11281 0.789667 0.338429 0.338429Z" fill="#B8B1AE" />
      </svg>
    </div>
</li>`;
            listaServicos.innerHTML = "";
            inputServico.value = "";
            let servicosAtivos = document.querySelectorAll(
              ".servico-lista-ativo",
            );
            excluiServico(servicosAtivos);
            agendar(servicosAtivos);
          });
        });
      });
  });
}

function excluiServico(servicosListaAtivo) {
  let botoesExcluirServico = document.querySelectorAll(".btn-servicos");
  botoesExcluirServico.forEach((botao) => {
    botao.addEventListener("click", function removerServico() {
      nomeServico = botao.dataset.servicoselecionado;
      servicosListaAtivo.forEach((servicoSelecionado) => {
        if (servicoSelecionado.dataset.servicoselecionado === nomeServico) {
          servicoSelecionado.remove();
        }
      });
    });
  });
}

function agendar(servicosAtivos) {
  // Botao de envio
  let botaoAgendar = document.querySelector("#btnAgendar");

  //Inputs
  let inputNome = document.querySelector(".nomeCliente");
  let inputNumero = document.querySelector(".numeroCliente");
  let inputHora = document.querySelector(".horaCliente");
  let inputData = document.querySelector(".dataCliente");
  let form = document.querySelector("#formAgendamento");
  botaoAgendar.addEventListener("click", function agendamento(event) {
    event.preventDefault();
    // Limpa aviso anterior do modal de agendamento
    document.querySelector(".modal-agendamento .aviso-modal").innerHTML = "";

    if (!form.checkValidity()) {
      form.reportValidity(); // mostra as mensagens de erro do HTML
      return;
    }
    //Lista de servicos, dentro do addEvent para zerar sempre que clicado
    let nomeDosServicos = [];

    //Coloco os nomes dos servicos na lista
    servicosAtivos.forEach((servicoSelecionado) => {
      nomeDosServicos.push(servicoSelecionado.dataset.servicoselecionado);
    });

    // Se nenhuma opção de serviço foi selecionada, exibe mensagem de erro no modal e impede o envio
    if (nomeDosServicos.length === 0) {
      document.querySelector(".modal-agendamento .aviso-modal").innerHTML =
        "Selecione pelo menos um serviço para agendar";
      return;
    }

    //Enviar via API para py
    fetch("/agendar", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idFuncionario: idFuncionario,
        nomesServicos: nomeDosServicos, //Mudar para lista pegando o nome dos servicos,
        nomeCliente: inputNome.value,
        numeroCliente: inputNumero.value,
        horaAgendamento: inputHora.value,
        dataAgendamento: inputData.value,
      }),
    })
      .then((resposta) => resposta.json()) // converte para JSON
      .then((dados) => {
        if (dados["mensagem"] == true) {
          window.location.reload();
          document.querySelector(".aviso-modal").innerHTML = dados["mensagem"];
        }
      });
  });
}

function atualizarPag(ocupados) {
  let dataPag;
  let horaPag;
  let botaoEnviar = document.querySelector("#btnAtualizar");

  //Pego a data e hora do clicado(So olho para os ocupados)

  ocupados.forEach((ocupado) => {
    ocupado.addEventListener("click", function formaPg() {
      if (ocupado.classList.contains("ativoPag")) {
        let informacoes = {
          data: ocupado.dataset.data,
          hora: ocupado.dataset.hora,
          servicos: ocupado.dataset.servico,
          valorPago: ocupado.dataset.valorpago,
          formaPagamento: ocupado.dataset.formapag,
        };
        abreModal("detalhes");
        document.querySelector(".data-detalhes").innerHTML = informacoes.data;
        document.querySelector(".hora-detalhes").innerHTML = informacoes.hora;
        document.querySelector(".servico-detalhes").innerHTML =
          informacoes.servicos;
        document.querySelector(".pagamento-detalhes").innerHTML =
          informacoes.formaPagamento;
        document.querySelector(".valor-detalhes").innerHTML =
          informacoes.valorPago;
        return;
      } else {
        abreModal("valor");
        dataPag = ocupado.dataset.data;
        horaPag = ocupado.dataset.hora;
      }
    });
  });

  document.querySelectorAll('input[name="formaPag"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      document.querySelectorAll(".aviso-modal")[1].innerHTML = "";
    });
  });
  //Quando enviar pego todos os valores
  botaoEnviar.addEventListener("click", function envio() {
    let inputValor = document.querySelector(".valorAgendamento");
    let formaPagamento = document.querySelector(
      'input[name="formaPag"]:checked',
    );
    if (!formaPagamento) {
      document.querySelectorAll(".aviso-modal")[1].innerHTML =
        "Selecione uma forma de pagamento";
      return;
    }

    //Envio para o JS
    fetch("/agendar/atualizarPg", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        idFuncionario: idFuncionario,
        valorAgendamento: inputValor.value,
        formaPagamento: formaPagamento.id,
        dataAgendamento: dataPag,
        horaAgendamento: horaPag,
      }),
    })
      .then((resposta) => resposta.json()) // converte para JSON
      .then((dados) => {
        if (dados["mensagem"] == true) {
          window.location.reload();
        }
        console.log(dados["mensagem"]);
      });
  });
}

buscarServico();
buscarNome();
hoje();
funcionarioId();

// ==================== CÓDIGO DO FILTRO DA AGENDA ====================

// Obtém o período do dia correspondente ao horário informado
// Períodos: manha (antes das 12h), tarde (das 12h às 17h59) e noite (a partir das 18h)
function obterPeriodo(horario) {
  // Extrai apenas a hora e converte para número inteiro
  const hora = parseInt(horario.split(":")[0], 10);

  // Retorna o período com base na hora
  if (hora < 12) {
    return "manha";
  } else if (hora < 18) {
    return "tarde";
  } else {
    return "noite";
  }
}

// Filtra a exibição dos horários na tela com base no período selecionado no dropdown
function filtrarAgenda() {
  // Captura o elemento do dropdown
  const dropdown = document.querySelector(".drop-down-filtro");
  // Obtém o filtro atualmente selecionado (padrão: "tudo")
  const filtroAtivo = dropdown.dataset.filtro || "tudo";
  // Pega todos os cards de agendamento na tela
  const horarios = document.querySelectorAll(".horarioTudo");

  // Percorre cada elemento de horário para aplicar o filtro
  horarios.forEach((bloco) => {
    // Localiza o elemento que possui a hora do agendamento
    const elementoHora = bloco.querySelector(".horario");
    if (!elementoHora) return;

    // Pega o valor da hora a partir do atributo data-hora ou do conteúdo de texto
    const horaTexto =
      elementoHora.dataset.hora || elementoHora.textContent.trim();
    // Identifica o período correspondente (manha, tarde ou noite)
    const periodo = obterPeriodo(horaTexto);

    // Se o filtro for "tudo" ou bater com o período do agendamento, mostra o card, senão esconde
    if (filtroAtivo === "tudo" || periodo === filtroAtivo) {
      bloco.style.display = ""; // Restaura a exibição padrão (grid/flex/etc)
    } else {
      bloco.style.display = "none"; // Oculta o card
    }
  });
}

// Inicializa o funcionamento e a interatividade do dropdown de filtros
function inicializarFiltro() {
  // Captura o container do dropdown e a lista de opções
  const dropdown = document.querySelector(".drop-down-filtro");
  const opcoesLista = document.querySelector(".opcoes-filtro");
  const spanFiltro = dropdown.querySelector("span");

  // Abre ou fecha o menu de opções ao clicar no dropdown
  dropdown.addEventListener("click", (evento) => {
    // Evita propagação para que o evento de fechar ao clicar fora não seja disparado imediatamente
    evento.stopPropagation();
    opcoesLista.classList.toggle("ativo");
  });

  // Adiciona evento de clique para cada opção da lista
  opcoesLista.querySelectorAll("li").forEach((opcao) => {
    opcao.addEventListener("click", (evento) => {
      // Impede que o clique na opção abra/feche o dropdown de forma errada
      evento.stopPropagation();

      // Atualiza o texto visual do dropdown com a opção escolhida
      spanFiltro.textContent = opcao.textContent;
      // Define a opção no atributo customizado data-filtro
      dropdown.dataset.filtro = opcao.dataset.opcao;

      // Fecha a lista de opções
      opcoesLista.classList.remove("ativo");

      // Executa a filtragem dos horários na tela
      filtrarAgenda();
    });
  });

  // Fecha a lista de opções se o usuário clicar em qualquer outro lugar da página
  document.addEventListener("click", () => {
    opcoesLista.classList.remove("ativo");
  });
}

// Salva a referência da função mostrarAgenda original para não interferir na sua implementação
const mostrarAgendaOriginal = mostrarAgenda;

// Sobrescrevemos mostrarAgenda para executar a lógica original e depois aplicar o filtro ativo
mostrarAgenda = function (dados) {
  // Executa a função original exatamente como foi criada sem interferir no seu funcionamento
  mostrarAgendaOriginal(dados);

  // Aplica o filtro selecionado nos novos elementos recém-renderizados
  filtrarAgenda();
};

// Executa a inicialização do filtro dropdown ao carregar a página
inicializarFiltro();

// ==================== ATUALIZAÇÃO DO TÍTULO DA AGENDA ====================

// Função simples para atualizar o título da agenda com o nome do profissional selecionado
function atualizarTituloAgenda() {
  // Pega o elemento do título da agenda no HTML
  const agendaTitulo = document.querySelector(".agenda-titulo");

  // Pega todos os cards dos profissionais/funcionários
  const funcionarios = document.querySelectorAll(".funcionario");

  // Percorre a lista de funcionários cadastrados na tela
  funcionarios.forEach((funcionario) => {
    // Se for o funcionário ativo no carregamento inicial (verificando o ID)
    if (funcionario.dataset.id == idFuncionario) {
      // Define o título inicial usando o atributo data-nome do profissional
      agendaTitulo.textContent = `Agenda de ${funcionario.dataset.nome}`;
    }

    // Adiciona o ouvinte de clique em cada card de funcionário para atualizar o título dinamicamente
    funcionario.addEventListener("click", () => {
      // Quando clicado, atualiza o texto do título para o nome do profissional selecionado
      agendaTitulo.textContent = `Agenda de ${funcionario.dataset.nome}`;
    });
  });
}

// Executa a inicialização da atualização do título da agenda
atualizarTituloAgenda();
