import { SECOES_CLIENTE } from "./data/anamnese_perguntas.js";
import { renderizarSecao, lerRespostasSecao, ativarDependencias } from "./ui/anamnese_campos.js";
import { enviarFicha } from "./api/anamnese_api.js";

const fundoCarregamento = document.querySelector(".anamnese-loading-fundo");
const logoCarregamento = document.querySelector(".anamnese-loading-logo");

if (fundoCarregamento && logoCarregamento) {
  setTimeout(() => {
    fundoCarregamento.classList.add("saindo");
    logoCarregamento.classList.add("no-canto");
  }, 900);

  fundoCarregamento.addEventListener("transitionend", () => fundoCarregamento.remove(), { once: true });
}

const containerEtapas = document.querySelector(".anamnese-etapas");
const barraPreenchida = document.querySelector(".anamnese-progresso-preenchido");
const progressoTexto = document.querySelector(".anamnese-progresso-texto");
const btnVoltar = document.querySelector(".anamnese-btn-voltar");
const btnAvancar = document.querySelector(".anamnese-btn-avancar");
const form = document.querySelector("#formAnamnesePublica");
const aviso = document.querySelector(".anamnese-aviso");
const cardFormulario = document.querySelector(".anamnese-form-card");
const telaSucesso = document.querySelector(".anamnese-sucesso");
const topoFormulario = document.querySelector(".anamnese-form-topo");

const totalEtapas = SECOES_CLIENTE.length + 1;
let etapaAtual = 0;
let enviando = false;

const estado = {
  nome: "",
  numero: "",
  respostas: {},
};

function renderizarEtapaIdentificacao() {
  containerEtapas.innerHTML = `
    <fieldset class="anamnese-secao">
      <legend>Vamos começar</legend>
      <label class="campo-anamnese">
        <span>Nome completo</span>
        <input type="text" id="nomeAnamnese" value="${estado.nome}" required>
      </label>
      <label class="campo-anamnese">
        <span>Número (WhatsApp)</span>
        <input type="text" id="numeroAnamnese" value="${estado.numero}" required>
      </label>
    </fieldset>`;

  if (window.Cleave) {
    new window.Cleave("#numeroAnamnese", {
      delimiters: ["(", ") ", "-"],
      blocks: [0, 2, 5, 4],
      numericOnly: true,
    });
  }
}

function renderizarEtapa() {
  aviso.innerHTML = "";

  if (etapaAtual === 0) {
    renderizarEtapaIdentificacao();
  } else {
    const secao = SECOES_CLIENTE[etapaAtual - 1];
    containerEtapas.innerHTML = renderizarSecao(secao, estado.respostas[secao.id]);
    ativarDependencias(containerEtapas, secao);
  }

  btnVoltar.hidden = etapaAtual === 0;
  btnAvancar.innerText = etapaAtual === totalEtapas - 1 ? "Enviar" : "Próximo";

  const progresso = Math.round(((etapaAtual + 1) / totalEtapas) * 100);
  barraPreenchida.style.width = `${progresso}%`;
  progressoTexto.innerText = `Etapa ${etapaAtual + 1} de ${totalEtapas}`;

  cardFormulario.scrollIntoView({ block: "start", behavior: "smooth" });
}

function lerEtapaAtual() {
  if (etapaAtual === 0) {
    estado.nome = document.querySelector("#nomeAnamnese").value.trim();
    estado.numero = document.querySelector("#numeroAnamnese").value.trim();
    return;
  }

  const secao = SECOES_CLIENTE[etapaAtual - 1];
  estado.respostas[secao.id] = lerRespostasSecao(containerEtapas, secao);
}

async function enviar() {
  if (enviando) return;
  enviando = true;
  btnAvancar.disabled = true;

  try {
    const resultado = await enviarFicha(estado.nome, estado.numero, estado.respostas);

    if (resultado.sucesso) {
      form.hidden = true;
      topoFormulario.hidden = true;
      document.querySelector(".anamnese-form-nav").hidden = true;
      document.querySelector(".anamnese-progresso").hidden = true;
      telaSucesso.hidden = false;
    } else {
      aviso.innerHTML = resultado.mensagem || "Não foi possível enviar a ficha.";
    }
  } catch (err) {
    aviso.innerHTML = "Erro de conexão. Tente novamente.";
  } finally {
    enviando = false;
    btnAvancar.disabled = false;
  }
}

btnAvancar.addEventListener("click", async () => {
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  lerEtapaAtual();

  if (etapaAtual === totalEtapas - 1) {
    await enviar();
    return;
  }

  etapaAtual++;
  renderizarEtapa();
});

btnVoltar.addEventListener("click", () => {
  lerEtapaAtual();
  etapaAtual--;
  renderizarEtapa();
});

renderizarEtapa();
