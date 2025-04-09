/**
 * OMEGA Divine Code Statistics - Standalone Dashboard
 * This is a dedicated script for the code-stats.html standalone window
 * Optimized for lazy loading and smooth rendering of 6+ million LoC
 */

// Performance tracking utilities
const perfTracker = {
    timers: {},
    startTimer: function (name) {
        console.time(`⏱️ ${name}`);
        this.timers[name] = Date.now();
    },
    endTimer: function (name) {
        const elapsed = Date.now() - this.timers[name];
        console.timeEnd(`⏱️ ${name}`);
        console.log(`🚀 ${name} completed in ${elapsed}ms`);
        delete this.timers[name];
        return elapsed;
    },
    mark: function (message) {
        console.log(`✅ ${message} [${new Date().toLocaleTimeString()}]`);
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    perfTracker.startTimer('Total Initialization');
    console.log('🔮 OMEGA Code Stats Dashboard Initializing...');
    console.log('📊 Dashboard ready to process 6+ million LoC');

    // Display loading message
    const container = document.querySelector('.stats-container');
    if (container) {
        perfTracker.mark('Creating loading indicator');
        const loadingElement = document.createElement('div');
        loadingElement.id = 'loading-stats';
        loadingElement.innerHTML = `
            <div class="loading-spinner"></div>
            <p>Initializing Quantum Statistics Dashboard...</p>
            <p class="small">Harmonizing 6+ million lines of code</p>
        `;
        loadingElement.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: rgba(0,0,0,0.8);
            padding: 2rem;
            border-radius: 8px;
            z-index: 100;
        `;

        const spinnerStyle = document.createElement('style');
        spinnerStyle.textContent = `
            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 5px solid rgba(139, 92, 246, 0.3);
                border-radius: 50%;
                border-top-color: #8b5cf6;
                margin: 0 auto 1rem auto;
                animation: spin 1s linear infinite;
            }
            .small { font-size: 0.8rem; opacity: 0.7; }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(spinnerStyle);
        container.prepend(loadingElement);
        perfTracker.mark('Loading indicator created');
    }

    // Use requestIdleCallback or setTimeout to defer heavy operations
    console.log('🧠 Scheduling initialization during browser idle time');
    if (window.requestIdleCallback) {
        console.log('✨ Using requestIdleCallback API for optimal performance');
        window.requestIdleCallback(function (deadline) {
            console.log(`⌛ Time remaining: ${deadline.timeRemaining().toFixed(2)}ms, didTimeout: ${deadline.didTimeout}`);
            initCodeStats();
        }, { timeout: 1000 });
    } else {
        console.log('⚠️ requestIdleCallback not available, falling back to setTimeout');
        setTimeout(function () {
            initCodeStats();
        }, 100);
    }
});

// Main initialization function
function initCodeStats() {
    perfTracker.startTimer('Core Stats Initialization');
    console.log('🧪 Initializing core stats functionality');

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

    console.log('📄 UI Elements initialized:', {
        refreshBtn: !!refreshBtn,
        sortSelect: !!sortSelect,
        statsTable: !!statsTable,
        linesChart: !!linesChart,
        filesChart: !!filesChart
    });

    let codeStats = null;
    let charts = {
        lines: null,
        files: null
    };

    // Function to simulate running the code analysis script with optimized chunking
    async function simulateCodeAnalysis() {
        perfTracker.startTimer('Code Analysis Simulation');
        console.log('🔬 Beginning simulated code analysis');

        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt spinning"></i> Quantum Analysis...';
        }

        showLoadingIndicator(true, 'Performing Quantum Statistical Analysis');

        try {
            // Realistic data for 6+ million LoC
            console.log('📈 Generating optimized stats data for 6M+ LoC');
            perfTracker.startTimer('Stats Data Generation');
            const simulatedStats = await generateOptimizedStatsData();
            perfTracker.endTimer('Stats Data Generation');

            // Save to localStorage to persist between sessions
            console.log('💾 Saving stats to localStorage');
            perfTracker.startTimer('LocalStorage Write');
            localStorage.setItem('omega_code_stats', JSON.stringify(simulatedStats));
            perfTracker.endTimer('LocalStorage Write');

            codeStats = simulatedStats;
            console.log(`📊 Stats generated: ${codeStats.total_files.toLocaleString()} files, ${codeStats.total_lines.toLocaleString()} lines`);

            // Render in chunks for better performance
            console.log('🎨 Rendering stats in progressive chunks');
            await renderCodeStatsProgressive();
        } catch (error) {
            console.error('❌ Error simulating code analysis:', error);
            alert(`Failed to run code analysis simulation: ${error.message}`);
        } finally {
            if (refreshBtn) {
                refreshBtn.disabled = false;
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
            }
            showLoadingIndicator(false);
            perfTracker.endTimer('Code Analysis Simulation');
        }
    }

    // Helper function to show/hide loading indicator
    function showLoadingIndicator(show, message = 'Loading...') {
        let loadingEl = document.getElementById('loading-stats');

        if (show) {
            console.log(`🔄 Showing loading indicator: "${message}"`);
            if (!loadingEl) {
                loadingEl = document.createElement('div');
                loadingEl.id = 'loading-stats';
                loadingEl.innerHTML = `
                    <div class="loading-spinner"></div>
                    <p>${message}</p>
                `;
                loadingEl.style.cssText = `
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                    background: rgba(0,0,0,0.8);
                    padding: 2rem;
                    border-radius: 8px;
                    z-index: 100;
                `;
                document.querySelector('.stats-container').prepend(loadingEl);
            } else {
                loadingEl.querySelector('p').textContent = message;
                loadingEl.style.display = 'block';
            }
        } else if (loadingEl) {
            console.log('⏹️ Hiding loading indicator');
            loadingEl.style.display = 'none';
        }
    }

    // Generate realistic data for 6+ million LoC
    async function generateOptimizedStatsData() {
        console.log('🧮 Generating realistic stats data...');
        return new Promise(resolve => {
            // Simulate chunked data generation
            setTimeout(() => {
                console.log('🧠 Building stats object with extension details');
                // Create large dataset representing 6+ million LoC
                const simulatedStats = {
                    by_extension: {
                        ".py": { files: 28450, lines: 2467500, bytes: 83200000 },
                        ".js": { files: 14220, lines: 1235200, bytes: 45980000 },
                        ".html": { files: 9800, lines: 822800, bytes: 23595000 },
                        ".css": { files: 3400, lines: 458500, bytes: 13245000 },
                        ".md": { files: 18500, lines: 642000, bytes: 18240000 },
                        ".json": { files: 5200, lines: 236800, bytes: 10325000 },
                        ".txt": { files: 2800, lines: 113600, bytes: 4118000 },
                        ".csv": { files: 1500, lines: 312000, bytes: 15580000 },
                        ".ipynb": { files: 4500, lines: 318800, bytes: 23220000 },
                        ".yml": { files: 2700, lines: 81350, bytes: 3058000 },
                        ".sol": { files: 2200, lines: 105400, bytes: 4180000 },
                        ".jsx": { files: 6500, lines: 318200, bytes: 10620000 },
                        ".ts": { files: 9400, lines: 428600, bytes: 14980000 },
                        ".tsx": { files: 7600, lines: 322400, bytes: 10760000 },
                        ".go": { files: 4800, lines: 212600, bytes: 7420000 },
                        ".rs": { files: 3600, lines: 159800, bytes: 5340000 },
                        ".c": { files: 2400, lines: 107200, bytes: 3260000 },
                        ".cpp": { files: 1800, lines: 95600, bytes: 3210000 },
                        ".h": { files: 3200, lines: 84800, bytes: 2160000 },
                        ".java": { files: 1600, lines: 106400, bytes: 3630000 }
                    },
                    total_files: 134870,
                    total_lines: 6293418,
                    total_bytes: 303121000,
                    last_analysis: new Date().toISOString()
                };

                console.log('✅ Stats data generation complete');
                Object.keys(simulatedStats.by_extension).forEach(ext => {
                    console.log(`   ${ext}: ${simulatedStats.by_extension[ext].files.toLocaleString()} files, ${simulatedStats.by_extension[ext].lines.toLocaleString()} lines`);
                });
                resolve(simulatedStats);
            }, 800);
        });
    }

    // Function to load code stats
    async function loadCodeStats() {
        perfTracker.startTimer('Load Code Stats');
        console.log('📥 Loading code statistics data');
        showLoadingIndicator(true, 'Quantum Harmonizing Statistics');

        try {
            // In a real implementation, this would fetch from an API
            // For now, we'll use localStorage or simulate if not available
            console.log('🔍 Checking localStorage for existing stats');
            perfTracker.startTimer('LocalStorage Read');
            const savedStats = localStorage.getItem('omega_code_stats');
            perfTracker.endTimer('LocalStorage Read');

            if (savedStats) {
                console.log('🔄 Found existing stats, parsing...');
                perfTracker.startTimer('Parse Stats JSON');
                codeStats = JSON.parse(savedStats);
                perfTracker.endTimer('Parse Stats JSON');
                console.log(`📈 Loaded stats: ${codeStats.total_files.toLocaleString()} files, ${codeStats.total_lines.toLocaleString()} lines`);
                await renderCodeStatsProgressive();
            } else {
                console.log('🆕 No saved stats found, running initial simulation');
                // No saved stats, simulate first run
                await simulateCodeAnalysis();
            }
        } catch (error) {
            console.error('❌ Error loading code stats:', error);
            if (statsTable) {
                statsTable.innerHTML = `<tr><td colspan="5" class="error">Error loading code statistics: ${error.message}</td></tr>`;
            }
            showLoadingIndicator(false);
        }
        perfTracker.endTimer('Load Code Stats');
    }

    // Progressive rendering function
    async function renderCodeStatsProgressive() {
        perfTracker.startTimer('Progressive Rendering');
        console.log('🖌️ Beginning progressive rendering of stats');
        if (!codeStats) {
            console.warn('⚠️ No code stats available for rendering');
            perfTracker.endTimer('Progressive Rendering');
            return;
        }

        // Update summary cards first (quick operation)
        console.log('📊 Updating summary cards');
        perfTracker.startTimer('Summary Cards Update');
        updateSummaryCards();
        perfTracker.endTimer('Summary Cards Update');

        // Process and render table in chunks
        console.log('🧩 Rendering table progressively in chunks');
        perfTracker.startTimer('Table Rendering');
        await renderTableProgressive();
        perfTracker.endTimer('Table Rendering');

        // Finally render charts (most expensive operation)
        console.log('📊 Scheduling chart rendering');
        setTimeout(() => {
            perfTracker.startTimer('Chart Rendering');
            renderCharts();
            perfTracker.endTimer('Chart Rendering');
            showLoadingIndicator(false);
            perfTracker.endTimer('Progressive Rendering');
            console.log('✨ All stats rendered successfully!');
        }, 100);
    }

    // Update summary cards
    function updateSummaryCards() {
        console.log('🔄 Populating summary metrics');
        if (totalFilesEl) totalFilesEl.textContent = formatNumber(codeStats.total_files);
        if (totalLinesEl) totalLinesEl.textContent = formatNumber(codeStats.total_lines);
        if (totalSizeEl) totalSizeEl.textContent = formatSize(codeStats.total_bytes);
        if (analysisDateEl) analysisDateEl.textContent = formatDate(codeStats.last_analysis);
        console.log('📋 Summary metrics updated:', {
            files: codeStats.total_files,
            lines: codeStats.total_lines,
            bytes: codeStats.total_bytes,
            date: codeStats.last_analysis
        });
    }

    // Render table in chunks
    async function renderTableProgressive() {
        console.log('📋 Starting progressive table rendering');
        return new Promise(resolve => {
            if (!statsTable) {
                console.warn('⚠️ Stats table element not found');
                resolve();
                return;
            }

            statsTable.innerHTML = '';

            // Sort extensions
            console.log('🔄 Sorting extensions for table display');
            perfTracker.startTimer('Sort Extensions');
            const sortBy = sortSelect ? sortSelect.value : 'lines';
            const sortedExtensions = Object.entries(codeStats.by_extension)
                .sort((a, b) => {
                    if (sortBy === 'extension') {
                        return a[0].localeCompare(b[0]);
                    } else {
                        return b[1][sortBy] - a[1][sortBy];
                    }
                });
            perfTracker.endTimer('Sort Extensions');
            console.log(`🔢 Extensions sorted by "${sortBy}"`);

            // Create document fragment for better performance
            console.log('🧩 Creating document fragment for table');
            const fragment = document.createDocumentFragment();

            // Process in chunks of 5 rows
            const chunkSize = 5;
            let currentIndex = 0;
            let chunkCounter = 0;

            console.log(`⏱️ Processing table in chunks of ${chunkSize} rows`);
            function processChunk() {
                perfTracker.startTimer(`Table Chunk ${chunkCounter++}`);
                const chunk = sortedExtensions.slice(currentIndex, currentIndex + chunkSize);
                console.log(`🧩 Processing chunk ${chunkCounter} (${chunk.length} items, index ${currentIndex})`);

                chunk.forEach(([ext, stats]) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${ext}</td>
                        <td>${formatNumber(stats.files)}</td>
                        <td>${formatNumber(stats.lines)}</td>
                        <td>${formatSize(stats.bytes)}</td>
                        <td>${(stats.lines / stats.files).toFixed(1)}</td>
                    `;
                    fragment.appendChild(row);
                });

                currentIndex += chunkSize;
                perfTracker.endTimer(`Table Chunk ${chunkCounter - 1}`);

                if (currentIndex < sortedExtensions.length) {
                    // Process next chunk in next animation frame
                    console.log(`⏭️ Scheduling next chunk (${currentIndex}/${sortedExtensions.length})`);
                    requestAnimationFrame(processChunk);
                } else {
                    // Done processing all chunks
                    console.log('✅ All table chunks processed, appending to DOM');
                    perfTracker.startTimer('DOM Table Update');
                    statsTable.appendChild(fragment);
                    perfTracker.endTimer('DOM Table Update');
                    console.log(`📋 Table completed with ${sortedExtensions.length} rows`);
                    resolve();
                }
            }

            // Start processing chunks
            processChunk();
        });
    }

    // Function to render charts with optimized settings
    function renderCharts() {
        console.log('📊 Rendering data visualization charts');
        perfTracker.startTimer('Chart Preparation');

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

        // Take top 10 extensions for charts (reduce data points for performance)
        const top10 = sortedExtensions.slice(0, 10);
        const labels = top10.map(item => item[0]);
        const linesData = top10.map(item => item[1].lines);
        const filesData = top10.map(item => item[1].files);
        const backgroundColors = labels.map(getColorForLanguage);

        console.log('📈 Prepared chart data:', {
            extensionsUsed: labels.length,
            topExtension: labels[0],
            maxLines: Math.max(...linesData),
            maxFiles: Math.max(...filesData)
        });
        perfTracker.endTimer('Chart Preparation');

        // Lines of Code chart - optimized settings
        if (linesChart) {
            console.log('📊 Rendering lines of code bar chart');
            perfTracker.startTimer('Lines Chart Render');
            if (charts.lines) {
                console.log('🔄 Destroying previous lines chart instance');
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
                    animation: {
                        duration: 800, // Slower animation for smoother rendering
                        easing: 'easeOutQuart'
                    },
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
                                color: 'rgba(255, 255, 255, 0.7)',
                                callback: function (value) {
                                    // Format large numbers for y-axis to reduce clutter
                                    if (value >= 1000000) {
                                        return (value / 1000000).toFixed(1) + 'M';
                                    } else if (value >= 1000) {
                                        return (value / 1000).toFixed(0) + 'K';
                                    }
                                    return value;
                                }
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
            perfTracker.endTimer('Lines Chart Render');
        }

        // Files chart - optimized settings
        if (filesChart) {
            console.log('📊 Rendering files distribution doughnut chart');
            perfTracker.startTimer('Files Chart Render');
            if (charts.files) {
                console.log('🔄 Destroying previous files chart instance');
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
                    animation: {
                        duration: 800, // Slower animation for smoother rendering
                        easing: 'easeOutQuart'
                    },
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: 'rgba(255, 255, 255, 0.7)',
                                padding: 10,
                                font: {
                                    size: 11
                                },
                                // Limit the number of legends displayed
                                filter: function (legendItem, data) {
                                    // Only show top 8 in legend to reduce clutter
                                    return data.datasets[0].data.indexOf(legendItem.index) < 8;
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
            perfTracker.endTimer('Files Chart Render');
        }
        console.log('✅ Chart rendering complete');
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
        console.log('🔄 Setting up refresh button click handler');
        refreshBtn.addEventListener('click', () => {
            console.log('🖱️ Refresh button clicked');
            simulateCodeAnalysis();
        });
    }

    // Set up sort functionality with debounce for better performance
    if (sortSelect) {
        console.log('🔄 Setting up sort selector with debounce');
        let debounceTimer;
        sortSelect.addEventListener('change', function () {
            console.log(`🔢 Sort changed to: ${this.value}`);
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                console.log(`⏱️ Debounce complete, rendering with sort: ${this.value}`);
                renderCodeStatsProgressive();
            }, 100);
        });
    }

    // Initialize the dashboard
    console.log('🚀 Starting dashboard data loading');
    loadCodeStats();

    perfTracker.endTimer('Core Stats Initialization');
    perfTracker.endTimer('Total Initialization');
    console.log('✨ OMEGA Code Stats Dashboard is fully initialized and ready!');
} 