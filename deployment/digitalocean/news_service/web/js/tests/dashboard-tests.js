// OMEGA BTC AI Dashboard Test Suite
console.log('Running OMEGA BTC AI Dashboard tests...');

// Test suite for dashboard functionality
const dashboardTests = {
    // Store test results
    results: {
        passed: 0,
        failed: 0,
        errors: []
    },

    // Run all tests
    runAll: function () {
        console.log('🔍 Starting all dashboard tests');

        // Run individual test cases
        this.testApiEndpoints();
        this.testSentimentCalculation();
        this.testVisualizationRendering();
        this.testFearGreedIndex();
        this.testFutureVisionsRendering();
        this.testTranslations();

        // Report results
        console.log(`✅ Passed: ${this.results.passed} | ❌ Failed: ${this.results.failed}`);
        if (this.results.errors.length > 0) {
            console.log('Errors:');
            this.results.errors.forEach(error => console.error(`- ${error}`));
        }

        return this.results.failed === 0;
    },

    // Helper to track test outcomes
    assert: function (condition, message) {
        if (condition) {
            this.results.passed++;
            console.log(`✅ PASS: ${message}`);
            return true;
        } else {
            this.results.failed++;
            this.results.errors.push(message);
            console.error(`❌ FAIL: ${message}`);
            return false;
        }
    },

    // Test API endpoints
    testApiEndpoints: function () {
        console.log('\n🔄 Testing API endpoints...');

        // Test /api/status endpoint
        fetch('/api/status')
            .then(response => {
                this.assert(response.ok, 'Status API should return 200 OK');
                return response.json();
            })
            .then(data => {
                this.assert(data && typeof data === 'object', 'Status API should return JSON object');
            })
            .catch(error => {
                this.assert(false, `Status API error: ${error.message}`);
            });

        // Test /api/news/latest endpoint
        fetch('/api/news/latest')
            .then(response => {
                this.assert(response.ok, 'News API should return 200 OK');
                return response.json();
            })
            .then(data => {
                this.assert(Array.isArray(data), 'News API should return an array');

                if (data.length > 0) {
                    const firstItem = data[0];
                    this.assert(
                        firstItem.title &&
                        typeof firstItem.sentiment_score === 'number' &&
                        firstItem.source &&
                        firstItem.url,
                        'News items should have required properties'
                    );
                }
            })
            .catch(error => {
                this.assert(false, `News API error: ${error.message}`);
            });

        // Test Fear & Greed API
        fetch('/api/fear-greed')
            .then(response => {
                // Just check if the endpoint exists, not required to work
                if (response.ok) {
                    console.log('💡 Fear & Greed API is available');
                } else {
                    console.log('💡 Fear & Greed API not found, using simulation');
                }
            })
            .catch(() => {
                console.log('💡 Fear & Greed API not available, using simulation');
            });
    },

    // Test sentiment calculation
    testSentimentCalculation: function () {
        console.log('\n🔄 Testing sentiment calculation logic...');

        // Mock news data
        const mockNewsData = [
            { sentiment_score: 0.8 },
            { sentiment_score: 0.2 },
            { sentiment_score: 0.5 }
        ];

        // Calculate average sentiment
        const totalSentiment = mockNewsData.reduce((sum, item) => sum + item.sentiment_score, 0);
        const avgSentiment = totalSentiment / mockNewsData.length;

        // Verify calculations
        this.assert(Math.abs(avgSentiment - 0.5) < 0.001, 'Average sentiment calculation should be correct');

        // Test recommendation generation logic
        let action, borderColor;

        if (avgSentiment >= 0.7) {
            action = "BUY";
            borderColor = "border-success";
        } else if (avgSentiment <= 0.3) {
            action = "SELL";
            borderColor = "border-danger";
        } else {
            action = "HOLD";
            borderColor = "border-warning";
        }

        this.assert(action === "HOLD", 'Sentiment 0.5 should generate HOLD recommendation');
        this.assert(borderColor === "border-warning", 'Sentiment 0.5 should use warning border');

        // Test edge cases
        this.assert(this.getActionForSentiment(0.8) === "BUY", 'Sentiment 0.8 should generate BUY recommendation');
        this.assert(this.getActionForSentiment(0.2) === "SELL", 'Sentiment 0.2 should generate SELL recommendation');
        this.assert(this.getActionForSentiment(0.5) === "HOLD", 'Sentiment 0.5 should generate HOLD recommendation');
    },

    // Helper for testing sentiment-to-action conversion
    getActionForSentiment: function (sentiment) {
        if (sentiment >= 0.7) return "BUY";
        if (sentiment <= 0.3) return "SELL";
        return "HOLD";
    },

    // Test visualization rendering
    testVisualizationRendering: function () {
        console.log('\n🔄 Testing 3D visualization components...');

        // Check if container exists
        const bitcoinContainer = document.getElementById('bitcoin-3d-container');
        this.assert(bitcoinContainer !== null, 'Bitcoin 3D container should exist in the DOM');

        // Check if updateBitcoinVisualization function exists
        this.assert(typeof window.updateBitcoinVisualization === 'function',
            'updateBitcoinVisualization function should be available globally');

        // Test if canvas is created in container
        if (bitcoinContainer) {
            const canvas = bitcoinContainer.querySelector('canvas');
            this.assert(canvas !== null, '3D visualization should create a canvas element');
        }

        // Check for WebGL support
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            this.assert(gl !== null, 'WebGL should be supported for 3D visualizations');
        } catch (e) {
            this.assert(false, 'WebGL test error: ' + e.message);
        }
    },

    // Test Fear & Greed Index
    testFearGreedIndex: function () {
        console.log('\n🔄 Testing Fear & Greed Index component...');

        // Check if container exists
        const fearGreedContainer = document.getElementById('fear-greed-3d');
        this.assert(fearGreedContainer !== null, 'Fear & Greed container should exist in the DOM');

        // Check if updateFearGreedValue function exists
        this.assert(typeof window.updateFearGreedValue === 'function',
            'updateFearGreedValue function should be available globally');

        // Test function with various inputs
        if (typeof window.updateFearGreedValue === 'function') {
            try {
                // Test with minimum value
                window.updateFearGreedValue(0);
                this.assert(true, 'updateFearGreedValue should accept 0');

                // Test with maximum value
                window.updateFearGreedValue(100);
                this.assert(true, 'updateFearGreedValue should accept 100');

                // Test with middle value
                window.updateFearGreedValue(50);
                this.assert(true, 'updateFearGreedValue should accept 50');
            } catch (e) {
                this.assert(false, 'updateFearGreedValue test error: ' + e.message);
            }
        }

        // Verify DOM updates with value changes
        const valueDisplay = document.querySelector('.fear-greed-value');
        if (valueDisplay) {
            window.updateFearGreedValue(75);
            this.assert(valueDisplay.textContent === '75', 'Fear & Greed value should update in the DOM');
        }
    },

    // Test Future Visions rendering
    testFutureVisionsRendering: function () {
        console.log('\n🔄 Testing Future Visions component...');

        // Check if container exists
        const futureVisionsContainer = document.getElementById('future-visions-container');
        this.assert(futureVisionsContainer !== null, 'Future Visions container should exist in the DOM');

        // Check if visions are rendered
        if (futureVisionsContainer) {
            // Wait for rendering to complete
            setTimeout(() => {
                const visionCards = futureVisionsContainer.querySelectorAll('.card');
                this.assert(visionCards.length >= 2, 'At least two vision cards should be rendered');

                // Check for specific vision IDs
                const vision2030 = document.getElementById('vision-2030');
                const visionQuantum = document.getElementById('vision-quantum');

                this.assert(vision2030 !== null, 'Bitcoin 2030 vision card should exist');
                this.assert(visionQuantum !== null, 'Quantum Bitcoin vision card should exist');

                // Check for images
                if (vision2030) {
                    const image = vision2030.querySelector('img');
                    this.assert(image !== null, 'Vision card should contain an image');

                    if (image) {
                        this.assert(image.getAttribute('src') === 'images/bitcoin_2030.png',
                            'Vision card should reference correct image');
                    }
                }
            }, 500);
        }
    },

    // Test translations
    testTranslations: function () {
        console.log('\n🔄 Testing internationalization...');

        // Check if translations object exists
        this.assert(typeof translations === 'object', 'Translations object should exist');

        if (typeof translations === 'object') {
            // Check if basic languages are available
            this.assert(translations.en !== undefined, 'English translations should exist');
            this.assert(translations.es !== undefined, 'Spanish translations should exist');
            this.assert(translations.fr !== undefined, 'French translations should exist');
            this.assert(translations.zh !== undefined, 'Chinese translations should exist');

            // Check if translatePage function exists
            this.assert(typeof translatePage === 'function', 'translatePage function should exist');

            // Test translation functionality (if function exists)
            if (typeof translatePage === 'function') {
                // Save current language
                const originalLang = currentLang;

                // Try Spanish translation
                translatePage('es');
                const spanishTitle = document.querySelector('[data-i18n="OMEGA BTC AI - Divine Blockchain Intelligence"]');

                if (spanishTitle) {
                    this.assert(
                        spanishTitle.innerHTML === translations.es["OMEGA BTC AI - Divine Blockchain Intelligence"],
                        'Spanish translation should be applied correctly'
                    );
                }

                // Restore original language
                translatePage(originalLang);
            }
        }
    }
};

// Run tests when page is fully loaded
window.addEventListener('load', function () {
    // Allow time for all components to initialize
    setTimeout(() => {
        dashboardTests.runAll();
    }, 2000);
});

// Add a simple UI control for tests
document.addEventListener('DOMContentLoaded', function () {
    // Create a simple test control button
    const testButton = document.createElement('button');
    testButton.id = 'run-tests-button';
    testButton.textContent = 'Run Tests';
    testButton.style.position = 'fixed';
    testButton.style.top = '10px';
    testButton.style.right = '10px';
    testButton.style.zIndex = '10000';
    testButton.style.padding = '5px 10px';
    testButton.style.backgroundColor = '#007bff';
    testButton.style.color = 'white';
    testButton.style.border = 'none';
    testButton.style.borderRadius = '3px';
    testButton.style.cursor = 'pointer';

    // Add click handler
    testButton.addEventListener('click', function () {
        runDashboardTests();
    });

    // Add to document
    document.body.appendChild(testButton);
});

// Make the dashboardTests runAll function accessible globally
function runDashboardTests() {
    console.log('Running dashboard tests manually...');
    dashboardTests.runAll();
}

// Expose the function to the window object
window.runDashboardTests = runDashboardTests; 