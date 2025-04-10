/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * Tests for the index-wrapper.js file
 * These tests validate the JavaScript wrapper around the index.html functionality
 */

import '@testing-library/jest-dom';
import { screen, fireEvent, waitFor } from '@testing-library/dom';
import { elements, functions, initPage } from '../js/index-wrapper';

// Set up document body with the index.html content before each test
beforeEach(() => {
    // We'll load the HTML file and set it as the document body
    const fs = require('fs');
    const path = require('path');
    const html = fs.readFileSync(path.resolve(__dirname, '../index.html'), 'utf8');
    document.body.innerHTML = html;

    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
        value: {
            getItem: jest.fn(),
            setItem: jest.fn()
        }
    });

    // Mock requestFullscreen
    HTMLElement.prototype.requestFullscreen = jest.fn();
});

// Clean up after each test
afterEach(() => {
    document.body.innerHTML = '';
    jest.clearAllMocks();
});

describe('Index Wrapper - Elements', () => {
    test('all element selectors should return DOM elements', () => {
        // Test that each element selector returns an element or collection
        expect(elements.navLinks().length).toBeGreaterThan(0);
        expect(elements.sections().length).toBeGreaterThan(0);
        expect(elements.themeToggle()).toBeInTheDocument();
        expect(elements.menuToggle()).toBeInTheDocument();
        expect(elements.searchBar()).toBeInTheDocument();
        expect(elements.refreshBtn()).toBeInTheDocument();
        expect(elements.statCards().length).toBeGreaterThan(0);
        expect(elements.projectItems().length).toBeGreaterThan(0);
        expect(elements.teslaQAFrame()).toBeInTheDocument();
        expect(elements.fullscreenBtn()).toBeInTheDocument();
        expect(elements.refreshDashboardBtn()).toBeInTheDocument();
        expect(elements.darkModeSwitch()).toBeInTheDocument();
        expect(elements.usernameInput()).toBeInTheDocument();
        expect(elements.emailInput()).toBeInTheDocument();
        expect(elements.addTaskBtn()).toBeInTheDocument();
        expect(elements.inProgressTasks()).toBeInTheDocument();
        expect(elements.docsSearch()).toBeInTheDocument();
        expect(elements.docsSearchBtn()).toBeInTheDocument();
        expect(elements.docsNavLinks().length).toBeGreaterThan(0);
        expect(elements.helpCards().length).toBeGreaterThan(0);
    });
});

describe('Index Wrapper - Functions', () => {
    test('navigateToSection should set active classes correctly', () => {
        // Call the function with a valid section ID
        const result = functions.navigateToSection('dashboard');

        // Check if the function worked as expected
        expect(result.success).toBe(true);
        expect(result.targetId).toBe('dashboard');

        // Check if the correct elements have the active class
        const dashboardLink = document.querySelector('a[href="#dashboard"]');
        const dashboardSection = document.getElementById('dashboard');

        expect(dashboardLink).toHaveClass('active');
        expect(dashboardSection).toHaveClass('active');

        // Also test with an invalid section ID
        const invalidResult = functions.navigateToSection('nonexistent');
        expect(invalidResult.success).toBe(true); // Function still succeeds even with invalid ID
        expect(invalidResult.targetId).toBe('nonexistent');
    });

    test('toggleDarkMode should toggle dark-mode class and save to localStorage', () => {
        // Initial state (no dark mode)
        expect(document.body).not.toHaveClass('dark-mode');

        // Toggle to dark mode
        const isDarkMode = functions.toggleDarkMode();

        // Check if dark mode is enabled
        expect(isDarkMode).toBe(true);
        expect(document.body).toHaveClass('dark-mode');
        expect(localStorage.setItem).toHaveBeenCalledWith('divineDashboardTheme', 'dark');

        // Toggle back to light mode
        const isLightMode = functions.toggleDarkMode();

        // Check if dark mode is disabled
        expect(isLightMode).toBe(false);
        expect(document.body).not.toHaveClass('dark-mode');
        expect(localStorage.setItem).toHaveBeenCalledWith('divineDashboardTheme', 'light');
    });

    test('toggleSidebar should toggle the collapsed class on sidebar', () => {
        const sidebar = document.querySelector('.sidebar');

        // Initial state (not collapsed)
        expect(sidebar).not.toHaveClass('collapsed');

        // Toggle to collapsed
        const isCollapsed = functions.toggleSidebar();

        // Check if sidebar is collapsed
        expect(isCollapsed).toBe(true);
        expect(sidebar).toHaveClass('collapsed');

        // Toggle back to expanded
        const isExpanded = functions.toggleSidebar();

        // Check if sidebar is expanded
        expect(isExpanded).toBe(false);
        expect(sidebar).not.toHaveClass('collapsed');
    });

    test('loadStatCard should update stat card values', () => {
        // Test with valid card ID
        const result = functions.loadStatCard('commits-today', '42', '+5%');

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if values were updated
        const valueElement = document.querySelector('#commits-today .stat-value');
        const changeElement = document.querySelector('#commits-today .stat-change');

        expect(valueElement.textContent).toBe('42');
        expect(changeElement.textContent).toBe('+5%');

        // Test with invalid card ID
        const invalidResult = functions.loadStatCard('nonexistent', '42', '+5%');
        expect(invalidResult).toBe(false);
    });

    test('openTeslaQAFullscreen should call requestFullscreen on iframe', () => {
        // Call the function
        const result = functions.openTeslaQAFullscreen();

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if requestFullscreen was called on the iframe
        expect(elements.teslaQAFrame().requestFullscreen).toHaveBeenCalled();
    });

    test('refreshTeslaQADashboard should reload the iframe', () => {
        const iframe = elements.teslaQAFrame();
        const originalSrc = iframe.src;

        // Call the function
        const result = functions.refreshTeslaQADashboard();

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if the src was "refreshed" (set to the same value, which would trigger a reload)
        expect(iframe.src).toBe(originalSrc);
    });

    test('updateUsername should update username in input and display', () => {
        // Call the function
        const result = functions.updateUsername('Tesla Engineer');

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if values were updated
        const usernameInput = elements.usernameInput();
        const userNameDisplay = document.querySelector('.user-name');

        expect(usernameInput.value).toBe('Tesla Engineer');
        expect(userNameDisplay.textContent).toBe('Tesla Engineer');
    });

    test('addTask should add a task to the in-progress list', () => {
        // Initial task count
        const initialCount = document.querySelectorAll('#in-progress-tasks .task-item').length;
        const initialCountText = document.querySelector('#in-progress-tasks .task-count').textContent;

        // Call the function
        const result = functions.addTask('Test Task', 'Test Description', 'Tomorrow');

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if task was added
        const newCount = document.querySelectorAll('#in-progress-tasks .task-item').length;
        const newCountText = document.querySelector('#in-progress-tasks .task-count').textContent;

        expect(newCount).toBe(initialCount + 1);
        expect(parseInt(newCountText)).toBe(parseInt(initialCountText) + 1);

        // Check task content
        const taskItem = document.querySelector('#in-progress-tasks .task-item:last-child');
        expect(taskItem.querySelector('h4').textContent).toBe('Test Task');
        expect(taskItem.querySelector('.task-content p').textContent).toBe('Test Description');
        expect(taskItem.querySelector('.task-due').textContent).toBe('Due: Tomorrow');
    });

    test('searchDocs should simulate searching documentation', () => {
        // Mock console.log
        console.log = jest.fn();

        // Call the function
        const result = functions.searchDocs('installation');

        // Check if function returned expected structure
        expect(result).toEqual({ results: [], query: 'installation' });

        // Check if console.log was called with the expected message
        expect(console.log).toHaveBeenCalledWith('Searching documentation for: installation');
    });

    test('handleResponsiveLayout should apply correct classes based on window width', () => {
        const sidebar = document.querySelector('.sidebar');

        // Test with small window width
        Object.defineProperty(window, 'innerWidth', { value: 800, writable: true });

        // Call the function
        let result = functions.handleResponsiveLayout();

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if sidebar is collapsed
        expect(sidebar).toHaveClass('collapsed');

        // Test with large window width
        Object.defineProperty(window, 'innerWidth', { value: 1200, writable: true });

        // Call the function
        result = functions.handleResponsiveLayout();

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if sidebar is expanded
        expect(sidebar).not.toHaveClass('collapsed');
    });
});

describe('Index Wrapper - Page Initialization', () => {
    test('initPage should set up event listeners and check for saved theme', () => {
        // Mock localStorage.getItem to return 'dark'
        localStorage.getItem.mockReturnValue('dark');

        // Call the function
        const result = initPage();

        // Check if function succeeded
        expect(result).toBe(true);

        // Check if dark mode was applied based on localStorage
        expect(document.body).toHaveClass('dark-mode');
        expect(localStorage.getItem).toHaveBeenCalledWith('divineDashboardTheme');

        // Test event listeners by simulating user actions

        // 1. Navigation
        const dashboardLink = document.querySelector('a[href="#dashboard"]');
        fireEvent.click(dashboardLink);
        expect(document.getElementById('dashboard')).toHaveClass('active');

        // 2. Theme toggle
        const themeToggle = elements.themeToggle();
        fireEvent.click(themeToggle);
        expect(document.body).not.toHaveClass('dark-mode');

        // 3. Sidebar toggle
        const menuToggle = elements.menuToggle();
        fireEvent.click(menuToggle);
        expect(document.querySelector('.sidebar')).toHaveClass('collapsed');

        // 4. Add task
        const addTaskBtn = elements.addTaskBtn();
        const initialTaskCount = document.querySelectorAll('#in-progress-tasks .task-item').length;
        fireEvent.click(addTaskBtn);
        const newTaskCount = document.querySelectorAll('#in-progress-tasks .task-item').length;
        expect(newTaskCount).toBe(initialTaskCount + 1);

        // 5. Tesla QA fullscreen
        const fullscreenBtn = elements.fullscreenBtn();
        fireEvent.click(fullscreenBtn);
        expect(elements.teslaQAFrame().requestFullscreen).toHaveBeenCalled();

        // 6. Tesla QA refresh
        const refreshDashboardBtn = elements.refreshDashboardBtn();
        const iframe = elements.teslaQAFrame();
        const originalSrc = iframe.src;
        fireEvent.click(refreshDashboardBtn);
        expect(iframe.src).toBe(originalSrc);

        // 7. Window resize
        window.dispatchEvent(new Event('resize'));
        // The resize handler should have been called, but we've already tested it
    });
}); 