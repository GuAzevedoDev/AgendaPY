import * as calendarioUI from "./ui/calendario_ui.js";
import * as agendaUI from "./ui/agenda_ui.js";
import * as agendaApi from "./api/agenda_api.js";
import * as dom from "./ui/dom.js";

export async function mostrarAgenda() {

    calendarioUI.mostrar_dias_calendario(
        dom.divDias,
        dom.primeiroDia,
        dom.ultimoDia,
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

    const dias = calendarioUI.obter_dias();

    dias.forEach(dia => {

        dia.addEventListener("click", async () => {

            calendarioUI.marcar_dia_ativo(dias, dia);

            const agenda = await agendaApi.enviar_dia_clicado(
                dia.dataset.data,
                id_funcionario
            );

            calendarioUI.limpar_agenda(dom.agendaDiv);

            agendaUI.mostrar_agenda_horarios(agenda);

        });

    });

}