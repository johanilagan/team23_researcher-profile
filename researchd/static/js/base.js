// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Update icon based on current theme
    if (savedTheme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        themeToggle.title = 'Switch to Light Mode';
    } else {
        themeIcon.className = 'fas fa-moon';
        themeToggle.title = 'Switch to Dark Mode';
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    const themeIcon = document.getElementById('theme-icon');
    const themeToggle = document.getElementById('theme-toggle');
    
    // Apply new theme
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon and tooltip
    if (newTheme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        themeToggle.title = 'Switch to Light Mode';
    } else {
        themeIcon.className = 'fas fa-moon';
        themeToggle.title = 'Switch to Dark Mode';
    }
}

// Check authentication status
function checkAuthStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const username = localStorage.getItem('username') || 'User';
    
    if (isLoggedIn) {
        console.log('User is logged in, showing user menu');
        const authButtons = document.getElementById('auth-buttons');
        const userMenu = document.getElementById('user-menu');
        const usernameSpan = document.getElementById('username');
        
        if (authButtons) authButtons.classList.add('d-none');
        if (userMenu) userMenu.classList.remove('d-none');
        if (usernameSpan) usernameSpan.textContent = username;
        
        // Show welcome message if this is a fresh login
        const hasShownWelcome = sessionStorage.getItem('hasShownWelcome');
        if (!hasShownWelcome) {
            showWelcomeMessage(username);
            sessionStorage.setItem('hasShownWelcome', 'true');
        }
    } else {
        console.log('User is not logged in, showing auth buttons');
        const authButtons = document.getElementById('auth-buttons');
        const userMenu = document.getElementById('user-menu');
        
        if (authButtons) authButtons.classList.remove('d-none');
        if (userMenu) userMenu.classList.add('d-none');
    }
}

// Sign out function
function signOut() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    window.location.href = "/";
}

// Initialize FAQ Accordion Functionality
function initAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    if (faqQuestions.length === 0) {
        return; // No FAQ accordion on this page
    }
    
    console.log('Initializing FAQ accordion for', faqQuestions.length, 'questions');
    
    faqQuestions.forEach(function(button) {
        button.addEventListener('click', function() {
            // Toggle active class for styling
            this.classList.toggle('active');
            
            // Get the answer panel (next sibling element)
            const answer = this.nextElementSibling;
            
            if (answer && answer.classList.contains('faq-answer')) {
                // Toggle the max-height for smooth animation
                if (answer.style.maxHeight) {
                    // Close the answer
                    answer.style.maxHeight = null;
                } else {
                    // Open the answer
                    answer.style.maxHeight = answer.scrollHeight + "px";
                }
            }
        });
    });
}

// FAQ Search Functionality
function initFAQSearch() {
    const searchInput = document.getElementById('faq-search-input');
    const searchBtn = document.getElementById('faq-search-btn');
    const resultsCount = document.getElementById('search-results-count');
    
    if (!searchInput || !searchBtn) {
        return; // Not on help centre page
    }
    
    console.log('Initializing FAQ search functionality');
    
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const faqQuestions = document.querySelectorAll('.faq-question');
        const faqAnswers = document.querySelectorAll('.faq-answer');
        const categoryHeadings = document.querySelectorAll('.faq-category-heading');
        
        let visibleCount = 0;
        let matchedCategories = new Set();
        
        if (searchTerm === '') {
            // Show all FAQs and categories
            faqQuestions.forEach(function(q, index) {
                q.classList.remove('hidden');
                faqAnswers[index].classList.remove('hidden');
            });
            categoryHeadings.forEach(function(h) {
                h.classList.remove('hidden');
            });
            resultsCount.textContent = '';
            return;
        }
        
        // Search through FAQs
        faqQuestions.forEach(function(question, index) {
            const questionText = question.querySelector('span').textContent.toLowerCase();
            const answer = faqAnswers[index];
            const answerText = answer ? answer.textContent.toLowerCase() : '';
            const category = question.getAttribute('data-category');
            
            // Check if search term matches question or answer
            if (questionText.includes(searchTerm) || answerText.includes(searchTerm)) {
                question.classList.remove('hidden');
                answer.classList.remove('hidden');
                visibleCount++;
                matchedCategories.add(category);
            } else {
                question.classList.add('hidden');
                answer.classList.add('hidden');
            }
        });
        
        // Show/hide category headings based on whether they have visible FAQs
        categoryHeadings.forEach(function(heading) {
            const category = heading.getAttribute('data-category');
            if (matchedCategories.has(category)) {
                heading.classList.remove('hidden');
            } else {
                heading.classList.add('hidden');
            }
        });
        
        // Update results count
        if (visibleCount === 0) {
            resultsCount.textContent = 'No results found. Try different keywords.';
            resultsCount.style.color = '#dc3545';
        } else if (visibleCount === 1) {
            resultsCount.textContent = '1 result found';
            resultsCount.style.color = '#28a745';
        } else {
            resultsCount.textContent = visibleCount + ' results found';
            resultsCount.style.color = '#28a745';
        }
    }
    
    // Search on button click
    searchBtn.addEventListener('click', performSearch);
    
    // Search on Enter key
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Real-time search as user types (with slight delay)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    console.log('Bootstrap version:', typeof bootstrap !== 'undefined' ? bootstrap.VERSION : 'Not loaded');
    
    // Initialize theme
    initTheme();
    
    // Add event listener to theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Check authentication status
    checkAuthStatus();
    
    // Initialize accordion
    initAccordion();
    
    // Initialize FAQ search
    initFAQSearch();
});

// Bulletproof mobile menu 
function makeMobileMenuWork() {
    console.log('Setting up bulletproof mobile menu...');
    
    // Find the hamburger button and menu
    const hamburger = document.querySelector('.navbar-toggler');
    const menu = document.querySelector('#navbarNav');
    
    if (!hamburger || !menu) {
        console.log('Menu elements not found, retrying...');
        setTimeout(makeMobileMenuWork, 500);
        return;
    }
        
    const newHamburger = hamburger.cloneNode(true);
    hamburger.parentNode.replaceChild(newHamburger, hamburger);
    
    // Add our click handler
    newHamburger.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Toggle the menu
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
            newHamburger.setAttribute('aria-expanded', 'false');
        } else {
            menu.classList.add('show');
            newHamburger.setAttribute('aria-expanded', 'true');
        }
    };
    
}

// Alternative approach - direct event listener on the toggler
function setupMobileMenu() {
    const toggler = document.querySelector('[data-bs-toggle="collapse"]');
    const target = document.querySelector('[data-bs-target="#navbarNav"]');
    
    if (toggler && target) {
        console.log('Setting up direct mobile menu listener...');
        
        toggler.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Direct toggler clicked!');
            
            const navbarCollapse = document.querySelector('#navbarNav');
            if (navbarCollapse) {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                    toggler.setAttribute('aria-expanded', 'false');
                    console.log('Menu closed via direct listener');
                } else {
                    navbarCollapse.classList.add('show');
                    toggler.setAttribute('aria-expanded', 'true');
                    console.log('Menu opened via direct listener');
                }
            }
        });
    }
}

makeMobileMenuWork();

// Also run on DOM ready
document.addEventListener('DOMContentLoaded', makeMobileMenuWork);

// Run on page load
window.addEventListener('load', makeMobileMenuWork);

// Run on page show (back/forward navigation)
window.addEventListener('pageshow', makeMobileMenuWork);

// Run every 2 seconds to catch any late-loading pages
setInterval(makeMobileMenuWork, 2000);

// override everything and make it work
function forceMobileMenuToWork() {
    console.log('FORCING mobile menu to work...');
    
    // Find all possible hamburger buttons
    const hamburgers = document.querySelectorAll('.navbar-toggler, [data-bs-toggle="collapse"]');
    const menus = document.querySelectorAll('.navbar-collapse, #navbarNav');
    
    
    hamburgers.forEach((hamburger, index) => {
        
        // Remove all existing event listeners
        const newHamburger = hamburger.cloneNode(true);
        hamburger.parentNode.replaceChild(newHamburger, hamburger);
        
        // Add our click handler
        newHamburger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            menus.forEach(menu => {
                if (menu.classList.contains('show')) {
                    menu.classList.remove('show');
                    console.log('Menu closed');
                } else {
                    menu.classList.add('show');
                    console.log('Menu opened');
                }
            });
        });
    });
}

// Run immediately
forceMobileMenuToWork();

// Run after a delay 
setTimeout(forceMobileMenuToWork, 1000);
setTimeout(forceMobileMenuToWork, 3000);

// Test function 
window.testMobileMenu = function() {
    console.log('Testing mobile menu...');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarCollapse) {
        console.log('Elements found, toggling menu...');
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        } else {
            navbarCollapse.classList.add('show');
        }
        console.log('Menu toggled');
    } else {
        console.error('Menu elements not found');
    }
};

// Force function
window.forceMobileMenu = forceMobileMenuToWork;

