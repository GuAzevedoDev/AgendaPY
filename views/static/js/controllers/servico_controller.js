import * as servicoApi from "../api/servico_api.js";
import * as agendaApi from "../api/agenda_api.js";

export function iniciarServicos() {
  configurarBuscaServico();
  configurarBotaoAgendar();
}

let indiceServicoSelecionado = -1;

function configurarBuscaServico() {
  const inputServico = document.querySelector(".servicoCliente");
  const listaServicos = document.querySelector(".lista-servicos");
  const listaServicosSelecionados = document.querySelector(".servicos-selecionados");

  if (!inputServico || !listaServicos || !listaServicosSelecionados) return;

  function atualizarSelecao() {
    const itens = listaServicos.querySelectorAll(".servico-lista");

    itens.forEach((item, index) => {
      item.classList.toggle("ativo", index === indiceServicoSelecionado);
    });

    if (indiceServicoSelecionado >= 0) {
      itens[indiceServicoSelecionado].scrollIntoView({
        block: "nearest",
      });
    }
  }

  function adicionarServico(item) {
    const servicoSelecionado = item.dataset.servico;

    // Evita adicionar duplicados
    const existe = [...listaServicosSelecionados.children].some(
      (li) =>
        li.dataset.servicoselecionado === servicoSelecionado
    );

    if (existe) {
      inputServico.value = "";
      listaServicos.innerHTML = "";
      indiceServicoSelecionado = -1;
      return;
    }

    const novoItem = document.createElement("li");
    novoItem.className = "servico-lista-ativo";
    novoItem.dataset.servicoselecionado = servicoSelecionado;

    novoItem.innerHTML = `
      <span>${servicoSelecionado}</span>

      <div class="btn-servicos">
        <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
          <path d="M0.338429 0.338429C0.789667 -0.11281 1.52129 -0.11281 1.97248 0.338429L5.00708 3.37307L8.04168 0.338459C8.49293 -0.112779 9.22443 -0.112779 9.67568 0.338459C10.1269 0.789698 10.1269 1.52132 9.67568 1.97263L6.64123 5.00708L9.67568 8.04152C10.1269 8.49277 10.1269 9.22443 9.67568 9.67568C9.22443 10.1269 8.49277 10.1269 8.04152 9.67568L5.00708 6.64123L1.97263 9.67568C1.52132 10.1269 0.789667 10.1269 0.338459 9.67568C-0.112779 9.22443 -0.112779 8.49293 0.338459 8.04168L3.37307 5.00708L0.338429 1.97248C-0.11281 1.52129 -0.11281 0.789667 0.338429 0.338429Z" fill="#B8B1AE"/>
        </svg>
      </div>
    `;

    listaServicosSelecionados.appendChild(novoItem);

    inputServico.value = "";
    listaServicos.innerHTML = "";
    indiceServicoSelecionado = -1;
  }

  inputServico.addEventListener("input", async () => {
    const query = inputServico.value.trim();

    if (!query) {
      listaServicos.innerHTML = "";
      indiceServicoSelecionado = -1;
      return;
    }

    try {
      const servicos = await servicoApi.buscarServicos(query);

      listaServicos.innerHTML = servicos
        .map(
          (servico) => `
            <li
              class="servico-lista"
              data-servico="${servico[1]}"
              tabindex="-1">
              ${servico[1]}
            </li>
          `
        )
        .join("");

      indiceServicoSelecionado = -1;
    } catch (err) {
      console.error("Erro ao buscar serviços:", err);
    }
  });

  // Clique na lista
  listaServicos.addEventListener("click", (e) => {
    const item = e.target.closest(".servico-lista");

    if (!item) return;

    adicionarServico(item);
  });

  // Navegação por teclado
  inputServico.addEventListener("keydown", (e) => {
    const itens = [...listaServicos.querySelectorAll(".servico-lista")];

    if (!itens.length) return;

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        indiceServicoSelecionado = Math.min(
          indiceServicoSelecionado + 1,
          itens.length - 1
        );
        atualizarSelecao();
        break;

      case "ArrowUp":
        e.preventDefault();
        indiceServicoSelecionado = Math.max(
          indiceServicoSelecionado - 1,
          0
        );
        atualizarSelecao();
        break;

      case "Enter":
      case "Tab":
        if (indiceServicoSelecionado >= 0) {
          e.preventDefault();
          adicionarServico(itens[indiceServicoSelecionado]);
        }
        break;

      case "Escape":
        listaServicos.innerHTML = "";
        indiceServicoSelecionado = -1;
        break;
    }
  });

  // Remover serviço (delegação de eventos)
  listaServicosSelecionados.addEventListener("click", (e) => {
    const botao = e.target.closest(".btn-servicos");

    if (!botao) return;

    botao.closest(".servico-lista-ativo").remove();
  });
}

function configurarBotaoAgendar() {
  const botaoAgendar = document.querySelector("#btnAgendar");
  if (!botaoAgendar) return;

  const inputNome = document.querySelector(".nomeCliente");
  const inputNumero = document.querySelector(".numeroCliente");
  const inputHora = document.querySelector(".horaCliente");
  const inputData = document.querySelector(".dataCliente");
  const areaObservacao = document.querySelector(".observacaoAgendamento");
  const form = document.querySelector("#formAgendamento");

  botaoAgendar.addEventListener("click", async function agendamento(event) {
    event.preventDefault();
    
    const avisoModal = document.querySelector(".modal-agendamento .aviso-modal");
    if (avisoModal) avisoModal.innerHTML = "";

    if (form && !form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const servicosAtivos = document.querySelectorAll(".servico-lista-ativo");
    const nomeDosServicos = [];
    servicosAtivos.forEach((servicoSelecionado) => {
      nomeDosServicos.push(servicoSelecionado.dataset.servicoselecionado);
    });

    if (nomeDosServicos.length === 0) {
      if (avisoModal) {
        avisoModal.innerHTML = "Selecione pelo menos um serviço para agendar";
      }
      return;
    }

    try {
      const dados = await agendaApi.agendarHorario(
        window.id_funcionario,
        nomeDosServicos,
        inputNome.value,
        inputNumero.value,
        inputHora.value,
        inputData.value,
        areaObservacao.value
      );

      if (dados["sucesso"] === true) {
        window.location.reload();
      } else if (avisoModal && dados["mensagem"]) {
        avisoModal.innerHTML = dados["mensagem"];
      }
    } catch (err) {
      console.error("Erro ao realizar agendamento:", err);
    }
  });
}
