document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme based on user preference or system setting
    initTheme();

    // Set up event listeners
    setupEventListeners();
});

/**
 * Initialize the theme based on stored preference or system setting
 */
function initTheme() {
    const savedTheme = localStorage.getItem('divine-theme');

    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    } else {
        // Check if user prefers dark mode
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (prefersDarkScheme) {
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('divine-theme', 'dark');
        } else {
            document.body.setAttribute('data-theme', 'light');
            localStorage.setItem('divine-theme', 'light');
        }
    }

    // Update theme toggle UI to match current theme
    updateThemeToggleUI();
}

/**
 * Set up all event listeners for the dashboard
 */
function setupEventListeners() {
    // Theme toggle functionality
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Navigation functionality
    const navLinks = document.querySelectorAll('.main-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavigation);
    });
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('divine-theme', newTheme);

    // Update the theme toggle UI
    updateThemeToggleUI();
}

/**
 * Update the theme toggle UI to match the current theme
 */
function updateThemeToggleUI() {
    const currentTheme = document.body.getAttribute('data-theme');
    const lightIcon = document.querySelector('.light-icon');
    const darkIcon = document.querySelector('.dark-icon');

    if (currentTheme === 'dark') {
        lightIcon.style.opacity = '0.5';
        darkIcon.style.opacity = '1';
    } else {
        lightIcon.style.opacity = '1';
        darkIcon.style.opacity = '0.5';
    }
}

/**
 * Handle navigation between different sections
 * @param {Event} e - Click event
 */
function handleNavigation(e) {
    e.preventDefault();

    // Remove active class from all links
    const navLinks = document.querySelectorAll('.main-nav a');
    navLinks.forEach(link => link.classList.remove('active'));

    // Add active class to clicked link
    e.target.classList.add('active');

    // Get the target section
    const targetSectionId = e.target.getAttribute('href').substring(1);

    // Hide all sections
    const sections = document.querySelectorAll('main section');
    sections.forEach(section => section.classList.remove('active'));

    // Show the target section
    const targetSection = document.getElementById(`${targetSectionId}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
    } else {
        console.log(`Section with ID "${targetSectionId}-section" not found. Loading content...`);
        // Here you could load content dynamically via fetch/AJAX if needed
    }
}

/**
 * Utility function to create a toast notification
 * @param {string} message - The notification message
 * @param {string} type - The type of notification (success, error, info)
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Trigger animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
} 