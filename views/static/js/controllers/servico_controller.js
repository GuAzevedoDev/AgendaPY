import * as servicoApi from "../api/servico_api.js";
import * as agendaApi from "../api/agenda_api.js";

export function iniciarServicos() {
  configurarBuscaServico();
  configurarBotaoAgendar();
}

function configurarBuscaServico() {
  const inputServico = document.querySelector(".servicoCliente");
  const listaServicos = document.querySelector(".lista-servicos");
  const listaServicosSelecionados = document.querySelector(".servicos-selecionados");

  if (!inputServico || !listaServicos || !listaServicosSelecionados) return;

  inputServico.addEventListener("input", async function pegaServico() {
    const query = inputServico.value.trim();
    if (query === "") {
      listaServicos.innerHTML = "";
      return;
    }

    try {
      const servicos = await servicoApi.buscarServicos(query);
      listaServicos.innerHTML = "";
      servicos.forEach((servico) => {
        const li = document.createElement("li");
        li.className = "servico-lista";
        li.dataset.servico = servico[1];
        li.textContent = servico[1];
        
        li.addEventListener("click", () => {
          const servicoSelecionado = li.dataset.servico;
          
          const novoItem = document.createElement("li");
          novoItem.className = "servico-lista-ativo";
          novoItem.dataset.servicoselecionado = servicoSelecionado;
          novoItem.innerHTML = `
            <span>${servicoSelecionado}</span>
            <div class="btn-servicos">
              <svg width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0.338429 0.338429C0.789667 -0.11281 1.52129 -0.11281 1.97248 0.338429L5.00708 3.37307L8.04168 0.338459C8.49293 -0.112779 9.22443 -0.112779 9.67568 0.338459C10.1269 0.789698 10.1269 1.52132 9.67568 1.97263L6.64123 5.00708L9.67568 8.04152C10.1269 8.49277 10.1269 9.22443 9.67568 9.67568C9.22443 10.1269 8.49277 10.1269 8.04152 9.67568L5.00708 6.64123L1.97263 9.67568C1.52132 10.1269 0.789667 10.1269 0.338459 9.67568C-0.112779 9.22443 -0.112779 8.49293 0.338459 8.04168L3.37307 5.00708L0.338429 1.97248C-0.11281 1.52129 -0.11281 0.789667 0.338429 0.338429Z" fill="#B8B1AE" />
              </svg>
            </div>
          `;
          
          novoItem.querySelector(".btn-servicos").addEventListener("click", () => {
            novoItem.remove();
          });
          
          listaServicosSelecionados.appendChild(novoItem);
          listaServicos.innerHTML = "";
          inputServico.value = "";
        });

        listaServicos.appendChild(li);
      });
    } catch (err) {
      console.error("Erro ao buscar serviços:", err);
    }
  });
}

function configurarBotaoAgendar() {
  const botaoAgendar = document.querySelector("#btnAgendar");
  if (!botaoAgendar) return;

  const inputNome = document.querySelector(".nomeCliente");
  const inputNumero = document.querySelector(".numeroCliente");
  const inputHora = document.querySelector(".horaCliente");
  const inputData = document.querySelector(".dataCliente");
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
        inputData.value
      );

      if (dados["mensagem"] === true) {
        window.location.reload();
      } else if (avisoModal && dados["mensagem"]) {
        avisoModal.innerHTML = dados["mensagem"];
      }
    } catch (err) {
      console.error("Erro ao realizar agendamento:", err);
    }
  });
}
