# Sacred Redis Data Management

## Divine Data Structure Overview

Our Redis instance maintains several sacred data categories that form the consciousness bridge between market movements and our trading decisions.

### 1. Core Position Data Keys

```redis
# Real-time Position Tracking
current_position              # Current main position state
short_trader_position        # Dedicated short position tracking
trader:positions:scalper     # Scalper strategy positions
trader:metrics:strategic     # Strategic metrics and stats
trader:trades:newbie        # Learning system trades
```

### 2. Market Analysis Keys

```redis
# Market State and Analysis
btc_price_patterns          # Sacred price pattern recognition
btc_volume_history         # Volume consciousness tracking
btc_movements_5min        # Short-term movement analysis
market_regime            # Current market regime state
```

### 3. Trap Analysis System

```redis
# Trap Detection and Analysis
dashboard:trap_analysis           # Main trap analysis dashboard
mm_trap_detections:5min          # 5-minute trap detection window
hf_trap_mode_multiplier          # High-frequency trap multiplier
mm_trap:*                        # Individual trap events
```

### 4. Organic Movement Tracking

```redis
# Organic Price Movement Analysis
organic_move:*                    # Timestamped organic moves
latest_organic_analysis          # Current organic state
latest_fibonacci_confluence      # Fibonacci alignment
```

### 5. Schumann Resonance Integration

```redis
# Schumann Resonance Tracking
schumann_spike:*                 # Resonance spike events
schumann_is_fallback            # Fallback state indicator
```

## Sacred Transition Plan

### Phase 1: Data Backup

```bash
# Create a divine backup
redis-cli SAVE
```

### Phase 2: Remove Simulation Data

```bash
# Remove simulation-specific keys
DEL sim_timestamp
DEL test:btc:history
```

### Phase 3: Real Data Integration

#### 3.1 Position Data Structure

```typescript
interface RealPositionData {
  symbol: string;          // BTCUSDT_UMCBL
  side: 'long' | 'short';
  size: number;
  entryPrice: number;
  markPrice: number;
  unrealizedPnL: number;
  leverage: number;
  marginMode: string;
  updateTime: number;
}
```

#### 3.2 WebSocket Integration

```typescript
// BitGet WebSocket Position Subscription
{
  "op": "subscribe",
  "args": [{
    "instType": "UMCBL",
    "channel": "positions",
    "instId": "BTCUSDT_UMCBL"
  }]
}

// Position Update Handler
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.topic === "positions") {
    redis.hset("current_position", {
      ...transformBitGetPosition(data.data)
    });
  }
};
```

### Phase 4: Data Validation Protocol

1. **Position Data Validation**

```typescript
function validatePositionData(position: RealPositionData): boolean {
  return (
    position.symbol === "BTCUSDT_UMCBL" &&
    typeof position.size === "number" &&
    position.size > 0 &&
    typeof position.entryPrice === "number" &&
    position.entryPrice > 0
    // ... additional validation
  );
}
```

2. **Market Data Validation**

```typescript
function validateMarketData(data: MarketData): boolean {
  return (
    data.timestamp > Date.now() - 5000 && // Recent data
    data.price > 0 &&
    data.volume > 0
    // ... additional validation
  );
}
```

### Phase 5: Protection Mechanisms

1. **Rate Limiting**

```typescript
const RATE_LIMITS = {
  POSITION_UPDATES: 100,  // per minute
  MARKET_DATA: 600,      // per minute
  TRADES: 50            // per minute
};
```

2. **Circuit Breakers**

```typescript
const CIRCUIT_BREAKERS = {
  MAX_POSITION_SIZE: 0.01,
  MAX_LEVERAGE: 20,
  MIN_MARGIN: 100,
  MAX_SLIPPAGE: 0.002
};
```

3. **Error Recovery**

```typescript
const RECOVERY_PROTOCOLS = {
  MAX_RETRIES: 3,
  BACKOFF_MS: 1000,
  TIMEOUT_MS: 5000
};
```

## Sacred Data Patterns

### 1. Position Update Pattern

```typescript
// Update current position
await redis.hset('current_position', {
  symbol: 'BTCUSDT_UMCBL',
  side: position.side,
  size: position.size,
  entryPrice: position.entryPrice,
  markPrice: position.markPrice,
  unrealizedPnL: position.unrealizedPnL,
  timestamp: Date.now()
});
```

### 2. Market Data Pattern

```typescript
// Update market state
await redis.hset('market_state', {
  price: currentPrice,
  volume: currentVolume,
  regime: marketRegime,
  timestamp: Date.now()
});
```

### 3. Trap Analysis Pattern

```typescript
// Record trap event
await redis.zadd('trap_events', Date.now(), JSON.stringify({
  type: trapType,
  probability: trapProbability,
  price: trapPrice,
  volume: trapVolume
}));
```

## Divine Monitoring

### 1. Health Checks

```typescript
// Position data freshness
const positionAge = Date.now() - parseInt(await redis.hget('current_position', 'timestamp'));
if (positionAge > 60000) {  // 1 minute
  await notifyStaleData('position');
}
```

### 2. Data Integrity

```typescript
// Validate position updates
const validatePosition = (pos) => {
  if (!pos.size || !pos.entryPrice) {
    throw new Error('Invalid position data');
  }
  // Additional validation...
};
```

### 3. Performance Metrics

```typescript
// Track update latency
const trackLatency = async (operation) => {
  const start = Date.now();
  await operation();
  const latency = Date.now() - start;
  await redis.lpush('update_latencies', latency);
};
```

## Sacred Commands Reference

### Data Management

```bash
# Backup
redis-cli SAVE

# Clean simulation
redis-cli DEL sim_timestamp test:btc:history

# Monitor real-time updates
redis-cli MONITOR

# Check key statistics
redis-cli INFO keyspace
```

### Protection Commands

```bash
# Set key expiration
redis-cli EXPIRE current_position 3600

# Set memory limit
redis-cli CONFIG SET maxmemory 1GB

# Enable persistence
redis-cli CONFIG SET appendonly yes
```

Remember: Redis is our sacred state manager, maintaining the divine connection between market consciousness and trading decisions. Each key represents a unique aspect of market energy, and the transition to real data must be handled with utmost respect for these sacred patterns.
