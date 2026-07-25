// Renderizacao e leitura dos campos da ficha de anamnese, compartilhado entre
// o formulario publico em etapas (anamnese_form.js) e o modal de edicao da
// equipe (anamnese_ui.js) — evita duplicar a lista de ~40 perguntas duas vezes.

function campoTexto(pergunta, valorAtual) {
  return `
    <label class="campo-anamnese">
      <span>${pergunta.label}</span>
      <input type="text" name="${pergunta.id}" value="${valorAtual || ""}">
    </label>`;
}

function campoTextarea(pergunta, valorAtual) {
  return `
    <label class="campo-anamnese">
      <span>${pergunta.label}</span>
      <textarea name="${pergunta.id}">${valorAtual || ""}</textarea>
    </label>`;
}

function campoNumero(pergunta, valorAtual) {
  return `
    <label class="campo-anamnese">
      <span>${pergunta.label}</span>
      <input type="number" name="${pergunta.id}" min="${pergunta.min}" max="${pergunta.max}" value="${valorAtual ?? ""}">
    </label>`;
}

function campoRadio(pergunta, valorAtual) {
  const opcoes = pergunta.opcoes
    .map(
      (opcao) => `
      <label class="opcao-radio">
        <input type="radio" name="${pergunta.id}" value="${opcao}" ${valorAtual === opcao ? "checked" : ""}>
        <span>${opcao}</span>
      </label>`,
    )
    .join("");
  return `
    <div class="campo-anamnese">
      <span>${pergunta.label}</span>
      <div class="opcoes-grupo">${opcoes}</div>
    </div>`;
}

function campoCheckbox(pergunta, valorAtual) {
  const selecionados = Array.isArray(valorAtual) ? valorAtual : [];
  const opcoes = pergunta.opcoes
    .map(
      (opcao) => `
      <label class="opcao-checkbox">
        <input type="checkbox" name="${pergunta.id}" value="${opcao}" ${selecionados.includes(opcao) ? "checked" : ""}>
        <span>${opcao}</span>
      </label>`,
    )
    .join("");
  return `
    <div class="campo-anamnese">
      <span>${pergunta.label}</span>
      <div class="opcoes-grupo">${opcoes}</div>
    </div>`;
}

function campoConfirmacao(pergunta, valorAtual) {
  return `
    <label class="opcao-confirmacao">
      <input type="checkbox" name="${pergunta.id}" ${valorAtual ? "checked" : ""} ${pergunta.obrigatorio ? "required" : ""}>
      <span>${pergunta.label}</span>
    </label>`;
}

export function renderizarPergunta(pergunta, valorAtual) {
  let html;
  switch (pergunta.tipo) {
    case "textarea":
      html = campoTextarea(pergunta, valorAtual);
      break;
    case "radio":
      html = campoRadio(pergunta, valorAtual);
      break;
    case "checkbox":
      html = campoCheckbox(pergunta, valorAtual);
      break;
    case "numero":
      html = campoNumero(pergunta, valorAtual);
      break;
    case "confirmacao":
      html = campoConfirmacao(pergunta, valorAtual);
      break;
    default:
      html = campoTexto(pergunta, valorAtual);
  }

  // Campos com "dependeDe" (ex.: "Se sim, especifique") so aparecem quando a
  // pergunta pai estiver respondida "Sim" — ver ativarDependencias().
  if (pergunta.dependeDe) {
    return `<div class="campo-dependente" data-campo-id="${pergunta.id}" data-depende-de="${pergunta.dependeDe}" hidden>${html}</div>`;
  }
  return html;
}

export function renderizarSecao(secao, respostasSecao = {}) {
  const campos = secao.perguntas
    .map((pergunta) => renderizarPergunta(pergunta, respostasSecao[pergunta.id]))
    .join("");

  return `
    <fieldset class="anamnese-secao" data-secao-id="${secao.id}">
      <legend>${secao.titulo}</legend>
      ${campos}
    </fieldset>`;
}

// Liga o show/hide dos campos "dependeDe" ao valor atual da pergunta pai (radio Sim/Não)
// e mantem isso reativo enquanto o usuario muda a resposta. Precisa ser chamada apos
// inserir o HTML da secao no DOM.
export function ativarDependencias(container, secao) {
  secao.perguntas.forEach((pergunta) => {
    if (!pergunta.dependeDe) return;

    const wrapper = container.querySelector(`[data-campo-id="${pergunta.id}"]`);
    if (!wrapper) return;

    const atualizar = () => {
      const marcado = container.querySelector(`input[name="${pergunta.dependeDe}"]:checked`);
      const mostrar = !!marcado && marcado.value === "Sim";
      wrapper.hidden = !mostrar;
      if (!mostrar) {
        const campo = wrapper.querySelector("input, textarea");
        if (campo) campo.value = "";
      }
    };

    container.querySelectorAll(`input[name="${pergunta.dependeDe}"]`).forEach((input) => {
      input.addEventListener("change", atualizar);
    });

    atualizar();
  });
}

// Le os valores preenchidos de uma secao a partir do container onde ela foi renderizada
export function lerRespostasSecao(container, secao) {
  const respostas = {};

  secao.perguntas.forEach((pergunta) => {
    if (pergunta.tipo === "radio") {
      const marcado = container.querySelector(`input[name="${pergunta.id}"]:checked`);
      respostas[pergunta.id] = marcado ? marcado.value : "";
    } else if (pergunta.tipo === "checkbox") {
      const marcados = container.querySelectorAll(`input[name="${pergunta.id}"]:checked`);
      respostas[pergunta.id] = [...marcados].map((el) => el.value);
    } else if (pergunta.tipo === "confirmacao") {
      const campo = container.querySelector(`[name="${pergunta.id}"]`);
      respostas[pergunta.id] = campo ? campo.checked : false;
    } else {
      const campo = container.querySelector(`[name="${pergunta.id}"]`);
      respostas[pergunta.id] = campo ? campo.value.trim() : "";
    }
  });

  return respostas;
}
