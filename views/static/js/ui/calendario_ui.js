export function mostrar_dias_calendario(
  div_dias,
  primeiro_dia,
  ultimo_dia,
  mes,
  ano,
) {
  //Mostra os dias do mes
  for (let i = 1; i <= primeiro_dia; i++) {
    div_dias.innerHTML += `<div class = "diaVazio"></div>`;
  }
  for (let i = 1; i <= ultimo_dia; i++) {
    div_dias.innerHTML += `<div class="dia" data-data="${i}/${String(mes).padStart(2, "0")}/${ano}" data-dia = "${i}">${i} </div>`;
  }
}

export function atualiza_cabecalho_calendario(
  mes_cima,
  ano_cima,
  ano_calendario_cima,
  meses,
  mes,
  ano,
) {
  //Atualiza dados em cima do calendario
  mes_cima.innerHTML = meses[mes - 1];
  mes_cima.dataset.mesCima = meses[mes - 1];

  ano_cima.innerHTML = ano;
  ano_cima.dataset.anoCima = ano;

  ano_calendario_cima.innerHTML = `${meses[mes - 1]} ${ano}`;
}

export function atualizar_dia_selecionado(
  diaCima,
  mostraDiaSemana,
  diaSemana,
  diasSemana,
  dia,
  mes,
  anoCima,
  mesNumero
) {
  diaCima.textContent = dia;
  const indice = new Date(
    Number(anoCima.dataset.anoCima),
    mesNumero - 1,
    Number(dia),
  ).getDay();
  mostraDiaSemana.textContent = diasSemana[indice];

  diaSemana.textContent = `${diasSemana[indice]}, ${dia} de ${mes}`;
}

export function marcar_dia_ativo(dias, diaSelecionado) {
  dias.forEach((d) => d.classList.remove("ativo"));

  diaSelecionado.classList.add("ativo");
}

export function obter_dias() {
  return document.querySelectorAll(".dia");
}

export function limpar_agenda(agendaDiv) {
  agendaDiv.innerHTML = "";
}
