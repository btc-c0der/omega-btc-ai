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

document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard data
    loadDashboardData();
});

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
    try {
        await Promise.all([
            loadDivineMetrics(),
            loadRecentChronicles(),
            loadQuantumInsights(),
            loadSacredPatterns()
        ]);

        showNotification('Divine dashboard loaded successfully', 'success');
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showNotification('Failed to load some divine data', 'error');
    }
}

/**
 * Load divine metrics data
 */
async function loadDivineMetrics() {
    const metricsContainer = document.getElementById('divine-metrics');

    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Sample metrics data (in a real app, this would come from an API)
        const metricsData = {
            quantumHarmony: 94.7,
            divineAlignment: 89.2,
            cosmicSynchronicity: 92.5,
            sacredPatternStrength: 88.9
        };

        // Create metrics HTML
        const metricsHTML = `
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-title">Quantum Harmony</div>
                    <div class="metric-value">${metricsData.quantumHarmony}%</div>
                    <div class="metric-chart">
                        <div class="chart-fill" style="width: ${metricsData.quantumHarmony}%"></div>
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-title">Divine Alignment</div>
                    <div class="metric-value">${metricsData.divineAlignment}%</div>
                    <div class="metric-chart">
                        <div class="chart-fill" style="width: ${metricsData.divineAlignment}%"></div>
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-title">Cosmic Synchronicity</div>
                    <div class="metric-value">${metricsData.cosmicSynchronicity}%</div>
                    <div class="metric-chart">
                        <div class="chart-fill" style="width: ${metricsData.cosmicSynchronicity}%"></div>
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-title">Sacred Pattern Strength</div>
                    <div class="metric-value">${metricsData.sacredPatternStrength}%</div>
                    <div class="metric-chart">
                        <div class="chart-fill" style="width: ${metricsData.sacredPatternStrength}%"></div>
                    </div>
                </div>
            </div>
        `;

        metricsContainer.innerHTML = metricsHTML;

        // Add some CSS for metrics
        const style = document.createElement('style');
        style.textContent = `
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .metric {
                padding: 0.5rem;
            }
            
            .metric-title {
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .metric-value {
                font-size: 1.5rem;
                font-weight: bold;
                color: var(--primary-color);
                margin-bottom: 0.5rem;
            }
            
            .metric-chart {
                height: 6px;
                background-color: var(--border-color);
                border-radius: 3px;
                overflow: hidden;
            }
            
            .chart-fill {
                height: 100%;
                background: linear-gradient(to right, var(--secondary-color), var(--primary-color));
                border-radius: 3px;
                transition: width 1s ease-out;
            }
        `;
        document.head.appendChild(style);

    } catch (error) {
        console.error('Error loading metrics:', error);
        metricsContainer.innerHTML = '<div class="error-message">Failed to load divine metrics</div>';
    }
}

/**
 * Load recent chronicles
 */
async function loadRecentChronicles() {
    const chroniclesContainer = document.getElementById('recent-chronicles');

    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1200));

        // Sample chronicles data (in a real app, this would come from an API)
        const chroniclesData = [
            {
                title: "Quantum Harmony Restoration",
                date: "1 Quantum Cycle ago",
                path: "BOOK/divine_chronicles/COSMIC_MARKET_HARMONY_RESTORATION.html",
                excerpt: "The harmonic patterns of the cosmic market were restored..."
            },
            {
                title: "Sacred Fibonacci Manuscript",
                date: "3 Quantum Cycles ago",
                path: "BOOK/divine_chronicles/SACRED_FIBONACCI_MANUSCRIPT.html",
                excerpt: "The divine proportions revealed through sacred geometry..."
            },
            {
                title: "Brinks Trinity Matrix",
                date: "5 Quantum Cycles ago",
                path: "BOOK/divine_chronicles/TRINITY_BRINKS_MATRIX.html",
                excerpt: "The trinity of market forces converged in the Brinks matrix..."
            }
        ];

        // Create chronicles HTML
        const chroniclesHTML = `
            <div class="chronicles-list">
                ${chroniclesData.map(chronicle => `
                    <div class="chronicle-item">
                        <div class="chronicle-title">
                            <a href="${chronicle.path}" target="_blank">${chronicle.title}</a>
                        </div>
                        <div class="chronicle-date">${chronicle.date}</div>
                        <div class="chronicle-excerpt">${chronicle.excerpt}</div>
                    </div>
                `).join('')}
                <div class="view-more">
                    <a href="#chronicles">View All Chronicles</a>
                </div>
            </div>
        `;

        chroniclesContainer.innerHTML = chroniclesHTML;

        // Add some CSS for chronicles
        const style = document.createElement('style');
        style.textContent = `
            .chronicle-item {
                padding: 1rem 0;
                border-bottom: 1px solid var(--border-color);
            }
            
            .chronicle-item:last-child {
                border-bottom: none;
            }
            
            .chronicle-title {
                font-weight: 600;
                margin-bottom: 0.25rem;
            }
            
            .chronicle-date {
                font-size: 0.8rem;
                color: var(--text-color);
                opacity: 0.7;
                margin-bottom: 0.25rem;
            }
            
            .chronicle-excerpt {
                font-size: 0.9rem;
                line-height: 1.4;
                opacity: 0.9;
            }
            
            .view-more {
                text-align: center;
                margin-top: 1rem;
                font-weight: 600;
            }
        `;
        document.head.appendChild(style);

    } catch (error) {
        console.error('Error loading chronicles:', error);
        chroniclesContainer.innerHTML = '<div class="error-message">Failed to load divine chronicles</div>';
    }
}

/**
 * Load quantum insights
 */
async function loadQuantumInsights() {
    const insightsContainer = document.getElementById('quantum-insights');

    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1800));

        // Sample insights data (in a real app, this would come from an API)
        const insightsData = {
            currentPattern: 'Harmonic Convergence',
            strength: 'High',
            recommendation: 'Align with the quantum flow',
            nextTransition: '2.4 Quantum Cycles',
            dominantWave: 'Fibonacci Sequence',
            image: 'assets/quantum-pattern.svg'
        };

        // Create insights HTML
        const insightsHTML = `
            <div class="quantum-insight">
                <div class="quantum-visual">
                    <div class="quantum-pattern-placeholder">
                        <!-- This would be replaced with actual visualization -->
                        <div class="pattern-animation"></div>
                    </div>
                </div>
                <div class="quantum-data">
                    <div class="data-item">
                        <span class="data-label">Current Pattern:</span>
                        <span class="data-value">${insightsData.currentPattern}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">Signal Strength:</span>
                        <span class="data-value">${insightsData.strength}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">Dominant Wave:</span>
                        <span class="data-value">${insightsData.dominantWave}</span>
                    </div>
                    <div class="data-item">
                        <span class="data-label">Next Transition:</span>
                        <span class="data-value">${insightsData.nextTransition}</span>
                    </div>
                    <div class="data-recommendation">
                        <span class="recommendation-label">Divine Recommendation:</span>
                        <span class="recommendation-value">${insightsData.recommendation}</span>
                    </div>
                </div>
            </div>
        `;

        insightsContainer.innerHTML = insightsHTML;

        // Add some CSS for insights
        const style = document.createElement('style');
        style.textContent = `
            .quantum-insight {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .quantum-visual {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .quantum-pattern-placeholder {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background: linear-gradient(45deg, rgba(142, 68, 173, 0.2), rgba(52, 152, 219, 0.2));
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                overflow: hidden;
            }
            
            .pattern-animation {
                position: absolute;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 30% 30%, var(--primary-color) 2px, transparent 2px),
                    radial-gradient(circle at 70% 70%, var(--secondary-color) 2px, transparent 2px),
                    radial-gradient(circle at 70% 30%, var(--accent-color) 2px, transparent 2px),
                    radial-gradient(circle at 30% 70%, var(--secondary-color) 2px, transparent 2px);
                background-size: 30px 30px;
                animation: rotate 20s linear infinite;
            }
            
            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .quantum-data {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .data-item {
                display: flex;
                justify-content: space-between;
            }
            
            .data-label {
                font-weight: 600;
                opacity: 0.8;
            }
            
            .data-value {
                color: var(--primary-color);
                font-weight: 600;
            }
            
            .data-recommendation {
                margin-top: 1rem;
                padding: 0.75rem;
                background-color: rgba(var(--primary-color-rgb), 0.1);
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }
            
            .recommendation-label {
                font-weight: 600;
                font-size: 0.9rem;
            }
            
            .recommendation-value {
                font-weight: 600;
                font-size: 1.1rem;
                color: var(--primary-color);
            }
        `;
        document.head.appendChild(style);

        // Add RGB version of primary color for transparency support
        document.documentElement.style.setProperty('--primary-color-rgb', '142, 68, 173'); // This should match the primary color

    } catch (error) {
        console.error('Error loading quantum insights:', error);
        insightsContainer.innerHTML = '<div class="error-message">Failed to load quantum insights</div>';
    }
}

/**
 * Load sacred patterns
 */
async function loadSacredPatterns() {
    const patternsContainer = document.getElementById('sacred-patterns');

    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1600));

        // Sample patterns data (in a real app, this would come from an API)
        const patternsData = [
            {
                name: 'Fibonacci Spiral',
                strength: 89,
                description: 'The divine proportion manifesting in market cycles',
                path: 'BOOK/SACRED_PATTERNS.html#fibonacci'
            },
            {
                name: 'Golden Triangle',
                strength: 76,
                description: 'Three-point harmonic balance in price movements',
                path: 'BOOK/SACRED_PATTERNS.html#golden-triangle'
            },
            {
                name: 'Quantum Metatron',
                strength: 94,
                description: 'The sacred geometry of perfect market equilibrium',
                path: 'BOOK/SACRED_PATTERNS.html#quantum-metatron'
            }
        ];

        // Create patterns HTML
        const patternsHTML = `
            <div class="patterns-list">
                ${patternsData.map(pattern => `
                    <div class="pattern-item">
                        <div class="pattern-header">
                            <div class="pattern-name">${pattern.name}</div>
                            <div class="pattern-strength">
                                <div class="strength-value">${pattern.strength}%</div>
                                <div class="strength-bar">
                                    <div class="strength-fill" style="width: ${pattern.strength}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="pattern-description">${pattern.description}</div>
                        <a href="${pattern.path}" class="pattern-link">View Pattern</a>
                    </div>
                `).join('')}
            </div>
        `;

        patternsContainer.innerHTML = patternsHTML;

        // Add some CSS for patterns
        const style = document.createElement('style');
        style.textContent = `
            .pattern-item {
                padding: 1rem 0;
                border-bottom: 1px solid var(--border-color);
            }
            
            .pattern-item:last-child {
                border-bottom: none;
            }
            
            .pattern-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            
            .pattern-name {
                font-weight: 600;
                color: var(--primary-color);
            }
            
            .pattern-strength {
                text-align: right;
            }
            
            .strength-value {
                font-size: 0.8rem;
                margin-bottom: 0.25rem;
            }
            
            .strength-bar {
                height: 4px;
                width: 80px;
                background-color: var(--border-color);
                border-radius: 2px;
                overflow: hidden;
            }
            
            .strength-fill {
                height: 100%;
                background: linear-gradient(to right, var(--secondary-color), var(--primary-color));
                border-radius: 2px;
            }
            
            .pattern-description {
                font-size: 0.9rem;
                opacity: 0.8;
                margin-bottom: 0.75rem;
            }
            
            .pattern-link {
                font-size: 0.9rem;
                font-weight: 600;
                color: var(--secondary-color);
            }
            
            .pattern-link:hover {
                text-decoration: underline;
            }
        `;
        document.head.appendChild(style);

    } catch (error) {
        console.error('Error loading sacred patterns:', error);
        patternsContainer.innerHTML = '<div class="error-message">Failed to load sacred patterns</div>';
    }
} 