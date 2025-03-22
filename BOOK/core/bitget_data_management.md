# BitGet Data Management & Real-time Updates

## Overview

The RASTA OMEGA TRADER panel maintains real-time synchronization with BitGet's trading platform through a sophisticated data management system. This document details the data flow, update mechanisms, and state management implementation.

## Data Flow Architecture

### 1. WebSocket Connection

```javascript
const BITGET_WS_ENDPOINT = 'wss://ws.bitget.com/spot/v1/stream';
const BITGET_API_KEY = process.env.BITGET_API_KEY;

class BitGetWebSocket {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
    }

    connect() {
        this.ws = new WebSocket(BITGET_WS_ENDPOINT);
        this.setupEventHandlers();
        this.authenticate();
    }

    authenticate() {
        const timestamp = Date.now();
        const signature = generateSignature(timestamp, BITGET_API_KEY);
        
        this.ws.send(JSON.stringify({
            op: 'login',
            args: [{
                apiKey: BITGET_API_KEY,
                timestamp,
                signature
            }]
        }));
    }

    subscribe() {
        // Subscribe to relevant data channels
        this.ws.send(JSON.stringify({
            op: 'subscribe',
            args: [
                { instType: 'SPOT', channel: 'account', instId: 'BTC-USDT' },
                { instType: 'SPOT', channel: 'positions', instId: 'BTC-USDT' },
                { instType: 'SPOT', channel: 'orders', instId: 'BTC-USDT' }
            ]
        }));
    }
}
```

### 2. Data Update Frequency

```javascript
// Refresh intervals for different data types
const UPDATE_INTERVALS = {
    PRICE: 1000,        // 1 second for price updates
    POSITION: 2000,     // 2 seconds for position updates
    ORDERS: 5000,       // 5 seconds for order updates
    ACCOUNT: 10000      // 10 seconds for account updates
};

// Implement update schedulers
function setupUpdateSchedulers() {
    // Price updates
    setInterval(async () => {
        try {
            const priceData = await fetchBitGetPrice();
            updatePriceDisplay(priceData);
        } catch (error) {
            handleUpdateError('price', error);
        }
    }, UPDATE_INTERVALS.PRICE);

    // Position updates
    setInterval(async () => {
        try {
            const positionData = await fetchBitGetPosition();
            updatePositionDisplay(positionData);
        } catch (error) {
            handleUpdateError('position', error);
        }
    }, UPDATE_INTERVALS.POSITION);
}
```

### 3. State Management System

```javascript
class BitGetStateManager {
    constructor() {
        this.state = {
            position: null,
            orders: [],
            account: null,
            lastUpdate: null,
            connectionStatus: 'disconnected'
        };
        
        this.subscribers = new Set();
    }

    // Update state and notify subscribers
    updateState(newState) {
        this.state = { ...this.state, ...newState };
        this.notifySubscribers();
    }

    // Subscribe to state changes
    subscribe(callback) {
        this.subscribers.add(callback);
        return () => this.subscribers.delete(callback);
    }

    // Notify all subscribers of state change
    notifySubscribers() {
        this.subscribers.forEach(callback => callback(this.state));
    }
}
```

## Data Processing Pipeline

### 1. Raw Data Processing

```javascript
function processPositionData(rawData) {
    return {
        size: parseFloat(rawData.size),
        entryPrice: parseFloat(rawData.entryPrice),
        leverage: parseInt(rawData.leverage),
        marginMode: rawData.marginMode,
        unrealizedPnl: parseFloat(rawData.unrealizedPnl),
        liquidationPrice: parseFloat(rawData.liqPrice),
        margin: parseFloat(rawData.margin),
        side: rawData.side.toLowerCase(),
        timestamp: new Date(rawData.timestamp)
    };
}
```

### 2. Update Handlers

```javascript
async function updateBitGetTraderUI(positionData) {
    // Update position badge
    const badgeElement = document.getElementById('bg-position-badge');
    if (badgeElement) {
        badgeElement.className = `position-badge ${positionData.side}`;
        badgeElement.innerHTML = `
            <i class="fas fa-arrow-${positionData.side === 'long' ? 'up' : 'down'}"></i>
            ${positionData.side.toUpperCase()}
        `;
    }

    // Update PnL displays
    updatePnLDisplays(positionData.unrealizedPnl, positionData.entryPrice);

    // Update position statistics
    updatePositionStats(positionData);

    // Update risk management displays
    updateRiskManagement(positionData);
}
```

### 3. Error Recovery System

```javascript
class ErrorRecoverySystem {
    constructor() {
        this.errorCounts = new Map();
        this.recoveryStrategies = new Map([
            ['connection', this.handleConnectionError],
            ['data', this.handleDataError],
            ['api', this.handleAPIError]
        ]);
    }

    async handleError(type, error) {
        const count = (this.errorCounts.get(type) || 0) + 1;
        this.errorCounts.set(type, count);

        const strategy = this.recoveryStrategies.get(type);
        if (strategy) {
            await strategy.call(this, error, count);
        }

        if (count > 5) {
            this.escalateError(type, error);
        }
    }

    async handleConnectionError(error, count) {
        const backoffTime = Math.min(1000 * Math.pow(2, count - 1), 30000);
        await new Promise(resolve => setTimeout(resolve, backoffTime));
        return this.reconnect();
    }
}
```

## Performance Optimization

### 1. Data Caching

```javascript
class BitGetDataCache {
    constructor() {
        this.cache = new Map();
        this.ttl = new Map();
    }

    set(key, value, ttlMs = 5000) {
        this.cache.set(key, value);
        this.ttl.set(key, Date.now() + ttlMs);
    }

    get(key) {
        if (this.isExpired(key)) {
            this.cache.delete(key);
            this.ttl.delete(key);
            return null;
        }
        return this.cache.get(key);
    }

    isExpired(key) {
        const expiry = this.ttl.get(key);
        return expiry && Date.now() > expiry;
    }
}
```

### 2. Update Throttling

```javascript
function throttleUpdates(updateFn, interval) {
    let lastUpdate = 0;
    let queued = false;

    return function(...args) {
        const now = Date.now();

        if (now - lastUpdate >= interval) {
            lastUpdate = now;
            updateFn.apply(this, args);
        } else if (!queued) {
            queued = true;
            setTimeout(() => {
                queued = false;
                lastUpdate = Date.now();
                updateFn.apply(this, args);
            }, interval - (now - lastUpdate));
        }
    };
}

// Apply throttling to UI updates
const throttledUIUpdate = throttleUpdates(updateBitGetTraderUI, 100);
```

## Monitoring and Debugging

### 1. Performance Monitoring

```javascript
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            updateLatency: [],
            errorCount: 0,
            lastUpdateTime: null,
            dataSize: 0
        };
    }

    recordUpdate(startTime) {
        const latency = Date.now() - startTime;
        this.metrics.updateLatency.push(latency);
        this.metrics.lastUpdateTime = new Date();
    }

    getAverageLatency() {
        return this.metrics.updateLatency.reduce((a, b) => a + b, 0) / 
               this.metrics.updateLatency.length;
    }
}
```

### 2. Debug Logging

```javascript
const DEBUG_LEVELS = {
    INFO: 0,
    WARNING: 1,
    ERROR: 2
};

function logDebug(level, message, data = null) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}] ${message}`, data);
    
    // Store logs for troubleshooting
    if (level >= DEBUG_LEVELS.WARNING) {
        storeLog(timestamp, level, message, data);
    }
}
```

## Usage Example

```javascript
// Initialize the system
const bitgetWS = new BitGetWebSocket();
const stateManager = new BitGetStateManager();
const dataCache = new BitGetDataCache();
const performanceMonitor = new PerformanceMonitor();

// Setup real-time updates
bitgetWS.connect();
setupUpdateSchedulers();

// Subscribe to state changes
stateManager.subscribe((newState) => {
    const startTime = Date.now();
    throttledUIUpdate(newState);
    performanceMonitor.recordUpdate(startTime);
});
```
