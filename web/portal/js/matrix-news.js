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

// Matrix Neo News Portal - Enhanced with UIverse.io components

// Matrix Digital Rain Effect
class MatrixRain {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.resizeCanvas();
        this.characters = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        this.fontSize = 14;
        this.columns = [];
        this.drops = [];

        this.initialize();
        this.loop();

        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.initialize();
    }

    initialize() {
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        this.drops = [];

        for (let x = 0; x < this.columns; x++) {
            // Start each drop at a random position
            this.drops[x] = Math.floor(Math.random() * -100);
        }
    }

    draw() {
        // Set semi-transparent black background for the trail effect
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.fillStyle = '#00FF00'; // Matrix green
        this.ctx.font = `${this.fontSize}px monospace`;

        // Render each drop
        for (let i = 0; i < this.drops.length; i++) {
            // Select a random character
            const char = this.characters.charAt(Math.floor(Math.random() * this.characters.length));

            // Draw the character
            this.ctx.fillText(
                char,
                i * this.fontSize,
                this.drops[i] * this.fontSize
            );

            // Check for behind elements to reduce opacity
            if (this.isBehindText(i * this.fontSize, this.drops[i] * this.fontSize)) {
                this.ctx.fillStyle = 'rgba(0, 255, 0, 0.2)'; // More transparent for text behind elements
            } else {
                this.ctx.fillStyle = '#00FF00'; // Matrix green
            }

            // Move drops down
            this.drops[i]++;

            // Reset drops back to top with some randomness
            if (this.drops[i] * this.fontSize > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
        }
    }

    isBehindText(x, y) {
        // Simplistic check if the current rain drop position is behind any important text elements
        const elements = document.querySelectorAll('.news-card, .header, .news-controls');

        for (const element of elements) {
            const rect = element.getBoundingClientRect();
            if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
                return true;
            }
        }

        return false;
    }

    loop() {
        this.draw();
        // Use a lower frame rate to save resources
        setTimeout(() => requestAnimationFrame(() => this.loop()), 40);
    }
}

// News Card Component
class NewsCardComponent {
    constructor() {
        this.newsContainer = document.getElementById('news-container');
        this.loader = document.getElementById('matrix-loader');
        this.newsData = [];
        this.filteredData = [];
        this.currentFilter = 'all';
        this.searchTerm = '';
    }

    async fetchNews() {
        try {
            this.showLoader();

            // Attempt to fetch from the API first
            try {
                const response = await fetch('/api/news');
                if (response.ok) {
                    this.newsData = await response.json();
                } else {
                    throw new Error('API request failed');
                }
            } catch (error) {
                console.log('Falling back to sample data', error);
                // Fallback to sample data
                this.newsData = this.getSampleNewsData();
            }

            this.filteredData = [...this.newsData];
            this.renderNews();
            this.hideLoader();

            // Initialize animation for progress bars
            this.animateProgressBars();
        } catch (error) {
            console.error('Error fetching news:', error);
            this.hideLoader();
        }
    }

    showLoader() {
        if (this.loader) {
            this.loader.style.display = 'block';
        }
    }

    hideLoader() {
        if (this.loader) {
            this.loader.style.display = 'none';
        }
    }

    renderNews() {
        if (!this.newsContainer) return;

        this.newsContainer.innerHTML = '';

        if (this.filteredData.length === 0) {
            this.newsContainer.innerHTML = `
        <div class="no-results">
          <h3>No news found</h3>
          <p>Try changing your filters or search term</p>
        </div>
      `;
            return;
        }

        this.filteredData.forEach(news => {
            const sentiment = this.calculateSentiment(news);
            const card = document.createElement('div');
            card.className = 'news-card';

            card.innerHTML = `
        <span class="source">${news.source}</span>
        <h3 class="glitch">${news.title}</h3>
        <p class="description">${news.description}</p>
        <div class="progress-container tooltip">
          <div class="progress-bar" data-progress="${sentiment.score}"></div>
          <span class="tooltip-text">${sentiment.label} Sentiment: ${sentiment.score}%</span>
        </div>
        <div class="category-pills">
          ${news.categories.map(cat => `<span class="category-pill">${cat}</span>`).join('')}
        </div>
        <span class="timestamp">${this.formatTimestamp(news.publishedAt)}</span>
      `;

            card.addEventListener('click', () => {
                if (news.url) {
                    window.open(news.url, '_blank');
                }
            });

            this.newsContainer.appendChild(card);
        });
    }

    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            setTimeout(() => {
                const progress = bar.getAttribute('data-progress');
                bar.style.width = `${progress}%`;
            }, 100);
        });
    }

    calculateSentiment(news) {
        // In a real implementation, this would come from the API
        // For now, we generate a random sentiment score
        const score = news.sentiment || Math.floor(Math.random() * 100);

        let label;
        if (score < 30) {
            label = 'Bearish';
        } else if (score < 50) {
            label = 'Neutral';
        } else if (score < 75) {
            label = 'Bullish';
        } else {
            label = 'Very Bullish';
        }

        return { score, label };
    }

    formatTimestamp(timestamp) {
        // Convert timestamp to relative time
        const date = new Date(timestamp);
        const now = new Date();
        const diff = Math.floor((now - date) / 1000); // Difference in seconds

        if (diff < 60) {
            return 'Just now';
        } else if (diff < 3600) {
            const minutes = Math.floor(diff / 60);
            return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        } else if (diff < 86400) {
            const hours = Math.floor(diff / 3600);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        } else {
            const days = Math.floor(diff / 86400);
            return `${days} day${days > 1 ? 's' : ''} ago`;
        }
    }

    filterByCategory(category) {
        this.currentFilter = category;
        this.applyFilters();
    }

    searchNews(term) {
        this.searchTerm = term.toLowerCase();
        this.applyFilters();
    }

    applyFilters() {
        this.filteredData = this.newsData.filter(news => {
            // Apply category filter
            const passesCategory = this.currentFilter === 'all' ||
                news.categories.includes(this.currentFilter);

            // Apply search filter
            const passesSearch = this.searchTerm === '' ||
                news.title.toLowerCase().includes(this.searchTerm) ||
                news.description.toLowerCase().includes(this.searchTerm);

            return passesCategory && passesSearch;
        });

        this.renderNews();
        this.animateProgressBars();
    }

    toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
    }

    getSampleNewsData() {
        return [
            {
                title: "Bitcoin Reaches $75,000, Sets New All-Time High",
                description: "After months of upward momentum, Bitcoin has reached a new all-time high of $75,000, surpassing previous records and validating bullish market predictions.",
                source: "CryptoNews",
                publishedAt: new Date(Date.now() - 3600000).toISOString(),
                categories: ["Bitcoin", "Markets", "Bullish"],
                url: "#",
                sentiment: 92
            },
            {
                title: "Ethereum Layer-2 Solutions See Record Transaction Volume",
                description: "Ethereum scaling solutions like Optimism and Arbitrum have recorded unprecedented transaction volumes as users seek to avoid high gas fees on the main network.",
                source: "DeFi Daily",
                publishedAt: new Date(Date.now() - 7200000).toISOString(),
                categories: ["Ethereum", "Layer-2", "DeFi"],
                url: "#",
                sentiment: 78
            },
            {
                title: "Regulatory Concerns Grow as Countries Discuss Crypto Policies",
                description: "Global regulatory bodies are ramping up discussions about cryptocurrency policies, raising concerns about potential restrictions in major markets.",
                source: "Blockchain Report",
                publishedAt: new Date(Date.now() - 86400000).toISOString(),
                categories: ["Regulation", "Policy", "Bearish"],
                url: "#",
                sentiment: 25
            },
            {
                title: "New DeFi Protocol Attracts $1 Billion in Total Value Locked",
                description: "A newly launched decentralized finance protocol has quickly accumulated over $1 billion in total value locked, highlighting continued interest in the DeFi space.",
                source: "DeFi Pulse",
                publishedAt: new Date(Date.now() - 43200000).toISOString(),
                categories: ["DeFi", "TVL", "Protocol"],
                url: "#",
                sentiment: 85
            },
            {
                title: "Crypto Mining Firms Expand Operations with Renewable Energy",
                description: "Major cryptocurrency mining companies are expanding their operations with a focus on renewable energy sources, addressing environmental concerns.",
                source: "Mining Report",
                publishedAt: new Date(Date.now() - 129600000).toISOString(),
                categories: ["Mining", "Sustainability", "Infrastructure"],
                url: "#",
                sentiment: 65
            },
            {
                title: "Central Banks Accelerate CBDC Development Efforts",
                description: "Multiple central banks have announced accelerated timelines for their Central Bank Digital Currency (CBDC) projects, indicating growing interest in government-backed digital currencies.",
                source: "Economic Times",
                publishedAt: new Date(Date.now() - 172800000).toISOString(),
                categories: ["CBDC", "Central Banks", "Regulation"],
                url: "#",
                sentiment: 50
            }
        ];
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Matrix Rain
    const canvas = document.getElementById('matrix-rain');
    if (canvas) {
        new MatrixRain(canvas);
    }

    // Initialize News Component
    const newsComponent = new NewsCardComponent();
    newsComponent.fetchNews();

    // Setup event listeners
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            newsComponent.searchNews(e.target.value);
        });
    }

    const categoryPills = document.querySelectorAll('.filter-pill');
    categoryPills.forEach(pill => {
        pill.addEventListener('click', () => {
            // Remove active class from all pills
            categoryPills.forEach(p => p.classList.remove('active'));
            // Add active class to clicked pill
            pill.classList.add('active');
            // Apply filter
            const category = pill.getAttribute('data-category');
            newsComponent.filterByCategory(category);
        });
    });

    // Toggle dark mode
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            newsComponent.toggleDarkMode();
        });
    }

    // Setup refresh button
    const refreshButton = document.getElementById('refresh-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', () => {
            newsComponent.fetchNews();
            // Add a spinning animation class to the refresh icon
            const refreshIcon = refreshButton.querySelector('i');
            refreshIcon.classList.add('fa-spin');

            // Remove the spinning animation after 2 seconds
            setTimeout(() => {
                refreshIcon.classList.remove('fa-spin');
            }, 2000);
        });
    }

    // Setup event delegation for dynamically created category pills
    document.body.addEventListener('click', (e) => {
        if (e.target.classList.contains('category-pill')) {
            const category = e.target.textContent;
            newsComponent.filterByCategory(category);

            // Update active state on filter pills
            const filterPills = document.querySelectorAll('.filter-pill');
            filterPills.forEach(pill => {
                if (pill.getAttribute('data-category') === category) {
                    pill.classList.add('active');
                } else {
                    pill.classList.remove('active');
                }
            });
        }
    });
}); 