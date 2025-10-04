import { renderNavbar } from "./components/navbar.js";
import { renderFooter } from "./components/footer.js";
import { initRouter } from "./router.js";

function mount(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

window.addEventListener("DOMContentLoaded", () => {
  mount("navbar", renderNavbar());
  mount("footer", renderFooter());
  initRouter();
});
