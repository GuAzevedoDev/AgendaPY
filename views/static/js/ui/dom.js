export let mostraDiaSemana = document.querySelector(".mostraDiaSemana");

export let divDias = document.querySelector(".dias-calendario");

export let diaSemana = document.querySelector(".dia-semana");

export let diaCima = document.querySelector(".mostraDia");

export let mesCima = document.querySelector(".mostraMes");

export let anoCima = document.querySelector(".mostraAno");

export let anoCalendario = document.querySelector(".anoCalendario");

export let agendaDiv = document.querySelector(".agenda-horarios");

export let diaAgenda = document.querySelector(".dia-agenda");

export let inputNome = document.querySelector(".nomeCliente");
export let inputNumero = document.querySelector(".numeroCliente");
export let listaNomes = document.querySelector(".lista-nomes");
export let nomesLista = document.querySelectorAll(".nome-lista");

export let meses = [
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

export let diasSemana = [
  "Domingo",
  "Segunda-feira",
  "Terça-feira",
  "Quarta-feira",
  "Quinta-feira",
  "Sexta-feira",
  "Sábado",
];

export let diasAtivos = document.querySelectorAll(".dia");

//Pego a data atual sem formatar
export const data = new Date();
export let datas = {
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

//Pego o ultimo dia do mes
//Zero do proximo mes e o ultimo dia do anterior
export let ultimoDia = new Date(datas.ano, datas.mes, 0).getDate();

//pego a data e o get day retorna o dia da semana(0 = domingo)
export let primeiroDia = new Date(datas.ano, datas.mes - 1, 1).getDay();
