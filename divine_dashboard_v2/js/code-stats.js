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

// Initialize localStorage with default stats if it doesn't exist
(function initializeLocalStorage() {
    if (!localStorage.getItem('omega_code_stats')) {
        console.log('Creating initial statistics in localStorage');
        // Create initial stats data
        const initialStats = {
            total_files: 248,
            total_lines: 53842,
            total_bytes: 44563200, // ~42.5MB
            last_updated: new Date().toISOString(),
            by_extension: {
                "py": { files: 32, lines: 12450 },
                "js": { files: 48, lines: 15890 },
                "html": { files: 25, lines: 8750 },
                "css": { files: 18, lines: 6300 },
                "md": { files: 125, lines: 10452 }
            }
        };
        localStorage.setItem('omega_code_stats', JSON.stringify(initialStats));
    }
})();

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

    // Function to fetch and update statistics - also made globally accessible
    window.updateCodeStatistics = function () {
        // Try to get stats from localStorage first
        let statistics;
        try {
            const savedStats = localStorage.getItem('omega_code_stats');
            if (savedStats) {
                const parsed = JSON.parse(savedStats);
                statistics = {
                    totalFiles: parsed.total_files,
                    totalLines: parsed.total_lines,
                    totalBytes: parsed.total_bytes,
                    lastUpdated: new Date(parsed.last_updated).toLocaleString(),
                    languages: {}
                };

                // Convert by_extension to languages format
                for (const [ext, data] of Object.entries(parsed.by_extension)) {
                    const languageName = getLanguageFromExtension(ext);
                    statistics.languages[languageName] = data.files;
                }
            } else {
                // This shouldn't happen as we initialize localStorage at the start,
                // but keeping as a fallback
                console.warn('No stats found in localStorage, creating new data');

                // Fallback to sample data
                statistics = {
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

                // Create localStorage entry for future use
                const initialStats = {
                    total_files: statistics.totalFiles,
                    total_lines: statistics.totalLines,
                    total_bytes: 44563200, // ~42.5MB
                    last_updated: new Date().toISOString(),
                    by_extension: {
                        "py": { files: 32, lines: 12450 },
                        "js": { files: 48, lines: 15890 },
                        "html": { files: 25, lines: 8750 },
                        "css": { files: 18, lines: 6300 },
                        "md": { files: 125, lines: 10452 }
                    }
                };
                localStorage.setItem('omega_code_stats', JSON.stringify(initialStats));
            }
        } catch (error) {
            console.error('Error parsing stats from localStorage:', error);
            // Fallback to sample data
            statistics = {
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
        }

        // Make the dashboard visible
        const dashboard = document.getElementById('code-stats-dashboard');
        if (dashboard) {
            dashboard.style.display = 'block';

            // If document browser exists, hide it
            const docBrowser = document.getElementById('document-browser');
            if (docBrowser) {
                docBrowser.style.display = 'none';
            }
        }

        // Update the statistics in the dashboard
        if (totalFilesEl) totalFilesEl.textContent = statistics.totalFiles;
        if (totalLinesEl) totalLinesEl.textContent = statistics.totalLines.toLocaleString();
        if (analysisDateEl) analysisDateEl.textContent = statistics.lastUpdated;

        // Set total size (using totalBytes from localStorage or fixed value)
        if (totalSizeEl) {
            const sizeInMB = statistics.totalBytes ? (statistics.totalBytes / (1024 * 1024)).toFixed(1) + ' MB' : '42.5 MB';
            totalSizeEl.textContent = sizeInMB;
        }

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
    };

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

    // Function to get a language name from a file extension
    function getLanguageFromExtension(ext) {
        const extensionMap = {
            "py": "Python",
            "js": "JavaScript",
            "html": "HTML",
            "css": "CSS",
            "md": "Markdown",
            "json": "JSON",
            "sh": "Shell",
            "yml": "YAML",
            "yaml": "YAML",
            "ts": "TypeScript",
            "jsx": "React",
            "tsx": "React",
            "rb": "Ruby",
            "default": "Other"
        };

        return extensionMap[ext] || extensionMap.default;
    }

    // Set up sort functionality
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            // Call our global updateCodeStatistics function
            window.updateCodeStatistics();
        });
    }

    // Initial update
    window.updateCodeStatistics();
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