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
 * NFT Coverage Reporter Utility
 * A utility for generating code coverage reports based on coverage metrics
 * 
 * Version: 1.0.0
 * License: MIT
 */

import NFTCoverageMetrics from './coverage_metrics.js';

class NFTCoverageReporter {
    /**
     * Initialize the coverage reporter
     * @param {Object} options Configuration options
     * @param {Object} options.data Raw coverage data
     * @param {Object} options.metrics Calculated coverage metrics
     * @param {number} options.targetCoverage Target coverage percentage (0-100)
     * @param {string} options.reportFormat Report format ('html', 'markdown', 'json')
     */
    constructor(options = {}) {
        this.data = options.data || null;
        this.metricsCalculator = options.metrics ||
            new NFTCoverageMetrics({
                data: this.data,
                targetCoverage: options.targetCoverage || 90
            });
        this.reportFormat = options.reportFormat || 'html';
        this.targetCoverage = options.targetCoverage || 90;
        this.metrics = null;
    }

    /**
     * Load raw coverage data
     * @param {Object} data Raw coverage data
     */
    loadData(data) {
        this.data = data;
        this.metricsCalculator.loadData(data);
        return this;
    }

    /**
     * Set the target coverage percentage
     * @param {number} targetCoverage Target coverage percentage (0-100)
     */
    setTargetCoverage(targetCoverage) {
        this.targetCoverage = targetCoverage;
        this.metricsCalculator.targetCoverage = targetCoverage;
        return this;
    }

    /**
     * Set the report format
     * @param {string} format Report format ('html', 'markdown', 'json')
     */
    setReportFormat(format) {
        if (!['html', 'markdown', 'json'].includes(format)) {
            throw new Error('Invalid report format. Use "html", "markdown", or "json".');
        }
        this.reportFormat = format;
        return this;
    }

    /**
     * Generate a coverage report
     * @returns {string} Generated report in the specified format
     */
    generateReport() {
        if (!this.data) {
            throw new Error('No coverage data available. Call loadData() first.');
        }

        this.metrics = this.metricsCalculator.calculateMetrics();

        switch (this.reportFormat) {
            case 'html':
                return this.generateHtmlReport();
            case 'markdown':
                return this.generateMarkdownReport();
            case 'json':
                return this.generateJsonReport();
            default:
                return this.generateHtmlReport();
        }
    }

    /**
     * Generate an HTML report
     * @returns {string} HTML report
     */
    generateHtmlReport() {
        const overall = this.metrics.overall;
        const recommendations = this.metricsCalculator.generateRecommendations();
        const components = this.metrics.components;
        const priorities = this.metrics.priorities;
        const benchmark = this.metricsCalculator.getBenchmarkData();

        // Format date
        const reportDate = new Date(this.metrics.timestamp).toLocaleString();

        // Create color classes based on coverage values
        const coverageColor = (coverage) => {
            if (coverage >= this.targetCoverage) return 'success';
            if (coverage >= this.targetCoverage * 0.8) return 'warning';
            return 'danger';
        };

        // Generate recommendations HTML
        const recommendationsHtml = recommendations.map(rec => {
            return `
        <div class="recommendation ${rec.type} ${rec.priority}">
          <h4>${rec.title}</h4>
          <p>${rec.description}</p>
          ${rec.uncoveredLines ? `
            <div class="uncovered-lines">
              <strong>Uncovered Lines:</strong> ${rec.uncoveredLines.join(', ')}
            </div>
          ` : ''}
        </div>
      `;
        }).join('');

        // Generate components table
        const componentsHtml = components
            .sort((a, b) => b.percentage - a.percentage)
            .map(comp => {
                return `
          <tr class="${coverageColor(comp.coverage)}">
            <td>${comp.name}</td>
            <td class="number">${comp.lines}</td>
            <td class="number">${comp.coveredLines}</td>
            <td class="number">${comp.uncoveredLines}</td>
            <td class="number ${coverageColor(comp.coverage)}">
              ${comp.coverage.toFixed(1)}%
              <div class="progress">
                <div class="progress-bar ${coverageColor(comp.coverage)}" 
                     style="width: ${comp.coverage}%"></div>
              </div>
            </td>
            <td class="number">${comp.targetGap > 0 ? comp.targetGap.toFixed(1) + '%' : '✓'}</td>
          </tr>
        `;
            }).join('');

        // Generate priorities table
        const prioritiesHtml = priorities.slice(0, 5).map((comp, index) => {
            return `
        <tr>
          <td>${index + 1}</td>
          <td>${comp.name}</td>
          <td class="number">${comp.coverage.toFixed(1)}%</td>
          <td class="number">${comp.targetGap.toFixed(1)}%</td>
          <td class="number">${Math.ceil(comp.lines * (this.targetCoverage / 100) - comp.coveredLines)}</td>
          <td class="number">${comp.priorityScore.toFixed(3)}</td>
        </tr>
      `;
        }).join('');

        // Generate the full HTML report
        return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>NFT Code Coverage Report</title>
      <style>
        :root {
          --success-color: #28a745;
          --warning-color: #ffc107;
          --danger-color: #dc3545;
          --info-color: #17a2b8;
          --primary-color: #0d6efd;
          --secondary-color: #6c757d;
          --light-color: #f8f9fa;
          --dark-color: #343a40;
        }
        
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #333;
          margin: 0;
          padding: 20px;
          background-color: #f9f9f9;
        }
        
        .container {
          max-width: 1200px;
          margin: 0 auto;
          background-color: #fff;
          border-radius: 5px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          padding: 20px;
        }
        
        header {
          text-align: center;
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 1px solid #eee;
        }
        
        header h1 {
          margin: 0;
          color: #333;
        }
        
        .report-info {
          font-size: 0.9rem;
          color: #666;
          margin-top: 10px;
        }
        
        .section {
          margin-bottom: 30px;
        }
        
        h2 {
          color: #0d6efd;
          border-bottom: 1px solid #eee;
          padding-bottom: 10px;
          margin-top: 30px;
        }
        
        h3 {
          color: #444;
        }
        
        .metrics {
          display: flex;
          flex-wrap: wrap;
          gap: 20px;
          margin-bottom: 20px;
        }
        
        .metric-card {
          flex: 1;
          min-width: 200px;
          background-color: #fff;
          border-radius: 5px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
          padding: 15px;
          text-align: center;
        }
        
        .metric-title {
          font-size: 0.9rem;
          font-weight: bold;
          margin-bottom: 5px;
          color: #555;
        }
        
        .metric-value {
          font-size: 2rem;
          font-weight: bold;
          margin: 10px 0;
        }
        
        .metric-value.success { color: var(--success-color); }
        .metric-value.warning { color: var(--warning-color); }
        .metric-value.danger { color: var(--danger-color); }
        
        .metric-comparison {
          font-size: 0.85rem;
          color: #777;
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 20px 0;
          font-size: 0.9rem;
        }
        
        th, td {
          padding: 12px 15px;
          text-align: left;
          border-bottom: 1px solid #eee;
        }
        
        th {
          background-color: #f8f9fa;
          font-weight: bold;
          color: #333;
        }
        
        tr:hover {
          background-color: #f5f5f5;
        }
        
        td.number {
          text-align: right;
          font-family: monospace;
          font-size: 0.95rem;
        }
        
        .success { color: var(--success-color); }
        .warning { color: var(--warning-color); }
        .danger { color: var(--danger-color); }
        
        .progress {
          height: 4px;
          background-color: #f0f0f0;
          border-radius: 2px;
          margin-top: 5px;
          overflow: hidden;
        }
        
        .progress-bar {
          height: 100%;
        }
        
        .progress-bar.success { background-color: var(--success-color); }
        .progress-bar.warning { background-color: var(--warning-color); }
        .progress-bar.danger { background-color: var(--danger-color); }
        
        .recommendation {
          margin-bottom: 15px;
          padding: 15px;
          border-radius: 5px;
          border-left: 4px solid #ddd;
        }
        
        .recommendation h4 {
          margin-top: 0;
          margin-bottom: 10px;
        }
        
        .recommendation p {
          margin: 0 0 10px 0;
        }
        
        .recommendation.success { border-left-color: var(--success-color); background-color: #f0f9f0; }
        .recommendation.warning { border-left-color: var(--warning-color); background-color: #fff9e6; }
        .recommendation.danger { border-left-color: var(--danger-color); background-color: #fdeeee; }
        .recommendation.info { border-left-color: var(--info-color); background-color: #e6f7f9; }
        .recommendation.action { border-left-color: var(--primary-color); background-color: #e6f0ff; }
        .recommendation.component { border-left-color: var(--secondary-color); background-color: #f0f0f0; }
        
        .high { order: 1; }
        .medium { order: 2; }
        .low { order: 3; }
        
        .recommendations-container {
          display: flex;
          flex-direction: column;
        }
        
        .uncovered-lines {
          font-family: monospace;
          font-size: 0.85rem;
          margin-top: 5px;
          padding: 8px;
          background-color: rgba(0,0,0,0.05);
          border-radius: 3px;
        }
        
        footer {
          margin-top: 40px;
          padding-top: 20px;
          border-top: 1px solid #eee;
          text-align: center;
          font-size: 0.85rem;
          color: #777;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <header>
          <h1>NFT Code Coverage Report</h1>
          <div class="report-info">
            Report generated on ${reportDate} | Target coverage: ${this.targetCoverage}%
          </div>
        </header>
        
        <section class="section">
          <h2>Overall Coverage</h2>
          
          <div class="metrics">
            <div class="metric-card">
              <div class="metric-title">Overall Coverage</div>
              <div class="metric-value ${coverageColor(overall.coverage)}">${overall.coverage.toFixed(1)}%</div>
              <div class="metric-comparison">
                ${overall.targetGap > 0 ?
                `${overall.targetGap.toFixed(1)}% below target` :
                'Target met'}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-title">Total Lines</div>
              <div class="metric-value">${overall.totalLines}</div>
              <div class="metric-comparison">
                ${overall.coveredLines} covered / ${overall.uncoveredLines} uncovered
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-title">Components Status</div>
              <div class="metric-value">
                ${this.metrics.targetStatus.componentsMeetingTarget} / ${this.metrics.targetStatus.componentsTotal}
              </div>
              <div class="metric-comparison">
                ${this.metrics.targetStatus.percentageMeetingTarget}% of components meet target
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-title">Industry Comparison</div>
              <div class="metric-value">
                ${benchmark.percentile}<sup>th</sup> percentile
              </div>
              <div class="metric-comparison">
                ${benchmark.comparison.vsIndustryNft > 0 ?
                `${benchmark.comparison.vsIndustryNft.toFixed(1)}% above` :
                `${Math.abs(benchmark.comparison.vsIndustryNft).toFixed(1)}% below`} 
                NFT industry average
              </div>
            </div>
          </div>
        </section>
        
        <section class="section">
          <h2>Recommendations</h2>
          
          <div class="recommendations-container">
            ${recommendationsHtml}
          </div>
        </section>
        
        <section class="section">
          <h2>Priority Components</h2>
          <p>Top 5 components that need attention, ordered by priority score:</p>
          
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Component</th>
                <th>Current Coverage</th>
                <th>Target Gap</th>
                <th>Lines to Cover</th>
                <th>Priority Score</th>
              </tr>
            </thead>
            <tbody>
              ${prioritiesHtml}
            </tbody>
          </table>
        </section>
        
        <section class="section">
          <h2>All Components</h2>
          
          <table>
            <thead>
              <tr>
                <th>Component</th>
                <th>Total Lines</th>
                <th>Covered Lines</th>
                <th>Uncovered Lines</th>
                <th>Coverage</th>
                <th>Target Gap</th>
              </tr>
            </thead>
            <tbody>
              ${componentsHtml}
            </tbody>
          </table>
        </section>
        
        <footer>
          Generated using NFT Coverage Reporter | Version 1.0.0
        </footer>
      </div>
    </body>
    </html>
    `;
    }

    /**
     * Generate a Markdown report
     * @returns {string} Markdown report
     */
    generateMarkdownReport() {
        const overall = this.metrics.overall;
        const recommendations = this.metricsCalculator.generateRecommendations();
        const components = this.metrics.components;
        const priorities = this.metrics.priorities;
        const benchmark = this.metricsCalculator.getBenchmarkData();

        // Format date
        const reportDate = new Date(this.metrics.timestamp).toLocaleString();

        // Define helper function for status emoji
        const statusEmoji = (value, target) => {
            if (value >= target) return '✅';
            if (value >= target * 0.8) return '⚠️';
            return '❌';
        };

        // Generate recommendations section
        const recommendationsMd = recommendations.map(rec => {
            const prefix = rec.type === 'success' ? '✅' :
                rec.type === 'warning' ? '⚠️' :
                    rec.type === 'info' ? 'ℹ️' :
                        rec.type === 'action' ? '🚀' :
                            rec.type === 'component' ? '🧩' : '➡️';

            let md = `### ${prefix} ${rec.title}\n\n${rec.description}\n\n`;

            if (rec.uncoveredLines && rec.uncoveredLines.length > 0) {
                md += `**Uncovered Lines:** ${rec.uncoveredLines.join(', ')}\n\n`;
            }

            return md;
        }).join('');

        // Generate components table
        const componentsMd = components
            .sort((a, b) => b.percentage - a.percentage)
            .map(comp => {
                const status = statusEmoji(comp.coverage, this.targetCoverage);
                return `| ${comp.name} | ${comp.lines} | ${comp.coveredLines} | ${comp.uncoveredLines} | ${comp.coverage.toFixed(1)}% ${status} | ${comp.targetGap > 0 ? comp.targetGap.toFixed(1) + '%' : '✅'} |`;
            }).join('\n');

        // Generate priorities table
        const prioritiesMd = priorities.slice(0, 5).map((comp, index) => {
            return `| ${index + 1} | ${comp.name} | ${comp.coverage.toFixed(1)}% | ${comp.targetGap.toFixed(1)}% | ${Math.ceil(comp.lines * (this.targetCoverage / 100) - comp.coveredLines)} | ${comp.priorityScore.toFixed(3)} |`;
        }).join('\n');

        // Generate the full Markdown report
        return `# NFT Code Coverage Report

*Report generated on ${reportDate} | Target coverage: ${this.targetCoverage}%*

## Overall Coverage

- **Overall Coverage:** ${overall.coverage.toFixed(1)}% ${statusEmoji(overall.coverage, this.targetCoverage)}
- **Total Lines:** ${overall.totalLines} (${overall.coveredLines} covered, ${overall.uncoveredLines} uncovered)
- **Components Meeting Target:** ${this.metrics.targetStatus.componentsMeetingTarget} / ${this.metrics.targetStatus.componentsTotal} (${this.metrics.targetStatus.percentageMeetingTarget}%)
- **Industry Comparison:** ${benchmark.percentile}th percentile (${benchmark.comparison.vsIndustryNft > 0 ? `${benchmark.comparison.vsIndustryNft.toFixed(1)}% above` : `${Math.abs(benchmark.comparison.vsIndustryNft).toFixed(1)}% below`} NFT industry average)

## Recommendations

${recommendationsMd}

## Priority Components

Top 5 components that need attention, ordered by priority score:

| Rank | Component | Current Coverage | Target Gap | Lines to Cover | Priority Score |
|------|-----------|------------------|------------|----------------|---------------|
${prioritiesMd}

## All Components

| Component | Total Lines | Covered Lines | Uncovered Lines | Coverage | Target Gap |
|-----------|-------------|---------------|----------------|----------|------------|
${componentsMd}

---

*Generated using NFT Coverage Reporter | Version 1.0.0*
`;
    }

    /**
     * Generate a JSON report
     * @returns {string} JSON report
     */
    generateJsonReport() {
        const recommendations = this.metricsCalculator.generateRecommendations();
        const benchmark = this.metricsCalculator.getBenchmarkData();

        // Create the report structure
        const report = {
            metadata: {
                title: 'NFT Code Coverage Report',
                timestamp: this.metrics.timestamp,
                targetCoverage: this.targetCoverage,
                version: '1.0.0'
            },
            metrics: this.metrics,
            recommendations,
            benchmark,
            formatVersion: '1.0'
        };

        return JSON.stringify(report, null, 2);
    }

    /**
     * Generate and download a report
     * @param {string} filename The filename for the download (without extension)
     */
    downloadReport(filename = 'nft-coverage-report') {
        const report = this.generateReport();
        let fileExtension = '';
        let mimeType = '';

        // Set the appropriate extension and MIME type
        switch (this.reportFormat) {
            case 'html':
                fileExtension = 'html';
                mimeType = 'text/html';
                break;
            case 'markdown':
                fileExtension = 'md';
                mimeType = 'text/markdown';
                break;
            case 'json':
                fileExtension = 'json';
                mimeType = 'application/json';
                break;
        }

        // Create a download link
        const blob = new Blob([report], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${filename}.${fileExtension}`;

        // Trigger the download
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Export the class
export default NFTCoverageReporter; 