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
 * NFT Coverage Metrics Utility
 * A utility for calculating and analyzing code coverage for NFT components
 * 
 * Version: 1.0.0
 * License: MIT
 */

class NFTCoverageMetrics {
    /**
     * Initialize the coverage metrics calculator
     * @param {Object} options Configuration options
     * @param {Object} options.data Coverage data object
     * @param {number} options.targetCoverage Target coverage percentage (0-100)
     */
    constructor(options = {}) {
        this.data = options.data || null;
        this.targetCoverage = options.targetCoverage || 90;
        this.metrics = {};
    }

    /**
     * Load coverage data
     * @param {Object} data Coverage data
     */
    loadData(data) {
        this.data = data;
        return this;
    }

    /**
     * Calculate all coverage metrics
     * @returns {Object} Calculated metrics
     */
    calculateMetrics() {
        if (!this.data) {
            throw new Error('No coverage data available. Call loadData() first.');
        }

        const metrics = {
            overall: this.calculateOverallMetrics(),
            components: this.calculateComponentMetrics(),
            targetStatus: this.calculateTargetStatus(),
            priorities: this.calculatePriorities(),
            complexity: this.calculateComplexityMetrics(),
            impact: this.calculateImpactAssessment(),
            timestamp: this.data.coverageTimestamp || new Date().toISOString()
        };

        this.metrics = metrics;
        return metrics;
    }

    /**
     * Calculate overall metrics
     * @returns {Object} Overall metrics
     */
    calculateOverallMetrics() {
        const overallStats = this.data.overallStats || {};

        // If no overall stats, calculate from components
        if (!overallStats.totalLines) {
            const totals = this.data.components.reduce((acc, component) => {
                acc.totalLines += component.lines || 0;
                acc.coveredLines += component.coveredLines || 0;
                return acc;
            }, { totalLines: 0, coveredLines: 0 });

            overallStats.totalLines = totals.totalLines;
            overallStats.coveredLines = totals.coveredLines;
            overallStats.coverage = totals.totalLines ?
                Math.round((totals.coveredLines / totals.totalLines) * 100) : 0;
        }

        return {
            totalLines: overallStats.totalLines || 0,
            coveredLines: overallStats.coveredLines || 0,
            uncoveredLines: overallStats.totalLines - overallStats.coveredLines || 0,
            coverage: overallStats.coverage || 0,
            targetGap: Math.max(0, this.targetCoverage - overallStats.coverage) || 0,
            status: (overallStats.coverage >= this.targetCoverage) ? 'met' : 'not met'
        };
    }

    /**
     * Calculate component-level metrics
     * @returns {Array} Component metrics
     */
    calculateComponentMetrics() {
        return (this.data.components || []).map(component => {
            return {
                name: component.name,
                path: component.path,
                lines: component.lines || 0,
                coveredLines: component.coveredLines || 0,
                uncoveredLines: component.lines - component.coveredLines || 0,
                coverage: component.coverage || 0,
                complexity: component.complexity || 0,
                targetGap: Math.max(0, this.targetCoverage - component.coverage) || 0,
                status: (component.coverage >= this.targetCoverage) ? 'met' : 'not met',
                percentage: ((component.lines || 0) / this.calculateOverallMetrics().totalLines) * 100,
                uncoveredLineNumbers: component.uncoveredLines || []
            };
        });
    }

    /**
     * Calculate target status metrics
     * @returns {Object} Target status metrics
     */
    calculateTargetStatus() {
        const components = this.calculateComponentMetrics();
        const meetingTarget = components.filter(c => c.coverage >= this.targetCoverage);

        return {
            componentsTotal: components.length,
            componentsMeetingTarget: meetingTarget.length,
            componentsBelowTarget: components.length - meetingTarget.length,
            percentageMeetingTarget: components.length ?
                Math.round((meetingTarget.length / components.length) * 100) : 0,
            averageTargetGap: components.length ?
                components.reduce((sum, c) => sum + c.targetGap, 0) / components.length : 0
        };
    }

    /**
     * Calculate prioritized list of components to improve
     * @returns {Array} Prioritized components
     */
    calculatePriorities() {
        const components = this.calculateComponentMetrics();

        // Calculate a priority score based on:
        // 1. Gap to target coverage
        // 2. Component size (bigger components are higher priority)
        // 3. Code complexity
        const withPriorityScore = components.map(component => {
            const gapWeight = 0.5;
            const sizeWeight = 0.3;
            const complexityWeight = 0.2;

            const gapScore = (component.targetGap / 100) * gapWeight;
            const sizeScore = (component.percentage / 100) * sizeWeight;
            const complexityScore = (component.complexity / 50) * complexityWeight; // Assuming max complexity of 50

            return {
                ...component,
                priorityScore: gapScore + sizeScore + complexityScore
            };
        });

        // Filter out components that already meet the target
        return withPriorityScore
            .filter(component => component.coverage < this.targetCoverage)
            .sort((a, b) => b.priorityScore - a.priorityScore);
    }

    /**
     * Calculate complexity metrics
     * @returns {Object} Complexity metrics
     */
    calculateComplexityMetrics() {
        const components = this.calculateComponentMetrics();

        const totalComplexity = components.reduce((sum, c) => sum + c.complexity, 0);
        const averageComplexity = components.length ? totalComplexity / components.length : 0;

        // Find the correlation between complexity and coverage
        const n = components.length;
        if (n <= 1) {
            return {
                totalComplexity,
                averageComplexity,
                complexityCoverageCorrelation: 0
            };
        }

        // Calculate Pearson correlation coefficient
        const sumX = components.reduce((sum, c) => sum + c.complexity, 0);
        const sumY = components.reduce((sum, c) => sum + c.coverage, 0);
        const sumXY = components.reduce((sum, c) => sum + (c.complexity * c.coverage), 0);
        const sumXSq = components.reduce((sum, c) => sum + (c.complexity * c.complexity), 0);
        const sumYSq = components.reduce((sum, c) => sum + (c.coverage * c.coverage), 0);

        const numerator = n * sumXY - sumX * sumY;
        const denominator = Math.sqrt((n * sumXSq - sumX * sumX) * (n * sumYSq - sumY * sumY));

        const correlation = denominator !== 0 ? numerator / denominator : 0;

        return {
            totalComplexity,
            averageComplexity,
            complexityCoverageCorrelation: correlation,
            interpretCorrelation: this.interpretCorrelation(correlation)
        };
    }

    /**
     * Interpret correlation value
     * @param {number} correlation Correlation coefficient
     * @returns {string} Interpretation of correlation
     */
    interpretCorrelation(correlation) {
        const abs = Math.abs(correlation);
        if (abs >= 0.7) {
            return correlation > 0 ?
                'Strong positive correlation between complexity and coverage' :
                'Strong negative correlation between complexity and coverage';
        } else if (abs >= 0.3) {
            return correlation > 0 ?
                'Moderate positive correlation between complexity and coverage' :
                'Moderate negative correlation between complexity and coverage';
        } else {
            return 'Weak or no correlation between complexity and coverage';
        }
    }

    /**
     * Calculate the impact assessment of improving coverage
     * @returns {Object} Impact assessment
     */
    calculateImpactAssessment() {
        const priorities = this.calculatePriorities();
        const overall = this.calculateOverallMetrics();

        // Simulate the impact of fixing the top components
        const impactAssessments = [1, 3, 5].map(count => {
            const topComponents = priorities.slice(0, count);

            // Calculate how many lines would need to be covered to reach the target
            const additionalLinesNeeded = topComponents.reduce((sum, component) => {
                const linesToTarget = Math.ceil(component.lines * (this.targetCoverage / 100)) - component.coveredLines;
                return sum + Math.max(0, linesToTarget);
            }, 0);

            // Calculate the new overall coverage if we covered these lines
            const newCoveredLines = overall.coveredLines + additionalLinesNeeded;
            const newCoverage = (newCoveredLines / overall.totalLines) * 100;

            return {
                componentCount: count,
                components: topComponents.map(c => c.name),
                additionalLinesNeeded,
                projectedCoverage: newCoverage,
                improvementPercentage: newCoverage - overall.coverage,
                wouldMeetTarget: newCoverage >= this.targetCoverage
            };
        });

        return {
            currentGap: overall.targetGap,
            minLinesNeeded: Math.ceil((overall.totalLines * (this.targetCoverage / 100)) - overall.coveredLines),
            impactAssessments
        };
    }

    /**
     * Generate recommendations for improving coverage
     * @returns {Array} List of recommendations
     */
    generateRecommendations() {
        const overall = this.calculateOverallMetrics();
        const priorities = this.calculatePriorities();
        const impact = this.calculateImpactAssessment();
        const complexity = this.calculateComplexityMetrics();

        const recommendations = [];

        // Overall status recommendation
        if (overall.status === 'met') {
            recommendations.push({
                type: 'success',
                title: 'Target Coverage Met',
                description: `Your overall coverage of ${overall.coverage.toFixed(1)}% meets the target of ${this.targetCoverage}%.`,
                priority: 'low'
            });
        } else {
            recommendations.push({
                type: 'warning',
                title: 'Increase Overall Coverage',
                description: `Your overall coverage of ${overall.coverage.toFixed(1)}% is below the target of ${this.targetCoverage}%. You need to cover approximately ${impact.minLinesNeeded} more lines.`,
                priority: 'high'
            });
        }

        // Top priority components
        if (priorities.length > 0) {
            const topThree = priorities.slice(0, 3);

            recommendations.push({
                type: 'info',
                title: 'Focus on High-Priority Components',
                description: `Prioritize improving coverage for: ${topThree.map(c => c.name).join(', ')}. These have the biggest impact on overall coverage.`,
                priority: 'high',
                components: topThree.map(c => c.name)
            });

            // For each top component, specific recommendations
            topThree.forEach(component => {
                recommendations.push({
                    type: 'component',
                    title: `Improve ${component.name}`,
                    description: `Current coverage: ${component.coverage.toFixed(1)}%. Target gap: ${component.targetGap.toFixed(1)}%. Focus on the ${Math.min(10, component.uncoveredLineNumbers.length)} uncovered lines, starting with: ${component.uncoveredLineNumbers.slice(0, 5).join(', ')}...`,
                    priority: 'medium',
                    component: component.name,
                    uncoveredLines: component.uncoveredLineNumbers.slice(0, 10)
                });
            });
        }

        // Complexity assessment
        if (complexity.complexityCoverageCorrelation < -0.3) {
            recommendations.push({
                type: 'warning',
                title: 'Address Complex Components',
                description: `There's a ${complexity.interpretCorrelation}. Complex components tend to have lower coverage, which may indicate unclear code that's difficult to test.`,
                priority: 'medium'
            });
        }

        // Impact assessment based on feasibility
        const bestImpact = impact.impactAssessments.find(ia => ia.wouldMeetTarget) ||
            impact.impactAssessments[impact.impactAssessments.length - 1];

        if (bestImpact) {
            recommendations.push({
                type: 'action',
                title: 'Most Efficient Path to Target',
                description: `Improve ${bestImpact.componentCount} component${bestImpact.componentCount !== 1 ? 's' : ''} (${bestImpact.components.join(', ')}) to reach a projected coverage of ${bestImpact.projectedCoverage.toFixed(1)}%. This requires covering approximately ${bestImpact.additionalLinesNeeded} more lines.`,
                priority: 'high',
                components: bestImpact.components
            });
        }

        return recommendations;
    }

    /**
     * Get the benchmarking data for comparison
     * @returns {Object} Benchmarking data
     */
    getBenchmarkData() {
        // Industry benchmarks (example values)
        const industryAverages = {
            web3: 85,
            blockchain: 82,
            nft: 78,
            fintech: 90,
            overall: 80
        };

        const overall = this.calculateOverallMetrics();

        return {
            current: overall.coverage,
            target: this.targetCoverage,
            industry: {
                nft: industryAverages.nft,
                blockchain: industryAverages.blockchain,
                overall: industryAverages.overall
            },
            comparison: {
                vsTarget: overall.coverage - this.targetCoverage,
                vsIndustryNft: overall.coverage - industryAverages.nft,
                vsIndustryBlockchain: overall.coverage - industryAverages.blockchain,
                percentile: this.calculatePercentile(overall.coverage)
            }
        };
    }

    /**
     * Calculate the approximate percentile based on industry data
     * @param {number} coverage The coverage percentage
     * @returns {number} Approximate percentile
     */
    calculatePercentile(coverage) {
        // This is a simplified model assuming normal distribution
        // Real implementation would use actual industry distribution data
        const mean = 75; // Industry mean coverage
        const stdDev = 15; // Standard deviation

        // Convert to z-score
        const zScore = (coverage - mean) / stdDev;

        // Approximate percentile using error function
        const percentile = Math.min(100, Math.max(0,
            Math.round(50 * (1 + this.erf(zScore / Math.sqrt(2))))
        ));

        return percentile;
    }

    /**
     * Error function approximation for percentile calculation
     * @param {number} x Input value
     * @returns {number} Error function result
     */
    erf(x) {
        // Constants
        const a1 = 0.254829592;
        const a2 = -0.284496736;
        const a3 = 1.421413741;
        const a4 = -1.453152027;
        const a5 = 1.061405429;
        const p = 0.3275911;

        // Save the sign
        const sign = x < 0 ? -1 : 1;
        x = Math.abs(x);

        // Formula 7.1.26 from Abramowitz and Stegun
        const t = 1.0 / (1.0 + p * x);
        const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

        return sign * y;
    }
}

// Export the class
export default NFTCoverageMetrics; 