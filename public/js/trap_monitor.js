// Trap Monitor - Real-time updates for the Rasta Omega Trader panel

class TrapMonitor {
    constructor() {
        // Initialize state
        this.lastUpdate = 0;
        this.updateInterval = 5000; // 5 seconds

        // Cache DOM elements
        this.elements = {
            probability: document.getElementById('trap-probability'),
            type: document.getElementById('trap-type'),
            trend: document.getElementById('trap-trend'),
            confidence: document.getElementById('trap-confidence'),
            time: document.getElementById('trap-time'),
            bar: document.getElementById('trap-bar'),
            components: document.getElementById('trap-components')
        };

        // Start monitoring
        this.startMonitoring();
    }

    async startMonitoring() {
        while (true) {
            try {
                // Get current time
                const now = Date.now();

                // Check if it's time to update
                if (now - this.lastUpdate >= this.updateInterval) {
                    await this.updateTrapData();
                    this.lastUpdate = now;
                }

                // Wait for next check
                await new Promise(resolve => setTimeout(resolve, 100));

            } catch (error) {
                console.error('Error in trap monitor:', error);
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
    }

    async updateTrapData() {
        try {
            // Fetch latest trap data
            const response = await fetch('/api/trap-data');
            const data = await response.json();

            if (!data) {
                console.warn('No trap data received');
                return;
            }

            // Update probability
            this.elements.probability.textContent = `${data.probability}%`;
            this.elements.probability.className = `value ${this.getTrendClass(data.trend)}`;

            // Update type
            this.elements.type.textContent = data.type;
            this.elements.type.className = `value ${this.getTrendClass(data.trend)}`;

            // Update trend
            this.elements.trend.textContent = data.trend;
            this.elements.trend.className = `value ${this.getTrendClass(data.trend)}`;

            // Update confidence
            this.elements.confidence.textContent = `${data.confidence}%`;
            this.elements.confidence.className = `value ${this.getTrendClass(data.trend)}`;

            // Update time
            this.elements.time.textContent = data.timestamp;

            // Update progress bar
            this.elements.bar.style.width = `${data.probability}%`;
            this.elements.bar.style.backgroundColor = this.getBarColor(data.probability);

            // Update components
            this.updateComponents(data.components);

            // Update Jah message
            this.updateJahMessage(data);

        } catch (error) {
            console.error('Error updating trap data:', error);
        }
    }

    updateComponents(components) {
        // Create component HTML
        const html = Object.entries(components)
            .map(([name, value]) => {
                const displayName = name.split('_')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');

                const percentage = Math.round(value * 100);
                const hue = this.getComponentHue(percentage);

                return `
                    <div class="component-item">
                        <div class="component-name">${displayName}</div>
                        <div class="component-value">
                            <div class="component-bar" style="width: ${percentage}%; background-color: hsl(${hue}, 80%, 45%)"></div>
                            <span class="value-text">${percentage}%</span>
                        </div>
                    </div>
                `;
            })
            .join('');

        // Update components grid
        this.elements.components.innerHTML = html;
    }

    updateJahMessage(data) {
        const jahMessage = document.getElementById('jah-message');
        if (!jahMessage) return;

        // Generate Rasta-style message based on trap data
        let message = 'JAH GUIDES THE TRADING PATH!';

        if (data.probability > 80) {
            message = 'I AND I SEE A MIGHTY TRADING SIGNAL!';
        } else if (data.probability > 60) {
            message = 'POSITIVE VIBRATIONS IN THE MARKET!';
        } else if (data.trend === 'Bullish') {
            message = 'UPFUL MOVEMENTS AHEAD, JAH BLESS!';
        } else if (data.trend === 'Bearish') {
            message = 'DOWNPRESSION COMES BEFORE UPLIFTMENT!';
        }

        jahMessage.textContent = message;
    }

    getTrendClass(trend) {
        switch (trend.toLowerCase()) {
            case 'bullish': return 'positive';
            case 'bearish': return 'negative';
            default: return 'neutral';
        }
    }

    getBarColor(probability) {
        // Convert probability to a color using HSL
        // Red (0) at 0%, Yellow (60) at 50%, Green (120) at 100%
        const hue = (probability * 1.2); // 120 degrees = green
        return `hsl(${hue}, 80%, 45%)`;
    }

    getComponentHue(percentage) {
        // Convert percentage to hue (red = 0, yellow = 60, green = 120)
        return percentage * 1.2; // 120 degrees = green
    }
}

// Initialize trap monitor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.trapMonitor = new TrapMonitor();
}); 