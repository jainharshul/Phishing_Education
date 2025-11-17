let navHistory = ['#/']; 

export function addToHistory(page) {
    if (page !== '#/back' && (navHistory.length === 0 || navHistory[navHistory.length - 1] !== page)) {
        navHistory.push(page);
        if (navHistory.length > 10) {
            navHistory.shift();
        }
    }
}

export function goBack() {
    if (navHistory.length > 1) {
        navHistory.pop();
        const previousPage = navHistory.pop();
        return previousPage || '#/';
    }
    return '#/';
}

export function renderNavbar() {
    return `
      <nav class="nav">
        <a class="brand" href="#/">PhishingApp</a>
        <div class="links">
          <a href="#/">Home</a>
          <a href="#/back" id="backButton">Back</a>
        </div>
      </nav>
    `;
}

export function initBackButton() {
    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.addEventListener('click', (e) => {
            e.preventDefault();
            const previousPage = goBack();
            window.location.hash = previousPage;
        });
    }
}

export function getNavHistory() {
    return [...navHistory];
}