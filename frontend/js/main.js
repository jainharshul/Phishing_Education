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
  initBackButton(); // Initialize back button functionality
  initRouter();
  
  // Track page changes for back button
  window.addEventListener('hashchange', () => {
      const currentHash = window.location.hash || '#/';
      addToHistory(currentHash);
  });

  // Add initial page to history
  addToHistory(window.location.hash || '#/');
});