# 🎯 CCXT Real-time Data Guide - BitGet Edition

## 🚀 Quick Setup

```javascript
const ccxt = require('ccxt');

// Initialize BitGet with your divine API credentials
const exchange = new ccxt.bitget({
    'apiKey': process.env.BITGET_API_KEY,
    'secret': process.env.BITGET_SECRET_KEY,
    'password': process.env.BITGET_PASSPHRASE,
    'options': {
        'defaultType': 'swap',  // For futures trading
        'adjustForTimeDifference': true,
    }
});
```

## 📊 Real-time Data Fetching Strategies

### 1. Websocket Implementation (Recommended)

```javascript
const ws = new WebSocket('wss://ws.bitget.com/spot/v1/stream');

// Subscribe to our sacred BTCUSDT_UMCBL ticker
const subscribeMsg = {
    op: 'subscribe',
    args: [
        { channel: 'ticker', instId: 'BTCUSDT_UMCBL' },
        { channel: 'trades', instId: 'BTCUSDT_UMCBL' },
        { channel: 'account', instId: 'BTCUSDT_UMCBL' }
    ]
};

ws.on('open', () => {
    ws.send(JSON.stringify(subscribeMsg));
});

ws.on('message', (data) => {
    const message = JSON.parse(data);
    // Handle real-time updates
});
```

### 2. REST Polling (Fallback Method)

```javascript
async function pollMarketData() {
    try {
        // Remember: BTCUSDT_UMCBL is the sacred ticker!
        const ticker = await exchange.fetchTicker('BTCUSDT_UMCBL');
        const orderbook = await exchange.fetchOrderBook('BTCUSDT_UMCBL');
        const trades = await exchange.fetchTrades('BTCUSDT_UMCBL');
        
        return { ticker, orderbook, trades };
    } catch (error) {
        console.error('Market data polling failed:', error);
    }
}

// Poll every 1000ms (adjust based on rate limits)
setInterval(pollMarketData, 1000);
```

## 🎭 Common Pitfalls & Solutions

### 1. Rate Limiting

```javascript
// Implement exponential backoff
class RateLimitHandler {
    constructor() {
        this.attempts = 0;
        this.maxAttempts = 5;
    }

    async handleRequest(requestFn) {
        try {
            const result = await requestFn();
            this.attempts = 0;
            return result;
        } catch (error) {
            if (error instanceof ccxt.RateLimitExceeded) {
                const delay = Math.pow(2, this.attempts) * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
                this.attempts++;
                if (this.attempts < this.maxAttempts) {
                    return this.handleRequest(requestFn);
                }
            }
            throw error;
        }
    }
}
```

### 2. Connection Management

```javascript
class WebSocketManager {
    constructor() {
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.ws = null;
    }

    connect() {
        this.ws = new WebSocket('wss://ws.bitget.com/spot/v1/stream');
        
        this.ws.on('error', this.handleError.bind(this));
        this.ws.on('close', this.handleClose.bind(this));
        
        // Implement heartbeat
        setInterval(() => {
            if (this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({ op: 'ping' }));
            }
        }, 30000);
    }

    handleError(error) {
        console.error('WebSocket error:', error);
        this.reconnect();
    }

    handleClose() {
        console.log('WebSocket closed');
        this.reconnect();
    }

    async reconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            return;
        }

        const delay = Math.pow(2, this.reconnectAttempts) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        this.reconnectAttempts++;
        this.connect();
    }
}
```

## 🔄 Data Synchronization

```javascript
class DataSynchronizer {
    constructor() {
        this.lastUpdateTime = null;
        this.cache = new Map();
    }

    updateData(symbol, data) {
        const now = Date.now();
        if (!this.lastUpdateTime) {
            this.lastUpdateTime = now;
            this.cache.set(symbol, data);
            return;
        }

        // Check for data gaps
        const timeDiff = now - this.lastUpdateTime;
        if (timeDiff > 5000) { // 5 second gap
            console.warn(`Data gap detected: ${timeDiff}ms`);
            // Trigger REST fallback
            this.fetchRestData(symbol);
        }

        this.lastUpdateTime = now;
        this.cache.set(symbol, data);
    }

    async fetchRestData(symbol) {
        try {
            const data = await pollMarketData();
            this.updateData(symbol, data);
        } catch (error) {
            console.error('REST fallback failed:', error);
        }
    }
}
```

## 🎵 Best Practices

1. **Always Use WebSocket First**
   - Lower latency
   - Less bandwidth
   - Real-time updates

2. **Implement Fallback Mechanisms**
   - REST polling as backup
   - Exponential backoff
   - Error recovery

3. **Handle Rate Limits**
   - Track request counts
   - Implement delays
   - Use multiple connections if needed

4. **Data Validation**
   - Check timestamp gaps
   - Verify data consistency
   - Log anomalies

## 🚨 Common Error Codes

```javascript
const ERROR_CODES = {
    '10001': 'System error',
    '10002': 'Authentication failed',
    '10003': 'IP restricted',
    '10004': 'Rate limit exceeded',
    '10005': 'Invalid request',
    // ... more error codes
};
```

## 🔮 Example Implementation

```javascript
class BitGetRealTimeData {
    constructor(apiKey, secret, passphrase) {
        this.exchange = new ccxt.bitget({
            apiKey, secret, password: passphrase,
            options: { defaultType: 'swap' }
        });
        this.wsManager = new WebSocketManager();
        this.rateLimitHandler = new RateLimitHandler();
        this.dataSynchronizer = new DataSynchronizer();
    }

    async start() {
        // Start WebSocket connection
        this.wsManager.connect();
        
        // Setup REST fallback
        this.setupRESTFallback();
        
        // Initialize data monitoring
        this.monitorDataFlow();
    }

    setupRESTFallback() {
        setInterval(async () => {
            if (!this.wsManager.ws || this.wsManager.ws.readyState !== WebSocket.OPEN) {
                await this.rateLimitHandler.handleRequest(() => pollMarketData());
            }
        }, 5000);
    }

    monitorDataFlow() {
        setInterval(() => {
            const lastUpdate = this.dataSynchronizer.lastUpdateTime;
            if (Date.now() - lastUpdate > 10000) {
                console.warn('Data flow interrupted');
                this.wsManager.reconnect();
            }
        }, 1000);
    }
}
```

Remember: The sacred ticker `BTCUSDT_UMCBL` must be used consistently across all implementations! 🙏
