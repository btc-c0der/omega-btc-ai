// Three.js Bitcoin Visualization
import * as THREE from 'https://unpkg.com/three@0.152.2/build/three.module.js';
import { GLTFLoader } from 'https://unpkg.com/three@0.152.2/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'https://unpkg.com/three@0.152.2/examples/jsm/controls/OrbitControls.js';

// Initialize Three.js Bitcoin visualization
document.addEventListener('DOMContentLoaded', function () {
    initBitcoinVisualization();
});

// Initialize Three.js Bitcoin visualization
function initBitcoinVisualization() {
    // Get the container
    const container = document.getElementById('bitcoin-3d-container');
    const loadingIndicator = document.getElementById('model-loading');

    if (!container) {
        console.error('Bitcoin 3D container not found');
        return;
    }

    // Show loading indicator
    if (loadingIndicator) {
        loadingIndicator.classList.add('active');
    }

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);

    // Add orbit controls for interaction
    let controls;
    try {
        controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.rotateSpeed = 0.5;
        controls.enableZoom = false;
        controls.enablePan = false;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.5;
    } catch (e) {
        console.error('Error creating OrbitControls:', e);
        // Create a simple fallback if OrbitControls fails
        controls = {
            update: function () { },
            autoRotateSpeed: 0.5
        };
    }

    // Create lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Add a backlight for better depth
    const backLight = new THREE.DirectionalLight(0xffffff, 0.8);
    backLight.position.set(-1, -1, -1);
    scene.add(backLight);

    // Fallback Bitcoin geometry (in case model loading fails)
    const fallbackGeometry = new THREE.CylinderGeometry(1.2, 1.2, 0.2, 50);

    // Materials
    const baseGoldMaterial = new THREE.MeshStandardMaterial({
        color: 0xF7931A, // Bitcoin gold
        metalness: 0.8,
        roughness: 0.3,
        emissive: 0xF7931A,
        emissiveIntensity: 0.2
    });

    // Create Bitcoin coin with fallback geometry
    let bitcoin = new THREE.Mesh(fallbackGeometry, baseGoldMaterial);
    let manualRotation = true;
    scene.add(bitcoin);

    // Try to load a more detailed 3D model
    let modelLoaded = false;
    try {
        const loader = new GLTFLoader();

        // Loading animation
        const loadingManager = new THREE.LoadingManager();
        loadingManager.onProgress = function (url, itemsLoaded, itemsTotal) {
            console.log('Loading model: ' + (itemsLoaded / itemsTotal * 100) + '%');
        };

        loadingManager.onLoad = function () {
            if (loadingIndicator) {
                loadingIndicator.classList.remove('active');
            }
        };

        loadingManager.onError = function (url) {
            console.error('Error loading:', url);
            if (loadingIndicator) {
                loadingIndicator.classList.remove('active');
            }
        };

        // Alternative model URLs to try
        const modelUrls = [
            'https://assets.codepen.io/16327/bitcoin.glb',
            'https://models.babylonjs.com/bitcoin.glb',
            'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/models/gltf/coin/scene.gltf'
        ];

        // Try loading models until one works
        function tryLoadModel(index) {
            if (index >= modelUrls.length) {
                console.log('Failed to load any 3D models, using fallback');
                // Hide loading indicator since we're using fallback
                if (loadingIndicator) {
                    loadingIndicator.classList.remove('active');
                }
                return;
            }

            loader.load(
                modelUrls[index],
                function (gltf) {
                    // Successfully loaded the model
                    console.log('Model loaded successfully from ' + modelUrls[index]);
                    modelLoaded = true;

                    // Remove the fallback model
                    scene.remove(bitcoin);

                    // Add the loaded model
                    const model = gltf.scene;
                    model.traverse(function (node) {
                        if (node.isMesh) {
                            node.material = baseGoldMaterial.clone();
                            node.material.needsUpdate = true;
                        }
                    });

                    // Scale and position the model
                    model.scale.set(0.5, 0.5, 0.5);
                    model.position.set(0, 0, 0);
                    scene.add(model);

                    // Update the reference to the bitcoin model
                    bitcoin = model;
                    manualRotation = false;

                    // Hide loading indicator
                    if (loadingIndicator) {
                        loadingIndicator.classList.remove('active');
                    }
                },
                function (xhr) {
                    // Loading progress
                    console.log('Loading ' + modelUrls[index] + ': ' + (xhr.loaded / xhr.total * 100) + '% loaded');
                },
                function (error) {
                    // Error loading model, try the next one
                    console.log('Error loading model:', error);
                    tryLoadModel(index + 1);
                }
            );
        }

        // Start trying to load models
        tryLoadModel(0);

        // Set a timeout to hide the loading indicator if the model loading takes too long
        setTimeout(function () {
            if (!modelLoaded && loadingIndicator) {
                loadingIndicator.classList.remove('active');
            }
        }, 8000); // 8 seconds timeout

    } catch (e) {
        console.error('Error setting up 3D model loader:', e);
        // Hide loading indicator since we're using fallback
        if (loadingIndicator) {
            loadingIndicator.classList.remove('active');
        }
    }

    // Position camera
    camera.position.z = 3;

    // Particle System for cosmic effect
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 3000; // More particles for better effect

    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        // Random position in a sphere around the bitcoin
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        color: 0xFFD700,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending // For better glow effect
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Sentiment value to control visualization
    let currentSentiment = 0.5;
    let rotationSpeed = 0.005;

    // Create cosmic glow effects
    const glowGeometry = new THREE.SphereGeometry(1.5, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
        color: 0xF7931A,
        transparent: true,
        opacity: 0.15,
        side: THREE.BackSide // Glow appears on the inside for better effect
    });
    const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
    scene.add(glowMesh);

    // Update the Bitcoin 3D wrapper based on sentiment
    function updateBitcoin3DWrapper(sentiment) {
        const wrapper = document.querySelector('.bitcoin-3d-wrapper');
        if (wrapper) {
            wrapper.classList.remove('bitcoin-bearish-glow', 'bitcoin-neutral-glow', 'bitcoin-bullish-glow');

            if (sentiment >= 0.7) {
                wrapper.classList.add('bitcoin-bullish-glow');
            } else if (sentiment <= 0.3) {
                wrapper.classList.add('bitcoin-bearish-glow');
            } else {
                wrapper.classList.add('bitcoin-neutral-glow');
            }
        }
    }

    // Animation
    function animate() {
        requestAnimationFrame(animate);

        try {
            // Update controls if available
            controls.update();
        } catch (e) {
            // Fallback manual rotation
            if (manualRotation) {
                bitcoin.rotation.y += rotationSpeed;
            }
        }

        // Additional rotation for particles
        particlesMesh.rotation.y -= 0.0005;
        particlesMesh.rotation.x += 0.0003;

        // Pulse effect based on sentiment
        const pulseIntensity = 0.1 + (Math.sin(Date.now() * 0.001) * 0.05 * currentSentiment);

        // Only scale the fallback model, not the loaded GLTF model
        if (bitcoin.geometry === fallbackGeometry) {
            bitcoin.scale.set(1 + pulseIntensity, 1 + pulseIntensity, 1 + pulseIntensity);
        }

        // Glow pulse effect
        glowMesh.scale.set(1 + pulseIntensity * 1.5, 1 + pulseIntensity * 1.5, 1 + pulseIntensity * 1.5);

        // Update material color and glow based on sentiment
        function updateColor() {
            if (currentSentiment >= 0.7) {
                // Bullish - green glow
                if (bitcoin.material) {
                    bitcoin.material.emissive.setHex(0x3fb950);
                    bitcoin.material.emissiveIntensity = 0.2 + (currentSentiment - 0.7) * 2;
                } else if (bitcoin.traverse) {
                    bitcoin.traverse(function (node) {
                        if (node.isMesh && node.material) {
                            node.material.emissive.setHex(0x3fb950);
                            node.material.emissiveIntensity = 0.2 + (currentSentiment - 0.7) * 2;
                        }
                    });
                }
                particlesMaterial.color.setHex(0x3fb950);
                glowMaterial.color.setHex(0x3fb950);
            } else if (currentSentiment <= 0.3) {
                // Bearish - red glow
                if (bitcoin.material) {
                    bitcoin.material.emissive.setHex(0xf85149);
                    bitcoin.material.emissiveIntensity = 0.2 + (0.3 - currentSentiment) * 2;
                } else if (bitcoin.traverse) {
                    bitcoin.traverse(function (node) {
                        if (node.isMesh && node.material) {
                            node.material.emissive.setHex(0xf85149);
                            node.material.emissiveIntensity = 0.2 + (0.3 - currentSentiment) * 2;
                        }
                    });
                }
                particlesMaterial.color.setHex(0xf85149);
                glowMaterial.color.setHex(0xf85149);
            } else {
                // Neutral - gold glow
                if (bitcoin.material) {
                    bitcoin.material.emissive.setHex(0xF7931A);
                    bitcoin.material.emissiveIntensity = 0.2;
                } else if (bitcoin.traverse) {
                    bitcoin.traverse(function (node) {
                        if (node.isMesh && node.material) {
                            node.material.emissive.setHex(0xF7931A);
                            node.material.emissiveIntensity = 0.2;
                        }
                    });
                }
                particlesMaterial.color.setHex(0xFFD700);
                glowMaterial.color.setHex(0xF7931A);
            }
        }

        updateColor();

        renderer.render(scene, camera);
    }

    // Start animation
    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    // Export function to update visualization based on sentiment
    window.updateBitcoinVisualization = function (sentiment) {
        currentSentiment = sentiment;

        // Update particle density based on sentiment
        particlesMaterial.size = 0.02 + (sentiment * 0.03);
        particlesMaterial.opacity = 0.4 + (sentiment * 0.6);

        // Update glow opacity based on sentiment (stronger when more extreme)
        const extremeness = Math.abs(sentiment - 0.5) * 2;
        glowMaterial.opacity = 0.1 + (extremeness * 0.3);

        // Update wrapper glow effect
        updateBitcoin3DWrapper(sentiment);

        // Update rotation speed based on sentiment
        try {
            controls.autoRotateSpeed = 0.5 + (sentiment * 1.0);
        } catch (e) {
            // Update manual rotation speed if controls are not available
            rotationSpeed = 0.003 + (sentiment * 0.01);
        }
    };

    // Set initial sentiment
    window.updateBitcoinVisualization(0.5);

    console.log('Bitcoin visualization initialized successfully');
} 