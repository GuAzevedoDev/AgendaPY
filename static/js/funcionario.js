const botao = document.querySelector("#btnEnvio");
botao.addEventListener("click", pegaDadosFunc);

function pegaDadosFunc(){
  const usuario = document.querySelector('#nome')
  const senha = document.querySelector('#numero')
  const dados = {
    usuario: usuario.value,
    senha: senha.value,
  }
  const usuarioLimpo = dados.usuario
  const senhaLimpa = dados.senha

  if (!usuarioLimpo.trim() || !senhaLimpa.trim()) {
    alert("Usuario ou senha invalidos");
    return;
  }
  fetch("/loginEntrada", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dados),
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
    usuario.value = ""
    senha.value = ""
    usuario.focus()
  }
