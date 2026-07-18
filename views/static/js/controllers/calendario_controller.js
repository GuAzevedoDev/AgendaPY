import * as dom from "../ui/dom.js";
import * as calendarioUI from "../ui/calendario_ui.js";
import { carregarAgendaDoDia } from "./agenda_controller.js";

export function iniciarCalendario() {
  // Bind functions to window so they are globally accessible from inline HTML
  window.somaSubtrai = somaSubtrai;
  window.hoje = hoje;

  recarregarCalendario();
}

export function recarregarCalendario() {
  dom.divDias.innerHTML = "";
  
  const ultimoDia = new Date(dom.datas.ano, dom.datas.mes, 0).getDate();
  const primeiroDia = new Date(dom.datas.ano, dom.datas.mes - 1, 1).getDay();

  calendarioUI.mostrar_dias_calendario(
    dom.divDias,
    primeiroDia,
    ultimoDia,
    dom.datas.mes,
    dom.datas.ano
  );

  calendarioUI.atualiza_cabecalho_calendario(
    dom.mesCima,
    dom.anoCima,
    dom.anoCalendario,
    dom.meses,
    dom.datas.mes,
    dom.datas.ano
  );
  
  configurarDiasListeners();
}

function configurarDiasListeners() {
  const dias = calendarioUI.obter_dias();
  
  const isMesAtual = (dom.datas.mesAtual === dom.datas.mes && dom.datas.anoAtual === dom.datas.ano);
  const diaAlvo = isMesAtual ? String(dom.datas.diaAtual) : "1";
  
  let diaAtivoElement = null;
  dias.forEach((dia) => {
    if (dia.dataset.dia === diaAlvo) {
      diaAtivoElement = dia;
    }
  });

  dias.forEach((dia) => {
    dia.addEventListener("click", async () => {
      calendarioUI.marcar_dia_ativo(dias, dia);
      const diaSelecionado = dia.dataset.dia;
      calendarioUI.atualizar_dia_selecionado(
        dom.diaCima,
        dom.mostraDiaSemana,
        dom.diaSemana,
        dom.diasSemana,
        diaSelecionado,
        dom.meses[dom.datas.mes - 1],
        dom.anoCima,
        dom.datas.mes
      );
      
      // Load the agenda for the clicked day
      await carregarAgendaDoDia(dia.dataset.data);
    });
  });

  if (diaAtivoElement) {
    diaAtivoElement.click();
  }
}

export function somaSubtrai(sinal) {
  if (sinal === -1 && dom.datas.mes === 1) {
    dom.datas.mes = 12;
    dom.datas.ano -= 1;
  } else if (sinal === +1 && dom.datas.mes === 12) {
    dom.datas.mes = 1;
    dom.datas.ano += 1;
  } else {
    dom.datas.mes += sinal;
  }
  
  recarregarCalendario();
}

export function hoje() {
  dom.datas.ano = dom.datas.anoAtual;
  dom.datas.mes = dom.datas.mesAtual;
  recarregarCalendario();
}
