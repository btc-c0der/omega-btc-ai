/**
 * OMEGA Divine Code Statistics - Standalone Dashboard
 * This is a dedicated script for the code-stats.html standalone window
 */

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initializing Standalone Code Stats Dashboard');
    initCodeStats();
});

// Main initialization function
function initCodeStats() {
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

    // Function to simulate running the code analysis script
    async function simulateCodeAnalysis() {
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt spinning"></i> Analyzing...';
        }

        try {
            // Create a more extensive stats object for the standalone view
            const simulatedStats = {
                by_extension: {
                    ".py": { files: 312, lines: 98500, bytes: 3200000 },
                    ".js": { files: 142, lines: 35200, bytes: 980000 },
                    ".html": { files: 98, lines: 22800, bytes: 595000 },
                    ".css": { files: 34, lines: 8500, bytes: 245000 },
                    ".md": { files: 185, lines: 42000, bytes: 1240000 },
                    ".json": { files: 52, lines: 6800, bytes: 325000 },
                    ".txt": { files: 28, lines: 3600, bytes: 118000 },
                    ".csv": { files: 15, lines: 12000, bytes: 580000 },
                    ".ipynb": { files: 45, lines: 18800, bytes: 1220000 },
                    ".yml": { files: 27, lines: 1350, bytes: 58000 },
                    ".sol": { files: 22, lines: 5400, bytes: 180000 },
                    ".jsx": { files: 65, lines: 18200, bytes: 620000 },
                    ".ts": { files: 94, lines: 28600, bytes: 980000 },
                    ".tsx": { files: 76, lines: 22400, bytes: 760000 },
                    ".go": { files: 48, lines: 12600, bytes: 420000 },
                    ".rs": { files: 36, lines: 9800, bytes: 340000 },
                    ".c": { files: 24, lines: 7200, bytes: 260000 },
                    ".cpp": { files: 18, lines: 5600, bytes: 210000 },
                    ".h": { files: 32, lines: 4800, bytes: 160000 },
                    ".java": { files: 16, lines: 6400, bytes: 230000 }
                },
                total_files: 1369,
                total_lines: 370750,
                total_bytes: 12726000,
                last_analysis: new Date().toISOString()
            };

            // Simulate network delay
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Save to localStorage to persist between sessions
            localStorage.setItem('omega_code_stats', JSON.stringify(simulatedStats));

            codeStats = simulatedStats;
            renderCodeStats();
        } catch (error) {
            console.error('Error simulating code analysis:', error);
            alert(`Failed to run code analysis simulation: ${error.message}`);
        } finally {
            if (refreshBtn) {
                refreshBtn.disabled = false;
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
            }
        }
    }

    // Function to load code stats
    async function loadCodeStats() {
        try {
            // In a real implementation, this would fetch from an API
            // For now, we'll use localStorage or simulate if not available
            const savedStats = localStorage.getItem('omega_code_stats');

            if (savedStats) {
                codeStats = JSON.parse(savedStats);
                renderCodeStats();
            } else {
                // No saved stats, simulate first run
                await simulateCodeAnalysis();
            }
        } catch (error) {
            console.error('Error loading code stats:', error);
            if (statsTable) {
                statsTable.innerHTML = `<tr><td colspan="5" class="error">Error loading code statistics: ${error.message}</td></tr>`;
            }
        }
    }

    // Function to render code stats
    function renderCodeStats() {
        if (!codeStats) return;

        // Update summary cards
        if (totalFilesEl) totalFilesEl.textContent = formatNumber(codeStats.total_files);
        if (totalLinesEl) totalLinesEl.textContent = formatNumber(codeStats.total_lines);
        if (totalSizeEl) totalSizeEl.textContent = formatSize(codeStats.total_bytes);
        if (analysisDateEl) analysisDateEl.textContent = formatDate(codeStats.last_analysis);

        // Sort extensions
        const sortBy = sortSelect ? sortSelect.value : 'lines';
        const sortedExtensions = Object.entries(codeStats.by_extension)
            .sort((a, b) => {
                if (sortBy === 'extension') {
                    return a[0].localeCompare(b[0]);
                } else {
                    return b[1][sortBy] - a[1][sortBy];
                }
            });

        // Render table
        if (statsTable) {
            statsTable.innerHTML = '';

            sortedExtensions.forEach(([ext, stats]) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${ext}</td>
                    <td>${formatNumber(stats.files)}</td>
                    <td>${formatNumber(stats.lines)}</td>
                    <td>${formatSize(stats.bytes)}</td>
                    <td>${(stats.lines / stats.files).toFixed(1)}</td>
                `;
                statsTable.appendChild(row);
            });
        }

        // Render charts
        renderCharts(sortedExtensions);
    }

    // Function to render charts
    function renderCharts(sortedExtensions) {
        // Take top 15 extensions for charts (to avoid overcrowding)
        const top15 = sortedExtensions.slice(0, 15);
        const labels = top15.map(item => item[0]);
        const linesData = top15.map(item => item[1].lines);
        const filesData = top15.map(item => item[1].files);
        const backgroundColors = labels.map(getColorForLanguage);

        // Lines of Code chart
        if (linesChart) {
            if (charts.lines) {
                charts.lines.destroy();
            }

            const ctx = linesChart.getContext('2d');
            charts.lines = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Lines of Code',
                        data: linesData,
                        backgroundColor: backgroundColors,
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `Lines: ${formatNumber(context.raw)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    }
                }
            });
        }

        // Files chart
        if (filesChart) {
            if (charts.files) {
                charts.files.destroy();
            }

            const ctx = filesChart.getContext('2d');
            charts.files = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Files',
                        data: filesData,
                        backgroundColor: backgroundColors,
                        borderColor: 'rgba(0, 0, 0, 0.3)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: 'rgba(255, 255, 255, 0.7)',
                                padding: 10,
                                font: {
                                    size: 11
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `Files: ${formatNumber(value)} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }

    // Function to get a color for a language extension
    function getColorForLanguage(ext) {
        const colors = {
            ".py": "#3572A5",
            ".js": "#f1e05a",
            ".html": "#e34c26",
            ".css": "#563d7c",
            ".md": "#083fa1",
            ".json": "#292929",
            ".txt": "#6e7681",
            ".csv": "#89e051",
            ".ipynb": "#DA5B0B",
            ".yml": "#cb171e",
            ".yaml": "#cb171e",
            ".sol": "#AA6746",
            ".jsx": "#61dafb",
            ".ts": "#3178c6",
            ".tsx": "#3178c6",
            ".go": "#00ADD8",
            ".rs": "#dea584",
            ".c": "#555555",
            ".cpp": "#f34b7d",
            ".h": "#555555",
            ".java": "#b07219"
        };

        return colors[ext] || '#6e7681';
    }

    // Utility functions
    function formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    function formatSize(bytes) {
        const units = ['B', 'KB', 'MB', 'GB'];
        let size = bytes;
        let unitIndex = 0;

        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }

        return `${size.toFixed(1)} ${units[unitIndex]}`;
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }

    // Set up click handler for refresh button
    if (refreshBtn) {
        refreshBtn.addEventListener('click', simulateCodeAnalysis);
    }

    // Set up sort functionality
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            renderCodeStats();
        });
    }

    // Initialize the dashboard
    loadCodeStats();
} 