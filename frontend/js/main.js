import { renderNavbar, addToHistory, initBackButton } from "./components/navbar.js";
import { renderFooter } from "./components/footer.js";
import { initRouter } from "./router.js";

function mount(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

window.addEventListener("DOMContentLoaded", () => {
  mount("navbar", renderNavbar());
  mount("footer", renderFooter());
  initBackButton(); 
  initRouter();
  

  window.addEventListener('hashchange', () => {
      const currentHash = window.location.hash || '#/';
      addToHistory(currentHash);
  });


  addToHistory(window.location.hash || '#/');
});