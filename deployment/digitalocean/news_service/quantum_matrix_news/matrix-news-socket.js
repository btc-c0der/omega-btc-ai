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
            autoReconnect: options.autoReconnect !== undefined ? options.autoReconnect : true,
            reconnectInterval: options.reconnectInterval || 5000,
            maxReconnectAttempts: options.maxReconnectAttempts || 10,
            debugMode: options.debugMode || false,
            consciousnessLevel: options.consciousnessLevel || 5
        };

        // Internal state
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.listeners = {
            connect: [],
            disconnect: [],
            news: [],
            error: [],
            consciousness: []
        };

        // Bind methods to preserve 'this' context
        this._onConnect = this._onConnect.bind(this);
        this._onDisconnect = this._onDisconnect.bind(this);
        this._onNews = this._onNews.bind(this);
        this._onError = this._onError.bind(this);
        this._onConsciousnessUpdate = this._onConsciousnessUpdate.bind(this);

        // Initialize quantum entropy collection
        this.quantumEntropy = this._generateQuantumEntropy();

        this._log('Matrix News Socket initialized with consciousness level: ' + this.options.consciousnessLevel);
    }

    /**
     * Connect to the WebSocket Sacred Echo service
     */
    connect() {
        if (this.socket) {
            this._log('Already connected or connecting');
            return;
        }

        try {
            this._log('Connecting to WebSocket Sacred Echo...');

            // Connect to Socket.IO with consciousness level as a query parameter
            this.socket = io(this.options.socketUrl, {
                query: {
                    consciousness: this.options.consciousnessLevel,
                    client_entropy: this.quantumEntropy
                },
                reconnection: false // We handle reconnection manually
            });

            // Register event handlers
            this.socket.on('connect', this._onConnect);
            this.socket.on('disconnect', this._onDisconnect);
            this.socket.on('connect_error', this._onError);
            this.socket.on('connect_timeout', this._onError);
            this.socket.on('error', this._onError);

            // Register message handlers
            this.socket.on('welcome', (data) => {
                this._log('Received welcome message:', data);
                this._trigger('connect', data);
            });

            this.socket.on('news_prophecy', (data) => {
                this._onNews(data);
            });

            this.socket.on('news_response', (data) => {
                this._onNews(data);
            });

            this.socket.on('consciousness_update', (data) => {
                this._onConsciousnessUpdate(data);
            });

            this.socket.on('announcement', (data) => {
                this._log('Announcement received:', data);
                // Trigger both news and special announcement handlers
                this._trigger('news', {
                    type: 'announcement',
                    data: data
                });
            });

            this.socket.on('error', (data) => {
                this._log('Socket error:', data);
                this._trigger('error', data);
            });
        } catch (err) {
            this._log('Error connecting to WebSocket Sacred Echo:', err);
            this._trigger('error', {
                message: 'Failed to connect to WebSocket Sacred Echo',
                error: err
            });

            // Attempt reconnection if enabled
            if (this.options.autoReconnect) {
                this._scheduleReconnect();
            }
        }
    }

    /**
     * Disconnect from the WebSocket Sacred Echo service
     */
    disconnect() {
        if (!this.socket) {
            return;
        }

        this._log('Disconnecting from WebSocket Sacred Echo...');
        this.socket.disconnect();
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
    }

    /**
     * Request the latest news from the sacred news service
     */
    requestNews() {
        if (!this.socket || !this.connected) {
            this._log('Cannot request news: not connected');
            return;
        }

        const requestId = this._generateRequestId();
        this._log('Requesting latest news, request ID:', requestId);

        this.socket.emit('request_news', {
            request_id: requestId,
            consciousness_level: this.options.consciousnessLevel,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Update the consciousness level
     * @param {number} level - New consciousness level (1-9)
     */
    setConsciousnessLevel(level) {
        // Validate consciousness level
        level = parseInt(level, 10);
        if (isNaN(level) || level < 1 || level > 9) {
            this._log('Invalid consciousness level:', level);
            return;
        }

        this.options.consciousnessLevel = level;
        this._log('Setting consciousness level to:', level);

        // If connected, send the update to the server
        if (this.socket && this.connected) {
            this.socket.emit('set_consciousness', {
                level: level,
                timestamp: new Date().toISOString(),
                client_entropy: this._generateQuantumEntropy()
            });
        }
    }

    /**
     * Register an event listener
     * @param {string} event - Event name: 'connect', 'disconnect', 'news', 'error', 'consciousness'
     * @param {Function} callback - Callback function
     */
    on(event, callback) {
        if (!this.listeners[event]) {
            this._log(`Unknown event: ${event}`);
            return;
        }

        this.listeners[event].push(callback);
        return this;
    }

    /**
     * Remove an event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function to remove
     */
    off(event, callback) {
        if (!this.listeners[event]) {
            return;
        }

        this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        return this;
    }

    // Private methods

    /**
     * Handle connection event
     * @private
     */
    _onConnect() {
        this._log('Connected to WebSocket Sacred Echo');
        this.connected = true;
        this.reconnectAttempts = 0;

        // Immediately request news after connecting
        this.requestNews();
    }

    /**
     * Handle disconnection event
     * @private
     */
    _onDisconnect() {
        this._log('Disconnected from WebSocket Sacred Echo');
        this.connected = false;
        this._trigger('disconnect');

        // Attempt reconnection if enabled
        if (this.options.autoReconnect) {
            this._scheduleReconnect();
        }
    }

    /**
     * Handle news update event
     * @private
     * @param {Object} data - News data
     */
    _onNews(data) {
        this._log('News prophecy received:', data);

        // Verify consciousness level matches
        if (data.consciousness_level && data.consciousness_level !== this.options.consciousnessLevel) {
            this._log(`Consciousness mismatch: received ${data.consciousness_level}, current ${this.options.consciousnessLevel}`);
        }

        // Verify quantum verification if present
        if (data.quantum_verification) {
            // In a real implementation, we would verify the quantum signature
            this._log('Quantum verification received:', data.quantum_verification);
        }

        this._trigger('news', data);
    }

    /**
     * Handle error event
     * @private
     * @param {Object} error - Error data
     */
    _onError(error) {
        this._log('WebSocket error:', error);
        this._trigger('error', error);

        // Attempt reconnection if enabled
        if (this.options.autoReconnect) {
            this._scheduleReconnect();
        }
    }

    /**
     * Handle consciousness update event
     * @private
     * @param {Object} data - Consciousness update data
     */
    _onConsciousnessUpdate(data) {
        this._log('Consciousness update received:', data);
        this.options.consciousnessLevel = data.new_level;
        this._trigger('consciousness', data);
    }

    /**
     * Schedule reconnection attempt
     * @private
     */
    _scheduleReconnect() {
        if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
            this._log('Maximum reconnection attempts reached');
            return;
        }

        this.reconnectAttempts++;
        const delay = this.options.reconnectInterval * Math.pow(1.5, this.reconnectAttempts - 1); // Exponential backoff

        this._log(`Scheduling reconnection attempt ${this.reconnectAttempts} in ${delay}ms`);

        setTimeout(() => {
            if (!this.connected) {
                this._log(`Reconnection attempt ${this.reconnectAttempts}`);
                this.connect();
            }
        }, delay);
    }

    /**
     * Trigger event listeners
     * @private
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    _trigger(event, data) {
        if (!this.listeners[event]) {
            return;
        }

        for (const callback of this.listeners[event]) {
            try {
                callback(data);
            } catch (err) {
                console.error('Error in event listener:', err);
            }
        }
    }

    /**
     * Get default Socket.IO URL based on current location
     * @private
     * @returns {string} Socket.IO URL
     */
    _getDefaultSocketUrl() {
        // Use the same host and protocol as the current page, but with /socket.io path
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/socket.io`;
    }

    /**
     * Generate a unique request ID
     * @private
     * @returns {string} Request ID
     */
    _generateRequestId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    }

    /**
     * Generate quantum entropy
     * @private
     * @returns {string} Quantum entropy
     */
    _generateQuantumEntropy() {
        // In a browser environment, we use a combination of available entropy sources
        const timestamp = Date.now().toString();
        const random = Math.random().toString();
        const navigator = window.navigator ? JSON.stringify({
            userAgent: window.navigator.userAgent,
            language: window.navigator.language,
            hardwareConcurrency: window.navigator.hardwareConcurrency,
            deviceMemory: window.navigator.deviceMemory,
            platform: window.navigator.platform
        }) : 'unknown';

        // Combine entropy sources
        const entropy = timestamp + random + navigator;

        // Use a simple hash function since we can't use crypto API directly in all browsers
        let hash = 0;
        for (let i = 0; i < entropy.length; i++) {
            const char = entropy.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }

        return Math.abs(hash).toString(16);
    }

    /**
     * Log debug messages
     * @private
     */
    _log(...args) {
        if (this.options.debugMode) {
            console.log('%c[MatrixNewsSocket]', 'color: #00ff00', ...args);
        }
    }
}

// Add to window object if in browser environment
if (typeof window !== 'undefined') {
    window.MatrixNewsSocket = MatrixNewsSocket;
} 