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
    
    console.log('checkAuthStatus called');
    console.log('isLoggedIn:', isLoggedIn);
    console.log('username:', username);
    console.log('Type of isLoggedIn:', typeof isLoggedIn);
    console.log('isLoggedIn === true:', isLoggedIn === true);
    console.log('isLoggedIn === "true":', isLoggedIn === 'true');
    
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
    
    console.log('Found menu elements, setting up click handler...');
    
    const newHamburger = hamburger.cloneNode(true);
    hamburger.parentNode.replaceChild(newHamburger, hamburger);
    
    // Add our click handler
    newHamburger.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Hamburger clicked!');
        
        // Toggle the menu
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
            newHamburger.setAttribute('aria-expanded', 'false');
            console.log('Menu closed');
        } else {
            menu.classList.add('show');
            newHamburger.setAttribute('aria-expanded', 'true');
            console.log('Menu opened');
        }
    };
    
    console.log('Mobile menu is now working!');
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
    
    console.log('Found hamburgers:', hamburgers.length);
    console.log('Found menus:', menus.length);
    
    hamburgers.forEach((hamburger, index) => {
        console.log(`Setting up hamburger ${index + 1}`);
        
        // Remove all existing event listeners
        const newHamburger = hamburger.cloneNode(true);
        hamburger.parentNode.replaceChild(newHamburger, hamburger);
        
        // Add our click handler
        newHamburger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`Hamburger ${index + 1} clicked!`);
            
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

