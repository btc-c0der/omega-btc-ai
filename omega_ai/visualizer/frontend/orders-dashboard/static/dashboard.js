/**
 * OMEGA BTC AI - Orders Dashboard
 * JavaScript for handling WebSocket connections and displaying live trading updates
 */

// Global variables
let socket;
let pnlChart;
let isPaused = false;
let currentBtcPrice = 0;
let orderLogFilter = 'all';
let pnlHistory = {
    labels: [],
    datasets: []
};

// DOM elements
const elements = {
    lastUpdate: document.getElementById('last-update'),
    systemStatus: document.getElementById('system-status'),
    totalPnl: document.getElementById('total-pnl'),
    activePositionsCount: document.getElementById('active-positions-count'),
    btcPrice: document.getElementById('btc-price'),
    traderStats: document.getElementById('trader-stats'),
    activePositions: document.getElementById('active-positions'),
    orderLog: document.getElementById('order-log'),
    pauseLogButton: document.getElementById('pause-log'),
    clearLogButton: document.getElementById('clear-log'),
    orderTypeFilter: document.getElementById('order-type-filter')
};

// Templates
const templates = {
    traderCard: document.getElementById('trader-card-template'),
    positionCard: document.getElementById('position-card-template'),
    orderLogEntry: document.getElementById('order-log-entry-template')
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the dashboard
    initDashboard();

    // Button event listeners
    const pauseLogButton = document.getElementById('pause-log');
    if (pauseLogButton) {
        pauseLogButton.addEventListener('click', togglePauseLog);
    }

    const clearLogButton = document.getElementById('clear-log');
    if (clearLogButton) {
        clearLogButton.addEventListener('click', clearOrderLog);
    }

    const logFilterDropdown = document.getElementById('log-filter');
    if (logFilterDropdown) {
        logFilterDropdown.addEventListener('change', filterOrderLog);
    }
});

/**
 * Initialize the dashboard and connect to WebSocket
 */
function initDashboard() {
    // Create PnL chart
    createPnlChart();

    // Connect to WebSocket
    connectWebSocket();
}

/**
 * Connect to the WebSocket server
 */
function connectWebSocket() {
    // Check if port is specified in URL parameters (for dynamic port configuration)
    const urlParams = new URLSearchParams(window.location.search);
    const portParam = urlParams.get('wsport');

    // Use the global configuration object if available, or default values
    const config = window.WEBSOCKET_CONFIG || {
        port: portParam || 8765, // Default to MM WebSocket server port 8765
        path: '/ws',
        reconnectDelay: 5000
    };

    // Build WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const host = window.location.hostname || 'localhost';
    const wsUrl = `${protocol}${host}:${config.port}${config.path}`;

    // Create WebSocket connection
    socket = new WebSocket(wsUrl);

    // WebSocket event handlers
    socket.onopen = handleSocketOpen;
    socket.onmessage = handleSocketMessage;
    socket.onerror = handleSocketError;
    socket.onclose = handleSocketClose;

    console.log(`Connecting to WebSocket at ${wsUrl}`);
}

/**
 * Handle WebSocket open event
 */
function handleSocketOpen() {
    console.log('WebSocket connection established');
    updateSystemStatus('CONNECTED', 'positive');
}

/**
 * Handle WebSocket message event
 */
function handleSocketMessage(event) {
    try {
        const message = JSON.parse(event.data);

        // Update last update time
        updateLastUpdateTime();

        // Process different message types
        if (message.btc_price) {
            // Update BTC price if available
            updateBtcPrice(message.btc_price);
        }

        if (message.system_status) {
            // Update system status
            updateSystemStatus(message.system_status, getStatusClass(message.system_status));
        }

        // Handle ticker data
        if (message.ticker_data) {
            updateTickerData(message.ticker_data);
        }

        // Check for full ticker data in log messages
        if (message.log && message.log.message.includes("Full ticker data")) {
            try {
                // Extract the JSON part from the log message
                const tickerJson = message.log.message.split("Full ticker data: ")[1];
                if (tickerJson) {
                    const tickerData = JSON.parse(tickerJson);
                    updateTickerData(tickerData);
                }
            } catch (e) {
                console.error("Error parsing ticker data:", e);
            }
        }

        if (message.trader_update) {
            // Update trader stats
            const trader = message.trader_update;
            updateTraderStats(trader.trader, trader.pnl, trader.active_positions);

            // Update total PnL
            updateTotalPnL();

            // Update active positions count
            updateActivePositionsCount();

            // Update PnL chart if there's a change
            updatePnLChart(trader.trader, trader.pnl);
        }

        if (message.position_update) {
            // Update position card
            const position = message.position_update;
            updatePositionCard(
                position.side,
                position.size,
                position.entry_price,
                position.unrealized_pnl,
                position.realized_pnl
            );
        }

        // Handle detailed position data from bridge
        if (message.detailed_position) {
            const position = message.detailed_position;

            // Add detailed position to the dashboard
            updateDetailedPositionCard(
                position.trader,
                position.symbol,
                position.side,
                position.contracts,
                position.entry_price,
                position.unrealized_pnl,
                position.leverage,
                position.liquidation_price,
                position.percentage,
                position.notional
            );

            // Also add an order log entry if this is a newly detected position
            addOrderLogEntry(
                `Position details: ${position.side.toUpperCase()} ${position.contracts} BTC (${position.trader})`,
                position.side === 'long' ? 'positive' : 'negative',
                message.btc_price,
                new Date(position.timestamp)
            );
        }

        if (message.new_order) {
            // Add new order to log
            const order = message.new_order;
            addOrderLogEntry(
                `New ${order.side.toUpperCase()} order (${order.trader})`,
                order.side === 'buy' ? 'positive' : 'negative',
                message.btc_price,
                new Date(order.timestamp)
            );
        }

        if (message.close_position) {
            // Add position closure to log
            const close = message.close_position;
            addOrderLogEntry(
                `Position closed (${close.trader})`,
                'neutral',
                message.btc_price,
                new Date(close.timestamp)
            );
        }

        if (message.error) {
            // Add error to log
            const error = message.error;
            addOrderLogEntry(
                `ERROR: ${error.message}`,
                'negative',
                message.btc_price,
                new Date(error.timestamp)
            );
        }

        if (message.log) {
            // Add generic log message
            const log = message.log;
            addOrderLogEntry(
                log.message,
                'neutral',
                message.btc_price,
                new Date(log.timestamp)
            );
        }

    } catch (error) {
        console.error('Error processing message:', error);
        console.error('Message data:', event.data);
    }
}

/**
 * Handle WebSocket error event
 */
function handleSocketError(error) {
    console.error('WebSocket error:', error);
    updateSystemStatus('ERROR', 'negative');
}

/**
 * Handle WebSocket close event
 */
function handleSocketClose(event) {
    console.log('WebSocket connection closed:', event);
    updateSystemStatus('DISCONNECTED', 'negative');

    // Use configured reconnect delay or default to 5000
    const config = window.WEBSOCKET_CONFIG || { reconnectDelay: 5000 };

    // Attempt to reconnect after delay
    setTimeout(() => {
        console.log('Attempting to reconnect...');
        connectWebSocket();
    }, config.reconnectDelay);
}

/**
 * Handle initial data from WebSocket
 */
function handleInitialData(data) {
    console.log('Received initial data');

    // Update system info
    if (data.system) {
        handleSystemUpdate({ system: data.system });
    }

    // Update positions
    if (data.positions) {
        handlePositionUpdate({ positions: data.positions });
    }

    // Add initial orders to log
    if (data.orders && data.orders.length > 0) {
        // Add orders in reverse order (newest last)
        [...data.orders].reverse().forEach(order => {
            switch (order.type) {
                case 'new_order':
                    handleNewOrder(order);
                    break;
                case 'close_position':
                    handleClosePosition(order);
                    break;
                case 'add_to_position':
                    handleAddToPosition(order);
                    break;
            }
        });
    }
}

/**
 * Handle new order message
 */
function handleNewOrder(data) {
    // Add to order log
    addOrderToLog({
        timestamp: data.timestamp,
        profile: data.profile,
        action: 'new_order',
        actionText: `New ${data.side}`,
        details: `${data.size} @ $${data.price.toFixed(2)} (${data.leverage}x)`
    });
}

/**
 * Handle close position message
 */
function handleClosePosition(data) {
    // Add to order log
    const pnlClass = data.pnl >= 0 ? 'positive' : 'negative';

    addOrderToLog({
        timestamp: data.timestamp,
        profile: data.profile,
        action: 'close_position',
        actionText: 'Close position',
        details: `PnL: <span class="${pnlClass}">$${data.pnl.toFixed(2)}</span>`,
        pnl: data.pnl
    });

    // Update PnL chart
    updatePnLChart(data);
}

/**
 * Handle add to position message
 */
function handleAddToPosition(data) {
    // Add to order log
    addOrderToLog({
        timestamp: data.timestamp,
        profile: data.profile,
        action: 'add_to_position',
        actionText: `Add to ${data.side}`,
        details: `${data.size} @ $${data.price.toFixed(2)}`
    });
}

/**
 * Handle position update message
 */
function handlePositionUpdate(data) {
    // Clear positions display
    elements.activePositions.innerHTML = '';

    // Add each position
    const positions = Object.values(data.positions);

    if (positions.length === 0) {
        elements.activePositions.innerHTML = '<div class="no-positions">No active positions</div>';
    } else {
        positions.forEach(position => {
            addPositionCard(position);
        });
    }

    // Update active positions count
    elements.activePositionsCount.textContent = positions.length;
}

/**
 * Handle system update message
 */
function handleSystemUpdate(data) {
    const system = data.system;

    // Update total PNL
    updateTotalPnl(system.total_pnl);

    // Update trader stats
    elements.traderStats.innerHTML = '';
    if (system.traders) {
        Object.entries(system.traders).forEach(([profile, stats]) => {
            addTraderCard(profile, stats);
        });
    }

    // Update system running status
    if (system.is_running !== undefined) {
        updateSystemStatus(system.is_running ? 'OPERATIONAL' : 'OFFLINE', system.is_running ? 'positive' : 'negative');
    }
}

/**
 * Handle market update message
 */
function handleMarketUpdate(data) {
    // Update BTC price
    currentBtcPrice = data.price;
    elements.btcPrice.textContent = `$${data.price.toFixed(2)}`;
}

/**
 * Add an order to the log
 */
function addOrderToLog(orderData) {
    if (isPaused) return;

    // Filter by order type
    if (orderLogFilter !== 'all' && orderLogFilter !== orderData.action) {
        return;
    }

    // Clone template
    const template = templates.orderLogEntry.content.cloneNode(true);

    // Format timestamp
    const date = new Date(orderData.timestamp);
    const formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Fill template
    template.querySelector('.log-timestamp').textContent = formattedTime;
    template.querySelector('.log-profile').textContent = orderData.profile;
    template.querySelector('.log-action').textContent = orderData.actionText;
    template.querySelector('.log-action').classList.add(orderData.action);
    template.querySelector('.log-details').innerHTML = orderData.details;

    // Add to log
    elements.orderLog.prepend(template);

    // Limit log entries to 100
    while (elements.orderLog.children.length > 100) {
        elements.orderLog.removeChild(elements.orderLog.lastChild);
    }
}

/**
 * Add a position card to the display
 */
function addPositionCard(position) {
    // Clone template
    const template = templates.positionCard.content.cloneNode(true);

    // Fill template
    template.querySelector('.position-profile').textContent = position.profile;

    const sideElement = template.querySelector('.position-side');
    sideElement.textContent = position.side.toUpperCase();
    sideElement.classList.add(position.side.toLowerCase());

    template.querySelector('.entry-price').textContent = `$${position.entry_price.toFixed(2)}`;
    template.querySelector('.current-price').textContent = `$${currentBtcPrice.toFixed(2)}`;
    template.querySelector('.position-size').textContent = position.size.toFixed(3);

    const pnlElement = template.querySelector('.position-pnl');
    pnlElement.textContent = `$${position.unrealized_pnl.toFixed(2)}`;
    pnlElement.classList.add(position.unrealized_pnl >= 0 ? 'positive' : 'negative');

    // Add to positions display
    elements.activePositions.appendChild(template);
}

/**
 * Add a trader card to the display
 */
function addTraderCard(profile, stats) {
    // Clone template
    const template = templates.traderCard.content.cloneNode(true);

    // Fill template
    template.querySelector('.trader-name').textContent = profile.charAt(0).toUpperCase() + profile.slice(1);

    const pnlElement = template.querySelector('.pnl');
    pnlElement.textContent = `$${stats.total_pnl.toFixed(2)}`;
    pnlElement.classList.add(stats.total_pnl >= 0 ? 'positive' : 'negative');

    template.querySelector('.win-rate').textContent = `${(stats.win_rate * 100).toFixed(0)}%`;

    // Add to trader stats display
    elements.traderStats.appendChild(template);
}

/**
 * Update the system status display
 */
function updateSystemStatus(status, className) {
    elements.systemStatus.textContent = status;
    elements.systemStatus.className = 'indicator-value ' + className;
}

/**
 * Update the total PnL display
 */
function updateTotalPnl(pnl) {
    elements.totalPnl.textContent = `$${pnl.toFixed(2)}`;
    elements.totalPnl.className = 'metric-value ' + (pnl >= 0 ? 'positive' : 'negative');
}

/**
 * Update the last updated timestamp
 */
function updateLastUpdateTime() {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString();

    const lastUpdateElement = document.getElementById('last-update-time');
    if (lastUpdateElement) {
        lastUpdateElement.textContent = formattedTime;
    }
}

/**
 * Toggle pausing the order log
 */
function togglePauseLog() {
    isPaused = !isPaused;
    const pauseButton = document.getElementById('pause-log');
    if (pauseButton) {
        pauseButton.textContent = isPaused ? 'Resume' : 'Pause';
        pauseButton.classList.toggle('paused', isPaused);
    }
}

/**
 * Clear the order log
 */
function clearOrderLog() {
    const logContainer = document.getElementById('order-log-entries');
    if (logContainer) {
        logContainer.innerHTML = '';
    }
}

/**
 * Filter the order log by type
 */
function filterOrderLog() {
    const filterElement = document.getElementById('log-filter');
    if (!filterElement) return;

    orderLogFilter = filterElement.value;

    // When filter changes, clear and reload from cache
    const allEntries = document.querySelectorAll('.log-entry');

    allEntries.forEach(entry => {
        if (orderLogFilter === 'all') {
            entry.style.display = '';
        } else if (orderLogFilter === 'positive' && entry.classList.contains('positive')) {
            entry.style.display = '';
        } else if (orderLogFilter === 'negative' && entry.classList.contains('negative')) {
            entry.style.display = '';
        } else if (orderLogFilter === 'neutral' && entry.classList.contains('neutral')) {
            entry.style.display = '';
        } else {
            entry.style.display = 'none';
        }
    });
}

/**
 * Create the PnL chart
 */
function createPnlChart() {
    // Initialize traders in the dataset
    const traders = ['strategic', 'aggressive', 'newbie', 'scalper'];

    // Create data structure
    pnlHistory = {
        labels: [],
        datasets: []
    };

    // Create color scheme for traders
    const colors = [
        'rgba(76, 175, 80, 0.8)',  // Green
        'rgba(255, 215, 0, 0.8)',  // Gold
        'rgba(244, 67, 54, 0.8)',  // Red
        'rgba(33, 150, 243, 0.8)'  // Blue
    ];

    // Initialize datasets
    pnlHistory.datasets = traders.map((trader, index) => ({
        label: trader.charAt(0).toUpperCase() + trader.slice(1),
        data: [],
        borderColor: colors[index],
        backgroundColor: colors[index].replace('0.8', '0.2'),
        tension: 0.3
    }));

    // Try to get chart canvas
    const canvas = document.getElementById('pnl-chart');

    if (!canvas) {
        console.error('Chart canvas element not found');
        return;
    }

    try {
        const ctx = canvas.getContext('2d');

        // Create chart with the global Chart object from Chart.js
        if (typeof window.Chart !== 'undefined') {
            pnlChart = new window.Chart(ctx, {
                type: 'line',
                data: pnlHistory,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                color: '#ffffff'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Trader PnL History',
                            color: '#ffffff'
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#ffffff'
                            }
                        },
                        y: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#ffffff'
                            }
                        }
                    }
                }
            });
        } else {
            console.error('Chart.js library not loaded');
            document.getElementById('pnl-chart-container').innerHTML = '<div class="chart-error">Chart library not available</div>';
        }
    } catch (error) {
        console.error('Error creating chart:', error);
        document.getElementById('pnl-chart-container').innerHTML = '<div class="chart-error">Error creating chart</div>';
    }
}

/**
 * Update the PnL chart with new data
 */
function updatePnLChart(traderType, pnlValue) {
    // Skip if no chart exists yet
    if (!pnlChart) return;

    // Add data point
    const now = new Date();
    const trader = traderType.toLowerCase();

    // Find the dataset index for this trader
    let datasetIndex = -1;
    for (let i = 0; i < pnlChart.data.datasets.length; i++) {
        if (pnlChart.data.datasets[i].label.toLowerCase() === trader) {
            datasetIndex = i;
            break;
        }
    }

    // If dataset doesn't exist, add it with specific colors based on trader type
    if (datasetIndex === -1) {
        // Color mapping based on trader type
        const colors = {
            'strategic': 'rgba(34, 139, 34, 1)', // Green for Strategic
            'aggressive': 'rgba(255, 165, 0, 1)', // Orange for Aggressive
            'newbie': 'rgba(220, 20, 60, 1)',    // Red for Newbie
            'scalping': 'rgba(30, 144, 255, 1)'  // Blue for Scalping
        };

        // Default color if not in mapping
        const color = colors[trader] || `hsl(${Math.random() * 360}, 70%, 50%)`;

        // Create new dataset
        const newDataset = {
            label: trader.charAt(0).toUpperCase() + trader.slice(1),
            data: [],
            borderColor: color,
            backgroundColor: color.replace('1)', '0.2)'),
            pointBackgroundColor: color,
            pointRadius: 2,
            pointHoverRadius: 4,
            tension: 0.4
        };

        pnlChart.data.datasets.push(newDataset);
        datasetIndex = pnlChart.data.datasets.length - 1;
    }

    // Add data point
    if (pnlChart.data.labels.length > 50) {
        // Remove oldest point when we have more than 50 points
        pnlChart.data.labels.shift();
        for (let dataset of pnlChart.data.datasets) {
            dataset.data.shift();
        }
    }

    // Add new point
    const timeLabel = now.toLocaleTimeString();
    if (pnlChart.data.labels.length === 0 || pnlChart.data.labels[pnlChart.data.labels.length - 1] !== timeLabel) {
        pnlChart.data.labels.push(timeLabel);
    }

    pnlChart.data.datasets[datasetIndex].data.push(pnlValue);

    // Update chart
    pnlChart.update();
}

/**
 * Convert MM WebSocket format to dashboard format
 */
function convertMMMessageToDashboardFormat(mmMessage) {
    // Default structure for dashboard messages
    const dashboardMsg = {
        timestamp: new Date().toISOString(),
        data: {}
    };

    // Determine message type and convert accordingly
    if (mmMessage.event === 'trade') {
        dashboardMsg.type = 'new_order';
        dashboardMsg.data = {
            order_id: mmMessage.id || generateRandomId(),
            trader: mmMessage.trader || 'unknown',
            symbol: mmMessage.symbol || 'BTC-USDT',
            side: mmMessage.side || 'buy',
            price: mmMessage.price || 0,
            size: mmMessage.size || 0,
            status: 'filled'
        };
    } else if (mmMessage.event === 'order') {
        dashboardMsg.type = 'position_update';
        dashboardMsg.data = {
            position_id: mmMessage.id || generateRandomId(),
            trader: mmMessage.trader || 'unknown',
            symbol: mmMessage.symbol || 'BTC-USDT',
            side: mmMessage.side || 'long',
            entry_price: mmMessage.entry || 0,
            current_price: mmMessage.price || 0,
            size: mmMessage.size || 0,
            pnl: mmMessage.pnl || 0
        };
    }

    return dashboardMsg;
}

/**
 * Generate a random ID for orders/positions
 */
function generateRandomId() {
    return 'id_' + Math.random().toString(36).substr(2, 9);
}

// Helper function for contains selector until it's widely supported
if (!HTMLElement.prototype.contains) {
    HTMLElement.prototype.contains = function (element) {
        return (this.compareDocumentPosition(element) & 16) !== 0;
    };
}

/**
 * Update the BTC price display
 */
function updateBtcPrice(price) {
    const priceElement = document.getElementById('btc-price');
    if (priceElement) {
        priceElement.textContent = `$${numberWithCommas(price.toFixed(2))}`;
    }
}

/**
 * Update trader statistics
 */
function updateTraderStats(traderType, pnl, activePositions) {
    // Convert trader type to lowercase for ID matching
    const trader = traderType.toLowerCase();

    // Find or create trader card
    let traderCard = document.getElementById(`trader-${trader}`);
    if (!traderCard) {
        // Create new trader card if it doesn't exist
        traderCard = createTraderCard(trader);
    }

    // Update trader PnL and active positions
    const pnlElement = traderCard.querySelector('.trader-pnl');
    const positionsElement = traderCard.querySelector('.trader-positions');

    if (pnlElement) {
        pnlElement.textContent = `$${pnl.toFixed(2)}`;
        pnlElement.className = `trader-pnl ${pnl >= 0 ? 'positive' : 'negative'}`;
    }

    if (positionsElement) {
        positionsElement.textContent = activePositions;
    }
}

/**
 * Create a new trader card
 */
function createTraderCard(traderType) {
    // Get traders container
    const tradersContainer = document.getElementById('trader-stats');
    if (!tradersContainer) return null;

    // Create trader card
    const traderCard = document.createElement('div');
    traderCard.id = `trader-${traderType}`;
    traderCard.className = 'trader-card';

    // Format trader name for display
    const displayName = traderType.charAt(0).toUpperCase() + traderType.slice(1);

    // Set trader card HTML
    traderCard.innerHTML = `
        <div class="trader-name">${displayName}</div>
        <div class="trader-pnl">$0.00</div>
        <div class="trader-positions-label">Positions:</div>
        <div class="trader-positions">0</div>
    `;

    // Add to container
    tradersContainer.appendChild(traderCard);

    return traderCard;
}

/**
 * Update position card
 */
function updatePositionCard(side, size, entryPrice, unrealizedPnl, realizedPnl) {
    // Find or create position card
    let positionCard = document.querySelector(`.position-card[data-side="${side}"]`);
    if (!positionCard) {
        // Create new position card if it doesn't exist
        positionCard = createPositionCard(side);
    }

    // Update position details
    const sizeElement = positionCard.querySelector('.position-size');
    const priceElement = positionCard.querySelector('.position-price');
    const pnlElement = positionCard.querySelector('.position-pnl');

    if (sizeElement) {
        sizeElement.textContent = size.toFixed(4);
    }

    if (priceElement) {
        priceElement.textContent = `$${entryPrice.toFixed(2)}`;
    }

    if (pnlElement) {
        const totalPnl = unrealizedPnl + realizedPnl;
        pnlElement.textContent = `$${totalPnl.toFixed(2)}`;
        pnlElement.className = `position-pnl ${totalPnl >= 0 ? 'positive' : 'negative'}`;
    }
}

/**
 * Create a new position card
 */
function createPositionCard(side) {
    // Get positions container
    const positionsContainer = document.getElementById('positions-container');
    if (!positionsContainer) return null;

    // Create position card
    const positionCard = document.createElement('div');
    positionCard.className = `position-card ${side === 'long' ? 'long' : 'short'}`;
    positionCard.setAttribute('data-side', side);

    // Set position card HTML
    positionCard.innerHTML = `
        <div class="position-side">${side.toUpperCase()}</div>
        <div class="position-size">0.0000</div>
        <div class="position-price">$0.00</div>
        <div class="position-pnl">$0.00</div>
    `;

    // Add to container
    positionsContainer.appendChild(positionCard);

    return positionCard;
}

/**
 * Update total PnL
 */
function updateTotalPnL() {
    // Calculate total PnL from all trader cards
    const traderPnLElements = document.querySelectorAll('.trader-pnl');
    let totalPnL = 0;

    traderPnLElements.forEach(element => {
        const pnl = parseFloat(element.textContent.replace('$', ''));
        if (!isNaN(pnl)) {
            totalPnL += pnl;
        }
    });

    // Update total PnL display
    const totalPnLElement = document.getElementById('total-pnl');
    if (totalPnLElement) {
        totalPnLElement.textContent = `$${totalPnL.toFixed(2)}`;
        totalPnLElement.className = `${totalPnL >= 0 ? 'positive' : 'negative'}`;
    }
}

/**
 * Update active positions count
 */
function updateActivePositionsCount() {
    // Count active positions from all trader cards
    const positionCountElements = document.querySelectorAll('.trader-positions');
    let totalPositions = 0;

    positionCountElements.forEach(element => {
        const count = parseInt(element.textContent);
        if (!isNaN(count)) {
            totalPositions += count;
        }
    });

    // Update active positions display
    const activePositionsElement = document.getElementById('active-positions-count');
    if (activePositionsElement) {
        activePositionsElement.textContent = totalPositions;
    }
}

/**
 * Format numbers with commas for thousands
 */
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Get CSS class based on status value
 */
function getStatusClass(status) {
    status = status.toUpperCase();

    if (status === 'CONNECTED' || status === 'ONLINE' || status === 'ACTIVE') {
        return 'positive';
    } else if (status === 'DISCONNECTED' || status === 'OFFLINE' || status === 'INACTIVE' || status === 'ERROR') {
        return 'negative';
    } else {
        return 'neutral';
    }
}

/**
 * Add an entry to the order log
 */
function addOrderLogEntry(message, type, price, timestamp) {
    // Skip if paused
    if (isPaused) return;

    // Get the filter element
    const filterElement = document.getElementById('log-filter');

    // Filter handling (only if filter element exists)
    if (filterElement) {
        const filterValue = filterElement.value;
        if (filterValue !== 'all') {
            // Filter implementation based on type
            if (filterValue === 'positive' && type !== 'positive') return;
            if (filterValue === 'negative' && type !== 'negative') return;
            if (filterValue === 'neutral' && type !== 'neutral') return;
        }
    }

    // Get the log container
    const logContainer = document.getElementById('order-log-entries');
    if (!logContainer) return;

    // Create log entry
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;

    // Format timestamp
    const timeStr = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();

    // Format price with commas for thousands
    const formattedPrice = price ? `$${numberWithCommas(price.toFixed(2))}` : '';

    // Set log entry HTML
    logEntry.innerHTML = `
        <span class="log-time">${timeStr}</span>
        <span class="log-message">${message}</span>
        ${price ? `<span class="log-price">${formattedPrice}</span>` : ''}
    `;

    // Add to log container at the top
    logContainer.insertBefore(logEntry, logContainer.firstChild);

    // Limit the number of entries (keep most recent 100)
    while (logContainer.children.length > 100) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

/**
 * Update or create a detailed position card
 */
function updateDetailedPositionCard(trader, symbol, side, size, entryPrice, unrealizedPnl, leverage, liquidationPrice, percentage, notional) {
    // Create unique position ID based on trader and side
    const positionId = `${trader.toLowerCase()}-${side}-position`;

    // Find or create position card
    let positionCard = document.getElementById(positionId);

    // Get positions container
    const positionsContainer = document.getElementById('active-positions');
    if (!positionsContainer) return;

    if (!positionCard) {
        // Create new position card if it doesn't exist
        positionCard = document.createElement('div');
        positionCard.id = positionId;
        positionCard.className = `position-card ${side.toLowerCase()}`;

        // Format trader name for display
        const displayName = trader.charAt(0).toUpperCase() + trader.slice(1);

        // Create HTML structure for the detailed position card
        positionCard.innerHTML = `
            <div class="position-header">
                <span class="trader-name">${displayName}</span>
                <span class="position-side ${side.toLowerCase()}">${side.toUpperCase()}</span>
            </div>
            <div class="position-details">
                <div class="detail-row">
                    <span class="detail-label">Size:</span>
                    <span class="detail-value size">${size.toFixed(4)} BTC</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Entry:</span>
                    <span class="detail-value entry-price">$${numberWithCommas(entryPrice.toFixed(2))}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Current:</span>
                    <span class="detail-value current-price">$${numberWithCommas(currentBtcPrice.toFixed(2))}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">PnL:</span>
                    <span class="detail-value pnl ${unrealizedPnl >= 0 ? 'positive' : 'negative'}">$${unrealizedPnl.toFixed(2)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Leverage:</span>
                    <span class="detail-value leverage">${leverage}x</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Liq. Price:</span>
                    <span class="detail-value liquidation">$${numberWithCommas(liquidationPrice.toFixed(2))}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Notional:</span>
                    <span class="detail-value notional">$${numberWithCommas(notional.toFixed(2))}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">% Change:</span>
                    <span class="detail-value percentage ${percentage >= 0 ? 'positive' : 'negative'}">${percentage.toFixed(2)}%</span>
                </div>
            </div>
        `;

        // Add to container
        positionsContainer.appendChild(positionCard);
    } else {
        // Update existing position card
        positionCard.querySelector('.size').textContent = `${size.toFixed(4)} BTC`;
        positionCard.querySelector('.entry-price').textContent = `$${numberWithCommas(entryPrice.toFixed(2))}`;
        positionCard.querySelector('.current-price').textContent = `$${numberWithCommas(currentBtcPrice.toFixed(2))}`;

        const pnlElement = positionCard.querySelector('.pnl');
        pnlElement.textContent = `$${unrealizedPnl.toFixed(2)}`;
        pnlElement.className = `detail-value pnl ${unrealizedPnl >= 0 ? 'positive' : 'negative'}`;

        positionCard.querySelector('.leverage').textContent = `${leverage}x`;
        positionCard.querySelector('.liquidation').textContent = `$${numberWithCommas(liquidationPrice.toFixed(2))}`;
        positionCard.querySelector('.notional').textContent = `$${numberWithCommas(notional.toFixed(2))}`;

        const percentageElement = positionCard.querySelector('.percentage');
        percentageElement.textContent = `${percentage.toFixed(2)}%`;
        percentageElement.className = `detail-value percentage ${percentage >= 0 ? 'positive' : 'negative'}`;
    }

    // Update trader stats for this trader
    updateTraderPositionCount(trader);
}

/**
 * Update trader position count
 */
function updateTraderPositionCount(traderType) {
    // Count positions for this trader
    const traderPositions = document.querySelectorAll(`.position-card[id^="${traderType.toLowerCase()}"]`).length;

    // Update the trader's position count in stats
    updateTraderStats(traderType, null, traderPositions);
}

/**
 * Update the dashboard with detailed ticker data
 */
function updateTickerData(tickerData) {
    const tickerContainer = document.getElementById('ticker-data');
    if (!tickerContainer) return;

    // Clear previous ticker data
    tickerContainer.innerHTML = '';

    // Create ticker items
    const tickerItems = [
        { label: 'Symbol', value: tickerData.symbol },
        { label: 'Last Price', value: `$${numberWithCommas(tickerData.last.toFixed(2))}` },
        { label: 'Bid', value: `$${numberWithCommas(tickerData.bid.toFixed(2))}` },
        { label: 'Ask', value: `$${numberWithCommas(tickerData.ask.toFixed(2))}` },
        { label: '24h High', value: `$${numberWithCommas(tickerData.high.toFixed(2))}` },
        { label: '24h Low', value: `$${numberWithCommas(tickerData.low.toFixed(2))}` },
        { label: '24h Change', value: `${tickerData.percentage.toFixed(2)}%`, isPercentage: true },
        { label: 'Volume', value: `${numberWithCommas(Math.round(tickerData.baseVolume))} BTC` },
        { label: 'Index Price', value: `$${numberWithCommas(tickerData.indexPrice.toFixed(2))}` },
        { label: 'Funding Rate', value: tickerData.info?.fundingRate ? `${(Number(tickerData.info.fundingRate) * 100).toFixed(4)}%` : 'N/A' }
    ];

    // Add ticker items to container
    tickerItems.forEach(item => {
        const tickerElement = document.createElement('div');
        tickerElement.className = 'ticker-item';

        const isPositive = item.isPercentage && parseFloat(item.value) > 0;
        const isNegative = item.isPercentage && parseFloat(item.value) < 0;

        tickerElement.innerHTML = `
            <div class="ticker-label">${item.label}</div>
            <div class="ticker-value ${isPositive ? 'positive' : isNegative ? 'negative' : ''}">${item.value}</div>
        `;

        tickerContainer.appendChild(tickerElement);
    });
} 