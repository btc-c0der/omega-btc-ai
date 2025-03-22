/**
 * OMEGA BTC AI - Big Brother Monitoring Panel
 * JavaScript for handling the Big Brother panel functionality
 */

// Use the existing debug function or create a simple console.log wrapper
// This assumes debug is defined in the main dashboard JavaScript
function logMessage(section, message, data = null) {
    if (typeof debug === 'function') {
        debug(section, message, data);
    } else {
        console.log(`[${section}] ${message}`, data || '');
    }
}

// Wrapper for fetching Redis keys
// This assumes fetchRedisKey is defined in the main dashboard JavaScript
async function getBigBrotherData(key) {
    if (typeof fetchRedisKey === 'function') {
        return await fetchRedisKey(key);
    } else {
        // Mock data for testing
        console.log(`[BIG_BROTHER] Would fetch Redis key: ${key}`);
        return getMockData(key);
    }
}

// Mock data generator for testing
function getMockData(key) {
    switch (key) {
        case 'long_position':
            return {
                entry_price: 84500,
                size: 0.01,
                leverage: 10,
                unrealized_pnl: 125.5,
                take_profits: [{ price: 85500 }],
                stop_loss: 83000
            };
        case 'short_position':
            return {
                entry_price: 84200,
                size: 0.015,
                leverage: 5,
                unrealized_pnl: -45.2,
                take_profits: [{ price: 83200 }],
                stop_loss: 85700
            };
        case 'position_stats':
            return {
                win_rate: 0.68,
                avg_profit: 125.75,
                avg_loss: 42.30,
                avg_hold_time: 3600 * 6 // 6 hours
            };
        default:
            return null;
    }
}

// Initialize Big Brother panel functionality
function initBigBrotherPanel() {
    logMessage('BIG_BROTHER', 'Initializing Big Brother monitoring panel');

    // Setup tab navigation
    setupTabNavigation();

    // Setup panel controls
    setupPanelControls();

    // Initialize the position data
    initPositionData();

    // Initialize Fibonacci data
    initFibonacciData();

    // Initialize Elite Exit monitoring
    initEliteExitMonitoring();

    // Initialize Trap Detection
    initTrapDetection();

    // Start periodic updates
    startPeriodicUpdates();

    logMessage('BIG_BROTHER', 'Big Brother monitoring panel initialized');
}

// Tab navigation setup
function setupTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // Remove active class from all buttons
            tabBtns.forEach(b => b.classList.remove('active'));

            // Add active class to the clicked button
            this.classList.add('active');

            // Hide all tab panes
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Show the corresponding tab pane
            const tabName = this.getAttribute('data-tab');
            document.getElementById(`${tabName}-tab`).classList.add('active');

            logMessage('BIG_BROTHER', `Switched to tab: ${tabName}`);
        });
    });
}

// Setup panel control buttons
function setupPanelControls() {
    // Expand button
    const expandBtn = document.getElementById('expand-bb-btn');
    if (expandBtn) {
        expandBtn.addEventListener('click', function () {
            const bbPanel = document.querySelector('.big-brother-panel');
            bbPanel.classList.toggle('expanded');

            if (bbPanel.classList.contains('expanded')) {
                bbPanel.style.gridColumn = 'span 2';
                expandBtn.title = 'Collapse Panel';
                expandBtn.innerHTML = '<i class="fas fa-compress"></i>';
            } else {
                bbPanel.style.gridColumn = '';
                expandBtn.title = 'Expand Panel';
                expandBtn.innerHTML = '<i class="fas fa-expand"></i>';
            }

            logMessage('BIG_BROTHER', 'Panel expanded/collapsed');
        });
    }

    // Fullscreen button
    const fullscreenBtn = document.getElementById('fullscreen-bb-btn');
    const modal = document.getElementById('big-brother-modal');
    const modalContent = document.getElementById('big-brother-modal-content');

    if (fullscreenBtn && modal && modalContent) {
        fullscreenBtn.addEventListener('click', function () {
            // Clone the tab content to the modal
            const tabsContainer = document.querySelector('.tabs-container').cloneNode(true);
            modalContent.innerHTML = '';
            modalContent.appendChild(tabsContainer);

            // Show the modal
            modal.style.display = 'flex';

            // Setup tab navigation in the modal
            setupModalTabNavigation();

            logMessage('BIG_BROTHER', 'Entered fullscreen mode');
        });

        // Minimize button
        const minimizeBtn = document.getElementById('minimize-bb-btn');
        if (minimizeBtn) {
            minimizeBtn.addEventListener('click', function () {
                modal.style.display = 'none';
                logMessage('BIG_BROTHER', 'Exited fullscreen mode');
            });
        }

        // Close button
        const closeBtn = document.getElementById('close-bb-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                modal.style.display = 'none';
                logMessage('BIG_BROTHER', 'Closed fullscreen mode');
            });
        }
    }
}

// Setup tab navigation in the modal
function setupModalTabNavigation() {
    const modalTabBtns = document.querySelectorAll('#big-brother-modal .tab-btn');
    const modalTabPanes = document.querySelectorAll('#big-brother-modal .tab-pane');

    modalTabBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // Remove active class from all buttons
            modalTabBtns.forEach(b => b.classList.remove('active'));

            // Add active class to the clicked button
            this.classList.add('active');

            // Hide all tab panes
            modalTabPanes.forEach(pane => pane.classList.remove('active'));

            // Show the corresponding tab pane
            const tabName = this.getAttribute('data-tab');
            document.querySelector(`#big-brother-modal #${tabName}-tab`).classList.add('active');

            logMessage('BIG_BROTHER', `Switched to tab in modal: ${tabName}`);
        });
    });
}

// Initialize position data
async function initPositionData() {
    try {
        logMessage('BIG_BROTHER', 'Loading position data');

        // Load data for long position
        const longData = await getBigBrotherData('long_position');
        updateLongPositionDisplay(longData);

        // Load data for short position
        const shortData = await getBigBrotherData('short_position');
        updateShortPositionDisplay(shortData);

        // Load position statistics
        const statsData = await getBigBrotherData('position_stats');
        updatePositionStats(statsData);

        logMessage('BIG_BROTHER', 'Position data loaded successfully');
    } catch (error) {
        logMessage('BIG_BROTHER', 'Error loading position data:', error);
    }
}

// Update long position display
function updateLongPositionDisplay(data) {
    if (!data) {
        logMessage('BIG_BROTHER', 'No long position data available');
        return;
    }

    // Update the long position card
    document.getElementById('long-entry-price').textContent = data.entry_price ? `$${data.entry_price.toFixed(2)}` : '--';
    document.getElementById('long-size').textContent = data.size || '--';
    document.getElementById('long-leverage').textContent = data.leverage ? `${data.leverage}x` : '--';

    // Update PnL with color
    const pnlElement = document.getElementById('long-pnl');
    if (data.unrealized_pnl) {
        const pnlValue = data.unrealized_pnl;
        pnlElement.textContent = `$${pnlValue.toFixed(2)}`;
        pnlElement.className = 'value ' + (pnlValue >= 0 ? 'positive' : 'negative');
    } else {
        pnlElement.textContent = '--';
        pnlElement.className = 'value';
    }

    // Update take profit and stop loss
    if (data.take_profits && data.take_profits.length > 0) {
        document.getElementById('long-tp').textContent = `$${data.take_profits[0].price.toFixed(2)}`;
    } else {
        document.getElementById('long-tp').textContent = '--';
    }

    if (data.stop_loss) {
        document.getElementById('long-sl').textContent = `$${data.stop_loss.toFixed(2)}`;
    } else {
        document.getElementById('long-sl').textContent = '--';
    }
}

// Update short position display
function updateShortPositionDisplay(data) {
    if (!data) {
        logMessage('BIG_BROTHER', 'No short position data available');
        return;
    }

    // Update the short position card
    document.getElementById('short-entry-price').textContent = data.entry_price ? `$${data.entry_price.toFixed(2)}` : '--';
    document.getElementById('short-size').textContent = data.size || '--';
    document.getElementById('short-leverage').textContent = data.leverage ? `${data.leverage}x` : '--';

    // Update PnL with color
    const pnlElement = document.getElementById('short-pnl');
    if (data.unrealized_pnl) {
        const pnlValue = data.unrealized_pnl;
        pnlElement.textContent = `$${pnlValue.toFixed(2)}`;
        pnlElement.className = 'value ' + (pnlValue >= 0 ? 'positive' : 'negative');
    } else {
        pnlElement.textContent = '--';
        pnlElement.className = 'value';
    }

    // Update take profit and stop loss
    if (data.take_profits && data.take_profits.length > 0) {
        document.getElementById('short-tp').textContent = `$${data.take_profits[0].price.toFixed(2)}`;
    } else {
        document.getElementById('short-tp').textContent = '--';
    }

    if (data.stop_loss) {
        document.getElementById('short-sl').textContent = `$${data.stop_loss.toFixed(2)}`;
    } else {
        document.getElementById('short-sl').textContent = '--';
    }
}

// Update position statistics
function updatePositionStats(data) {
    if (!data) {
        logMessage('BIG_BROTHER', 'No position stats data available');
        return;
    }

    // Update the stats
    document.getElementById('win-rate').textContent = data.win_rate ? `${(data.win_rate * 100).toFixed(1)}%` : '--';
    document.getElementById('avg-profit').textContent = data.avg_profit ? `$${data.avg_profit.toFixed(2)}` : '--';
    document.getElementById('avg-loss').textContent = data.avg_loss ? `$${data.avg_loss.toFixed(2)}` : '--';
    document.getElementById('avg-hold-time').textContent = data.avg_hold_time ? formatHoldTime(data.avg_hold_time) : '--';
}

// Format hold time (in seconds) to a readable format
function formatHoldTime(seconds) {
    if (seconds < 60) {
        return `${seconds}s`;
    } else if (seconds < 3600) {
        return `${Math.floor(seconds / 60)}m`;
    } else if (seconds < 86400) {
        return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
    } else {
        return `${Math.floor(seconds / 86400)}d ${Math.floor((seconds % 86400) / 3600)}h`;
    }
}

// Start periodic updates
function startPeriodicUpdates() {
    // Update position data every 10 seconds
    setInterval(async function () {
        await initPositionData();

        // Update the "last updated" time
        const now = new Date();
        document.getElementById('bb-update-time').textContent = `Last updated: ${now.toLocaleTimeString()}`;
        document.getElementById('bb-data-source').textContent = 'Data source: Redis';
    }, 10000);
}

// Generate 3D Flow visualization
function generate3DFlow() {
    const hoursValue = document.getElementById('flow-hours').value;
    const container = document.getElementById('flow-visual-container');

    // Clear previous content
    container.innerHTML = '';

    // Show loading message
    container.innerHTML = '<div class="loading-spinner"></div><div class="loading-message">Generating 3D Flow visualization...</div>';

    // This would be an API call to generate and fetch the visualization
    // For now, we'll simulate the process

    setTimeout(function () {
        // Replace with actual visualization
        container.innerHTML = '<img src="/api/flow/3d?hours=' + hoursValue + '" alt="3D Flow Visualization" class="flow-image" />';

        // Update footer
        document.getElementById('bb-update-time').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        document.getElementById('bb-data-source').textContent = 'Data source: Flow Generator API';
    }, 2000);
}

// Generate 2D Flow chart
function generate2DFlow() {
    const hoursValue = document.getElementById('flow-hours').value;
    const container = document.getElementById('flow-visual-container');

    // Clear previous content
    container.innerHTML = '';

    // Show loading message
    container.innerHTML = '<div class="loading-spinner"></div><div class="loading-message">Generating 2D Flow chart...</div>';

    // This would be an API call to generate and fetch the visualization
    // For now, we'll simulate the process

    setTimeout(function () {
        // Replace with actual visualization
        container.innerHTML = '<img src="/api/flow/2d?hours=' + hoursValue + '" alt="2D Flow Chart" class="flow-image" />';

        // Update footer
        document.getElementById('bb-update-time').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        document.getElementById('bb-data-source').textContent = 'Data source: Flow Generator API';
    }, 1500);
}

// Initialize Fibonacci data
async function initFibonacciData() {
    // Implementation will be added when the API endpoints are available
}

// Initialize Elite Exit monitoring
async function initEliteExitMonitoring() {
    // Implementation will be added when the API endpoints are available
}

// Initialize Trap Detection
async function initTrapDetection() {
    // Implementation will be added when the API endpoints are available
}

// Add event listeners for flow generation buttons
document.addEventListener('DOMContentLoaded', function () {
    const generate3DBtn = document.getElementById('generate-3d-flow');
    if (generate3DBtn) {
        generate3DBtn.addEventListener('click', generate3DFlow);
    }

    const generate2DBtn = document.getElementById('generate-2d-flow');
    if (generate2DBtn) {
        generate2DBtn.addEventListener('click', generate2DFlow);
    }

    // Initialize when document is ready
    if (document.querySelector('.big-brother-panel')) {
        initBigBrotherPanel();
    }
});
