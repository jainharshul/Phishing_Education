// navbar.js - with back button functionality
let navHistory = ['#/']; // Start with home page

// Track navigation history
export function addToHistory(page) {
    // Don't add consecutive duplicates or the back route itself
    if (page !== '#/back' && (navHistory.length === 0 || navHistory[navHistory.length - 1] !== page)) {
        navHistory.push(page);
        // Keep only last 10 pages to prevent memory issues
        if (navHistory.length > 10) {
            navHistory.shift();
        }
    }
}

// Function to go back to previous page
export function goBack() {
    if (navHistory.length > 1) {
        // Remove current page
        navHistory.pop();
        // Get previous page
        const previousPage = navHistory.pop();
        return previousPage || '#/';
    }
    return '#/'; // Default to home if no history
}

// Simple, scalable navbar with hash routes
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

// Initialize back button functionality
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

// Get current navigation history (for debugging)
export function getNavHistory() {
    return [...navHistory];
}