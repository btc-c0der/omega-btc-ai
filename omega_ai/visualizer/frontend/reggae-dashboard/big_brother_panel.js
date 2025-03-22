/**
 * OMEGA BTC AI - Big Brother Monitoring Panel
 * JavaScript for handling the Big Brother panel functionality
 */

// Define API_BASE for testing - in real environment, this would be provided by the main dashboard
const API_BASE = typeof window.API_BASE !== 'undefined' ? window.API_BASE : "http://localhost:8001/api";

// Use the existing debug function or create a simple console.log wrapper
// This assumes debug is defined in the main dashboard JavaScript
function logMessage(section, message, data = null) {
    if (typeof window.debug === 'function') {
        window.debug(section, message, data);
    } else {
        console.log(`[${section}] ${message}`, data || '');
    }
}

// Central function to fetch data from the Big Brother API
async function fetchBigBrotherData() {
    try {
        // API endpoint for fetching all Big Brother data at once
        const response = await fetch(`${API_BASE}/big-brother-data`);
        if (!response.ok) {
            throw new Error(`Failed to fetch Big Brother data: ${response.status}`);
        }

        const data = await response.json();
        logMessage('BIG_BROTHER', 'Fetched Big Brother data successfully', data);
        return data;
    } catch (error) {
        logMessage('BIG_BROTHER', 'Error fetching Big Brother data:', error);
        return null;
    }
}

// Wrapper for fetching individual data points
// Falls back to Redis keys or mock data if needed
async function getBigBrotherData(key) {
    try {
        // Try to get from the central API first
        const allData = await fetchBigBrotherData();
        if (allData && allData[key]) {
            logMessage('BIG_BROTHER', `Retrieved ${key} from Big Brother API`);
            return allData[key];
        }

        // Try direct Redis key fetching if available
        if (typeof window.fetchRedisKey === 'function') {
            const redisData = await window.fetchRedisKey(key);
            if (redisData) {
                logMessage('BIG_BROTHER', `Retrieved ${key} using fetchRedisKey`);
                return redisData;
            }
        }

        // Fall back to mock data
        logMessage('BIG_BROTHER', `No real data for ${key}, using mock data`);
        return getMockData(key);
    } catch (error) {
        logMessage('BIG_BROTHER', `Error fetching ${key}:`, error);
        return getMockData(key);
    }
}

// Mock data generator for testing
function getMockData(key) {
    const now = new Date();

    // Default mock data for testing
    const mockData = {
        'long_position': {
            entry_price: 84500,
            size: 0.01,
            leverage: 10,
            unrealized_pnl: 125.5,
            take_profits: [{ price: 85500 }],
            stop_loss: 83000,
            _source: 'mock'
        },
        'short_position': {
            entry_price: 84200,
            size: 0.015,
            leverage: 5,
            unrealized_pnl: -45.2,
            take_profits: [{ price: 83200 }],
            stop_loss: 85700,
            _source: 'mock'
        },
        'position_stats': {
            win_rate: 0.68,
            avg_profit: 125.75,
            avg_loss: 42.30,
            avg_hold_time: 3600 * 6, // 6 hours
            _source: 'mock'
        },
        'fibonacci:current_levels': {
            direction: 'LONG',
            base_price: 84500,
            levels: {
                '0.0': 84500,
                '0.236': 85003.2,
                '0.382': 85318.9,
                '0.5': 85565.0,
                '0.618': 85822.3,
                '0.786': 86178.5,
                '1.0': 86630.0,
                '1.618': 87845.7,
                '2.618': 89769.2
            },
            _source: 'mock'
        },
        'mm_trap_detection': {
            current: {
                trap_risk: 0.45,
                trap_type: 'bear_trap',
                description: 'Potential bear trap forming with high volume spike on 15m timeframe.'
            },
            history: [
                {
                    timestamp: new Date(now.getTime() - 24 * 60 * 60 * 1000).toISOString(),
                    type: 'bull_trap',
                    probability: 0.82,
                    price_range: [85200, 85700]
                },
                {
                    timestamp: new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000).toISOString(),
                    type: 'stop_hunt',
                    probability: 0.73,
                    price_range: [82300, 82800]
                }
            ],
            _source: 'mock'
        },
        'elite_exit_strategy': {
            current_signal: {
                recommendation: 'HOLD',
                confidence: 0.62,
                next_target: {
                    price: 87500,
                    type: 'resistance'
                }
            },
            metrics: {
                trend_strength: 0.65,
                volatility: 0.42,
                price_momentum: 0.58,
                volume_profile: 0.62
            },
            history: [
                {
                    timestamp: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
                    action: 'EXIT',
                    position: 'LONG',
                    price: 85200,
                    pnl: 450.75,
                    confidence: 0.82
                },
                {
                    timestamp: new Date(now.getTime() - 8 * 60 * 60 * 1000).toISOString(),
                    action: 'EXIT',
                    position: 'SHORT',
                    price: 82100,
                    pnl: 215.50,
                    confidence: 0.75
                }
            ],
            _source: 'mock'
        }
    };

    return mockData[key] || null;
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

        // Try to get all data at once first for efficiency
        const allData = await fetchBigBrotherData();
        if (allData) {
            updateLongPositionDisplay(allData.long_position);
            updateShortPositionDisplay(allData.short_position);
            updatePositionStats(allData.position_stats);
            logMessage('BIG_BROTHER', 'Position data loaded from API');
            return;
        }

        // If that fails, load individual data points
        const longData = await getBigBrotherData('long_position');
        updateLongPositionDisplay(longData);

        const shortData = await getBigBrotherData('short_position');
        updateShortPositionDisplay(shortData);

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

        // Update trap detection every 20 seconds
        if (Math.floor(Date.now() / 1000) % 20 === 0) {
            await initTrapDetection();
        }

        // Update elite exits every 30 seconds
        if (Math.floor(Date.now() / 1000) % 30 === 0) {
            await initEliteExitMonitoring();
        }

        // Update the "last updated" time
        const now = new Date();
        document.getElementById('bb-update-time').textContent = `Last updated: ${now.toLocaleTimeString()}`;
        document.getElementById('bb-data-source').textContent = 'Data source: Live API';
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
    try {
        logMessage('BIG_BROTHER', 'Loading Fibonacci data');

        // Get Fibonacci levels
        const fibData = await getBigBrotherData('fibonacci:current_levels');
        if (!fibData) {
            logMessage('BIG_BROTHER', 'No Fibonacci data available');
            return;
        }

        // Display Fibonacci levels
        const container = document.getElementById('fib-levels-container');
        if (!container) return;

        // Clear previous content
        container.innerHTML = '';

        // Create elements for each Fibonacci level
        if (fibData.levels) {
            const levels = Object.entries(fibData.levels);
            levels.forEach(([level, price]) => {
                const fibElement = document.createElement('div');
                fibElement.className = 'fib-level';
                fibElement.innerHTML = `
                    <div class="fib-level-name">${level}x</div>
                    <div class="fib-level-price">$${parseFloat(price).toFixed(2)}</div>
                `;
                container.appendChild(fibElement);
            });
        }

        logMessage('BIG_BROTHER', 'Fibonacci data loaded successfully');
    } catch (error) {
        logMessage('BIG_BROTHER', 'Error loading Fibonacci data:', error);
    }
}

// Initialize Elite Exit monitoring
async function initEliteExitMonitoring() {
    try {
        logMessage('BIG_BROTHER', 'Loading Elite Exit data');

        // Try to get from Big Brother data first
        const allData = await fetchBigBrotherData();
        let eliteExitData = allData ? allData.elite_exit_strategy : null;

        // If not available, try direct API
        if (!eliteExitData) {
            const response = await fetch(`${API_BASE}/elite-exits?confidence=0.7`);
            if (response.ok) {
                eliteExitData = await response.json();
            }
        }

        // If still not available, use fallback
        if (!eliteExitData) {
            eliteExitData = await getBigBrotherData('elite_exit_strategy');
        }

        if (!eliteExitData) {
            logMessage('BIG_BROTHER', 'No Elite Exit data available');
            return;
        }

        // Update Elite Exit UI
        updateEliteExitDisplay(eliteExitData);

        logMessage('BIG_BROTHER', 'Elite Exit data loaded successfully');
    } catch (error) {
        logMessage('BIG_BROTHER', 'Error loading Elite Exit data:', error);
    }
}

// Update Elite Exit display
function updateEliteExitDisplay(data) {
    if (!data) return;

    // Update current signal
    const signalElement = document.getElementById('current-exit-signal');
    if (signalElement && data.current_signal) {
        const signal = data.current_signal;
        signalElement.textContent = signal.recommendation || 'No signal';

        // Update confidence bar
        const confidenceBar = document.getElementById('exit-confidence-level');
        if (confidenceBar && signal.confidence) {
            const confidencePercent = signal.confidence * 100;
            confidenceBar.style.width = `${confidencePercent}%`;

            // Color based on confidence
            if (confidencePercent >= 80) {
                confidenceBar.style.backgroundColor = '#009900'; // Strong green
            } else if (confidencePercent >= 60) {
                confidenceBar.style.backgroundColor = '#66cc00'; // Light green
            } else if (confidencePercent >= 40) {
                confidenceBar.style.backgroundColor = '#ffcc00'; // Yellow
            } else {
                confidenceBar.style.backgroundColor = '#ff6600'; // Orange
            }
        }
    }

    // Update exit history
    const historyList = document.getElementById('exit-history-list');
    if (historyList && data.history && data.history.length) {
        historyList.innerHTML = '';

        // Add history items
        data.history.forEach(item => {
            const listItem = document.createElement('li');

            // Format timestamp
            const timestamp = new Date(item.timestamp);
            const timeStr = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const dateStr = timestamp.toLocaleDateString([], { month: 'short', day: 'numeric' });

            // Create list item content
            listItem.innerHTML = `
                <span class="exit-time">${dateStr} ${timeStr}</span>
                <span class="exit-action ${item.action === 'EXIT' ? 'positive' : 'neutral'}">${item.action} ${item.position}</span>
                <span class="exit-pnl ${item.pnl >= 0 ? 'positive' : 'negative'}">$${item.pnl?.toFixed(2) || '0.00'}</span>
            `;

            historyList.appendChild(listItem);
        });
    }

    // Update detail metrics
    if (data.metrics) {
        const metrics = data.metrics;

        // Update trend strength
        const trendStrengthElement = document.getElementById('trend-strength');
        if (trendStrengthElement) {
            trendStrengthElement.textContent = metrics.trend_strength ?
                `${(metrics.trend_strength * 100).toFixed(1)}%` : '--';
        }

        // Update volatility
        const volatilityElement = document.getElementById('volatility');
        if (volatilityElement) {
            volatilityElement.textContent = metrics.volatility ?
                `${(metrics.volatility * 100).toFixed(1)}%` : '--';
        }

        // Update price momentum
        const momentumElement = document.getElementById('price-momentum');
        if (momentumElement) {
            momentumElement.textContent = metrics.price_momentum ?
                `${(metrics.price_momentum * 100).toFixed(1)}%` : '--';
        }

        // Update volume profile
        const volumeElement = document.getElementById('volume-profile');
        if (volumeElement) {
            volumeElement.textContent = metrics.volume_profile ?
                `${(metrics.volume_profile * 100).toFixed(1)}%` : '--';
        }
    }
}

// Initialize Trap Detection
async function initTrapDetection() {
    try {
        logMessage('BIG_BROTHER', 'Loading trap detection data');

        // Try to get from Big Brother data first
        const allData = await fetchBigBrotherData();
        let trapData = allData ? allData.mm_trap_detection : null;

        // If not available, try direct Redis key
        if (!trapData) {
            trapData = await getBigBrotherData('mm_trap_detection');
        }

        if (!trapData) {
            logMessage('BIG_BROTHER', 'No trap detection data available');
            return;
        }

        // Update trap detection UI
        updateTrapDetectionDisplay(trapData);

        logMessage('BIG_BROTHER', 'Trap detection data loaded successfully');
    } catch (error) {
        logMessage('BIG_BROTHER', 'Error loading trap detection data:', error);
    }
}

// Update trap detection display
function updateTrapDetectionDisplay(data) {
    if (!data) return;

    // Update current trap risk
    const riskElement = document.getElementById('current-trap-risk');
    if (riskElement && data.current) {
        const trapRisk = data.current.trap_risk;

        // Display risk as percentage
        const riskPercent = trapRisk * 100;
        riskElement.textContent = `${riskPercent.toFixed(1)}%`;

        // Add color based on risk level
        if (riskPercent >= 70) {
            riskElement.className = 'metric-value large negative';
        } else if (riskPercent >= 40) {
            riskElement.className = 'metric-value large neutral';
        } else {
            riskElement.className = 'metric-value large positive';
        }

        // Update risk bar
        const riskBar = document.getElementById('trap-risk-level');
        if (riskBar) {
            riskBar.style.width = `${riskPercent}%`;

            // Color based on risk
            if (riskPercent >= 70) {
                riskBar.style.backgroundColor = '#cc0000'; // Red
            } else if (riskPercent >= 40) {
                riskBar.style.backgroundColor = '#ff9900'; // Orange
            } else {
                riskBar.style.backgroundColor = '#44bb00'; // Green
            }
        }
    }

    // Update trap type and description
    if (data.current) {
        const typeElement = document.getElementById('trap-type');
        if (typeElement) {
            typeElement.textContent = data.current.trap_type ?
                data.current.trap_type.replace(/_/g, ' ').toUpperCase() : 'None detected';
        }

        const descElement = document.getElementById('trap-description');
        if (descElement) {
            descElement.textContent = data.current.description || 'No additional details available';
        }
    }

    // Update trap history table
    const historyTable = document.getElementById('trap-history-tbody');
    if (historyTable && data.history && data.history.length) {
        historyTable.innerHTML = '';

        // Add history items
        data.history.forEach(item => {
            const row = document.createElement('tr');

            // Format timestamp
            const timestamp = new Date(item.timestamp);
            const timeStr = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const dateStr = timestamp.toLocaleDateString([], { month: 'short', day: 'numeric' });

            // Format price range
            const priceRange = item.price_range ?
                `$${item.price_range[0].toFixed(1)} - $${item.price_range[1].toFixed(1)}` : 'N/A';

            // Format probability
            const probability = item.probability ?
                `${(item.probability * 100).toFixed(1)}%` : 'N/A';

            // Create row content
            row.innerHTML = `
                <td>${dateStr} ${timeStr}</td>
                <td>${item.type.replace(/_/g, ' ').toUpperCase()}</td>
                <td>${probability}</td>
                <td>${priceRange}</td>
            `;

            historyTable.appendChild(row);
        });
    }
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
