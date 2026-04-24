const botao = document.querySelector("#btnEnvio");
botao.addEventListener("click", pegaDadosCliente);

function pegaDadosCliente() {
  const nome = document.querySelector("#nome");
  const numero = document.querySelector("#numero");

  const dadosCliente = {
    nome: nome.value,
    telefone: numero.value,
  };

  const nomeLimpo = dadosCliente.nome;
  const telefoneLimpo = dadosCliente.telefone;

  if (!nomeLimpo.trim() || !telefoneLimpo.trim()) {
    alert("Preencha todos os campos");
    return;
  }
  fetch("/CadastroClientes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dadosCliente),
  })
    .then(async (response) => {
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.mensagem)
  }

  return data
})
.then(data => {
  alert(data.mensagem)
})
.catch(err => {
  alert(err.message)
})
  nome.value = ""
  numero.value = ""
  nome.focus()
}
 