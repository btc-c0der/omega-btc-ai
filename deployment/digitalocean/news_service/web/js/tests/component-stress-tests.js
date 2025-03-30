// OMEGA BTC AI Component Stress Tests
console.log('Loading component stress tests...');

// Main stress test controller
class ComponentStressTests {
    constructor() {
        this.tests = {
            bitcoin3D: {
                enabled: true,
                duration: 30000, // 30 seconds by default
                updateInterval: 50, // 50ms intervals = 20 updates per second
                intensity: 'medium', // low, medium, high
                running: false
            },
            fearGreed: {
                enabled: true,
                duration: 30000,
                updateInterval: 100,
                intensity: 'medium',
                running: false
            },
            translations: {
                enabled: true,
                duration: 20000,
                updateInterval: 1000,
                running: false
            },
            domUpdates: {
                enabled: true,
                duration: 20000,
                updateInterval: 200,
                running: false
            }
        };

        // Performance metrics
        this.metrics = {
            frames: 0,
            lastFrameTime: 0,
            frameRates: [],
            memoryUsage: [],
            startMemory: null,
            peakMemory: 0,
            domOperations: 0,
            errors: []
        };

        // FPS monitoring
        this.fpsMonitoring = false;
    }

    // Start all stress tests
    async runAll(duration = 60000) {
        console.log(`🔄 Starting all component stress tests for ${duration / 1000} seconds`);

        // Reset metrics
        this.resetMetrics();

        // Start FPS monitoring
        this.startFpsMonitoring();

        // Start memory monitoring
        this.startMemoryMonitoring();

        // Start individual tests
        const testPromises = [];
        if (this.tests.bitcoin3D.enabled) {
            testPromises.push(this.runBitcoin3DStressTest({ duration }));
        }

        if (this.tests.fearGreed.enabled) {
            testPromises.push(this.runFearGreedStressTest({ duration }));
        }

        if (this.tests.translations.enabled) {
            testPromises.push(this.runTranslationStressTest({ duration }));
        }

        if (this.tests.domUpdates.enabled) {
            testPromises.push(this.runDomStressTest({ duration }));
        }

        // Wait for all tests to complete
        await Promise.all(testPromises);

        // Stop monitoring
        this.stopFpsMonitoring();
        this.stopMemoryMonitoring();

        // Report results
        this.reportResults();

        return this.metrics;
    }

    // Reset metrics before starting tests
    resetMetrics() {
        this.metrics = {
            frames: 0,
            lastFrameTime: 0,
            frameRates: [],
            memoryUsage: [],
            startMemory: null,
            peakMemory: 0,
            domOperations: 0,
            errors: []
        };
    }

    // Report test results
    reportResults() {
        console.log('📊 Component Stress Test Results:');

        // Calculate average frame rate
        const avgFrameRate = this.metrics.frameRates.length
            ? this.metrics.frameRates.reduce((sum, rate) => sum + rate, 0) / this.metrics.frameRates.length
            : 0;

        console.log(`Average frame rate: ${avgFrameRate.toFixed(2)} FPS`);
        console.log(`Lowest frame rate: ${Math.min(...this.metrics.frameRates).toFixed(2)} FPS`);

        // Memory usage
        const memoryIncrease = this.metrics.memoryUsage.length
            ? this.metrics.memoryUsage[this.metrics.memoryUsage.length - 1] - this.metrics.startMemory
            : 0;

        console.log(`Memory usage increase: ${(memoryIncrease / (1024 * 1024)).toFixed(2)} MB`);
        console.log(`Peak memory usage: ${(this.metrics.peakMemory / (1024 * 1024)).toFixed(2)} MB`);

        // DOM operations
        console.log(`Total DOM operations: ${this.metrics.domOperations}`);

        // Errors
        console.log(`Errors encountered: ${this.metrics.errors.length}`);
        if (this.metrics.errors.length > 0) {
            console.log('Error details:');
            this.metrics.errors.forEach((error, index) => {
                console.error(`${index + 1}. ${error.message} (${error.component})`);
            });
        }

        // Performance assessment
        let performanceRating = 'Excellent';
        if (avgFrameRate < 30) performanceRating = 'Poor';
        else if (avgFrameRate < 45) performanceRating = 'Fair';
        else if (avgFrameRate < 55) performanceRating = 'Good';

        console.log(`Overall performance rating: ${performanceRating}`);
    }

    // Start monitoring frame rate
    startFpsMonitoring() {
        this.fpsMonitoring = true;
        this.metrics.lastFrameTime = performance.now();
        this.metrics.frames = 0;

        const measureFps = () => {
            this.metrics.frames++;

            const now = performance.now();
            const elapsed = now - this.metrics.lastFrameTime;

            // Calculate FPS every second
            if (elapsed >= 1000) {
                const fps = (this.metrics.frames * 1000) / elapsed;
                this.metrics.frameRates.push(fps);

                // Reset counters
                this.metrics.frames = 0;
                this.metrics.lastFrameTime = now;
            }

            // Continue monitoring
            if (this.fpsMonitoring) {
                requestAnimationFrame(measureFps);
            }
        };

        requestAnimationFrame(measureFps);
    }

    // Stop monitoring frame rate
    stopFpsMonitoring() {
        this.fpsMonitoring = false;
    }

    // Start monitoring memory usage
    startMemoryMonitoring() {
        if (!window.performance || !window.performance.memory) {
            console.log('Memory API not available in this browser');
            return;
        }

        this.metrics.startMemory = window.performance.memory.usedJSHeapSize;
        this.metrics.peakMemory = this.metrics.startMemory;

        this.memoryInterval = setInterval(() => {
            const currentMemory = window.performance.memory.usedJSHeapSize;
            this.metrics.memoryUsage.push(currentMemory);

            if (currentMemory > this.metrics.peakMemory) {
                this.metrics.peakMemory = currentMemory;
            }
        }, 1000);
    }

    // Stop monitoring memory usage
    stopMemoryMonitoring() {
        clearInterval(this.memoryInterval);
    }

    // Run stress test for 3D Bitcoin visualization
    runBitcoin3DStressTest({ duration = 30000, interval = null, intensity = null }) {
        return new Promise(resolve => {
            console.log('🔄 Running Bitcoin 3D visualization stress test');

            // Use configured values if not specified
            const updateInterval = interval || this.tests.bitcoin3D.updateInterval;
            const testIntensity = intensity || this.tests.bitcoin3D.intensity;

            // Define update magnitude based on intensity
            let updateMagnitude = 0.05; // Default for medium
            if (testIntensity === 'low') updateMagnitude = 0.02;
            if (testIntensity === 'high') updateMagnitude = 0.1;

            // Mark as running
            this.tests.bitcoin3D.running = true;

            // Setup interval for rapid sentiment updates
            let iterations = 0;
            let lastSentiment = 0.5;

            const updateInterval3D = setInterval(() => {
                try {
                    // Verify function exists
                    if (typeof window.updateBitcoinVisualization !== 'function') {
                        throw new Error('updateBitcoinVisualization function not found');
                    }

                    // Calculate new sentiment with some oscillation
                    const oscillation = Math.sin(iterations * 0.1) * updateMagnitude;
                    let newSentiment = lastSentiment + oscillation;

                    // Ensure sentiment stays in valid range
                    newSentiment = Math.max(0, Math.min(1, newSentiment));

                    // Update visualization
                    window.updateBitcoinVisualization(newSentiment);

                    // Remember last value
                    lastSentiment = newSentiment;
                    iterations++;

                    // Count as DOM operation
                    this.metrics.domOperations++;
                } catch (error) {
                    // Record error
                    this.metrics.errors.push({
                        component: 'Bitcoin3D',
                        message: error.message,
                        timestamp: new Date()
                    });

                    // Stop on critical errors
                    if (this.metrics.errors.length > 10) {
                        clearInterval(updateInterval3D);
                        this.tests.bitcoin3D.running = false;
                        console.error('Bitcoin 3D test stopped due to multiple errors');
                    }
                }
            }, updateInterval);

            // Stop after duration
            setTimeout(() => {
                clearInterval(updateInterval3D);
                this.tests.bitcoin3D.running = false;
                console.log(`Bitcoin 3D test completed with ${iterations} updates`);
                resolve();
            }, duration);
        });
    }

    // Run stress test for Fear & Greed Index
    runFearGreedStressTest({ duration = 30000, interval = null, intensity = null }) {
        return new Promise(resolve => {
            console.log('🔄 Running Fear & Greed Index stress test');

            // Use configured values if not specified
            const updateInterval = interval || this.tests.fearGreed.updateInterval;
            const testIntensity = intensity || this.tests.fearGreed.intensity;

            // Define update magnitude based on intensity
            let updateStep = 5; // Default for medium
            if (testIntensity === 'low') updateStep = 2;
            if (testIntensity === 'high') updateStep = 10;

            // Mark as running
            this.tests.fearGreed.running = true;

            // Setup interval for rapid fear & greed updates
            let iterations = 0;
            let currentValue = 50;
            let direction = 1;

            const updateIntervalFG = setInterval(() => {
                try {
                    // Verify function exists
                    if (typeof window.updateFearGreedValue !== 'function') {
                        throw new Error('updateFearGreedValue function not found');
                    }

                    // Update direction occasionally for oscillation
                    if (iterations % 10 === 0) {
                        direction = Math.random() > 0.5 ? 1 : -1;
                    }

                    // Calculate new value
                    currentValue += direction * updateStep;

                    // Ensure value stays in valid range
                    if (currentValue > 100) {
                        currentValue = 100;
                        direction = -1;
                    } else if (currentValue < 0) {
                        currentValue = 0;
                        direction = 1;
                    }

                    // Update visualization
                    window.updateFearGreedValue(currentValue);

                    iterations++;

                    // Count as DOM operation
                    this.metrics.domOperations++;
                } catch (error) {
                    // Record error
                    this.metrics.errors.push({
                        component: 'FearGreed',
                        message: error.message,
                        timestamp: new Date()
                    });

                    // Stop on critical errors
                    if (this.metrics.errors.length > 10) {
                        clearInterval(updateIntervalFG);
                        this.tests.fearGreed.running = false;
                        console.error('Fear & Greed test stopped due to multiple errors');
                    }
                }
            }, updateInterval);

            // Stop after duration
            setTimeout(() => {
                clearInterval(updateIntervalFG);
                this.tests.fearGreed.running = false;
                console.log(`Fear & Greed test completed with ${iterations} updates`);
                resolve();
            }, duration);
        });
    }

    // Run stress test for translation system
    runTranslationStressTest({ duration = 20000, interval = null }) {
        return new Promise(resolve => {
            console.log('🔄 Running translation system stress test');

            // Use configured values if not specified
            const updateInterval = interval || this.tests.translations.updateInterval;

            // Check if translation function exists
            if (typeof translatePage !== 'function') {
                this.metrics.errors.push({
                    component: 'Translations',
                    message: 'translatePage function not found',
                    timestamp: new Date()
                });
                console.error('Translation test aborted: translatePage function not found');
                resolve();
                return;
            }

            // Mark as running
            this.tests.translations.running = true;

            // Available languages
            const languages = Object.keys(translations || { en: {}, es: {}, fr: {}, zh: {}, om: {} });

            // Remember original language
            const originalLang = currentLang || 'en';

            // Setup interval for rapid language changes
            let iterations = 0;

            const updateIntervalTrans = setInterval(() => {
                try {
                    // Select next language
                    const langIndex = iterations % languages.length;
                    const language = languages[langIndex];

                    // Change language
                    translatePage(language);

                    iterations++;

                    // Count as DOM operation
                    this.metrics.domOperations++;
                } catch (error) {
                    // Record error
                    this.metrics.errors.push({
                        component: 'Translations',
                        message: error.message,
                        timestamp: new Date()
                    });

                    // Stop on critical errors
                    if (this.metrics.errors.length > 5) {
                        clearInterval(updateIntervalTrans);
                        this.tests.translations.running = false;
                        console.error('Translation test stopped due to multiple errors');
                    }
                }
            }, updateInterval);

            // Stop after duration
            setTimeout(() => {
                clearInterval(updateIntervalTrans);
                this.tests.translations.running = false;

                // Restore original language
                try {
                    translatePage(originalLang);
                } catch (e) {
                    console.error('Failed to restore original language', e);
                }

                console.log(`Translation test completed with ${iterations} language changes`);
                resolve();
            }, duration);
        });
    }

    // Run stress test for DOM updates
    runDomStressTest({ duration = 20000, interval = null }) {
        return new Promise(resolve => {
            console.log('🔄 Running DOM update stress test');

            // Use configured values if not specified
            const updateInterval = interval || this.tests.domUpdates.updateInterval;

            // Mark as running
            this.tests.domUpdates.running = true;

            // Setup interval for rapid DOM updates
            let iterations = 0;

            // Create test container
            const testContainer = document.createElement('div');
            testContainer.id = 'stress-test-container';
            testContainer.style.position = 'fixed';
            testContainer.style.bottom = '10px';
            testContainer.style.right = '10px';
            testContainer.style.background = 'rgba(0,0,0,0.5)';
            testContainer.style.color = 'white';
            testContainer.style.padding = '5px';
            testContainer.style.fontSize = '10px';
            testContainer.style.zIndex = '9999';
            testContainer.style.borderRadius = '3px';
            testContainer.style.maxWidth = '200px';
            testContainer.style.maxHeight = '100px';
            testContainer.style.overflow = 'hidden';
            document.body.appendChild(testContainer);

            const updateIntervalDOM = setInterval(() => {
                try {
                    // Update test container content
                    testContainer.innerHTML = `
            <div>Stress Test Running</div>
            <div>Iteration: ${iterations}</div>
            <div>Timestamp: ${new Date().toISOString()}</div>
            <div>Memory: ${window.performance && window.performance.memory ?
                            (window.performance.memory.usedJSHeapSize / (1024 * 1024)).toFixed(2) + ' MB' :
                            'N/A'
                        }</div>
          `;

                    // Also update actual dashboard elements
                    this.updateRandomDashboardElement();

                    iterations++;

                    // Count as DOM operation (we're doing multiple operations)
                    this.metrics.domOperations += 2;
                } catch (error) {
                    // Record error
                    this.metrics.errors.push({
                        component: 'DOMUpdates',
                        message: error.message,
                        timestamp: new Date()
                    });

                    // Stop on critical errors
                    if (this.metrics.errors.length > 10) {
                        clearInterval(updateIntervalDOM);
                        this.tests.domUpdates.running = false;
                        console.error('DOM update test stopped due to multiple errors');
                    }
                }
            }, updateInterval);

            // Stop after duration
            setTimeout(() => {
                clearInterval(updateIntervalDOM);
                this.tests.domUpdates.running = false;

                // Remove test container
                if (testContainer && testContainer.parentNode) {
                    testContainer.parentNode.removeChild(testContainer);
                }

                console.log(`DOM update test completed with ${iterations} updates`);
                resolve();
            }, duration);
        });
    }

    // Helper to update a random dashboard element
    updateRandomDashboardElement() {
        const elements = [
            {
                id: 'last-updated',
                update: () => document.getElementById('last-updated').textContent = 'Last updated: ' + new Date().toLocaleTimeString()
            },
            {
                id: 'recommendationTime',
                update: () => document.getElementById('recommendationTime').textContent = 'Last updated: ' + new Date().toLocaleTimeString()
            },
            {
                id: 'news-count',
                update: () => document.getElementById('news-count').textContent = Math.floor(Math.random() * 50)
            },
            {
                id: 'confidence',
                update: () => document.getElementById('confidence').textContent = (Math.random()).toFixed(2)
            },
            {
                id: 'sentimentValue',
                update: () => document.getElementById('sentimentValue').textContent = (Math.random()).toFixed(1)
            }
        ];

        // Select random element
        const randomIndex = Math.floor(Math.random() * elements.length);
        const element = elements[randomIndex];

        // Update if element exists
        try {
            if (document.getElementById(element.id)) {
                element.update();
            }
        } catch (e) {
            console.error(`Failed to update element ${element.id}:`, e);
        }
    }
}

// Create global instance
window.componentStressTests = new ComponentStressTests();

// Expose test functions to window for easier console testing
window.runAllStressTests = (duration) => window.componentStressTests.runAll(duration);
window.runBitcoin3DTest = (options = {}) => window.componentStressTests.runBitcoin3DStressTest(options);
window.runFearGreedTest = (options = {}) => window.componentStressTests.runFearGreedStressTest(options);

console.log('✅ Component stress tests loaded. Use window.runAllStressTests() to start testing.'); 