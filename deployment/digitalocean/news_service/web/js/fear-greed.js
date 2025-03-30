/**
 * Fear & Greed Index Module
 * Fetches data from the API and displays it in the dashboard
 * with lazy loading to avoid blocking the main content
 */

// Constants for the Fear & Greed ranges
const RANGES = {
    EXTREME_FEAR: { min: 0, max: 25, class: 'extreme-fear-color', label: 'Extreme Fear' },
    FEAR: { min: 25, max: 40, class: 'fear-color', label: 'Fear' },
    NEUTRAL: { min: 40, max: 60, class: 'neutral-color', label: 'Neutral' },
    GREED: { min: 60, max: 80, class: 'greed-color', label: 'Greed' },
    EXTREME_GREED: { min: 80, max: 100, class: 'extreme-greed-color', label: 'Extreme Greed' }
};

// State
let fearGreedData = null;
let chart = null;
let isIntersectionObserverSupported = 'IntersectionObserver' in window;
let observer = null;
let isDataLoaded = false;

/**
 * Get the classification range for a value
 * @param {number} value - Fear & Greed value (0-100)
 * @returns {object} Range object with min, max, class, and label
 */
function getClassificationForValue(value) {
    if (value <= RANGES.EXTREME_FEAR.max) return RANGES.EXTREME_FEAR;
    if (value <= RANGES.FEAR.max) return RANGES.FEAR;
    if (value <= RANGES.NEUTRAL.max) return RANGES.NEUTRAL;
    if (value <= RANGES.GREED.max) return RANGES.GREED;
    return RANGES.EXTREME_GREED;
}

/**
 * Calculate needle rotation based on value
 * @param {number} value - Fear & Greed value (0-100)
 * @returns {number} Rotation in degrees
 */
function getNeedleRotation(value) {
    // Calculate rotation from -90 (min) to 90 (max)
    return (value / 100) * 180 - 90;
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format date for chart labels
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date for chart (MM/DD)
 */
function formatChartDate(dateString) {
    const date = new Date(dateString);
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

/**
 * Update the UI with Fear & Greed data
 * @param {object} data - Fear & Greed data from API
 */
function updateUI(data) {
    // Get elements only when needed to avoid blocking
    const elements = {
        value: document.getElementById('fear-greed-value'),
        classification: document.getElementById('fear-greed-classification'),
        needle: document.getElementById('fear-greed-needle'),
        timestamp: document.getElementById('fear-greed-timestamp'),
        chartCanvas: document.getElementById('fear-greed-history-chart'),
        container: document.querySelector('.fear-greed-container'),
        chart: document.getElementById('fear-greed-chart')
    };

    if (!data || !data.fgi || !elements.value) return;

    // Remove loading states
    if (elements.container) {
        elements.container.classList.remove('loading');
    }

    if (elements.chart) {
        elements.chart.classList.remove('loading');
    }

    const fgi = data.fgi;
    const classification = getClassificationForValue(fgi.value);

    // Update value and classification
    elements.value.textContent = fgi.value;
    elements.value.className = 'fear-greed-value ' + classification.class;
    elements.classification.textContent = classification.label;
    elements.classification.className = 'fear-greed-label ' + classification.class;

    // Update needle position
    const rotation = getNeedleRotation(fgi.value);
    elements.needle.style.transform = `translateX(-50%) translateY(-100%) rotate(${rotation}deg)`;

    // Update timestamp
    elements.timestamp.textContent = `Last updated: ${formatDate(fgi.timestamp)}`;

    // Update chart if we have history data
    if (data.history && data.history.length > 0 && elements.chartCanvas) {
        updateChart(data.history, elements.chartCanvas);
    }
}

/**
 * Update the history chart
 * @param {array} historyData - Array of historical Fear & Greed data
 * @param {HTMLElement} chartCanvas - Canvas element for the chart
 */
function updateChart(historyData, chartCanvas) {
    // Sort data by date
    const sortedData = [...historyData].sort((a, b) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    // Prepare data for the chart
    const labels = sortedData.map(item => formatChartDate(item.timestamp));
    const values = sortedData.map(item => item.value);
    const backgroundColors = sortedData.map(item => {
        const classification = getClassificationForValue(item.value);
        switch (classification.label) {
            case 'Extreme Fear': return 'rgba(244, 67, 54, 0.7)';
            case 'Fear': return 'rgba(255, 152, 0, 0.7)';
            case 'Neutral': return 'rgba(255, 193, 7, 0.7)';
            case 'Greed': return 'rgba(76, 175, 80, 0.7)';
            case 'Extreme Greed': return 'rgba(139, 195, 74, 0.7)';
            default: return 'rgba(255, 193, 7, 0.7)';
        }
    });

    // Destroy existing chart if it exists
    if (chart) {
        chart.destroy();
    }

    // Create new chart
    const ctx = chartCanvas.getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Fear & Greed Index',
                data: values,
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: backgroundColors,
                pointBorderColor: '#fff',
                pointRadius: 4,
                tension: 0.2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            const classification = getClassificationForValue(value);
                            return `Value: ${value} (${classification.label})`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Fetch Fear & Greed data from API
 */
async function fetchFearGreedData() {
    if (isDataLoaded) return;

    try {
        const response = await fetch('/api/fear-greed');

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        fearGreedData = data;
        isDataLoaded = true;
        updateUI(data);
    } catch (error) {
        console.error('Error fetching Fear & Greed data:', error);
        // Show error in UI
        const elements = {
            value: document.getElementById('fear-greed-value'),
            classification: document.getElementById('fear-greed-classification'),
            timestamp: document.getElementById('fear-greed-timestamp')
        };

        if (elements.value) elements.value.textContent = '--';
        if (elements.classification) elements.classification.textContent = 'Data unavailable';
        if (elements.timestamp) elements.timestamp.textContent = 'Error fetching data';
    }
}

/**
 * Lazy load the Fear & Greed data when section is visible
 */
function lazyLoadFearGreed() {
    const fearGreedSection = document.getElementById('fear-greed-section');
    if (!fearGreedSection) return;

    // If IntersectionObserver is not supported, load immediately
    if (!isIntersectionObserverSupported) {
        fetchFearGreedData();
        return;
    }

    observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                fetchFearGreedData();
                // Stop observing once data is loaded
                observer.disconnect();
            }
        });
    }, {
        rootMargin: '100px',  // Load when within 100px of viewport
        threshold: 0.1        // Trigger when at least 10% visible
    });

    observer.observe(fearGreedSection);
}

/**
 * Initialize the Fear & Greed module
 */
function initFearGreedIndex() {
    // Add loading state to elements
    const fearGreedContainer = document.querySelector('.fear-greed-container');
    const fearGreedChart = document.getElementById('fear-greed-chart');

    if (fearGreedContainer) {
        fearGreedContainer.classList.add('loading');
    }

    if (fearGreedChart) {
        fearGreedChart.classList.add('loading');
    }

    // Set up lazy loading
    lazyLoadFearGreed();

    // Also set up a fallback to load after a small delay if user hasn't scrolled
    setTimeout(() => {
        if (!isDataLoaded) {
            fetchFearGreedData();
        }
    }, 5000);  // 5-second delay
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initFearGreedIndex); 