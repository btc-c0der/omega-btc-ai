class TPSLManagementPanel {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.position = null;
        this.exitStrategies = {
            scalper: 0.3,    // 30% weight
            strategic: 0.5,   // 50% weight
            aggressive: 0.2   // 20% weight
        };
        this.trailingStopEnabled = false;
        this.trailingStopDistance = 0;
        this.exitHistory = [];

        this.init();
    }

    init() {
        this.render();
        this.attachEventListeners();
        this.startPriceUpdates();
    }

    render() {
        this.container.innerHTML = `
            <div class="tp-sl-management-panel">
                <h2>
                    TP/SL Management
                    <span class="position-side ${this.position?.side.toLowerCase() || ''}">
                        ${this.position?.side || 'No Position'}
                    </span>
                </h2>
                
                <div class="tp-sl-content">
                    <div class="position-summary">
                        <h3>Position Summary</h3>
                        <div class="position-details">
                            <div>Entry: ${this.formatPrice(this.position?.entryPrice)}</div>
                            <div>Current: ${this.formatPrice(this.position?.currentPrice)}</div>
                            <div>P&L: ${this.calculatePnL()}</div>
                        </div>
                        
                        <div class="risk-reward-ratio">
                            <span class="risk-label">Risk</span>
                            <div class="risk-bar">
                                <div class="risk-segment" style="width: ${this.calculateRiskPercentage()}%"></div>
                                <div class="reward-segment" style="width: ${this.calculateRewardPercentage()}%"></div>
                            </div>
                            <span class="reward-label">Reward</span>
                            <span class="r-r-value">${this.calculateRR()}R</span>
                        </div>
                    </div>

                    <div class="exit-strategy">
                        <h3>Exit Strategy</h3>
                        <div class="strategy-blend">
                            <div class="blend-label">Strategy Blend</div>
                            <div class="blend-segments">
                                ${this.renderStrategyBlend()}
                            </div>
                        </div>
                        
                        <div class="tp-sl-visual">
                            <div class="price-scale">
                                ${this.renderPriceScale()}
                            </div>
                            <div class="price-visual">
                                ${this.renderPriceMarkers()}
                            </div>
                        </div>
                    </div>

                    <div class="exit-controls">
                        <h3>Exit Controls</h3>
                        <div class="control-buttons">
                            <button class="exit-btn partial">Exit 25%</button>
                            <button class="exit-btn half">Exit 50%</button>
                            <button class="exit-btn full">Exit 100%</button>
                        </div>
                        
                        <div class="trailing-stop-control">
                            <span class="control-label">Trailing Stop</span>
                            <div class="toggle-switch">
                                <input type="checkbox" id="trailing-stop-toggle">
                                <label for="trailing-stop-toggle"></label>
                            </div>
                            <span class="trailing-value">${this.trailingStopDistance}%</span>
                        </div>
                    </div>
                </div>

                <div class="exit-history">
                    <h3>Exit History</h3>
                    <div class="exit-list">
                        ${this.renderExitHistory()}
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        // Exit buttons
        this.container.querySelectorAll('.exit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const percentage = this.getExitPercentage(e.target.classList);
                this.executeExit(percentage);
            });
        });

        // Trailing stop toggle
        const trailingStopToggle = this.container.querySelector('#trailing-stop-toggle');
        trailingStopToggle.addEventListener('change', (e) => {
            this.trailingStopEnabled = e.target.checked;
            this.updateTrailingStop();
        });
    }

    getExitPercentage(classList) {
        if (classList.contains('partial')) return 0.25;
        if (classList.contains('half')) return 0.50;
        if (classList.contains('full')) return 1.00;
        return 0;
    }

    executeExit(percentage) {
        if (!this.position || percentage <= 0) return;

        const exitSize = this.position.size * percentage;
        const exitPrice = this.position.currentPrice;
        const pnl = this.calculateExitPnL(exitSize, exitPrice);

        this.exitHistory.unshift({
            time: new Date(),
            size: exitSize,
            price: exitPrice,
            pnl: pnl,
            percentage: percentage * 100
        });

        this.position.size -= exitSize;
        if (this.position.size <= 0) {
            this.position = null;
        }

        this.render();
        this.notifyExitExecution(exitSize, exitPrice, pnl);
    }

    calculateExitPnL(size, exitPrice) {
        if (!this.position) return 0;

        const direction = this.position.side === 'LONG' ? 1 : -1;
        return direction * (exitPrice - this.position.entryPrice) * size;
    }

    updateTrailingStop() {
        if (!this.trailingStopEnabled || !this.position) return;

        const currentPrice = this.position.currentPrice;
        const direction = this.position.side === 'LONG' ? 1 : -1;
        const stopDistance = currentPrice * (this.trailingStopDistance / 100);

        if (this.position.side === 'LONG') {
            const newStopPrice = currentPrice - stopDistance;
            if (!this.position.stopLoss || newStopPrice > this.position.stopLoss) {
                this.position.stopLoss = newStopPrice;
            }
        } else {
            const newStopPrice = currentPrice + stopDistance;
            if (!this.position.stopLoss || newStopPrice < this.position.stopLoss) {
                this.position.stopLoss = newStopPrice;
            }
        }

        this.render();
    }

    startPriceUpdates() {
        // Subscribe to price updates
        this.priceUpdateInterval = setInterval(() => {
            if (this.position) {
                // Simulate price updates for demo
                this.position.currentPrice += (Math.random() - 0.5) * 10;
                this.updateTrailingStop();
                this.render();
            }
        }, 1000);
    }

    renderStrategyBlend() {
        return Object.entries(this.exitStrategies)
            .map(([strategy, weight]) => `
                <div class="blend-segment ${strategy}" style="width: ${weight * 100}%">
                    <span class="blend-name">${strategy}</span>
                    <span class="blend-value">${(weight * 100).toFixed(0)}%</span>
                </div>
            `).join('');
    }

    renderPriceScale() {
        if (!this.position) return '';

        const prices = [
            this.position.stopLoss,
            this.position.entryPrice,
            this.position.currentPrice,
            this.position.takeProfit
        ].filter(Boolean).sort((a, b) => a - b);

        return prices.map(price => `
            <div class="price-level">${this.formatPrice(price)}</div>
        `).join('');
    }

    renderPriceMarkers() {
        if (!this.position) return '';

        const lowestPrice = Math.min(
            this.position.stopLoss || Infinity,
            this.position.entryPrice,
            this.position.currentPrice,
            this.position.takeProfit || -Infinity
        );

        const highestPrice = Math.max(
            this.position.stopLoss || -Infinity,
            this.position.entryPrice,
            this.position.currentPrice,
            this.position.takeProfit || Infinity
        );

        const range = highestPrice - lowestPrice;
        const getPosition = price => ((price - lowestPrice) / range * 100).toFixed(2);

        return `
            ${this.position.stopLoss ? `
                <div class="stop-loss" style="bottom: ${getPosition(this.position.stopLoss)}%">
                    <div class="sl-marker"></div>
                </div>
            ` : ''}
            
            <div class="entry-price" style="bottom: ${getPosition(this.position.entryPrice)}%">
                <div class="entry-marker"></div>
            </div>
            
            <div class="current-price" style="bottom: ${getPosition(this.position.currentPrice)}%">
                <div class="price-marker"></div>
            </div>
            
            ${this.position.takeProfit ? `
                <div class="take-profit" style="bottom: ${getPosition(this.position.takeProfit)}%">
                    <div class="tp-marker"></div>
                </div>
            ` : ''}
        `;
    }

    renderExitHistory() {
        if (this.exitHistory.length === 0) {
            return '<div class="no-exits">No exits yet</div>';
        }

        return this.exitHistory.map(exit => `
            <div class="exit-item">
                <span class="exit-time">${this.formatTime(exit.time)}</span>
                <span class="exit-details">
                    ${exit.percentage}% @ ${this.formatPrice(exit.price)}
                    <span class="exit-pnl ${exit.pnl >= 0 ? 'positive' : 'negative'}">
                        ${this.formatPnL(exit.pnl)}
                    </span>
                </span>
            </div>
        `).join('');
    }

    calculateRR() {
        if (!this.position || !this.position.takeProfit || !this.position.stopLoss) {
            return 'N/A';
        }

        const risk = Math.abs(this.position.entryPrice - this.position.stopLoss);
        const reward = Math.abs(this.position.takeProfit - this.position.entryPrice);
        return (reward / risk).toFixed(2);
    }

    calculateRiskPercentage() {
        if (!this.position || !this.position.stopLoss) return 0;
        const totalRange = Math.abs(this.position.takeProfit - this.position.stopLoss);
        const risk = Math.abs(this.position.entryPrice - this.position.stopLoss);
        return (risk / totalRange * 100).toFixed(2);
    }

    calculateRewardPercentage() {
        if (!this.position || !this.position.takeProfit) return 0;
        const totalRange = Math.abs(this.position.takeProfit - this.position.stopLoss);
        const reward = Math.abs(this.position.takeProfit - this.position.entryPrice);
        return (reward / totalRange * 100).toFixed(2);
    }

    calculatePnL() {
        if (!this.position) return '0.00';
        const direction = this.position.side === 'LONG' ? 1 : -1;
        const pnl = direction * (this.position.currentPrice - this.position.entryPrice) * this.position.size;
        return this.formatPnL(pnl);
    }

    formatPrice(price) {
        return price ? price.toFixed(2) : 'N/A';
    }

    formatPnL(pnl) {
        return pnl >= 0 ? `+${pnl.toFixed(2)}` : pnl.toFixed(2);
    }

    formatTime(date) {
        return date.toLocaleTimeString();
    }

    notifyExitExecution(size, price, pnl) {
        // Implement WebSocket or API call to notify the backend
        console.log('Exit executed:', { size, price, pnl });
    }

    // Public methods for external interaction
    updatePosition(positionData) {
        this.position = positionData;
        this.render();
    }

    setExitStrategies(strategies) {
        this.exitStrategies = strategies;
        this.render();
    }

    setTrailingStop(distance) {
        this.trailingStopDistance = distance;
        this.render();
    }

    destroy() {
        clearInterval(this.priceUpdateInterval);
        this.container.innerHTML = '';
    }
}

// Export the class for use in other modules
export default TPSLManagementPanel; 