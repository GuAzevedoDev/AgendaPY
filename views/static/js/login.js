
function mostrarSenha(){
  let senha = document.querySelector("#senha")
  if (senha.type === 'text'){
    senha.type = 'password'
  }
  else{
    senha.type = 'text'
  }
}