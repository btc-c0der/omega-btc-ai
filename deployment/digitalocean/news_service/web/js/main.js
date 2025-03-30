// Main application functionality
document.addEventListener('DOMContentLoaded', function () {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const newsContainer = document.getElementById('news-container');
    const refreshButton = document.getElementById('refresh-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const lastUpdated = document.getElementById('last-updated');
    const avgSentiment = document.getElementById('avg-sentiment');
    const newsCount = document.getElementById('news-count');
    const confidence = document.getElementById('confidence');
    const sentimentProgress = document.getElementById('sentiment-progress');
    const recommendationIcon = document.getElementById('recommendation-icon');
    const recommendationContainer = document.getElementById('recommendation-container');
    const sentimentDial = document.getElementById('sentimentDial');
    const sentimentValue = document.getElementById('sentimentValue');
    const tradingRecommendation = document.getElementById('tradingRecommendation');
    const recommendationTime = document.getElementById('recommendationTime');
    const sentimentBarFill = document.getElementById('sentimentBarFill');

    // Check service status
    checkServiceStatus();

    // Load initial data
    loadNewsData();

    // Set up refresh handler
    refreshButton.addEventListener('click', function () {
        loadNewsData();
        checkServiceStatus();
    });

    // Initialize sentiment dial if Chart.js is available
    let sentimentChart = null;
    if (window.Chart && sentimentDial) {
        initSentimentDial();
    }

    // Function to check service status
    function checkServiceStatus() {
        fetch('/api/status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Service unavailable');
                }
                statusIndicator.className = 'bg-success';
                statusText.textContent = 'Connected';
                return response.json();
            })
            .then(data => {
                console.log('Status:', data);
            })
            .catch(error => {
                console.error('Error checking status:', error);
                statusIndicator.className = 'bg-danger';
                statusText.textContent = 'Disconnected';
            });
    }

    // Function to load news data
    async function loadNewsData() {
        try {
            // Show loading spinner
            loadingSpinner.style.display = 'inline-block';

            console.log('Fetching news data...');

            // First try the main endpoint
            let response = await fetch('/api/news/latest');

            // If main endpoint fails, try alternative endpoints
            if (!response.ok) {
                console.warn(`Main news endpoint failed with status ${response.status}, trying alternative...`);
                response = await fetch('/api/latest-news');

                // If that fails too, try direct URL
                if (!response.ok) {
                    console.warn(`Alternative news endpoint failed with status ${response.status}, trying direct URL...`);
                    response = await fetch('http://localhost:10080/api/news/latest');

                    // If everything fails, use mock data
                    if (!response.ok) {
                        console.error('All news API endpoints failed, using mock data');
                        return useMockNewsData();
                    }
                }
            }

            // Process the news data
            const newsData = await response.json();
            console.log(`Loaded ${newsData.length} news items`);

            if (!Array.isArray(newsData) || newsData.length === 0) {
                console.warn('News API returned empty or invalid data, using mock data');
                return useMockNewsData();
            }

            // Update last updated timestamp
            lastUpdated.textContent = 'Last updated: ' + new Date().toLocaleTimeString();

            // Update news count
            newsCount.textContent = newsData.length;

            // Calculate average sentiment
            const totalSentiment = newsData.reduce((sum, item) => sum + item.sentiment_score, 0);
            const avgSentimentValue = totalSentiment / newsData.length;
            avgSentiment.textContent = avgSentimentValue.toFixed(2);

            // Update sentiment progress bar
            sentimentProgress.style.width = (avgSentimentValue * 100) + '%';

            // Set color based on sentiment
            if (avgSentimentValue >= 0.7) {
                sentimentProgress.className = 'progress-bar bg-success';
            } else if (avgSentimentValue <= 0.3) {
                sentimentProgress.className = 'progress-bar bg-danger';
            } else {
                sentimentProgress.className = 'progress-bar bg-warning';
            }

            // Update sentiment dial if available
            if (sentimentChart) {
                updateSentimentDial(avgSentimentValue);
            }

            // Update sentiment bar fill
            if (sentimentBarFill) {
                sentimentBarFill.style.width = (avgSentimentValue * 100) + '%';
            }

            // Update sentiment value display
            if (sentimentValue) {
                sentimentValue.textContent = avgSentimentValue.toFixed(1);
            }

            // Update 3D visualization with new sentiment
            if (window.updateBitcoinVisualization) {
                window.updateBitcoinVisualization(avgSentimentValue);
            }

            // Manually update Fear & Greed with sentiment data rather than API
            // to avoid the 404 errors temporarily
            if (window.updateFearGreedValue) {
                // Map sentiment (0-1) to Fear & Greed scale (0-100)
                const fearGreedValue = Math.round(avgSentimentValue * 100);
                console.log('Updating Fear & Greed with mapped sentiment value:', fearGreedValue);
                window.updateFearGreedValue(fearGreedValue);
            }

            // Generate recommendation
            generateRecommendation(avgSentimentValue);

            // Display news items
            displayNewsItems(newsData);

            return newsData;
        } catch (error) {
            console.error('Error loading news:', error);
            newsContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-exclamation-triangle text-warning" style="font-size: 3rem;"></i>
                    <p class="mt-3">Failed to load news. Please try again later.</p>
                </div>
            `;
        } finally {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
        }
    }

    // Function to use mock news data as fallback
    function useMockNewsData() {
        console.log('Using mock news data...');
        const mockNews = generateMockNewsData();
        displayNewsItems(mockNews);
        updateSentiment(mockNews);
        return mockNews;
    }

    // Function to generate mock news data
    function generateMockNewsData(count = 8) {
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
                id: `mock-news-${Date.now()}-${i}`,
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

    // Function to initialize sentiment dial
    function initSentimentDial() {
        const ctx = sentimentDial.getContext('2d');
        sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0.5, 0.5],
                    backgroundColor: [
                        'rgba(63, 185, 80, 0.7)',
                        'rgba(240, 246, 252, 0.1)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '75%',
                rotation: 270,
                circumference: 180,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        });
    }

    // Function to update sentiment dial
    function updateSentimentDial(sentiment) {
        let color = 'rgba(210, 153, 34, 0.7)'; // Warning/neutral

        if (sentiment >= 0.7) {
            color = 'rgba(63, 185, 80, 0.7)'; // Success/bullish
        } else if (sentiment <= 0.3) {
            color = 'rgba(248, 81, 73, 0.7)'; // Danger/bearish
        }

        sentimentChart.data.datasets[0].data = [sentiment, 1 - sentiment];
        sentimentChart.data.datasets[0].backgroundColor[0] = color;
        sentimentChart.update();
    }

    // Function to display news items
    function displayNewsItems(newsItems) {
        // Clear existing news
        newsContainer.innerHTML = '';

        // Add news items
        newsItems.forEach(item => {
            // Check if translations is defined
            const hasTranslations = typeof translations !== 'undefined' && typeof currentLang !== 'undefined';

            // Calculate sentiment class and text
            let sentimentClass, sentimentText;
            if (item.sentiment_score >= 0.7) {
                sentimentClass = 'bg-success';
                sentimentText = hasTranslations && translations[currentLang]?.["Bullish"] || 'Bullish';
            } else if (item.sentiment_score <= 0.3) {
                sentimentClass = 'bg-danger';
                sentimentText = hasTranslations && translations[currentLang]?.["Bearish"] || 'Bearish';
            } else {
                sentimentClass = 'bg-warning';
                sentimentText = 'Neutral';
            }

            // Format date
            const publishedDate = typeof item.published_at === 'number'
                ? new Date(item.published_at * 1000).toLocaleString()
                : new Date(item.published_at).toLocaleString();

            // Create news card
            const newsCard = document.createElement('div');
            newsCard.className = 'col-md-6 col-lg-4';
            newsCard.innerHTML = `
                <div class="card h-100 position-relative">
                    <div class="sentiment-badge ${sentimentClass}">${(item.sentiment_score * 10).toFixed(1)}</div>
                    <div class="card-body">
                        <h5 class="card-title mb-3">${item.title}</h5>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="source-tag">${item.source}</span>
                            <span class="news-date">${publishedDate}</span>
                        </div>
                        <div class="mt-3">
                            <a href="${item.url}" target="_blank" class="btn btn-sm btn-outline-light">${hasTranslations && translations[currentLang]?.["Read More"] || 'Read More'}</a>
                            <span class="badge ${sentimentClass} ms-2">${sentimentText}</span>
                        </div>
                    </div>
                </div>
            `;

            newsContainer.appendChild(newsCard);
        });
    }

    // Function to generate recommendation
    function generateRecommendation(sentiment) {
        let action, confidenceValue, iconClass, borderColor, description;

        if (sentiment >= 0.7) {
            action = "BUY";
            confidenceValue = (sentiment * 1.2).toFixed(2);
            iconClass = "bi-arrow-up-circle-fill text-success";
            borderColor = "border-success";
            description = "Strong positive sentiment detected in recent news. According to OMEGA analysis, consider accumulating Bitcoin with proper risk management.";
        } else if (sentiment <= 0.3) {
            action = "SELL";
            confidenceValue = ((1 - sentiment) * 1.2).toFixed(2);
            iconClass = "bi-arrow-down-circle-fill text-danger";
            borderColor = "border-danger";
            description = "Negative sentiment detected in recent news. OMEGA analysis suggests reducing exposure to Bitcoin temporarily while maintaining long-term perspective.";
        } else {
            action = "HOLD";
            confidenceValue = (1 - Math.abs(sentiment - 0.5) * 2).toFixed(2);
            iconClass = "bi-dash-circle-fill text-warning";
            borderColor = "border-warning";
            description = "Neutral market sentiment detected. OMEGA wisdom suggests maintaining current position and using this time for education and research.";
        }

        // Update confidence
        confidence.textContent = confidenceValue;

        // Update trading recommendation
        if (tradingRecommendation) {
            tradingRecommendation.textContent = `OMEGA Guidance: ${action}`;
        }

        // Update recommendation time
        if (recommendationTime) {
            recommendationTime.textContent = 'Last updated: ' + new Date().toLocaleTimeString();
        }

        // Update recommendation icon
        recommendationIcon.innerHTML = `<i class="bi ${iconClass}"></i>`;
        recommendationContainer.className = `recommendation-card mb-4 ${borderColor}`;
        recommendationContainer.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="recommendation-icon">
                    <i class="bi ${iconClass}"></i>
                </div>
                <div>
                    <h3 class="mb-1">OMEGA Guidance: ${action}</h3>
                    <p class="mb-0 text-light">${description}</p>
                    <p class="mt-2 mb-0">Confidence: ${confidenceValue}</p>
                    <small class="text-light mt-2 d-block">Remember: All financial decisions should be made with proper research and in alignment with your personal financial goals.</small>
                </div>
            </div>
        `;
    }
}); 