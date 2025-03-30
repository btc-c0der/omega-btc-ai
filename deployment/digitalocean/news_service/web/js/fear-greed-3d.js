// Fear and Greed 3D Visualization
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.154.0/build/three.module.js';

// Set this to false to disable the API calls
const ENABLE_FEAR_GREED_API = true;
// Default mock value to use when API is disabled
const DEFAULT_FEAR_GREED_VALUE = 55;

// API endpoint for Fear & Greed Index
const FEAR_GREED_ENDPOINT = '/api/fear-greed';

// Keep track of current value for animations
let currentValue = 50;

document.addEventListener('DOMContentLoaded', function () {
    initFearGreed3D();
});

function initFearGreed3D() {
    const container = document.getElementById('fear-greed-3d');

    if (!container) {
        console.error('Fear and Greed 3D container not found');
        return;
    }

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);

    // Camera position
    camera.position.z = 5;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Create gauge components
    const gaugeRadius = 2;
    const gaugeDepth = 0.2;
    const segments = 64;

    // Gauge background (full circle)
    const bgGeometry = new THREE.RingGeometry(gaugeRadius - 0.3, gaugeRadius, segments);
    const bgMaterial = new THREE.MeshBasicMaterial({
        color: 0x222222,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.7
    });
    const bgMesh = new THREE.Mesh(bgGeometry, bgMaterial);
    scene.add(bgMesh);

    // Create gauge segments
    const segmentCount = 6;
    const segmentAngle = Math.PI / segmentCount;
    const segmentColors = [
        0xcc0000, // Extreme Fear (red)
        0xff4500, // Fear (orange-red)
        0xffa500, // Moderate Fear (orange)
        0xffff00, // Neutral (yellow)
        0x90ee90, // Greed (light green)
        0x00cc00  // Extreme Greed (green)
    ];

    const segmentMeshes = [];

    for (let i = 0; i < segmentCount; i++) {
        const startAngle = Math.PI + i * segmentAngle;
        const endAngle = startAngle + segmentAngle;

        const segGeometry = new THREE.RingGeometry(gaugeRadius - 0.3, gaugeRadius, segments, 1, startAngle, segmentAngle);
        const segMaterial = new THREE.MeshBasicMaterial({
            color: segmentColors[i],
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.85
        });

        const segMesh = new THREE.Mesh(segGeometry, segMaterial);
        scene.add(segMesh);
        segmentMeshes.push(segMesh);
    }

    // Create indicator needle
    const needleGeometry = new THREE.ConeGeometry(0.05, 1.5, 32);
    const needleMaterial = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        metalness: 0.8,
        roughness: 0.2,
        emissive: 0xffffff,
        emissiveIntensity: 0.2
    });

    const needle = new THREE.Mesh(needleGeometry, needleMaterial);
    needle.rotation.z = Math.PI / 2;
    needle.position.y = -0.7;
    scene.add(needle);

    // Center point
    const centerGeometry = new THREE.CircleGeometry(0.15, 32);
    const centerMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const centerPoint = new THREE.Mesh(centerGeometry, centerMaterial);
    centerPoint.position.z = 0.01;
    scene.add(centerPoint);

    // Text labels
    // Rather than using Three.js text (which requires fonts), we'll add HTML labels
    const labelStyle = document.createElement('style');
    labelStyle.textContent = `
        .fear-greed-label {
            position: absolute;
            color: white;
            font-size: 0.75rem;
            text-shadow: 0 0 3px rgba(0,0,0,0.8);
            font-weight: bold;
            transform: translate(-50%, -50%);
        }
        
        .fear-greed-value {
            position: absolute;
            top: 85%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            text-shadow: 0 0 5px rgba(0,0,0,0.8);
        }
    `;
    document.head.appendChild(labelStyle);

    // Add labels
    const labels = [
        { text: "Extreme Fear", angle: Math.PI + segmentAngle * 0.5, distance: 2.3 },
        { text: "Fear", angle: Math.PI + segmentAngle * 1.5, distance: 2.3 },
        { text: "Moderate Fear", angle: Math.PI + segmentAngle * 2.5, distance: 2.3 },
        { text: "Neutral", angle: Math.PI + segmentAngle * 3.5, distance: 2.3 },
        { text: "Greed", angle: Math.PI + segmentAngle * 4.5, distance: 2.3 },
        { text: "Extreme Greed", angle: Math.PI + segmentAngle * 5.5, distance: 2.3 }
    ];

    labels.forEach(label => {
        const labelElem = document.createElement('div');
        labelElem.className = 'fear-greed-label';
        labelElem.textContent = label.text;
        container.appendChild(labelElem);

        // Position based on angle
        const x = Math.cos(label.angle) * label.distance;
        const y = Math.sin(label.angle) * label.distance;

        // Convert to screen coordinates
        const vector = new THREE.Vector3(x, y, 0);
        vector.project(camera);

        const posX = (vector.x * 0.5 + 0.5) * container.clientWidth;
        const posY = (-vector.y * 0.5 + 0.5) * container.clientHeight;

        labelElem.style.left = posX + 'px';
        labelElem.style.top = posY + 'px';
    });

    // Add value display
    const valueDisplay = document.createElement('div');
    valueDisplay.className = 'fear-greed-value';
    valueDisplay.textContent = '50';
    container.appendChild(valueDisplay);

    // Particles for effect
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 200;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i += 3) {
        // Position in a half-circle around the gauge
        const angle = Math.random() * Math.PI + Math.PI;
        const radius = 2 + Math.random() * 3;

        posArray[i] = Math.cos(angle) * radius;
        posArray[i + 1] = Math.sin(angle) * radius;
        posArray[i + 2] = (Math.random() - 0.5) * 0.5;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        transparent: true,
        opacity: 0.5,
        color: 0xffffff,
        blending: THREE.AdditiveBlending
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Animation
    function animate() {
        requestAnimationFrame(animate);

        // Gentle rotation for particles
        particlesMesh.rotation.z += 0.001;

        // Pulse effect for particles
        const pulse = 1 + Math.sin(Date.now() * 0.001) * 0.2;
        particlesMaterial.size = 0.02 * pulse;

        renderer.render(scene, camera);
    }

    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);

        // Reposition labels
        const labelElements = document.querySelectorAll('.fear-greed-label');
        labels.forEach((label, index) => {
            if (labelElements[index]) {
                const x = Math.cos(label.angle) * label.distance;
                const y = Math.sin(label.angle) * label.distance;

                const vector = new THREE.Vector3(x, y, 0);
                vector.project(camera);

                const posX = (vector.x * 0.5 + 0.5) * container.clientWidth;
                const posY = (-vector.y * 0.5 + 0.5) * container.clientHeight;

                labelElements[index].style.left = posX + 'px';
                labelElements[index].style.top = posY + 'px';
            }
        });
    });

    // Function to update the needle position
    function updateFearGreedValue(value) {
        // Update current value for animations
        currentValue = value;

        // Normalize value from 0-100 to 0-1
        const normalizedValue = value / 100;

        // Map to the correct angle (from PI to 2*PI)
        const angle = Math.PI + normalizedValue * Math.PI;

        // Rotate needle
        needle.rotation.z = angle + Math.PI / 2;

        // Update value display
        valueDisplay.textContent = Math.round(value);

        // Color based on value
        let color;
        if (value < 20) {
            color = '#cc0000'; // Extreme Fear
        } else if (value < 40) {
            color = '#ff4500'; // Fear
        } else if (value < 60) {
            color = '#ffff00'; // Neutral
        } else if (value < 80) {
            color = '#90ee90'; // Greed
        } else {
            color = '#00cc00'; // Extreme Greed
        }

        valueDisplay.style.color = color;
        centerPoint.material.color.set(color);

        // Update particles color
        particlesMaterial.color.set(color);
    }

    // Initial value
    updateFearGreedValue(50);

    // Expose function to global scope
    window.updateFearGreedValue = updateFearGreedValue;

    // Load the Fear & Greed data
    async function loadFearGreedData() {
        try {
            // Try the API endpoint
            let response = await fetch(FEAR_GREED_ENDPOINT);

            // If we have a successful response, parse the JSON
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                console.error('Failed to load Fear & Greed data:', response.status);
                // Use mock data as fallback
                return { value: 55, classification: "Neutral", timestamp: new Date().toISOString() };
            }
        } catch (error) {
            console.error('Error loading Fear & Greed data:', error);
            // Use mock data as fallback
            return { value: 55, classification: "Neutral", timestamp: new Date().toISOString() };
        }
    }

    // Add text display to the visualization
    function addTextDisplay() {
        // Create a div for value display if it doesn't exist
        if (!document.getElementById('fear-greed-display')) {
            const display = document.createElement('div');
            display.id = 'fear-greed-display';
            display.style.position = 'absolute';
            display.style.bottom = '20px';
            display.style.left = '0';
            display.style.right = '0';
            display.style.textAlign = 'center';
            display.style.color = 'white';
            display.style.pointerEvents = 'none';
            display.innerHTML = `
                <div id="fear-greed-value" style="font-size: 24px; font-weight: bold;">50</div>
                <div id="fear-greed-label" style="font-size: 14px;">Neutral</div>
            `;

            // Add to the container
            container.appendChild(display);
        }
    }

    // Add text display
    addTextDisplay();

    // Animate to a new value
    function animateToValue(newValue) {
        const startValue = currentValue;
        const duration = 1000; // 1 second
        const startTime = performance.now();

        function animate(time) {
            const elapsed = time - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeInOutCubic(progress);
            const currentVal = startValue + (newValue - startValue) * easedProgress;

            updateFearGreedValue(currentVal);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    }

    // Easing function
    function easeInOutCubic(x) {
        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    }

    function fetchFearGreedIndex() {
        // Try the endpoint
        fetch(FEAR_GREED_ENDPOINT)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data && data.fgi && typeof data.fgi.value === 'number') {
                    console.log(`Fetched Fear & Greed value: ${data.fgi.value}`);
                    animateToValue(data.fgi.value);
                } else {
                    console.warn('Invalid Fear & Greed data format, using mock data');
                    animateToValue(DEFAULT_FEAR_GREED_VALUE);
                }
            })
            .catch(error => {
                console.warn(`Error fetching from ${FEAR_GREED_ENDPOINT}:`, error.message);
                // Use mock data as fallback
                animateToValue(DEFAULT_FEAR_GREED_VALUE);
            });
    }

    // Simulate changing values for demonstration
    function simulateFearGreedChanges() {
        // Instead of simulation, use the real API with fallbacks
        fetchFearGreedIndex();

        // Poll every 5 minutes (300000 ms) instead of every 3 seconds
        setTimeout(simulateFearGreedChanges, 300000);
    }

    // If API is enabled, start fetching data
    if (ENABLE_FEAR_GREED_API) {
        // Load initial data
        fetchFearGreedIndex();

        // Set up polling for updates (every 5 minutes)
        setInterval(fetchFearGreedIndex, 5 * 60 * 1000);
    } else {
        console.log('Fear & Greed API calls disabled, using default value:', DEFAULT_FEAR_GREED_VALUE);
        updateFearGreedValue(DEFAULT_FEAR_GREED_VALUE);
    }
} 