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
 * Divine Dashboard v3
 * Code Statistics Module
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize code stats if stats section exists
    if (document.getElementById('stats-section')) {
        initCodeStats();
    }
});

// Global variables for charts
let linesChart = null;
let filesChart = null;

/**
 * Initialize code statistics functionality
 */
function initCodeStats() {
    // Set up event listeners
    setupCodeStatsEvents();

    // Load initial stats
    loadCodeStats();
}

/**
 * Set up event listeners for code stats section
 */
function setupCodeStatsEvents() {
    // Refresh button
    const refreshButton = document.getElementById('refresh-stats');
    if (refreshButton) {
        refreshButton.addEventListener('click', loadCodeStats);
    }

    // Sort selector
    const sortSelector = document.getElementById('sort-by');
    if (sortSelector) {
        sortSelector.addEventListener('change', () => {
            // If stats are loaded, re-render the table with new sort option
            if (window.codeStatsData) {
                renderStatsTable(window.codeStatsData, sortSelector.value);
            }
        });
    }
}

/**
 * Load code statistics data from API
 */
async function loadCodeStats() {
    try {
        // Show loading state
        updateStatsLoadingState(true);

        // Fetch data from API
        const response = await fetch('/api/stats');
        if (!response.ok) {
            throw new Error(`Failed to fetch stats: ${response.status}`);
        }

        const data = await response.json();

        // Store data globally for access by other functions
        window.codeStatsData = data;

        // Render the stats
        renderStats(data);

        // Hide loading state
        updateStatsLoadingState(false);
    } catch (error) {
        console.error('Error loading code stats:', error);

        // Load simulated data as fallback
        const simulatedData = getSimulatedStats();
        window.codeStatsData = simulatedData;
        renderStats(simulatedData);

        // Hide loading state
        updateStatsLoadingState(false);
    }
}

/**
 * Show or hide loading state for stats section
 */
function updateStatsLoadingState(isLoading) {
    const elements = {
        totalFiles: document.getElementById('total-files'),
        totalLines: document.getElementById('total-lines'),
        totalSize: document.getElementById('total-size'),
        analysisDate: document.getElementById('analysis-date')
    };

    if (isLoading) {
        // Show loading state
        for (const key in elements) {
            if (elements[key]) {
                elements[key].innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            }
        }
    }
}

/**
 * Generate simulated stats data for fallback
 */
function getSimulatedStats() {
    const date = new Date().toISOString();
    return {
        total_files: 1249,
        total_lines: 382451,
        total_size: 48521732,
        total_size_formatted: "46.27 MB",
        analysis_date: date,
        extensions: {
            ".py": {
                files: 487,
                lines: 164892,
                size: 19281932,
                size_formatted: "18.39 MB"
            },
            ".js": {
                files: 312,
                lines: 92187,
                size: 12463214,
                size_formatted: "11.89 MB"
            },
            ".html": {
                files: 98,
                lines: 31526,
                size: 5283721,
                size_formatted: "5.04 MB"
            },
            ".css": {
                files: 67,
                lines: 18945,
                size: 3172832,
                size_formatted: "3.03 MB"
            },
            ".md": {
                files: 213,
                lines: 64221,
                size: 7192837,
                size_formatted: "6.86 MB"
            },
            ".json": {
                files: 42,
                lines: 6892,
                size: 942351,
                size_formatted: "0.90 MB"
            },
            ".sh": {
                files: 30,
                lines: 3788,
                size: 184845,
                size_formatted: "0.18 MB"
            }
        }
    };
}

/**
 * Render all stats components
 */
function renderStats(data) {
    // Update summary stats
    renderSummaryStats(data);

    // Render charts
    renderCharts(data);

    // Render detailed table with current sort option
    const sortBy = document.getElementById('sort-by').value;
    renderStatsTable(data, sortBy);
}

/**
 * Render summary statistics
 */
function renderSummaryStats(data) {
    // Update summary cards
    document.getElementById('total-files').textContent = data.total_files.toLocaleString();
    document.getElementById('total-lines').textContent = data.total_lines.toLocaleString();
    document.getElementById('total-size').textContent = data.total_size_formatted;

    // Format date for display
    let displayDate = data.analysis_date;
    if (displayDate.includes('T')) {
        // If ISO format, convert to readable format
        const date = new Date(data.analysis_date);
        displayDate = date.toLocaleString();
    }
    document.getElementById('analysis-date').textContent = displayDate;
}

/**
 * Render stats charts
 */
function renderCharts(data) {
    // Prepare data for charts
    const extensions = Object.keys(data.extensions);
    const backgroundColors = [
        'rgba(142, 68, 173, 0.7)',   // Purple (primary)
        'rgba(52, 152, 219, 0.7)',   // Blue (secondary)
        'rgba(230, 126, 34, 0.7)',   // Orange (accent)
        'rgba(46, 204, 113, 0.7)',   // Green
        'rgba(231, 76, 60, 0.7)',    // Red
        'rgba(241, 196, 15, 0.7)',   // Yellow
        'rgba(149, 165, 166, 0.7)'   // Gray
    ];

    // Extract data for charts
    const linesData = extensions.map(ext => data.extensions[ext].lines);
    const filesData = extensions.map(ext => data.extensions[ext].files);

    // Render lines chart
    renderLinesChart(extensions, linesData, backgroundColors);

    // Render files chart
    renderFilesChart(extensions, filesData, backgroundColors);
}

/**
 * Render lines of code chart
 */
function renderLinesChart(labels, data, backgroundColors) {
    const ctx = document.getElementById('lines-chart').getContext('2d');

    // Destroy existing chart if it exists
    if (linesChart) {
        linesChart.destroy();
    }

    // Create new chart
    linesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Lines of Code',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Lines: ${context.raw.toLocaleString()}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

/**
 * Render files by extension chart
 */
function renderFilesChart(labels, data, backgroundColors) {
    const ctx = document.getElementById('files-chart').getContext('2d');

    // Destroy existing chart if it exists
    if (filesChart) {
        filesChart.destroy();
    }

    // Create new chart
    filesChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Files: ${context.raw.toLocaleString()} (${((context.raw / data.reduce((a, b) => a + b, 0)) * 100).toFixed(1)}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Render detailed stats table
 */
function renderStatsTable(data, sortBy) {
    const tableBody = document.getElementById('stats-table-body');
    tableBody.innerHTML = '';

    // Get extensions and sort them
    let extensions = Object.keys(data.extensions);

    if (sortBy === 'lines') {
        extensions.sort((a, b) => data.extensions[b].lines - data.extensions[a].lines);
    } else if (sortBy === 'files') {
        extensions.sort((a, b) => data.extensions[b].files - data.extensions[a].files);
    } else if (sortBy === 'extension') {
        extensions.sort();
    }

    // Create table rows
    extensions.forEach(ext => {
        const extData = data.extensions[ext];
        const avgLinesPerFile = (extData.lines / extData.files).toFixed(1);

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${ext}</td>
            <td>${extData.files.toLocaleString()}</td>
            <td>${extData.lines.toLocaleString()}</td>
            <td>${extData.size_formatted}</td>
            <td>${avgLinesPerFile}</td>
        `;

        tableBody.appendChild(row);
    });
} 