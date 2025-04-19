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
 * NFT Coverage Reporter
 * 
 * Generates comprehensive code coverage reports for NFT components
 * with visualization and recommendations for improving test coverage.
 * 
 * @license MIT
 * @version 1.0.0
 */

// Import dependencies
import { NFTCoverageMetrics } from './coverage_metrics.js';

class NFTCoverageReporter {
    constructor(options = {}) {
        this.options = {
            dataSource: options.dataSource || 'coverage-data.json',
            targetCoverage: options.targetCoverage || 90,
            reportContainer: options.reportContainer || 'coverage-report',
            chartContainer: options.chartContainer || 'coverage-chart',
            autoRun: options.autoRun !== undefined ? options.autoRun : false
        };

        this.metrics = new NFTCoverageMetrics();
        this.metrics.targetCoverage = this.options.targetCoverage;

        if (this.options.autoRun) {
            this.initialize();
        }
    }

    /**
     * Initialize the reporter
     * @returns {Promise<void>}
     */
    async initialize() {
        try {
            await this.loadData();
            this.renderReport();
            this.renderVisualizations();
            this.displayRecommendations();
        } catch (error) {
            console.error('Failed to initialize coverage reporter:', error);
            this.showError(error.message);
        }
    }

    /**
     * Load coverage data from the specified source
     * @returns {Promise<Object>} The loaded coverage data
     */
    async loadData() {
        try {
            return await this.metrics.loadCoverageData(this.options.dataSource);
        } catch (error) {
            console.error('Error loading coverage data:', error);
            throw new Error(`Failed to load coverage data: ${error.message}`);
        }
    }

    /**
     * Render the coverage report
     * @returns {void}
     */
    renderReport() {
        const container = document.getElementById(this.options.reportContainer);
        if (!container) {
            console.warn(`Report container "${this.options.reportContainer}" not found, creating it`);
            const newContainer = document.createElement('div');
            newContainer.id = this.options.reportContainer;
            document.body.appendChild(newContainer);
            this.metrics.renderCoverageReport(this.options.reportContainer);
        } else {
            this.metrics.renderCoverageReport(this.options.reportContainer);
        }
    }

    /**
     * Render coverage visualizations
     * @returns {void}
     */
    renderVisualizations() {
        // Check if Chart.js is loaded
        if (typeof Chart === 'undefined') {
            this.loadChartJs().then(() => {
                this.createChartCanvas();
                this.metrics.renderCoverageChart(this.options.chartContainer);
            }).catch(error => {
                console.error('Failed to load Chart.js:', error);
            });
        } else {
            this.createChartCanvas();
            this.metrics.renderCoverageChart(this.options.chartContainer);
        }
    }

    /**
     * Create canvas for the chart if not exists
     * @returns {void}
     */
    createChartCanvas() {
        if (!document.getElementById(this.options.chartContainer)) {
            const reportContainer = document.getElementById(this.options.reportContainer);
            const chartSection = document.createElement('div');
            chartSection.className = 'coverage-chart-section';

            const chartTitle = document.createElement('h3');
            chartTitle.textContent = 'Coverage Visualization';

            const canvas = document.createElement('canvas');
            canvas.id = this.options.chartContainer;
            canvas.width = 800;
            canvas.height = 400;

            chartSection.appendChild(chartTitle);
            chartSection.appendChild(canvas);

            if (reportContainer) {
                reportContainer.appendChild(chartSection);
            } else {
                document.body.appendChild(chartSection);
            }
        }
    }

    /**
     * Load Chart.js dynamically if not available
     * @returns {Promise<void>}
     */
    loadChartJs() {
        return new Promise((resolve, reject) => {
            if (typeof Chart !== 'undefined') {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = () => {
                // Load the annotation plugin for target line
                const annotationScript = document.createElement('script');
                annotationScript.src = 'https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation';
                annotationScript.onload = resolve;
                annotationScript.onerror = () => reject(new Error('Failed to load Chart.js annotation plugin'));
                document.head.appendChild(annotationScript);
            };
            script.onerror = () => reject(new Error('Failed to load Chart.js'));
            document.head.appendChild(script);
        });
    }

    /**
     * Display recommendations for improving coverage
     * @returns {void}
     */
    displayRecommendations() {
        const recommendations = this.metrics.generateRecommendations();
        if (recommendations.length === 0) {
            return;
        }

        const container = document.getElementById(this.options.reportContainer);
        if (!container) return;

        const recSection = document.createElement('div');
        recSection.className = 'coverage-recommendations';

        const title = document.createElement('h3');
        title.textContent = 'Recommendations to Improve Coverage';
        recSection.appendChild(title);

        const list = document.createElement('ul');
        list.className = 'recommendations-list';

        recommendations.forEach(rec => {
            const item = document.createElement('li');
            item.className = `recommendation priority-${rec.priority}`;

            const header = document.createElement('div');
            header.className = 'recommendation-header';
            header.innerHTML = `
        <span class="component-name">${rec.component}</span>
        <span class="priority-badge ${rec.priority}">Priority: ${rec.priority}</span>
      `;

            const body = document.createElement('div');
            body.className = 'recommendation-body';
            body.innerHTML = `
        <p>${rec.suggestion}</p>
      `;

            // Add uncovered lines if available
            if (rec.uncoveredLines && rec.uncoveredLines.length > 0) {
                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'toggle-lines-btn';
                toggleBtn.textContent = 'Show uncovered lines';

                const linesList = document.createElement('ul');
                linesList.className = 'uncovered-lines';
                linesList.style.display = 'none';

                rec.uncoveredLines.slice(0, 10).forEach(line => {
                    const lineItem = document.createElement('li');
                    lineItem.textContent = `Line ${line.line}: ${line.code || 'Unknown code'}`;
                    linesList.appendChild(lineItem);
                });

                if (rec.uncoveredLines.length > 10) {
                    const moreItem = document.createElement('li');
                    moreItem.className = 'more-lines';
                    moreItem.textContent = `...and ${rec.uncoveredLines.length - 10} more lines`;
                    linesList.appendChild(moreItem);
                }

                toggleBtn.addEventListener('click', () => {
                    const isHidden = linesList.style.display === 'none';
                    linesList.style.display = isHidden ? 'block' : 'none';
                    toggleBtn.textContent = isHidden ? 'Hide uncovered lines' : 'Show uncovered lines';
                });

                body.appendChild(toggleBtn);
                body.appendChild(linesList);
            }

            item.appendChild(header);
            item.appendChild(body);
            list.appendChild(item);
        });

        recSection.appendChild(list);
        container.appendChild(recSection);
    }

    /**
     * Show error message in the report container
     * @param {string} message - Error message to display
     * @returns {void}
     */
    showError(message) {
        const container = document.getElementById(this.options.reportContainer);
        if (!container) {
            console.error('Report container not found, cannot display error');
            return;
        }

        container.innerHTML = `
      <div class="coverage-error">
        <h2>Error Generating Coverage Report</h2>
        <p>${message}</p>
        <button class="retry-btn">Retry</button>
      </div>
    `;

        const retryBtn = container.querySelector('.retry-btn');
        if (retryBtn) {
            retryBtn.addEventListener('click', () => this.initialize());
        }
    }

    /**
     * Generate a static coverage report as HTML
     * @returns {string} HTML content for the report
     */
    generateStaticReport() {
        const overallCoverage = this.metrics.calculateOverallCoverage();
        const coverageStatus = this.metrics.getCoverageStatus(overallCoverage);
        const belowTarget = this.metrics.getComponentsBelowTarget();
        const recommendations = this.metrics.generateRecommendations();

        let html = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NFT Components Coverage Report</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }
          .coverage-report { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
          .coverage-summary { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
          .coverage-gauge { width: 120px; height: 120px; border-radius: 50%; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; }
          .coverage-gauge.low { background-color: #ff4d4d; }
          .coverage-gauge.medium { background-color: #ffa64d; }
          .coverage-gauge.high { background-color: #4dca73; }
          .gauge-value { font-size: 2em; font-weight: bold; }
          .gauge-label { font-size: 0.8em; }
          .coverage-target { text-align: center; }
          .target-status.met { color: #4dca73; font-weight: bold; }
          .target-status.not-met { color: #ff4d4d; font-weight: bold; }
          .coverage-table { width: 100%; border-collapse: collapse; }
          .coverage-table th, .coverage-table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
          .status-badge { padding: 3px 8px; border-radius: 12px; font-size: 0.8em; color: white; }
          .status-badge.low { background-color: #ff4d4d; }
          .status-badge.medium { background-color: #ffa64d; }
          .status-badge.high { background-color: #4dca73; }
          .recommendations-list { list-style-type: none; padding: 0; }
          .recommendation { border: 1px solid #ddd; border-radius: 4px; margin-bottom: 10px; overflow: hidden; }
          .recommendation-header { padding: 10px; display: flex; justify-content: space-between; align-items: center; background-color: #f5f5f5; }
          .recommendation-body { padding: 10px; }
          .priority-badge { padding: 3px 8px; border-radius: 12px; font-size: 0.8em; color: white; }
          .priority-badge.high { background-color: #ff4d4d; }
          .priority-badge.medium { background-color: #ffa64d; }
          .priority-badge.low { background-color: #4dca73; }
          .uncovered-lines { font-family: monospace; background-color: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 4px; }
          .timestamp { font-style: italic; color: #777; margin-top: 20px; }
        </style>
      </head>
      <body>
        <h1>NFT Components Coverage Report</h1>
        <div class="coverage-report">
          <div class="coverage-summary">
            <h2>Test Coverage Summary</h2>
            <div class="coverage-gauge ${coverageStatus}">
              <div class="gauge-value">${overallCoverage}%</div>
              <div class="gauge-label">Overall Coverage</div>
            </div>
            <div class="coverage-target">
              <div class="target-label">Target: ${this.metrics.targetCoverage}%</div>
              <div class="target-status ${overallCoverage >= this.metrics.targetCoverage ? 'met' : 'not-met'}">
                ${overallCoverage >= this.metrics.targetCoverage ? 'Target Met' : 'Target Not Met'}
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
                const status = this.metrics.getCoverageStatus(component.coverage);
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

        if (recommendations.length > 0) {
            html += `
        <div class="coverage-recommendations">
          <h3>Recommendations to Improve Coverage</h3>
          <ul class="recommendations-list">
      `;

            recommendations.forEach(rec => {
                html += `
          <li class="recommendation priority-${rec.priority}">
            <div class="recommendation-header">
              <span class="component-name">${rec.component}</span>
              <span class="priority-badge ${rec.priority}">Priority: ${rec.priority}</span>
            </div>
            <div class="recommendation-body">
              <p>${rec.suggestion}</p>
        `;

                if (rec.uncoveredLines && rec.uncoveredLines.length > 0) {
                    html += `
              <details>
                <summary>Uncovered Lines (${rec.uncoveredLines.length})</summary>
                <ul class="uncovered-lines">
          `;

                    rec.uncoveredLines.slice(0, 10).forEach(line => {
                        html += `<li>Line ${line.line}: ${line.code || 'Unknown code'}</li>`;
                    });

                    if (rec.uncoveredLines.length > 10) {
                        html += `<li class="more-lines">...and ${rec.uncoveredLines.length - 10} more lines</li>`;
                    }

                    html += `
                </ul>
              </details>
          `;
                }

                html += `
            </div>
          </li>
        `;
            });

            html += `
          </ul>
        </div>
      `;
        }

        // Add timestamp
        const now = new Date();
        html += `
        <div class="timestamp">
          Report generated on ${now.toLocaleDateString()} at ${now.toLocaleTimeString()}
        </div>
      </div>
    </body>
    </html>
    `;

        return html;
    }

    /**
     * Download the coverage report as HTML file
     * @param {string} filename - Output filename
     * @returns {void}
     */
    downloadReport(filename = 'nft-coverage-report.html') {
        const html = this.generateStaticReport();
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Export for use in other modules
export default NFTCoverageReporter; 