// Main JavaScript for OMEGA BTC AI Presentation

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initMobileNav();
    initPersonaTabs();
    initScrollAnimations();
    initQuantumParticles();
    initConsciousnessMeters();
    initQuantumCircuitAnimation();
    initFibonacciChart();
    initBtcPriceSimulator();
});

// Mobile Navigation Toggle
function initMobileNav() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('nav ul');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
        });
    }
}

// Persona Tab Switching
function initPersonaTabs() {
    const personaTabs = document.querySelectorAll('.persona-tab');
    const personaContents = document.querySelectorAll('.persona-content');

    personaTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            personaTabs.forEach(t => t.classList.remove('active'));
            personaContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            const target = tab.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });
}

// Scroll Animations
function initScrollAnimations() {
    const fadeElements = document.querySelectorAll('.fade-in');

    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    fadeElements.forEach(element => {
        fadeInObserver.observe(element);
    });
}

// Quantum Particle Animation
function initQuantumParticles() {
    const quantumContainers = document.querySelectorAll('.quantum-container');

    quantumContainers.forEach(container => {
        // Create particles
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.classList.add('quantum-particle');

            // Random positioning
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';

            // Random size
            const size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';

            // Random animation delay
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';

            container.appendChild(particle);
        }
    });
}

// Consciousness Meter Animation
function initConsciousnessMeters() {
    const meters = document.querySelectorAll('.consciousness-meter');

    meters.forEach(meter => {
        const level = meter.querySelector('.consciousness-level');
        const percentage = meter.getAttribute('data-level') || '50';

        // Animate the level
        setTimeout(() => {
            level.style.width = percentage + '%';
        }, 500);
    });
}

// Quantum Circuit Animation
function initQuantumCircuitAnimation() {
    const circuitContainer = document.querySelector('.quantum-circuit-animation');

    if (!circuitContainer) return;

    // Gate types
    const gateTypes = ['H', 'X', 'Z', 'CNOT', 'RZ', 'RY', 'M'];
    const gateColors = {
        'H': '#8b5cf6',
        'X': '#ef4444',
        'Z': '#3b82f6',
        'CNOT': '#ef4444',
        'RZ': '#10b981',
        'RY': '#f59e0b',
        'M': '#0ea5e9'
    };

    // Function to create quantum gate
    function createGate(type, position, wire) {
        const gate = document.createElement('div');
        gate.classList.add('quantum-gate');
        gate.textContent = type;
        gate.style.backgroundColor = gateColors[type];
        gate.style.left = position + '%';

        // Add to the circuit
        const wireLine = document.querySelector(`.qbit-line:nth-child(${wire}) .quantum-wire`);
        wireLine.appendChild(gate);

        // Add animation
        gate.style.opacity = '0';
        gate.style.transform = 'translateY(-50%) scale(0)';

        setTimeout(() => {
            gate.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            gate.style.opacity = '1';
            gate.style.transform = 'translateY(-50%) scale(1)';
        }, Math.random() * 1000 + 500);

        return gate;
    }

    // Setup initial gates
    for (let i = 1; i <= 5; i++) {
        // Hadamard gates for each qubit
        createGate('H', 10, i);

        // Add random gates
        const numGates = Math.floor(Math.random() * 3) + 1;
        for (let j = 0; j < numGates; j++) {
            const gateType = gateTypes[Math.floor(Math.random() * (gateTypes.length - 1))]; // Exclude measurement
            const position = Math.random() * 50 + 25;
            createGate(gateType, position, i);
        }

        // Measurement gates
        createGate('M', 85, i);
    }

    // Add control lines for CNOT gates
    setTimeout(() => {
        const cnotGates = document.querySelectorAll('.quantum-gate');
        cnotGates.forEach(gate => {
            if (gate.textContent === 'CNOT') {
                // Add a control line
                const controlLine = document.createElement('div');
                controlLine.classList.add('control-line');
                controlLine.style.position = 'absolute';
                controlLine.style.width = '2px';
                controlLine.style.backgroundColor = '#ef4444';
                controlLine.style.left = gate.style.left;
                controlLine.style.top = '-20px';
                controlLine.style.height = '40px';
                controlLine.style.opacity = '0';

                gate.parentNode.appendChild(controlLine);

                setTimeout(() => {
                    controlLine.style.transition = 'opacity 0.5s ease';
                    controlLine.style.opacity = '1';
                }, 200);
            }
        });
    }, 2000);
}

// Fibonacci Chart
function initFibonacciChart() {
    const chartContainer = document.getElementById('fibonacci-chart');

    if (!chartContainer) return;

    // Fibonacci levels
    const fibLevels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];

    // Create SVG
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("viewBox", "0 0 800 300");
    chartContainer.appendChild(svg);

    // Price data points (simulated BTC price)
    const startPrice = 30000;
    const dataPoints = [];
    let currentPrice = startPrice;

    for (let i = 0; i < 100; i++) {
        currentPrice += (Math.random() - 0.48) * 200;
        dataPoints.push(currentPrice);
    }

    // Find min and max
    const minPrice = Math.min(...dataPoints) * 0.99;
    const maxPrice = Math.max(...dataPoints) * 1.01;
    const priceRange = maxPrice - minPrice;

    // Scale functions
    const scaleX = (i) => (i / (dataPoints.length - 1)) * 700 + 50;
    const scaleY = (price) => 280 - ((price - minPrice) / priceRange) * 240;

    // Draw axes
    const xAxis = document.createElementNS(svgNS, "line");
    xAxis.setAttribute("x1", "50");
    xAxis.setAttribute("y1", "280");
    xAxis.setAttribute("x2", "750");
    xAxis.setAttribute("y2", "280");
    xAxis.setAttribute("stroke", "#ccc");
    xAxis.setAttribute("stroke-width", "1");
    svg.appendChild(xAxis);

    const yAxis = document.createElementNS(svgNS, "line");
    yAxis.setAttribute("x1", "50");
    yAxis.setAttribute("y1", "40");
    yAxis.setAttribute("x2", "50");
    yAxis.setAttribute("y2", "280");
    yAxis.setAttribute("stroke", "#ccc");
    yAxis.setAttribute("stroke-width", "1");
    svg.appendChild(yAxis);

    // Draw y-axis labels
    for (let i = 0; i <= 4; i++) {
        const label = document.createElementNS(svgNS, "text");
        const price = minPrice + (priceRange * i / 4);
        label.setAttribute("x", "40");
        label.setAttribute("y", scaleY(price) + 5);
        label.setAttribute("text-anchor", "end");
        label.setAttribute("font-size", "12");
        label.setAttribute("fill", "#666");
        label.textContent = Math.round(price).toLocaleString();
        svg.appendChild(label);

        // Grid line
        const gridLine = document.createElementNS(svgNS, "line");
        gridLine.setAttribute("x1", "50");
        gridLine.setAttribute("y1", scaleY(price));
        gridLine.setAttribute("x2", "750");
        gridLine.setAttribute("y2", scaleY(price));
        gridLine.setAttribute("stroke", "#eee");
        gridLine.setAttribute("stroke-width", "1");
        svg.appendChild(gridLine);
    }

    // Draw price line
    const pricePath = document.createElementNS(svgNS, "path");
    let pathData = `M ${scaleX(0)} ${scaleY(dataPoints[0])}`;

    for (let i = 1; i < dataPoints.length; i++) {
        pathData += ` L ${scaleX(i)} ${scaleY(dataPoints[i])}`;
    }

    pricePath.setAttribute("d", pathData);
    pricePath.setAttribute("fill", "none");
    pricePath.setAttribute("stroke", "#6b46c1");
    pricePath.setAttribute("stroke-width", "2");
    svg.appendChild(pricePath);

    // Draw fibonacci levels
    const lastPrice = dataPoints[dataPoints.length - 1];
    const firstPrice = dataPoints[0];
    const trend = lastPrice > firstPrice ? "up" : "down";
    const highPrice = trend === "up" ? lastPrice : firstPrice;
    const lowPrice = trend === "up" ? firstPrice : lastPrice;
    const fibRange = highPrice - lowPrice;

    fibLevels.forEach(level => {
        const fibPrice = trend === "up"
            ? highPrice - (fibRange * level)
            : lowPrice + (fibRange * level);

        // Fibonacci line
        const fibLine = document.createElementNS(svgNS, "line");
        fibLine.setAttribute("x1", "50");
        fibLine.setAttribute("y1", scaleY(fibPrice));
        fibLine.setAttribute("x2", "750");
        fibLine.setAttribute("y2", scaleY(fibPrice));
        fibLine.setAttribute("stroke", "#ed8936");
        fibLine.setAttribute("stroke-width", "1");
        fibLine.setAttribute("stroke-dasharray", "5,5");
        svg.appendChild(fibLine);

        // Fibonacci label
        const fibLabel = document.createElementNS(svgNS, "text");
        fibLabel.setAttribute("x", "55");
        fibLabel.setAttribute("y", scaleY(fibPrice) - 5);
        fibLabel.setAttribute("font-size", "10");
        fibLabel.setAttribute("fill", "#ed8936");
        fibLabel.textContent = level === 0 || level === 1 ? level : level.toFixed(3);
        svg.appendChild(fibLabel);

        // Price label
        const priceLabel = document.createElementNS(svgNS, "text");
        priceLabel.setAttribute("x", "745");
        priceLabel.setAttribute("y", scaleY(fibPrice) - 5);
        priceLabel.setAttribute("text-anchor", "end");
        priceLabel.setAttribute("font-size", "10");
        priceLabel.setAttribute("fill", "#ed8936");
        priceLabel.textContent = Math.round(fibPrice).toLocaleString();
        svg.appendChild(priceLabel);
    });
}

// BTC Price Simulator 
function initBtcPriceSimulator() {
    const priceDisplay = document.getElementById('btc-price-display');

    if (!priceDisplay) return;

    let price = 30000 + Math.random() * 2000;
    updatePrice();

    setInterval(updatePrice, 3000);

    function updatePrice() {
        // Random price change
        price += (Math.random() - 0.48) * 200;

        // Format price
        const formattedPrice = price.toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        // Apply animation
        priceDisplay.classList.add('price-update');

        setTimeout(() => {
            priceDisplay.textContent = formattedPrice;
            priceDisplay.classList.remove('price-update');
        }, 300);
    }
} 