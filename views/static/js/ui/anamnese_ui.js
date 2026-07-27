import { SECOES_ANAMNESE } from "../data/anamnese_perguntas.js";
import { renderizarSecao, lerRespostasSecao, ativarDependencias } from "./anamnese_campos.js";
import { escapeHtml } from "../utils/html.js";

export function renderizarTabela(fichas, corpoTabela) {
  corpoTabela.innerHTML = fichas
    .map(
      (ficha) => `
      <tr data-id="${ficha.id}">
        <td>${ficha.id}</td>
        <td>${escapeHtml(ficha.nome)}</td>
        <td>${escapeHtml(ficha.numero)}</td>
        <td>${ficha.data}</td>
        <td>${renderizarStatusAvaliacao(ficha.avaliacao_concluida)}</td>
        <td>
          <button type="button" class="btn-ver-ficha" data-id="${ficha.id}">Ver / editar</button>
          <button type="button" class="btn-excluir-ficha" data-id="${ficha.id}">Excluir</button>
        </td>
      </tr>`,
    )
    .join("");
}

function renderizarStatusAvaliacao(concluida) {
  if (concluida) {
    return `<span class="status-badge concluido">Avaliação concluída</span>`;
  }
  return `<span class="status-badge pendente">Pendente</span>`;
}

export function atualizarContador(total, elementoContador) {
  elementoContador.innerText = total;
}

export function mostrarEstadoVazio(vazio, wrapperTabela, elementoVazio) {
  wrapperTabela.hidden = vazio;
  elementoVazio.hidden = !vazio;
}

export function preencherModal(ficha, elementos) {
  elementos.inicial.innerText = ficha.nome ? ficha.nome[0].toUpperCase() : "-";
  elementos.nome.innerText = ficha.nome;
  elementos.numero.innerText = ficha.numero;

  elementos.secoes.innerHTML = SECOES_ANAMNESE.map((secao) =>
    renderizarSecao(secao, ficha.respostas ? ficha.respostas[secao.id] : {}),
  ).join("");

  SECOES_ANAMNESE.forEach((secao) => ativarDependencias(elementos.secoes, secao));
}

export function lerRespostasModal(containerSecoes) {
  const respostas = {};

  SECOES_ANAMNESE.forEach((secao) => {
    const fieldset = containerSecoes.querySelector(`[data-secao-id="${secao.id}"]`);
    if (fieldset) {
      respostas[secao.id] = lerRespostasSecao(fieldset, secao);
    }
  });

  return respostas;
}
