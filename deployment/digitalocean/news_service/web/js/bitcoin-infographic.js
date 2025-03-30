// OMEGA BTC AI Bitcoin Infographic
console.log('Loading Bitcoin infographic...');

class BitcoinInfographic {
    constructor() {
        this.container = null;

        // Initialize when the DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }
    }

    // Initialize the infographic
    initialize() {
        // Create container if it doesn't exist
        if (!document.getElementById('infographic-container')) {
            this.container = document.createElement('div');
            this.container.id = 'infographic-container';
            this.container.className = 'mb-5';

            // Find where to insert the infographic (before news section, after future visions)
            const futureVisions = document.getElementById('future-visions-container');
            const newsSection = document.getElementById('news-section');

            if (futureVisions && futureVisions.nextElementSibling) {
                // Insert after future visions section
                futureVisions.parentNode.insertBefore(this.container, futureVisions.nextElementSibling);
            } else if (newsSection) {
                // Insert before news section
                newsSection.parentNode.insertBefore(this.container, newsSection);
            } else {
                // Fallback: append to main container
                const container = document.querySelector('.container');
                if (container) {
                    container.appendChild(this.container);
                } else {
                    console.error('No suitable container found for infographic');
                    return;
                }
            }
        } else {
            this.container = document.getElementById('infographic-container');
        }

        // Create and render the infographic
        this.renderInfographic();
    }

    // Render the infographic
    renderInfographic() {
        // Data for the infographic
        const infographicData = {
            title: "Bitcoin Evolution & Ecosystem",
            sections: [
                {
                    title: "Bitcoin Timeline",
                    type: "timeline",
                    items: [
                        { year: 2008, title: "Bitcoin Whitepaper", description: "Satoshi Nakamoto publishes the Bitcoin whitepaper" },
                        { year: 2009, title: "Genesis Block", description: "The first Bitcoin block is mined" },
                        { year: 2010, title: "First Transaction", description: "First commercial transaction: 10,000 BTC for two pizzas" },
                        { year: 2013, title: "First Major Bull Run", description: "Bitcoin surpasses $1,000 for the first time" },
                        { year: 2017, title: "Mainstream Attention", description: "Bitcoin reaches nearly $20,000" },
                        { year: 2020, title: "Institutional Adoption", description: "MicroStrategy and Square begin adding BTC to balance sheets" },
                        { year: 2021, title: "New All-Time High", description: "Bitcoin reaches $69,000" }
                    ]
                },
                {
                    title: "Bitcoin Network Stats",
                    type: "stats",
                    items: [
                        { label: "Hash Rate", value: "~400 EH/s", icon: "bi-cpu" },
                        { label: "Nodes", value: "~15,000", icon: "bi-hdd-network" },
                        { label: "Blockchain Size", value: "~500 GB", icon: "bi-database" },
                        { label: "Block Time", value: "10 minutes", icon: "bi-clock" },
                        { label: "Block Reward", value: "6.25 BTC", icon: "bi-trophy" },
                        { label: "Next Halving", value: "~2024", icon: "bi-calendar" }
                    ]
                },
                {
                    title: "Bitcoin Market Cycles",
                    type: "cycle",
                    cycles: [
                        { phase: "Accumulation", color: "#2e5984", description: "Smart money accumulates BTC at low prices" },
                        { phase: "Early Bull", color: "#3fb950", description: "Price begins rising as sentiment improves" },
                        { phase: "FOMO", color: "#7ee787", description: "Rapid price increase with maximum media coverage" },
                        { phase: "Peak", color: "#f7931a", description: "Parabolic price action & euphoria" },
                        { phase: "Correction", color: "#f85149", description: "Price crashes as bubble pops" },
                        { phase: "Bear Market", color: "#da3633", description: "Extended period of declining prices & low interest" }
                    ]
                }
            ]
        };

        // Create the infographic HTML
        this.container.innerHTML = `
      <div class="card mb-4">
        <div class="card-body">
          <h3 class="card-title mb-4">
            <i class="bi bi-info-circle-fill text-warning me-2"></i>
            ${infographicData.title}
          </h3>
          
          <!-- Timeline Section -->
          <div class="mb-4 pb-3 border-bottom border-secondary">
            <h4 class="mb-3">
              <i class="bi bi-calendar-event me-2"></i>
              ${infographicData.sections[0].title}
            </h4>
            <div class="bitcoin-timeline position-relative">
              <div class="timeline-line"></div>
              <div class="row g-3">
                ${this.renderTimelineItems(infographicData.sections[0].items)}
              </div>
            </div>
          </div>
          
          <!-- Network Stats Section -->
          <div class="mb-4 pb-3 border-bottom border-secondary">
            <h4 class="mb-3">
              <i class="bi bi-graph-up me-2"></i>
              ${infographicData.sections[1].title}
            </h4>
            <div class="row g-3">
              ${this.renderStatsItems(infographicData.sections[1].items)}
            </div>
          </div>
          
          <!-- Market Cycles Section -->
          <div class="mb-3">
            <h4 class="mb-3">
              <i class="bi bi-arrow-repeat me-2"></i>
              ${infographicData.sections[2].title}
            </h4>
            <div class="bitcoin-cycle-chart">
              ${this.renderCycleChart(infographicData.sections[2].cycles)}
            </div>
          </div>
        </div>
      </div>
    `;

        // Add custom styling
        this.addStyles();

        console.log('Bitcoin infographic rendered');
    }

    // Render timeline items
    renderTimelineItems(items) {
        return items.map(item => `
      <div class="col-md-6 col-lg-3">
        <div class="timeline-item position-relative">
          <div class="timeline-point"></div>
          <div class="timeline-content card bg-dark">
            <div class="card-body p-3">
              <div class="timeline-year badge bg-warning text-dark mb-2">${item.year}</div>
              <h5 class="timeline-title">${item.title}</h5>
              <p class="timeline-description small text-muted mb-0">${item.description}</p>
            </div>
          </div>
        </div>
      </div>
    `).join('');
    }

    // Render network stats
    renderStatsItems(items) {
        return items.map(item => `
      <div class="col-md-6 col-lg-4">
        <div class="card bg-dark h-100">
          <div class="card-body d-flex align-items-center p-3">
            <div class="stats-icon me-3">
              <i class="bi ${item.icon} fs-1 text-warning"></i>
            </div>
            <div>
              <h5 class="mb-1">${item.label}</h5>
              <div class="stats-value fs-4">${item.value}</div>
            </div>
          </div>
        </div>
      </div>
    `).join('');
    }

    // Render market cycle chart
    renderCycleChart(cycles) {
        const cycleSegments = cycles.map((cycle, index) => {
            const segmentAngle = 360 / cycles.length;
            const rotation = index * segmentAngle;
            return `
        <div class="cycle-segment" style="
          transform: rotate(${rotation}deg);
          background-color: ${cycle.color};
        " data-phase="${cycle.phase}" data-description="${cycle.description}">
          <span class="cycle-label">${cycle.phase}</span>
        </div>
      `;
        }).join('');

        return `
      <div class="cycle-container text-center">
        <div class="cycle-chart">
          ${cycleSegments}
          <div class="cycle-center">
            <i class="bi bi-currency-bitcoin fs-1"></i>
          </div>
        </div>
        <div class="cycle-description mt-3" id="cycle-description">
          <p class="fw-bold mb-1">Market Cycles</p>
          <p class="small mb-0">Hover over segments to learn about each market phase</p>
        </div>
      </div>
    `;
    }

    // Add required styles
    addStyles() {
        // Only add styles once
        if (document.getElementById('infographic-styles')) return;

        const style = document.createElement('style');
        style.id = 'infographic-styles';
        style.textContent = `
      /* Timeline Styles */
      .bitcoin-timeline {
        padding: 20px 0;
        position: relative;
      }
      
      .timeline-line {
        position: absolute;
        height: 3px;
        background: linear-gradient(90deg, #f7931a, #f85149, #2e5984, #3fb950, #f7931a);
        top: 50%;
        left: 0;
        right: 0;
        z-index: 1;
        transform: translateY(-50%);
      }
      
      .timeline-item {
        padding: 20px 10px;
        margin-bottom: 15px;
      }
      
      .timeline-point {
        width: 12px;
        height: 12px;
        background-color: #f7931a;
        border-radius: 50%;
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2;
        box-shadow: 0 0 0 4px rgba(247, 147, 26, 0.3);
      }
      
      .timeline-year {
        display: inline-block;
        font-weight: bold;
      }
      
      /* Stats Styles */
      .stats-icon {
        opacity: 0.8;
      }
      
      /* Cycle Chart Styles */
      .cycle-container {
        padding: 20px;
      }
      
      .cycle-chart {
        width: 300px;
        height: 300px;
        position: relative;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
      }
      
      .cycle-segment {
        position: absolute;
        width: 50%;
        height: 50%;
        top: 0;
        right: 0;
        transform-origin: bottom left;
        clip-path: polygon(0 0, 100% 0, 100% 100%);
        transition: all 0.3s ease;
        cursor: pointer;
      }
      
      .cycle-segment:hover {
        opacity: 0.8;
        transform-origin: bottom left;
        transform: rotate(calc(var(--rotation) * 1deg)) scale(1.05);
      }
      
      .cycle-center {
        position: absolute;
        width: 80px;
        height: 80px;
        background: #161b22;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
        color: #f7931a;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
      }
      
      .cycle-label {
        position: absolute;
        font-size: 0;
        opacity: 0;
      }
      
      /* Responsive adjustments */
      @media (max-width: 768px) {
        .cycle-chart {
          width: 250px;
          height: 250px;
        }
        
        .cycle-center {
          width: 60px;
          height: 60px;
        }
      }
    `;

        document.head.appendChild(style);

        // Add event listeners for cycle segments
        setTimeout(() => {
            const cycleSegments = document.querySelectorAll('.cycle-segment');
            const cycleDescription = document.getElementById('cycle-description');

            cycleSegments.forEach(segment => {
                segment.addEventListener('mouseenter', () => {
                    const phase = segment.getAttribute('data-phase');
                    const description = segment.getAttribute('data-description');

                    cycleDescription.innerHTML = `
            <p class="fw-bold mb-1">${phase} Phase</p>
            <p class="small mb-0">${description}</p>
          `;
                });

                segment.addEventListener('mouseleave', () => {
                    cycleDescription.innerHTML = `
            <p class="fw-bold mb-1">Market Cycles</p>
            <p class="small mb-0">Hover over segments to learn about each market phase</p>
          `;
                });
            });
        }, 500);
    }
}

// Create global instance
window.bitcoinInfographic = new BitcoinInfographic();

console.log('✅ Bitcoin infographic loaded.');