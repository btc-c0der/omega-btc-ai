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
 * NFT Component Coverage Metrics Utility
 * 
 * This utility provides functions to calculate, analyze and visualize code coverage
 * metrics for the NFT components in the Divine Dashboard.
 * 
 * @license MIT
 * @version 1.0.0
 */

class NFTCoverageMetrics {
    constructor() {
        this.coverageData = {};
        this.targetCoverage = 90;
        this.coverageThresholds = {
            low: 50,
            medium: 75,
            high: 90
        };
    }

    /**
     * Load coverage data from a JSON file or API
     * @param {Object|string} source - Coverage data object or URL to fetch from
     * @returns {Promise<Object>} The loaded coverage data
     */
    async loadCoverageData(source) {
        try {
            if (typeof source === 'string') {
                const response = await fetch(source);
                if (!response.ok) {
                    throw new Error(`Failed to fetch coverage data: ${response.statusText}`);
                }
                this.coverageData = await response.json();
            } else {
                this.coverageData = source;
            }
            return this.coverageData;
        } catch (error) {
            console.error('Error loading coverage data:', error);
            throw error;
        }
    }

    /**
     * Calculate overall coverage percentage
     * @returns {number} Coverage percentage (0-100)
     */
    calculateOverallCoverage() {
        if (!this.coverageData || !this.coverageData.components) {
            return 0;
        }

        const components = this.coverageData.components;
        let totalLines = 0;
        let coveredLines = 0;

        Object.keys(components).forEach(component => {
            totalLines += components[component].totalLines || 0;
            coveredLines += components[component].coveredLines || 0;
        });

        return totalLines === 0 ? 0 : Math.round((coveredLines / totalLines) * 100);
    }

    /**
     * Get coverage status based on thresholds
     * @param {number} coverage - Coverage percentage
     * @returns {string} Status: 'low', 'medium', or 'high'
     */
    getCoverageStatus(coverage) {
        if (coverage < this.coverageThresholds.low) return 'low';
        if (coverage < this.coverageThresholds.medium) return 'medium';
        return 'high';
    }

    /**
     * Identify components with coverage below target
     * @returns {Array} List of components below target coverage
     */
    getComponentsBelowTarget() {
        if (!this.coverageData || !this.coverageData.components) {
            return [];
        }

        const components = this.coverageData.components;
        const belowTarget = [];

        Object.keys(components).forEach(component => {
            const comp = components[component];
            const coverage = comp.totalLines === 0 ? 0 :
                Math.round((comp.coveredLines / comp.totalLines) * 100);

            if (coverage < this.targetCoverage) {
                belowTarget.push({
                    name: component,
                    coverage: coverage,
                    missingCoverage: this.targetCoverage - coverage,
                    uncoveredLines: comp.uncoveredLines || []
                });
            }
        });

        return belowTarget.sort((a, b) => a.coverage - b.coverage);
    }

    /**
     * Generate an HTML report for coverage metrics
     * @param {string} containerId - ID of the container element to render the report
     * @returns {void}
     */
    renderCoverageReport(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID "${containerId}" not found`);
            return;
        }

        const overallCoverage = this.calculateOverallCoverage();
        const coverageStatus = this.getCoverageStatus(overallCoverage);
        const belowTarget = this.getComponentsBelowTarget();

        // Create report HTML
        let html = `
      <div class="coverage-report">
        <div class="coverage-summary">
          <h2>NFT Components Test Coverage</h2>
          <div class="coverage-gauge ${coverageStatus}">
            <div class="gauge-value">${overallCoverage}%</div>
            <div class="gauge-label">Overall Coverage</div>
          </div>
          <div class="coverage-target">
            <div class="target-label">Target: ${this.targetCoverage}%</div>
            <div class="target-status ${overallCoverage >= this.targetCoverage ? 'met' : 'not-met'}">
              ${overallCoverage >= this.targetCoverage ? 'Target Met' : 'Target Not Met'}
            </div>
          </div>
        </div>
    `;

        if (belowTarget.length > 0) {
            html += `
        <div class="components-below-target">
          <h3>Components Below Target Coverage</h3>
          <table class="coverage-table">
            <thead>
              <tr>
                <th>Component</th>
                <th>Coverage</th>
                <th>Missing</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
      `;

            belowTarget.forEach(component => {
                const status = this.getCoverageStatus(component.coverage);
                html += `
          <tr>
            <td>${component.name}</td>
            <td>${component.coverage}%</td>
            <td>${component.missingCoverage}%</td>
            <td><span class="status-badge ${status}">${status}</span></td>
          </tr>
        `;
            });

            html += `
            </tbody>
          </table>
        </div>
      `;
        }

        html += `</div>`;
        container.innerHTML = html;
    }

    /**
     * Generate coverage data for visualization (e.g., charts)
     * @returns {Object} Data formatted for visualization libraries
     */
    getVisualizationData() {
        if (!this.coverageData || !this.coverageData.components) {
            return { labels: [], values: [] };
        }

        const components = this.coverageData.components;
        const labels = [];
        const values = [];

        Object.keys(components).forEach(component => {
            const comp = components[component];
            const coverage = comp.totalLines === 0 ? 0 :
                Math.round((comp.coveredLines / comp.totalLines) * 100);

            labels.push(component);
            values.push(coverage);
        });

        return {
            labels,
            values,
            target: this.targetCoverage
        };
    }

    /**
     * Render a bar chart of component coverage using Chart.js
     * @param {string} canvasId - ID of the canvas element for the chart
     * @returns {void}
     */
    renderCoverageChart(canvasId) {
        if (typeof Chart === 'undefined') {
            console.error('Chart.js is required for rendering charts');
            return;
        }

        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            console.error(`Canvas with ID "${canvasId}" not found`);
            return;
        }

        const ctx = canvas.getContext('2d');
        const { labels, values, target } = this.getVisualizationData();

        const backgroundColors = values.map(value => {
            if (value < this.coverageThresholds.low) return '#ff4d4d';
            if (value < this.coverageThresholds.medium) return '#ffa64d';
            return '#4dca73';
        });

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Coverage (%)',
                    data: values,
                    backgroundColor: backgroundColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Coverage (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Components'
                        }
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                yMin: target,
                                yMax: target,
                                borderColor: 'rgb(75, 192, 192)',
                                borderWidth: 2,
                                label: {
                                    content: `Target (${target}%)`,
                                    enabled: true,
                                    position: 'end'
                                }
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Generate recommendations to improve coverage
     * @returns {Array} List of recommendations
     */
    generateRecommendations() {
        const belowTarget = this.getComponentsBelowTarget();
        const recommendations = [];

        belowTarget.forEach(component => {
            const status = this.getCoverageStatus(component.coverage);
            let priority = 'low';

            if (status === 'low') {
                priority = 'high';
            } else if (status === 'medium') {
                priority = 'medium';
            }

            recommendations.push({
                component: component.name,
                priority: priority,
                missingCoverage: component.missingCoverage,
                suggestion: `Add tests for ${component.uncoveredLines.length} uncovered lines to improve coverage by ${component.missingCoverage}%.`,
                uncoveredLines: component.uncoveredLines
            });
        });

        return recommendations.sort((a, b) => {
            const priorityOrder = { high: 0, medium: 1, low: 2 };
            return priorityOrder[a.priority] - priorityOrder[b.priority];
        });
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NFTCoverageMetrics };
} else {
    window.NFTCoverageMetrics = NFTCoverageMetrics;
} 