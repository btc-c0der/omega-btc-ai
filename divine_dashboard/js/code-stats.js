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

// Code Statistics Dashboard functionality
// Make the function globally accessible so it can be called from main.js
window.initCodeStats = function () {
    console.log('Initializing Code Stats Dashboard');

    // Elements
    const refreshBtn = document.getElementById('refresh-stats');
    const sortSelect = document.getElementById('sort-by');
    const statsTable = document.getElementById('stats-table-body');
    const totalFilesEl = document.getElementById('total-files');
    const totalLinesEl = document.getElementById('total-lines');
    const totalSizeEl = document.getElementById('total-size');
    const analysisDateEl = document.getElementById('analysis-date');

    // Chart elements
    const linesChart = document.getElementById('lines-chart');
    const filesChart = document.getElementById('files-chart');

    let codeStats = null;
    let charts = {
        lines: null,
        files: null
    };

    // Function to fetch and update statistics
    function updateCodeStatistics() {
        // In a real implementation, this would fetch data from the server
        // For now, we'll use sample data
        const statistics = {
            totalFiles: 248,
            totalDirectories: 42,
            totalLines: 53842,
            lastUpdated: new Date().toLocaleString(),
            languages: {
                "Python": 32,
                "JavaScript": 48,
                "HTML": 25,
                "CSS": 18,
                "Markdown": 125
            }
        };

        // Update the statistics in the dashboard
        if (totalFilesEl) totalFilesEl.textContent = statistics.totalFiles;
        if (totalLinesEl) totalLinesEl.textContent = statistics.totalLines.toLocaleString();
        if (analysisDateEl) analysisDateEl.textContent = statistics.lastUpdated;

        // Set total size (this wasn't in the original statistics object)
        if (totalSizeEl) totalSizeEl.textContent = '42.5 MB';

        // Since we don't have a language-stats element in the HTML, we'll use
        // the stats-table-body to display language distribution
        if (statsTable) {
            statsTable.innerHTML = '';

            for (const [language, count] of Object.entries(statistics.languages)) {
                const percentage = Math.round((count / statistics.totalFiles) * 100);

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${language}</td>
                    <td>${count}</td>
                    <td>${percentage}%</td>
                    <td>${Math.round(statistics.totalLines * (percentage / 100))}</td>
                    <td>${Math.round(statistics.totalLines / count)}</td>
                `;
                statsTable.appendChild(row);
            }
        }

        // Generate simple charts if Chart.js is available
        if (typeof Chart !== 'undefined' && linesChart && filesChart) {
            // Create/update charts
            createCharts(statistics);
        }
    }

    // Function to create charts
    function createCharts(statistics) {
        const languages = Object.keys(statistics.languages);
        const counts = Object.values(statistics.languages);
        const backgroundColors = languages.map(getColorForLanguage);

        // Destroy existing charts if they exist
        if (charts.lines) charts.lines.destroy();
        if (charts.files) charts.files.destroy();

        // Create lines chart
        charts.lines = new Chart(linesChart.getContext('2d'), {
            type: 'bar',
            data: {
                labels: languages,
                datasets: [{
                    label: 'Files by Language',
                    data: counts,
                    backgroundColor: backgroundColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        // Create files chart
        charts.files = new Chart(filesChart.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: languages,
                datasets: [{
                    data: counts,
                    backgroundColor: backgroundColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Function to get a color for a language
    function getColorForLanguage(language) {
        const colors = {
            "Python": "#3572A5",
            "JavaScript": "#f1e05a",
            "HTML": "#e34c26",
            "CSS": "#563d7c",
            "Markdown": "#083fa1",
            "default": "#6e7681"
        };

        return colors[language] || colors.default;
    }

    // Set up click handler for refresh button
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function () {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt spinning"></i> Refreshing...';

            // Simulate API call delay
            setTimeout(function () {
                updateCodeStatistics();
                refreshBtn.disabled = false;
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
            }, 1000);
        });
    }

    // Set up sort functionality
    if (sortSelect) {
        sortSelect.addEventListener('change', updateCodeStatistics);
    }

    // Initial update
    updateCodeStatistics();

    // Ensure dashboard is visible
    const dashboard = document.getElementById('code-stats-dashboard');
    if (dashboard) {
        dashboard.style.display = 'block';
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    // We don't auto-initialize here anymore, 
    // as it will be triggered by the click handler in main.js

    // However, if there's a hash in the URL with #stats, show stats directly
    if (window.location.hash === '#stats') {
        window.initCodeStats();
    }
}); 