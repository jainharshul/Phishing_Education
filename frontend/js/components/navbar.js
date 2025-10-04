// Simple, scalable navbar with hash routes
export function renderNavbar() {
    return `
      <nav class="nav">
        <a class="brand" href="#/">PhishingApp</a>
        <div class="links">
          <a href="#/">Home</a>
          <a href="#/about">About</a>
        </div>
      </nav>
    `;
  }
  