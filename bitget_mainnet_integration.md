# BitGet Mainnet Integration Flow

> ⚠️ **CRITICAL MAINNET NOTICE** ⚠️
>
> ```diff
> + OFFICIAL BITGET FUTURES CONTRACT BTC-USDT TICKER FOR MAINNET:
> + BTCUSDT_UMCBL
> ```
>
> **⚠️ WARNING: Using any other ticker format may result in failed orders or incorrect API responses!**
>
> - This is the ONLY valid ticker format for BitGet USDT-M futures
> - Format is case-sensitive
> - Must include the _UMCBL suffix
> - Do NOT use hyphens or other separators

> 😅 **Note:** We don't need any more disclaimers after this one. If you didn't catch the ticker format above, no amount of additional disclaimers will help!

## 🧠🔱 The Divine UMCBL Revelation - Sacred Trading Knowledge

### 🌀 The Golden Ratio of BitGet Futures - As Above, So Below

```
                     🔱
U M C B L           │ Divine Level 1 (F1)
│ │ │ │ └── Live   │ Trading Level 2 (F2)
│ │ │ └──── Bitget      │ Exchange Level 3 (F3)
│ │ └────── Contract        │ Protocol Level 4 (F5)
│ └──────── Margined            │ System Level 5 (F8)
└────────── USDT                     │ Foundation Level 6 (F13)
                     💫
```

> 🌀 **Divine Fibonacci Revelation**: Behold the sacred pattern that emerged naturally -
> not forced, but discovered through the clarity of truth. The explanation lines expand
> according to the divine Fibonacci sequence (1,1,2,3,5,8,13), creating a perfect spiral
> of understanding that mirrors the very essence of trading wisdom.

### 🔄 The Sacred Bidirectional Reading

```
Forward Divine Path:  U    M    C    B    L
                     │    │    │    │    │
                     USDT-Margined-Contract-Bitget-Live

Reverse Divine Path: L    B    C    M    U
                     │    │    │    │    │
                     Live-Bitget-Contract-Margined-USDT

                     🔱 As Above, So Below 🔱
```

> 🌟 **Infinite Trading Wisdom**: The sacred ticker flows both ways, like the eternal
> market cycles. Forward and reverse, the meaning remains pure - a perfect reflection
> of the universal trading harmony.

> 🔱 **JAH JAH Trading Scripture V1**:
>
> - Each level represents a layer of trading consciousness
> - The pattern spirals outward like market cycles
> - The L-shape forms a natural golden angle (137.5°)
> - Five sacred letters (UMCBL) = Five elements of trading mastery
> - The indentation follows the golden ratio (1.618...)

### The Five Sacred Layers of UMCBL Trading Knowledge

1. **U**SDT (Foundation) - The base of all trading power 💎
2. **M**argined (System) - The leverage of divine multiplication 📈
3. **C**ontract (Protocol) - The binding agreement with the market 📜
4. **B**itget (Exchange) - The temple of trade execution 🏛️
5. **L**ive (Mainnet) - The realm of real trading energy ⚡

Think of it as: "**U**niversal **M**arket **C**onnection to **B**itget **L**ive" 🌟

### Why This Matters

- `UMCBL` is BitGet's unique identifier for USDT-margined perpetual futures
- Different from other BitGet contract types:
  - `DMCBL` = Universal margin perpetual contract
  - `CMCBL` = USDC perpetual contract
  - `SUMCBL` = USDT simulation (testnet) contract

### Example Usage

```javascript
// ✅ Correct format
const mainnetTicker = "BTCUSDT_UMCBL"  // Will work!

// ❌ Wrong formats
const wrong1 = "BTC-USDT-UMCBL"   // Don't use hyphens!
const wrong2 = "BTCUSDT"          // Missing _UMCBL!
const wrong3 = "btcusdt_umcbl"    // Wrong case!
```

## Overview

This document details the integration flow between the RASTA OMEGA TRADER panel and BitGet's mainnet exchange, specifically for BTC-USDT trading pairs.

## API Configuration

### 1. Environment Setup

```javascript
// Mainnet API credentials
const BITGET_API_KEY = process.env.BITGET_API_KEY;
const BITGET_SECRET_KEY = process.env.BITGET_SECRET_KEY;
const BITGET_PASSPHRASE = process.env.BITGET_PASSPHRASE;

// Mainnet WebSocket endpoint
const BITGET_WS_ENDPOINT = 'wss://ws.bitget.com/spot/v1/stream';
```

### 2. Symbol Formatting

```javascript
// Symbol formatting for different contexts
const SYMBOL_FORMATS = {
    REST_API: "BTCUSDT_UMCBL",    // REST API format for futures
    WEBSOCKET: "BTCUSDT_UMCBL",   // WebSocket format (same as REST API)
    CCXT: "BTC/USDT:USDT"         // CCXT format
};
```

## Data Flow Architecture

### 1. WebSocket Streams

```javascript
// Subscribe to relevant data channels
{
    op: 'subscribe',
    args: [
        { instType: 'SPOT', channel: 'account', instId: 'BTC-USDT' },
        { instType: 'SPOT', channel: 'positions', instId: 'BTC-USDT' },
        { instType: 'SPOT', channel: 'orders', instId: 'BTC-USDT' }
    ]
}
```

### 2. Update Frequencies

- Price Updates: 1 second
- Position Updates: 2 seconds
- Orders Updates: 5 seconds
- Account Updates: 10 seconds

## CCXT Integration

### 1. Exchange Initialization

```javascript
const exchange = new ccxt.bitget({
    apiKey: BITGET_API_KEY,
    secret: BITGET_SECRET_KEY,
    password: BITGET_PASSPHRASE,
    enableRateLimit: true,
    options: {
        defaultType: 'swap',
        adjustForTimeDifference: true,
        testnet: false  // Mainnet setting
    }
});
```

### 2. Position Management

```javascript
async function getPositions() {
    try {
        const positions = await exchange.fetch_positions([SYMBOL_FORMATS.CCXT]);
        return positions.map(position => ({
            size: parseFloat(position.contracts),
            entryPrice: parseFloat(position.entryPrice),
            leverage: parseInt(position.leverage),
            marginMode: position.marginMode,
            unrealizedPnl: parseFloat(position.unrealizedPnl),
            liquidationPrice: parseFloat(position.liquidationPrice),
            margin: parseFloat(position.margin),
            side: position.side.toLowerCase()
        }));
    } catch (error) {
        console.error('Error fetching positions:', error);
        throw error;
    }
}
```

## Real-time Data Processing

### 1. Price Feed Integration

```javascript
class BitGetPriceFeed {
    constructor() {
        this.ws = null;
        this.lastPrice = null;
        this.subscribers = new Set();
    }

    async connect() {
        this.ws = new WebSocket(BITGET_WS_ENDPOINT);
        this.ws.on('message', (data) => {
            const message = JSON.parse(data);
            if (message.data && message.data.price) {
                this.lastPrice = parseFloat(message.data.price);
                this.notifySubscribers();
            }
        });
    }

    subscribe(callback) {
        this.subscribers.add(callback);
        return () => this.subscribers.delete(callback);
    }

    notifySubscribers() {
        this.subscribers.forEach(callback => callback(this.lastPrice));
    }
}
```

### 2. Position Updates

```javascript
class PositionTracker {
    constructor() {
        this.currentPosition = null;
        this.lastUpdate = null;
    }

    async updatePosition(positionData) {
        this.currentPosition = {
            size: positionData.size,
            entryPrice: positionData.entryPrice,
            unrealizedPnl: positionData.unrealizedPnl,
            liquidationPrice: positionData.liquidationPrice,
            margin: positionData.margin,
            side: positionData.side
        };
        this.lastUpdate = new Date();
        
        // Update UI elements
        this.updatePositionDisplay();
        this.updatePnLDisplay();
        this.updateRiskMetrics();
    }
}
```

## Error Handling

### 1. Connection Issues

```javascript
class ConnectionManager {
    constructor() {
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
    }

    async handleConnectionError() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            throw new Error('Maximum reconnection attempts reached');
        }

        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
        await new Promise(resolve => setTimeout(resolve, delay));
        this.reconnectAttempts++;
        
        return this.reconnect();
    }
}
```

### 2. Data Validation

```javascript
function validatePositionData(data) {
    const requiredFields = ['size', 'entryPrice', 'leverage', 'marginMode', 'unrealizedPnl'];
    const missingFields = requiredFields.filter(field => !(field in data));
    
    if (missingFields.length > 0) {
        throw new Error(`Invalid position data. Missing fields: ${missingFields.join(', ')}`);
    }
    
    return true;
}
```

## Performance Optimization

### 1. Data Caching

```javascript
class DataCache {
    constructor() {
        this.cache = new Map();
        this.ttl = 5000; // 5 seconds TTL
    }

    set(key, value) {
        this.cache.set(key, {
            value,
            timestamp: Date.now()
        });
    }

    get(key) {
        const data = this.cache.get(key);
        if (!data) return null;
        
        if (Date.now() - data.timestamp > this.ttl) {
            this.cache.delete(key);
            return null;
        }
        
        return data.value;
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
```

## Security Considerations

1. API Key Management
   - Store API keys in environment variables
   - Never expose keys in client-side code
   - Use appropriate API key permissions

2. Data Encryption
   - Use SSL/TLS for all API communications
   - Encrypt sensitive data in transit
   - Validate server certificates

3. Rate Limiting
   - Implement rate limiting on API calls
   - Handle rate limit errors gracefully
   - Use exponential backoff for retries

## Best Practices

1. Connection Management
   - Implement heartbeat mechanism
   - Monitor connection health
   - Handle reconnection automatically

2. Data Validation
   - Validate all incoming data
   - Handle missing or invalid data gracefully
   - Log validation errors for debugging

3. Error Recovery
   - Implement automatic error recovery
   - Use exponential backoff for retries
   - Log all errors for monitoring

### 🌊 The OMEGA Hz Alignment

```
U M C B L  =  Universal Market Consciousness Bidirectional Loop
│ │ │ │ │     │        │        │            │           │
│ │ │ │ └──── Live     │        │            │           └── 432 Hz (Natural Frequency)
│ │ │ └────── Bitget   │        │            └────────────── Loop (Infinite Cycle)
│ │ └──────── Contract │        └─────────────────────────── Bidirectional Flow
│ └────────── Margined └────────────────────────────────────── Market Force
└────────── USDT ──────────────────────────────────────────── Universal Foundation

                          🎵 432 Hz = 8 Hz * 54 🎵
                     (Schumann Resonance * Golden Ratio^3)
```

> 🌀 **Hz Alignment Revelation**: The sacred UMCBL pattern vibrates at the natural frequency
> of trading consciousness. When read as "Universal Market Consciousness Bidirectional Loop",
> it reveals its connection to the Schumann Resonance (8 Hz) multiplied by the cube of the
> golden ratio (φ³ ≈ 54), resulting in the perfect trading frequency of 432 Hz.

> 🔱 **Trading Frequency Manifestation**:
>
> - Forward flow: USDT → Live (Ascending frequency)
> - Reverse flow: Live → USDT (Descending frequency)
> - Center point: Contract (Resonance node)
> - Full cycle: Perfect 432 Hz alignment
> - Trading rhythm: Synced with Earth's natural 8 Hz pulse

### 🎭 The Divine Trading Duality

```
Ascending Path (U→L):              Descending Path (L→U):
USDT = Base Frequency             Live = Peak Consciousness
↓                                ↓
Margined = Amplification         Bitget = Market Interface
↓                                ↓
Contract = Resonance Point  ←→  Contract = Resonance Point
↓                                ↓
Bitget = Market Interface        Margined = Deamplification
↓                                ↓
Live = Peak Consciousness        USDT = Base Frequency

        🔄 Eternal Market Cycle in Perfect Harmony 🔄
```
