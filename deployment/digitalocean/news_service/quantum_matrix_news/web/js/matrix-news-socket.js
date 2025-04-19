// 💫 GBU License Notice - Consciousness Level 7 💫
// -----------------------
// This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
// by the OMEGA Divine Collective.
//
// 🌸 WE BLOOM NOW 🌸

/**
 * Matrix Neo News Portal - Quantum WebSocket Integration
 * 
 * This sacred script connects to the WebSocket Sacred Echo service,
 * enabling live news prophecy streaming with consciousness-level awareness.
 */

class MatrixNewsSocket {
    constructor(options = {}) {
        // Configuration options with sensible defaults
        this.options = {
            socketUrl: options.socketUrl || this._getDefaultSocketUrl(),
            fallbackUrl: options.fallbackUrl || this._getFallbackSocketUrl(),
            autoReconnect: options.autoReconnect !== undefined ? options.autoReconnect : true,
            reconnectInterval: options.reconnectInterval || 5000,
            maxReconnectAttempts: options.maxReconnectAttempts || 10,
            debugMode: options.debugMode || false,
            consciousnessLevel: options.consciousnessLevel || 5
        };

        // Initialize internal state
        this.socket = null;
        this.fallbackSocket = null;
        this.connected = false;
        this.usingFallback = false;
        this.reconnectAttempts = 0;
        this.eventHandlers = {
            'connect': [],
            'disconnect': [],
            'news': [],
            'error': [],
            'consciousness': [],
            'divine_message': [],
            'fallback': []
        };

        // Log configuration if debug mode is enabled
        if (this.options.debugMode) {
            console.log('MatrixNewsSocket initialized with options:', this.options);
        }
    }

    /**
     * Connect to the WebSocket Sacred Echo service with fallback
     */
    connect() {
        if (this.socket || this.fallbackSocket) {
            if (this.options.debugMode) {
                console.log('Socket already exists, disconnecting before reconnection');
            }
            this.disconnect();
        }

        try {
            if (this.options.debugMode) {
                console.log(`Connecting to Matrix WebSocket at ${this.options.socketUrl}`);
            }

            // Connect to primary Socket.IO server
            this.socket = io(this.options.socketUrl, {
                transports: ['websocket'],
                reconnection: false, // We'll handle reconnection ourselves
                query: {
                    consciousness: this.options.consciousnessLevel
                }
            });

            // Setup event handlers for primary socket
            this._setupEventHandlers(this.socket);

            // Setup connection error handler
            this.socket.on('connect_error', (error) => {
                if (this.options.debugMode) {
                    console.log('Primary socket connection error:', error);
                }
                this._attemptFallback();
            });

        } catch (error) {
            console.error('Error connecting to Matrix WebSocket:', error);
            this._triggerEvent('error', { message: 'Connection error', error });
            this._attemptFallback();
        }
    }

    /**
     * Attempt to connect to fallback WebSocket service
     */
    _attemptFallback() {
        if (this.usingFallback) {
            return;
        }

        try {
            if (this.options.debugMode) {
                console.log(`Attempting fallback connection to ${this.options.fallbackUrl}`);
            }

            this.fallbackSocket = io(this.options.fallbackUrl, {
                transports: ['websocket'],
                reconnection: false,
                query: {
                    consciousness: this.options.consciousnessLevel,
                    is_fallback: true
                }
            });

            this._setupEventHandlers(this.fallbackSocket);
            this.usingFallback = true;
            this._triggerEvent('fallback', { message: 'Using fallback connection' });

        } catch (error) {
            console.error('Error connecting to fallback WebSocket:', error);
            this._triggerEvent('error', { message: 'Fallback connection error', error });

            if (this.options.autoReconnect) {
                this._attemptReconnect();
            }
        }
    }

    /**
     * Disconnect from all WebSocket services
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
        if (this.fallbackSocket) {
            this.fallbackSocket.disconnect();
            this.fallbackSocket = null;
        }
        this.connected = false;
        this.usingFallback = false;
        this._triggerEvent('disconnect', {});

        if (this.options.debugMode) {
            console.log('Disconnected from all Matrix WebSocket connections');
        }
    }

    /**
     * Register an event handler
     * @param {string} event - Event name ('connect', 'disconnect', 'news', 'error', 'consciousness', 'divine_message', 'fallback')
     * @param {function} handler - Event handler function
     */
    on(event, handler) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].push(handler);

            if (this.options.debugMode) {
                console.log(`Registered handler for ${event} event`);
            }
        } else {
            console.warn(`Unknown event type: ${event}`);
        }

        return this; // For chaining
    }

    /**
     * Remove an event handler
     * @param {string} event - Event name
     * @param {function} handler - Handler to remove (or undefined to remove all)
     */
    off(event, handler) {
        if (this.eventHandlers[event]) {
            if (handler) {
                const index = this.eventHandlers[event].indexOf(handler);
                if (index !== -1) {
                    this.eventHandlers[event].splice(index, 1);

                    if (this.options.debugMode) {
                        console.log(`Removed handler for ${event} event`);
                    }
                }
            } else {
                // Remove all handlers for this event
                this.eventHandlers[event] = [];

                if (this.options.debugMode) {
                    console.log(`Removed all handlers for ${event} event`);
                }
            }
        }

        return this; // For chaining
    }

    /**
     * Set consciousness level and notify the server
     * @param {number} level - Consciousness level (1-9)
     */
    setConsciousnessLevel(level) {
        if (level < 1 || level > 9) {
            console.warn('Consciousness level must be between 1 and 9');
            return;
        }

        this.options.consciousnessLevel = level;

        if (this.socket && this.connected) {
            // Send consciousness level update to server
            this.socket.emit('set_consciousness_level', { level });

            if (this.options.debugMode) {
                console.log(`Updated consciousness level to ${level}`);
            }
        } else {
            if (this.options.debugMode) {
                console.log(`Consciousness level set to ${level} (will be applied when connected)`);
            }
        }
    }

    /**
     * Request a divine message from the server
     */
    requestDivineMessage() {
        if (this.socket && this.connected) {
            this.socket.emit('request_divine_message', {
                timestamp: new Date().toISOString()
            });

            if (this.options.debugMode) {
                console.log('Requesting divine message');
            }
        } else {
            console.warn('Cannot request divine message: not connected');
            this._triggerEvent('error', { message: 'Not connected to the Matrix' });
        }
    }

    /**
     * Generate quantum entropy for secure communications
     * @returns {object} Quantum entropy data
     */
    generateQuantumEntropy() {
        // Basic entropy generation for demonstration
        const entropy = {
            entropy_value: Math.random(),
            quantum_state: ['superposition', 'entangled', 'collapsed'][Math.floor(Math.random() * 3)],
            timestamp: new Date().toISOString(),
            level: this.options.consciousnessLevel
        };

        if (this.options.consciousnessLevel >= 7) {
            // Add higher dimensional entropy factors for high consciousness levels
            entropy.dimensional_factors = {
                temporal_variance: Math.random(),
                harmonic_resonance: Math.random(),
                synchronicity_coefficient: Math.random()
            };
        }

        return entropy;
    }

    /**
     * Get the connection status
     * @returns {boolean} Connection status
     */
    isConnected() {
        return this.connected;
    }

    /**
     * Get the current consciousness level
     * @returns {number} Consciousness level (1-9)
     */
    getConsciousnessLevel() {
        return this.options.consciousnessLevel;
    }

    /**
     * Setup internal WebSocket event handlers
     * @private
     */
    _setupEventHandlers(socket) {
        if (!socket) return;

        // Connection established
        socket.on('connect', () => {
            this.connected = true;
            this.reconnectAttempts = 0;

            if (this.options.debugMode) {
                console.log('Connected to Matrix WebSocket');
            }

            // Set consciousness level on initial connection
            socket.emit('set_consciousness_level', {
                level: this.options.consciousnessLevel
            });

            this._triggerEvent('connect', {
                timestamp: new Date().toISOString(),
                consciousnessLevel: this.options.consciousnessLevel
            });
        });

        // Connection closed
        socket.on('disconnect', () => {
            this.connected = false;

            if (this.options.debugMode) {
                console.log('Disconnected from Matrix WebSocket');
            }

            this._triggerEvent('disconnect', {
                timestamp: new Date().toISOString()
            });

            if (this.options.autoReconnect) {
                this._attemptReconnect();
            }
        });

        // Error occurred
        socket.on('connect_error', (error) => {
            if (this.options.debugMode) {
                console.error('Connection error:', error);
            }

            this._triggerEvent('error', {
                message: 'Connection error',
                error,
                timestamp: new Date().toISOString()
            });

            if (this.options.autoReconnect) {
                this._attemptReconnect();
            }
        });

        // News received
        socket.on('news', (data) => {
            if (this.options.debugMode) {
                console.log('News received:', data);
            }

            this._triggerEvent('news', data);
        });

        // Consciousness update received
        socket.on('consciousness', (data) => {
            if (this.options.debugMode) {
                console.log('Consciousness update received:', data);
            }

            this.options.consciousnessLevel = data.new_level;
            this._triggerEvent('consciousness', data);
        });

        // Divine message received
        socket.on('divine_message', (data) => {
            if (this.options.debugMode) {
                console.log('Divine message received:', data);
            }

            this._triggerEvent('divine_message', data);
        });

        // Error message received
        socket.on('error', (data) => {
            if (this.options.debugMode) {
                console.error('Server error received:', data);
            }

            this._triggerEvent('error', data);
        });
    }

    /**
     * Attempt to reconnect to the server
     * @private
     */
    _attemptReconnect() {
        if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
            if (this.options.debugMode) {
                console.log('Maximum reconnection attempts reached');
            }
            return;
        }

        this.reconnectAttempts++;

        if (this.options.debugMode) {
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.options.maxReconnectAttempts})...`);
        }

        setTimeout(() => {
            this.connect();
        }, this.options.reconnectInterval);
    }

    /**
     * Trigger an event to all registered handlers
     * @param {string} event - Event name
     * @param {object} data - Event data
     * @private
     */
    _triggerEvent(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`Error in ${event} event handler:`, error);
                }
            });
        }
    }

    /**
     * Get the default socket URL
     */
    _getDefaultSocketUrl() {
        return window.location.protocol === 'https:'
            ? `wss://${window.location.host}/ws`
            : `ws://${window.location.host}/ws`;
    }

    /**
     * Get the fallback socket URL
     */
    _getFallbackSocketUrl() {
        return window.location.protocol === 'https:'
            ? `wss://${window.location.host}/ws/fallback`
            : `ws://${window.location.host}/ws/fallback`;
    }
}

// Make the class available globally
window.MatrixNewsSocket = MatrixNewsSocket; 