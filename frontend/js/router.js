const routes = {
    "/": "/static/pages/home.html",
    "/about": "/static/pages/about.html",
    "/page1": "/static/pages/page1.html",   
    "/page2": "/static/pages/page2.html",  
  };
  
  
  async function fetchPage(url) {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`Failed to load ${url}`);
    return res.text();
  }
  
  export async function navigate() {
    const outlet = document.getElementById("app");
    const path = location.hash.replace(/^#/, "") || "/";
    const pageUrl = routes[path] || routes["/"]; // fallback to home or make a 404 page
  
    try {
      outlet.innerHTML = await fetchPage(pageUrl);
      // Optionally run per-page JS hooks:
      if (path === "/dashboard" && window.dashboardInit) {
        window.dashboardInit();
      }
    } catch (e) {
      outlet.innerHTML = `<div class="error">Page failed to load.</div>`;
      console.error(e);
    }
  }
  
  export function initRouter() {
    window.addEventListener("hashchange", navigate);
    navigate(); // initial load
  }
  