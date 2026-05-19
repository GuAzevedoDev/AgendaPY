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
    diaCima.dataset.diaCima = 1;
  }

  //Percorro todos para pegar o clicado
  diasAtivos.forEach((dia) => {
    //Quando chegar no dia atual coloca ele ativo
    if (dia.dataset.dia === diaCima.dataset.diaCima) {
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
      fetch("/calendario", {
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
  dados.forEach((dado, i) => {
    if (dado.status == "Livre") {
      agenda = {
        status: dado.status,
        horario: dado.hora,
        dia: dado.dia,
      };
      agendaDiv.innerHTML += `<div class="horarioTudo">
      <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
      <div class="status" data-hora="${agenda.horario}" data-status = "${agenda.status}"><button>+</button></div>
    </div>`;
    } else {
      agenda = {
        status: dado.status,
        horario: dado.hora,
        servico: dado.servico,
        cliente: dado.cliente,
        profissional: dado.profissional,
      };
      agendaDiv.innerHTML += `<div class="horarioTudo">
      <div class="horario" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.horario}</div>
      <div class="servico" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.servico}</div>
      <div class="cliente" data-hora="${agenda.horario}" data-status = "${agenda.status}">${agenda.cliente}</div>
    </div>`;
    }
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

function abreModal() {
  document.querySelector(".modal-agendamento").showModal();
}

function fechaModal() {
  document.querySelector(".modal-agendamento").close();
}

function buscarNome() {
  let inputNome = document.querySelector(".nomeCliente");
  let inputNumero = document.querySelector(".numeroCliente");
  let listaNomes = document.querySelector(".lista-nomes");
  let nomesLista = document.querySelectorAll(".nome-lista");

  inputNome.addEventListener("input", function pegaNome() {
    fetch("/buscaNome", {
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
    fetch("/buscaServico", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nomeServico: inputServico.value,
      }),
    })
      .then((resposta) => resposta.json()) // converte para JSON
      .then((servicos) => {
        listaServicos.innerHTML = "";
        servicos.forEach((servico) => {
          listaServicos.innerHTML += `<li class="servico-lista" data-servico="${servico[1]}" data-servicovalor="${servico[3]}"> ${servico[1]} </li>`;
        });
        if (inputServico.value == "") {
          listaServicos.innerHTML = "";
        }
        servicosLista = document.querySelectorAll(".servico-lista");
        servicosLista.forEach((servicoLista) => {
          servicoLista.addEventListener("click", function colocaServico() {
            servicoSelecionado = servicoLista.dataset.servico;
            valorServicoSelecionado = servicoLista.dataset.servicovalor;
            listaServicosSelecionados.innerHTML += `<li class="servico-lista-ativo" data-servicoSelecionadoValor="${valorServicoSelecionado}" data-servicoSelecionado="${servicoSelecionado}"> <span>${servicoSelecionado}</span>
              <div><span>R$${valorServicoSelecionado}</span> <div data-servicoSelecionado="${servicoSelecionado}" class="btn-servicos"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0.338429 0.338429C0.789667 -0.11281 1.52129 -0.11281 1.97248 0.338429L5.00708 3.37307L8.04168 0.338459C8.49293 -0.112779 9.22443 -0.112779 9.67568 0.338459C10.1269 0.789698 10.1269 1.52132 9.67568 1.97263L6.64123 5.00708L9.67568 8.04152C10.1269 8.49277 10.1269 9.22443 9.67568 9.67568C9.22443 10.1269 8.49277 10.1269 8.04152 9.67568L5.00708 6.64123L1.97263 9.67568C1.52132 10.1269 0.789698 10.1269 0.338459 9.67568C-0.112779 9.22443 -0.112779 8.49293 0.338459 8.04168L3.37307 5.00708L0.338429 1.97248C-0.11281 1.52129 -0.11281 0.789667 0.338429 0.338429Z" fill="#B8B1AE"/>
</svg>
</div></div>
            </li>`;
            listaServicos.innerHTML = "";
            inputServico.value = "";
            let servicosAtivos = document.querySelectorAll(
              ".servico-lista-ativo",
            );
            excluiServico(servicosAtivos);
            agendar(servicosAtivos)
            calculaTotal(servicosAtivos)
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

  //Lista de servicos
  let nomeDosServicos = [];
  //Inputs
  let inputNome = document.querySelector(".nomeCliente");
  let inputNumero = document.querySelector(".numeroCliente");
  let inputHora = document.querySelector(".horaCliente");
  let inputData = document.querySelector(".dataCliente");

  botaoAgendar.addEventListener("click", function agendamento(event) {
    //Coloco os nomes dos servicos na lista
    servicosAtivos.forEach((servicoSelecionado) => {
      nomeDosServicos.push(servicoSelecionado.dataset.servicoselecionado);
    });

    //Enviar via API para py
    fetch("/agendar", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nomesServicos: nomeDosServicos, //Mudar para lista pegando o nome dos servicos,
        nomeCliente: inputNome.value,
        numeroCliente: inputNumero.value,
        horaAgendamento: inputHora.value,
        dataAgendamento: inputData.value,
      }),
    });
  });
}

function calculaTotal(servicosAtivos){
  let valorHtml = document.querySelector('.valor-total')
  let valorTotal = 0
  servicosAtivos.forEach((servicoSelecionado) => {
      valorDosServicos = servicoSelecionado.dataset.servicoselecionadovalor;
      valorTotal = Number(valorDosServicos) + valorTotal
    });
  valorHtml.innerHTML = `R$${valorTotal}`
}

buscarServico();
buscarNome();
hoje();
funcionarioId();
calculaTotal([])