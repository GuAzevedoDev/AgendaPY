import * as anamneseApi from "../api/anamnese_api.js";
import * as anamneseUi from "../ui/anamnese_ui.js";
import { abreModal } from "../ui/modal_ui.js";

const corpoTabela = document.querySelector(".corpo-tabela-fichas");
const wrapperTabela = document.querySelector(".tabela-fichas");
const elementoVazio = document.querySelector(".fichas-vazio");
const contadorFichas = document.querySelector(".contador-fichas");
const inputBusca = document.querySelector(".busca-ficha");
const dropdownFiltro = document.querySelector(".filtro-anamnese .drop-down-filtro");

const modalElementos = {
  inicial: document.querySelector(".anamnese-inicial"),
  nome: document.querySelector(".anamnese-nome"),
  numero: document.querySelector(".anamnese-numero"),
  secoes: document.querySelector(".anamnese-secoes"),
};
const avisoModal = document.querySelector(".modal-anamnese .aviso-modal");
const btnSalvar = document.querySelector("#btnSalvarAnamnese");

let todasFichas = [];
let fichaAbertaId = null;
let periodoAtivo = "tudo";

export async function iniciarAnamnese() {
  if (!corpoTabela) return;

  await carregarFichas();
  configurarBusca();
  configurarFiltroPeriodo();
  configurarAbrirFicha();
  configurarSalvarFicha();
}

async function carregarFichas() {
  todasFichas = await anamneseApi.mostrarFichas();
  aplicarFiltros();
}

function dentroDoPeriodo(ficha) {
  if (periodoAtivo === "tudo") return true;

  const hoje = new Date();
  const dataFicha = new Date(ficha.data_iso);
  const diffDias = (hoje - dataFicha) / (1000 * 60 * 60 * 24);

  if (periodoAtivo === "semana") return diffDias <= 7;
  if (periodoAtivo === "mes") return diffDias <= 30;
  return true;
}

function aplicarFiltros() {
  const termo = (inputBusca?.value || "").trim().toLowerCase();

  const fichasFiltradas = todasFichas.filter(
    (ficha) => ficha.nome.toLowerCase().includes(termo) && dentroDoPeriodo(ficha),
  );

  anamneseUi.renderizarTabela(fichasFiltradas, corpoTabela);
  anamneseUi.atualizarContador(fichasFiltradas.length, contadorFichas);
  anamneseUi.mostrarEstadoVazio(fichasFiltradas.length === 0, wrapperTabela, elementoVazio);
}

function configurarBusca() {
  if (!inputBusca) return;
  inputBusca.addEventListener("input", aplicarFiltros);
}

function configurarFiltroPeriodo() {
  if (!dropdownFiltro) return;

  const rotulo = dropdownFiltro.querySelector("span");
  const opcoes = dropdownFiltro.querySelectorAll(".opcoes-filtro li");

  opcoes.forEach((opcao) => {
    opcao.addEventListener("click", () => {
      periodoAtivo = opcao.dataset.opcao;
      rotulo.innerText = opcao.innerText;
      aplicarFiltros();
    });
  });
}

function configurarAbrirFicha() {
  corpoTabela.addEventListener("click", async (e) => {
    const botaoExcluir = e.target.closest(".btn-excluir-ficha");
    if (botaoExcluir) {
      if (!confirm("Deseja realmente excluir esta ficha de anamnese?")) return;

      const resultado = await anamneseApi.excluirFicha(botaoExcluir.dataset.id);
      if (resultado.sucesso) {
        await carregarFichas();
      } else {
        alert("Erro ao excluir ficha: " + (resultado.mensagem || "Erro desconhecido"));
      }
      return;
    }

    const botao = e.target.closest(".btn-ver-ficha");
    if (!botao) return;

    if (avisoModal) avisoModal.innerHTML = "";
    const ficha = await anamneseApi.buscarFicha(botao.dataset.id);

    if (ficha.sucesso === false) {
      return;
    }

    fichaAbertaId = ficha.id;
    anamneseUi.preencherModal(ficha, modalElementos);
    abreModal("anamnese");
  });
}

function configurarSalvarFicha() {
  if (!btnSalvar) return;

  btnSalvar.addEventListener("click", async (e) => {
    e.preventDefault();
    if (!fichaAbertaId) return;

    const respostas = anamneseUi.lerRespostasModal(modalElementos.secoes);
    const resultado = await anamneseApi.atualizarFicha(fichaAbertaId, respostas);

    if (resultado.sucesso) {
      await carregarFichas();
      document.querySelector(".modal-anamnese").close();
    } else if (avisoModal) {
      avisoModal.innerHTML = resultado.mensagem || "Não foi possível salvar as alterações.";
    }
  });
}
