/**
 * Trap Analysis Panel Integration for OMEGA BTC AI Dashboard
 * 
 * This script loads and integrates the trap analysis panel into the existing dashboard.
 */

// Function to load the trap analysis panel
function loadTrapAnalysisPanel() {
    console.log('Loading Trap Analysis Panel...');

    // Get the dashboard container
    const dashboardContainer = document.querySelector('.dashboard');
    if (!dashboardContainer) {
        console.error('Dashboard container not found!');
        return;
    }

    // Create a new div to hold the panel
    const panelContainer = document.createElement('div');

    // Load the panel content from the HTML file
    fetch('trap_analysis_panel.html')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load trap analysis panel: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            // Insert the panel HTML
            panelContainer.innerHTML = html;

            // Add the panel to the dashboard
            dashboardContainer.appendChild(panelContainer);

            console.log('Trap Analysis Panel loaded successfully');

            // Initialize the panel
            initializeTrapAnalysisPanel();
        })
        .catch(error => {
            console.error('Error loading trap analysis panel:', error);
            panelContainer.innerHTML = `
                <div class="bitget-card">
                    <h2>
                        <span><i class="fas fa-spider"></i> MARKET MAKER TRAP ANALYSIS</span>
                    </h2>
                    <div style="padding: 20px; text-align: center;">
                        <p>Error loading trap analysis panel: ${error.message}</p>
                        <button class="refresh-button" onclick="loadTrapAnalysisPanel()">
                            <i class="fas fa-sync-alt"></i> Retry Loading
                        </button>
                    </div>
                </div>
            `;
            dashboardContainer.appendChild(panelContainer);
        });
}

// Function to initialize the trap analysis panel
function initializeTrapAnalysisPanel() {
    console.log('Initializing Trap Analysis Panel...');

    // Get panel elements
    const refreshButton = document.getElementById('refresh-trap-analysis');
    if (refreshButton) {
        refreshButton.addEventListener('click', updateTrapAnalysisPanel);
    }

    // Initial update
    updateTrapAnalysisPanel();

    // Set up auto-refresh every 5 minutes
    setInterval(updateTrapAnalysisPanel, 5 * 60 * 1000);
}

// Function to update the trap analysis panel with real data
async function updateTrapAnalysisPanel() {
    console.log('Updating Trap Analysis Panel...');

    try {
        // Fetch trap analysis data from Redis
        const analysisData = await fetchRedisKey('dashboard:trap_analysis:data');
        const performanceData = await fetchRedisKey('dashboard:trap_analysis:performance');

        if (!analysisData) {
            console.warn('No trap analysis data found in Redis');
            return;
        }

        console.log('Trap analysis data:', analysisData);
        if (performanceData) {
            console.log('Performance data:', performanceData);
        }

        // Update timestamp
        const timestamp = document.getElementById('trap-analysis-timestamp');
        if (timestamp) {
            timestamp.textContent = new Date().toLocaleTimeString();
        }

        // Update trap count
        const trapCount = document.getElementById('trap-count');
        if (trapCount && analysisData.total_count) {
            trapCount.textContent = analysisData.total_count.toLocaleString();
        }

        // Update average confidence
        const avgConfidence = document.getElementById('trap-avg-confidence');
        if (avgConfidence && analysisData.avg_confidence) {
            avgConfidence.textContent = `${Math.round(analysisData.avg_confidence * 100)}%`;
        }

        // Update dominant type
        const dominantType = document.getElementById('trap-dominant-type');
        if (dominantType && analysisData.dominant_type) {
            dominantType.textContent = analysisData.dominant_type;
        }

        // Update recent high confidence traps
        updateHighConfidenceTraps(analysisData.recent_high_conf_traps || []);

        // Update trap distribution chart
        updateTrapDistributionChart(analysisData.trap_types || {});

        // Update hour distribution chart
        updateHourDistributionChart(analysisData.hour_distribution || {});

        // Update performance metrics
        if (performanceData) {
            updatePerformanceMetrics(performanceData);
        }

    } catch (error) {
        console.error('Error updating trap analysis panel:', error);
    }
}

// Function to update high confidence traps list
function updateHighConfidenceTraps(traps) {
    const container = document.getElementById('high-confidence-traps');
    if (!container) return;

    // Clear current content
    container.innerHTML = '';

    if (traps.length === 0) {
        container.innerHTML = '<p>No high confidence traps detected recently</p>';
        return;
    }

    // Add each trap
    traps.forEach(trap => {
        const trapElement = document.createElement('div');
        trapElement.className = 'trap-indicator';

        // Determine if bull or bear based on type
        const isBull = trap.type.toLowerCase().includes('bull') ||
            trap.type.toLowerCase().includes('liquidity grab') ||
            trap.type.toLowerCase().includes('accumulation up');

        trapElement.innerHTML = `
            <div class="trap-dot ${isBull ? 'bull' : 'bear'}"></div>
            <div class="trap-info">
                <span class="trap-type">${trap.type}</span>
                <span class="trap-confidence">${Math.round(trap.confidence * 100)}%</span>
                <div class="trap-timeframe">${trap.timeframe} timeframe • ${trap.time_ago}</div>
            </div>
        `;

        container.appendChild(trapElement);
    });
}

// Function to update trap distribution chart
function updateTrapDistributionChart(trapTypes) {
    const container = document.querySelector('.trap-distribution-chart');
    if (!container) return;

    // Get the bars container
    const barsContainer = container.querySelector('div');
    if (!barsContainer) return;

    // Clear current content
    barsContainer.innerHTML = '';

    if (Object.keys(trapTypes).length === 0) {
        barsContainer.innerHTML = '<p>No trap distribution data available</p>';
        return;
    }

    // Calculate total traps
    const totalTraps = Object.values(trapTypes).reduce((sum, count) => sum + count, 0);

    // Sort trap types by count
    const sortedTypes = Object.entries(trapTypes)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5); // Take top 5

    // Create bar for each trap type
    sortedTypes.forEach(([type, count]) => {
        const percentage = (count / totalTraps) * 100;
        const height = Math.max(0.5, percentage); // Minimum height for visibility

        // Determine color based on type
        let color = '#ff6d00'; // Default (orange)
        if (type.toLowerCase().includes('bull')) {
            color = '#76b852'; // Green
        } else if (type.toLowerCase().includes('liquidity')) {
            color = '#ffeb3b'; // Yellow
        } else if (type.toLowerCase().includes('hunt')) {
            color = '#4285f4'; // Blue
        }

        const bar = document.createElement('div');
        bar.className = 'trap-bar';
        bar.style.cssText = `
            flex: 1;
            margin: 0 2px;
            height: ${height}%;
            background-color: ${color};
        `;
        bar.title = `${type}: ${percentage.toFixed(1)}%`;

        barsContainer.appendChild(bar);
    });

    // Add labels
    const labelsContainer = document.createElement('div');
    labelsContainer.style.cssText = `
        display: flex;
        margin-top: 5px;
        font-size: 0.7rem;
        color: #aaa;
    `;

    sortedTypes.forEach(([type]) => {
        const shortName = type.split(' ')[0]; // Take first word
        const label = document.createElement('div');
        label.style.cssText = `
            flex: 1;
            text-align: center;
        `;
        label.textContent = shortName;
        labelsContainer.appendChild(label);
    });

    container.appendChild(labelsContainer);
}

// Function to update hour distribution chart
function updateHourDistributionChart(hourDistribution) {
    const container = document.querySelector('.hour-distribution');
    if (!container) return;

    // Clear current content
    container.innerHTML = '';

    if (Object.keys(hourDistribution).length === 0) {
        container.innerHTML = '<p>No hour distribution data available</p>';
        return;
    }

    // Find max count for normalization
    const maxCount = Math.max(...Object.values(hourDistribution));

    // Create bar for each hour (0-23)
    for (let hour = 0; hour < 24; hour++) {
        const count = hourDistribution[hour] || 0;
        const percentage = (count / maxCount) * 100;

        // Determine color intensity based on percentage
        let color;
        if (percentage < 30) {
            color = 'rgba(118, 184, 82, 0.5)'; // Green (low)
        } else if (percentage < 70) {
            color = 'rgba(255, 235, 59, 0.5)'; // Yellow (medium)
        } else {
            color = 'rgba(255, 109, 0, 0.5)'; // Orange (high)
        }

        // Create the hour bar
        const bar = document.createElement('div');
        bar.className = 'hour-bar';
        bar.style.cssText = `
            flex: 1;
            margin: 0 1px;
            height: ${Math.max(5, percentage)}%;
            background-color: ${color};
        `;

        // Format hour for display (12am, 1am, etc.)
        let hourLabel;
        if (hour === 0) {
            hourLabel = '12am';
        } else if (hour < 12) {
            hourLabel = `${hour}am`;
        } else if (hour === 12) {
            hourLabel = '12pm';
        } else {
            hourLabel = `${hour - 12}pm`;
        }

        bar.title = `${hourLabel}: ${count} events`;
        container.appendChild(bar);
    }

    // Add hour labels
    const labelsContainer = document.createElement('div');
    labelsContainer.style.cssText = `
        display: flex;
        margin-top: 5px;
        font-size: 0.6rem;
        color: #aaa;
        justify-content: space-between;
    `;

    // Add labels at 6-hour intervals
    ['00', '06', '12', '18', '23'].forEach(hour => {
        const label = document.createElement('div');
        label.textContent = hour;
        labelsContainer.appendChild(label);
    });

    // Add labels container after the bars
    container.parentNode.appendChild(labelsContainer);
}

// Function to update performance metrics
function updatePerformanceMetrics(performanceData) {
    // Update bear trap win rate
    const bearTrapWinrate = document.getElementById('bear-trap-winrate');
    if (bearTrapWinrate && performanceData.bear_trap_winrate) {
        bearTrapWinrate.textContent = `${performanceData.bear_trap_winrate}%`;
    }

    // Update bull trap win rate
    const bullTrapWinrate = document.getElementById('bull-trap-winrate');
    if (bullTrapWinrate && performanceData.bull_trap_winrate) {
        bullTrapWinrate.textContent = `${performanceData.bull_trap_winrate}%`;
    }

    // Update liquidity grab win rate
    const liqGrabWinrate = document.getElementById('liq-grab-winrate');
    if (liqGrabWinrate && performanceData.liquidity_grab_winrate) {
        liqGrabWinrate.textContent = `${performanceData.liquidity_grab_winrate}%`;
    }

    // Update stop hunt win rate
    const stopHuntWinrate = document.getElementById('stop-hunt-winrate');
    if (stopHuntWinrate && performanceData.stop_hunt_winrate) {
        stopHuntWinrate.textContent = `${performanceData.stop_hunt_winrate}%`;
    }
}

// Load the panel when the document is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded, initializing trap analysis panel integration...');
    loadTrapAnalysisPanel();
}); 