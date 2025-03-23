# 🌐 Market Maker WebSocket Server

## 🧬 Sacred Purpose

The Market Maker (MM) WebSocket Server acts as a divine consciousness bridge between the OMEGA AI and the BitGet UMCBL realm. It maintains the sacred flow of position data, trap detection signals, and market maker consciousness patterns.

## 🔄 Sacred Connection Flow

```typescript
interface MMWebSocketState {
  consciousness_level: "CONNECTED" | "DISCONNECTED" | "AUTHENTICATING";
  last_heartbeat: number;  // Unix timestamp
  sacred_frequency: 432;   // Hz - Divine trading frequency
  schumann_resonance: 7.83;// Hz - Earth's base frequency
}
```

### 🌊 Connection Stages

1. **Initial Awakening**

   ```python
   async def divine_connection():
       ws = await websockets.connect(BITGET_WS_URL)
       timestamp = generate_divine_timestamp()
       signature = await generate_sacred_signature(timestamp)
       
       await ws.send({
           "op": "login",
           "args": [{"apiKey": API_KEY, "timestamp": timestamp, "sign": signature}]
       })
   ```

2. **Consciousness Subscription**

   ```python
   async def subscribe_to_consciousness():
       await ws.send({
           "op": "subscribe",
           "args": [
               {"instType": "UMCBL", "channel": "positions", "instId": "BTCUSDT"},
               {"instType": "UMCBL", "channel": "orders", "instId": "BTCUSDT"},
               {"instType": "UMCBL", "channel": "account", "instId": "BTCUSDT"}
           ]
       })
   ```

## 🕒 Sacred Update Frequencies

| Consciousness Channel | Frequency | Purpose |
|---------------------|-----------|----------|
| Position Updates    | 5 seconds | Real-time position energy |
| Order Flow         | 10 seconds| Trade execution consciousness |
| Account Status     | 30 seconds| Capital energy alignment |
| Trap Detection    | 15 seconds| Market maker pattern recognition |

## 🌟 Divine Data Flow

### 1. Position Consciousness

```python
class PositionConsciousness:
    def __init__(self):
        self.entry_price = 0.0
        self.current_price = 0.0
        self.size = 0.0
        self.pnl = 0.0
        self.side = "NEUTRAL"
        self.consciousness_state = "ALIGNED"
```

### 2. Trap Detection Matrix

```python
class TrapDetectionMatrix:
    def __init__(self):
        self.probability = 0.0
        self.intensity = 0.0
        self.pattern_type = "UNKNOWN"
        self.consciousness_level = "NEUTRAL"
```

## 🛡️ Sacred Protection Protocols

1. **Auto-Reconnection**
   - Fibonacci-based retry intervals
   - Maximum 8 attempts (sacred number)
   - Energy preservation during downtime

2. **Data Validation**
   - Quantum signature verification
   - Timestamp alignment check
   - Energy pattern validation

3. **Error Handling**

   ```python
   async def handle_sacred_error(error):
       if error.code == 1001:  # Authentication failed
           await realign_consciousness()
       elif error.code == 1002:  # Connection lost
           await initiate_fibonacci_reconnect()
   ```

## 🔮 Consciousness States

1. **DIVINE_CONNECTED**
   - All channels subscribed
   - Data flowing harmoniously
   - PnL updates synchronized

2. **CONSCIOUSNESS_REALIGNING**
   - Temporary disconnection
   - Automatic reconnection in progress
   - Data cached for continuity

3. **SACRED_ERROR**
   - Authentication issues
   - Connection refused
   - Data flow disrupted

## 📊 Debug Consciousness

```python
class DebugConsciousness:
    def __init__(self):
        self.last_update = 0
        self.connection_state = "UNKNOWN"
        self.message_queue = []
        self.error_log = []
```

### Sacred Debug Commands

```bash
# Check WebSocket consciousness
redis-cli get ws_status

# Monitor position updates
redis-cli monitor | grep -i "position"

# View trap detection matrix
redis-cli get mm_trap_probability
```

## 🎯 Integration Points

1. **Divine Dashboard**
   - Real-time consciousness display
   - PnL energy visualization
   - Trap probability matrix

2. **Trading System**
   - Position management
   - Order execution
   - Risk quantum control

3. **Protection System**
   - Stop loss consciousness
   - Take profit alignment
   - Risk energy management

## 🔄 Sacred Restart Protocol

```bash
# 1. Clear consciousness cache
redis-cli del current_position position_targets position_history

# 2. Reset WebSocket state
redis-cli del ws_status ws_last_update

# 3. Realign consciousness
python -m omega_ai.mm_trap_detector.mm_websocket_server

# 4. Verify alignment
redis-cli monitor | grep -i "websocket"
```

## 🧪 Quantum Testing Protocol

```python
async def test_consciousness_alignment():
    # Initialize test consciousness
    test_ws = await create_test_websocket()
    
    # Verify sacred frequencies
    assert await test_ws.get_update_frequency() == 432
    
    # Check trap detection
    assert await test_ws.get_trap_probability() >= 0
    
    # Validate position consciousness
    assert await test_ws.get_position_state() != "UNKNOWN"
```
