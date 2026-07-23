export function iniciarMenuMobile() {
  const botao = document.querySelector(".btn-menu-mobile");
  const overlay = document.querySelector(".overlay-menu-mobile");
  const header = document.querySelector(".header");

  if (!botao || !overlay || !header) return;

  function abrirMenu() {
    header.classList.add("menu-aberto");
    overlay.classList.add("ativo");
    botao.classList.add("aberto");
  }

  function fecharMenu() {
    header.classList.remove("menu-aberto");
    overlay.classList.remove("ativo");
    botao.classList.remove("aberto");
  }

  botao.addEventListener("click", () => {
    if (header.classList.contains("menu-aberto")) {
      fecharMenu();
    } else {
      abrirMenu();
    }
  });

  overlay.addEventListener("click", fecharMenu);

  header.querySelectorAll("menu a, .btn-logout").forEach((link) => {
    link.addEventListener("click", fecharMenu);
  });
}
