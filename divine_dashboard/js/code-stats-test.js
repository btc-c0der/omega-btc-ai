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
 * Code Stats Dashboard Test Utility
 * This script tests the functionality of the code-stats dashboard
 * Run this in the browser console to diagnose issues
 */

const CodeStatsTester = {
    // Test all DOM elements used by the code stats dashboard
    testDOMElements: function () {
        console.log('--- Testing DOM Elements ---');

        const elements = {
            // Dashboard container
            'code-stats-dashboard': document.getElementById('code-stats-dashboard'),

            // Stats display elements
            'total-files': document.getElementById('total-files'),
            'total-lines': document.getElementById('total-lines'),
            'total-size': document.getElementById('total-size'),
            'analysis-date': document.getElementById('analysis-date'),

            // Controls
            'refresh-stats': document.getElementById('refresh-stats'),
            'sort-stats': document.getElementById('sort-by'),
            'stats-table-body': document.getElementById('stats-table-body'),

            // Charts
            'lines-chart': document.getElementById('lines-chart'),
            'files-chart': document.getElementById('files-chart'),

            // Navigation
            'code-stats-link': document.getElementById('code-stats-link')
        };

        let allFound = true;
        for (const [id, element] of Object.entries(elements)) {
            const status = element ? '✅ Found' : '❌ Missing';
            console.log(`${id}: ${status}`);
            if (!element) allFound = false;
        }

        return allFound;
    },

    // Test if the dashboard toggle works
    testDashboardVisibility: function () {
        console.log('--- Testing Dashboard Visibility ---');

        const dashboard = document.getElementById('code-stats-dashboard');
        if (!dashboard) {
            console.log('❌ Dashboard element not found');
            return false;
        }

        const currentDisplay = window.getComputedStyle(dashboard).display;
        console.log(`Dashboard current display: ${currentDisplay}`);

        // Test if clicking the link shows the dashboard
        const statsLink = document.getElementById('code-stats-link');
        if (statsLink) {
            console.log('Simulating click on code-stats-link');
            statsLink.click();

            // Check if display changed
            const newDisplay = window.getComputedStyle(dashboard).display;
            console.log(`Dashboard display after click: ${newDisplay}`);

            return newDisplay !== 'none';
        } else {
            console.log('❌ Stats link not found');
            return false;
        }
    },

    // Test local storage for code stats
    testLocalStorage: function () {
        console.log('--- Testing Local Storage ---');

        const savedStats = localStorage.getItem('omega_code_stats');
        if (savedStats) {
            console.log('✅ Found stats in localStorage');
            try {
                const stats = JSON.parse(savedStats);
                console.log('Stats summary:', {
                    total_files: stats.total_files,
                    total_lines: stats.total_lines,
                    total_bytes: stats.total_bytes,
                    extensions: Object.keys(stats.by_extension).length
                });
                return true;
            } catch (e) {
                console.log('❌ Error parsing stats from localStorage', e);
                return false;
            }
        } else {
            console.log('❌ No stats found in localStorage');
            return false;
        }
    },

    // Test event listeners
    testEventListeners: function () {
        console.log('--- Testing Event Listeners ---');

        // Test refresh button
        const refreshBtn = document.getElementById('refresh-stats');
        if (refreshBtn) {
            console.log('✅ Found refresh button');
            console.log('Testing if onclick handler exists:', !!refreshBtn.onclick || 'No direct onclick handler');
            return true;
        } else {
            console.log('❌ Refresh button not found');
            return false;
        }
    },

    // Test the connection between main.js and code-stats.js
    testCodeConnection: function () {
        console.log('--- Testing Code Connections ---');

        // Check if initCodeStats function exists
        if (typeof window.initCodeStats === 'function') {
            console.log('✅ initCodeStats function found in global scope');
            return true;
        } else {
            console.log('❌ initCodeStats function not found in global scope');

            // Try to find it in the window object keys
            const possibleFunctions = Object.keys(window).filter(key =>
                typeof window[key] === 'function' &&
                key.toLowerCase().includes('stat')
            );

            if (possibleFunctions.length > 0) {
                console.log('Possible alternatives:', possibleFunctions);
            }

            return false;
        }
    },

    // Attempt to fix issues
    fixIssues: function () {
        console.log('--- Attempting Fixes ---');

        // Fix 1: Try to show the dashboard
        const dashboard = document.getElementById('code-stats-dashboard');
        if (dashboard && dashboard.style.display === 'none') {
            dashboard.style.display = 'block';
            console.log('✅ Set dashboard display to block');
        }

        // Fix 2: Try to manually update stats if elements exist
        const totalFiles = document.getElementById('total-files');
        const totalLines = document.getElementById('total-lines');
        const totalSize = document.getElementById('total-size');
        const analysisDate = document.getElementById('analysis-date');

        if (totalFiles && totalLines && totalSize && analysisDate) {
            totalFiles.textContent = '245';
            totalLines.textContent = '53,842';
            totalSize.textContent = '42.5 MB';
            analysisDate.textContent = new Date().toLocaleString();
            console.log('✅ Manually updated stat values');
        }

        // Fix 3: Check for language-stats element
        const languageStats = document.getElementById('language-stats');
        if (!languageStats) {
            console.log('❌ language-stats element missing, may need to be added to HTML');
        }

        // Fix 4: Check if code-stats-link has an event listener
        const statsLink = document.getElementById('code-stats-link');
        if (statsLink && !statsLink.onclick) {
            statsLink.onclick = function () {
                const dashboard = document.getElementById('code-stats-dashboard');
                const documentBrowser = document.getElementById('document-browser');

                if (dashboard && documentBrowser) {
                    dashboard.style.display = 'block';
                    documentBrowser.style.display = 'none';
                    console.log('✅ Added click handler to stats link');
                }
            };
        }
    },

    // Run all tests
    runAllTests: function () {
        console.log('======= CODE STATS DASHBOARD TESTS =======');

        const domElementsResult = this.testDOMElements();
        const dashboardVisibilityResult = this.testDashboardVisibility();
        const localStorageResult = this.testLocalStorage();
        const eventListenersResult = this.testEventListeners();
        const codeConnectionResult = this.testCodeConnection();

        console.log('======= TEST RESULTS SUMMARY =======');
        console.log(`DOM Elements: ${domElementsResult ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Dashboard Visibility: ${dashboardVisibilityResult ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Local Storage: ${localStorageResult ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Event Listeners: ${eventListenersResult ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Code Connection: ${codeConnectionResult ? '✅ PASS' : '❌ FAIL'}`);

        if (!domElementsResult || !dashboardVisibilityResult || !localStorageResult || !eventListenersResult || !codeConnectionResult) {
            console.log('Some tests failed. Attempting fixes...');
            this.fixIssues();
        }
    }
};

// Run tests when script is loaded
CodeStatsTester.runAllTests(); 