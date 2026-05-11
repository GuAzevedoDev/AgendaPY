let divDias = document.querySelector(".dias-calendario");

let diaCima = document.querySelector(".mostraDia");

let mesCima = document.querySelector(".mostraMes");

let anoCima = document.querySelector(".mostraAno");

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

      //Envio o dia clicado para o back
      fetch("/calendario", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: dia.dataset.data }),
      })
        .then((resposta) => resposta.json()) // converte para JSON
        .then((dados) => {
          // dados prontos
          console.log(dados);
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
}

function hoje() {
  datas.ano = datas.anoAtual;
  datas.mes = datas.mesAtual;

  divDias.innerHTML = "";
  mostraDias(datas.diaAtual);

  document.querySelector(".ativo").click()
}

function amanha() {
  datas.ano = datas.anoAtual;
  datas.mes = datas.mesAtual;

  divDias.innerHTML = "";
  mostraDias(+datas.diaAtual + 1);

  document.querySelector(".ativo").click()
}

hoje()

