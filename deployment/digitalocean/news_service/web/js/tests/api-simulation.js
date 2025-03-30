// OMEGA BTC AI API Simulation Service
console.log('Loading API simulation for testing...');

// API simulation for testing purposes
class ApiSimulation {
    constructor() {
        // Set up configuration
        this.config = {
            enabled: false,
            interceptXHR: false,
            interceptFetch: false,
            logRequests: true,
            simulateDelay: true,
            minDelay: 100,
            maxDelay: 500
        };

        // API endpoints and their mock responses
        this.endpoints = {
            '/api/status': () => ({
                status: 'connected',
                version: '1.0.0',
                server_time: new Date().toISOString(),
                uptime: 3600
            }),

            '/api/news/latest': () => this.generateMockNews(),

            '/api/fear-greed': () => ({
                value: Math.floor(Math.random() * 100),
                classification: this.getFearGreedClassification(Math.floor(Math.random() * 100)),
                timestamp: new Date().toISOString()
            })
        };

        // Initialize if auto-start is enabled
        if (this.config.enabled) {
            this.initialize();
        }
    }

    // Set up the simulation
    initialize() {
        console.log('🔄 Initializing API simulation');

        // Intercept XMLHttpRequest
        if (this.config.interceptXHR) {
            this.interceptXHR();
        }

        // Intercept fetch
        if (this.config.interceptFetch) {
            this.interceptFetch();
        }

        console.log('✅ API simulation ready');
    }

    // Start simulation
    start() {
        this.config.enabled = true;
        this.initialize();
    }

    // Stop simulation
    stop() {
        this.config.enabled = false;
        console.log('⏹️ API simulation stopped');
    }

    // Generate random delay
    getRandomDelay() {
        return this.config.simulateDelay
            ? Math.floor(Math.random() * (this.config.maxDelay - this.config.minDelay)) + this.config.minDelay
            : 0;
    }

    // Intercept XMLHttpRequest
    interceptXHR() {
        const originalXHR = window.XMLHttpRequest;
        const self = this;

        window.XMLHttpRequest = function () {
            const xhr = new originalXHR();
            const originalOpen = xhr.open;
            const originalSend = xhr.send;

            xhr.open = function (method, url, ...args) {
                this._url = url;
                this._method = method;
                return originalOpen.call(this, method, url, ...args);
            };

            xhr.send = function (...args) {
                if (self.config.enabled && self.endpoints[this._url]) {
                    if (self.config.logRequests) {
                        console.log(`🔄 Intercepted XHR ${this._method} request to ${this._url}`);
                    }

                    // Prevent actual request
                    this.onreadystatechange = () => { };

                    // Simulate response
                    setTimeout(() => {
                        const mockResponse = self.endpoints[this._url]();
                        const responseText = JSON.stringify(mockResponse);

                        Object.defineProperty(this, 'responseText', { value: responseText });
                        Object.defineProperty(this, 'response', { value: responseText });
                        Object.defineProperty(this, 'status', { value: 200 });
                        Object.defineProperty(this, 'readyState', { value: 4 });

                        this.dispatchEvent(new Event('readystatechange'));
                        this.dispatchEvent(new Event('load'));
                    }, self.getRandomDelay());

                    return;
                }

                return originalSend.apply(this, args);
            };

            return xhr;
        };
    }

    // Intercept fetch
    interceptFetch() {
        const originalFetch = window.fetch;
        const self = this;

        window.fetch = function (url, options = {}) {
            // Extract URL from Request object if needed
            const urlString = typeof url === 'string' ? url : url.url;

            // Check if we should handle this request
            if (self.config.enabled) {
                for (const endpoint in self.endpoints) {
                    if (urlString === endpoint || urlString.startsWith(endpoint)) {
                        if (self.config.logRequests) {
                            console.log(`🔄 Intercepted fetch request to ${urlString}`);
                        }

                        // Get mock response
                        const mockResponse = self.endpoints[endpoint]();

                        // Simulate network delay
                        return new Promise(resolve => {
                            setTimeout(() => {
                                resolve(new Response(JSON.stringify(mockResponse), {
                                    status: 200,
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                }));
                            }, self.getRandomDelay());
                        });
                    }
                }
            }

            // Pass through to original fetch for non-intercepted URLs
            return originalFetch(url, options);
        };
    }

    // Generate mock news data
    generateMockNews(count = 10) {
        const sources = ['CoinDesk', 'Cointelegraph', 'Bitcoin Magazine', 'Decrypt', 'The Block'];
        const sentimentRange = [
            { range: [0.0, 0.3], words: ['bearish', 'crash', 'decline', 'loss', 'sell-off', 'danger', 'risk'] },
            { range: [0.3, 0.7], words: ['stable', 'steady', 'consolidation', 'neutral', 'sideways', 'awaiting'] },
            { range: [0.7, 1.0], words: ['bullish', 'rally', 'surge', 'gains', 'adoption', 'breakthrough', 'positive'] }
        ];

        const getRandomSentiment = () => {
            // Weight distribution to make neutrals more common
            const r = Math.random();
            if (r < 0.25) return Math.random() * 0.3; // 25% bearish
            if (r < 0.75) return 0.3 + Math.random() * 0.4; // 50% neutral
            return 0.7 + Math.random() * 0.3; // 25% bullish
        };

        const getTitle = (sentiment) => {
            let range;
            for (const r of sentimentRange) {
                if (sentiment >= r.range[0] && sentiment <= r.range[1]) {
                    range = r;
                    break;
                }
            }

            const word = range.words[Math.floor(Math.random() * range.words.length)];

            if (sentiment < 0.3) {
                return `Bitcoin Experiences ${word.charAt(0).toUpperCase() + word.slice(1)} Trend as Markets React to Latest News`;
            } else if (sentiment < 0.7) {
                return `Bitcoin Enters ${word.charAt(0).toUpperCase() + word.slice(1)} Phase as Traders Await Directional Cues`;
            } else {
                return `Bitcoin Shows ${word.charAt(0).toUpperCase() + word.slice(1)} Signals Amid Increasing Institutional Interest`;
            }
        };

        // Generate news items
        const news = [];
        for (let i = 0; i < count; i++) {
            const sentiment_score = getRandomSentiment();
            const published_at = new Date(Date.now() - Math.random() * 86400000).toISOString(); // Last 24 hours

            news.push({
                id: `news-${Date.now()}-${i}`,
                title: getTitle(sentiment_score),
                url: `https://example.com/news/${Date.now()}-${i}`,
                source: sources[Math.floor(Math.random() * sources.length)],
                published_at: published_at,
                sentiment_score: sentiment_score,
                summary: `This is a simulated news article with sentiment score of ${sentiment_score.toFixed(2)}. Used for testing purposes.`
            });
        }

        return news;
    }

    // Get Fear & Greed classification
    getFearGreedClassification(value) {
        if (value < 20) return 'Extreme Fear';
        if (value < 40) return 'Fear';
        if (value < 60) return 'Neutral';
        if (value < 80) return 'Greed';
        return 'Extreme Greed';
    }
}

// Create global instance
window.apiSimulation = new ApiSimulation();

// Expose API functions to window for easier console testing
window.startApiSimulation = () => window.apiSimulation.start();
window.stopApiSimulation = () => window.apiSimulation.stop();

// Function to run automated load test
window.runLoadTest = async function (iterations = 100, parallelRequests = 5) {
    console.log(`🔄 Running load test with ${iterations} iterations, ${parallelRequests} parallel requests`);

    const startTime = performance.now();
    const results = {
        totalRequests: iterations * 3, // status, news, fear-greed
        successfulRequests: 0,
        failedRequests: 0,
        averageResponseTime: 0
    };

    const endpoints = ['/api/status', '/api/news/latest', '/api/fear-greed'];
    const responseTimes = [];

    const makeRequest = async (endpoint) => {
        const requestStart = performance.now();
        try {
            const response = await fetch(endpoint);
            const data = await response.json();
            const requestTime = performance.now() - requestStart;

            responseTimes.push(requestTime);
            results.successfulRequests++;

            return {
                success: true,
                time: requestTime,
                data
            };
        } catch (error) {
            results.failedRequests++;
            return {
                success: false,
                error: error.message
            };
        }
    };

    // Run batches of parallel requests
    for (let i = 0; i < iterations; i++) {
        // Create a batch of promises for parallel execution
        const batch = [];

        // Add requests for all endpoints
        for (const endpoint of endpoints) {
            batch.push(makeRequest(endpoint));
        }

        // Wait for batch to complete
        await Promise.all(batch);

        // Log progress for long-running tests
        if (iterations > 10 && i % 10 === 0) {
            console.log(`Load test progress: ${Math.round((i / iterations) * 100)}%`);
        }
    }

    const totalTime = performance.now() - startTime;
    results.averageResponseTime = responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length;

    console.log('📊 Load test results:');
    console.log(`Total time: ${(totalTime / 1000).toFixed(2)} seconds`);
    console.log(`Requests: ${results.successfulRequests} successful, ${results.failedRequests} failed`);
    console.log(`Average response time: ${results.averageResponseTime.toFixed(2)} ms`);
    console.log(`Requests per second: ${(results.successfulRequests / (totalTime / 1000)).toFixed(2)}`);

    return results;
}; 