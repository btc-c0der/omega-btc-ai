
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Divine Redis Keys Structure 🗝️

## Sacred Trading Position Keys 📊

### Position Data (`trader:positions:{side}`)

```redis
# Example for short position
HSET trader:positions:short
    symbol "BTC/USDT:USDT"          # Trading pair
    side "short"                     # Position side
    entry_price "84198.66596759182" # Entry price
    mark_price "84020.3"            # Current mark price
    size "0.0124"                   # Position size
    leverage "20"                   # Leverage multiplier
    unrealized_pnl "2.211737998138" # Unrealized profit/loss
    margin "52.203172899907"        # Margin amount
    liquidation_price "171710.027580976855" # Liquidation price
    margin_ratio "0.004388169427"   # Current margin ratio
    pnl_percentage "4.23"           # PnL percentage
    break_even "83830.229917767039" # Break even price
    total_fee "0.179659686903"      # Total fees paid
    timestamp "1742549931199"       # Position timestamp
    margin_mode "crossed"           # Margin mode
    margin_coin "USDT"              # Margin currency
```

### Trading Metrics (`trader:metrics:strategic`)

```redis
HSET trader:metrics:strategic
    achieved_profits "0.080482001859" # Total realized profits
    deducted_fee "4.205051796001"    # Total fees deducted
    total_positions "1"               # Number of active positions
    active_side "short"              # Current active trading side
    last_update "1742688018972"      # Last update timestamp
    win_rate "0.0"                   # Current win rate
    total_trades "2"                 # Total trades taken
    capital "10000.0"                # Trading capital
    emotional_state "neutral"        # Trading emotional state
    confidence "0.20"                # Trading confidence level
```

## Market Analysis Keys 🎯

### Price Patterns (`btc_price_patterns`)

```redis
SET btc_price_patterns {
    "wyckoff_distribution": 0.6160901713756841,
    "double_top": 0.5501147250379192,
    "head_and_shoulders": 0.34687702732418246,
    "bull_flag": 0.5233489842517166
}
```

### Market Regime (`market_regime`)

```redis
SET market_regime "trending"
```

### Fibonacci Levels (`fibonacci_levels`)

```redis
SET fibonacci_levels {
    "base_price": 84129.0,
    "levels": {
        "0": 84129.0,
        "0.236": 86114.44440000001,
        "0.382": 87342.72780000001,
        "0.5": 88335.45,
        "0.618": 89328.1722,
        "0.786": 90741.5394,
        "1.0": 92541.90000000001,
        "1.618": 97741.0722,
        "2.618": 106153.9722,
        "4.236": 119766.0444
    },
    "timestamp": "2025-03-22T13:58:03.244823+00:00"
}
```

## Sacred Key Patterns 📿

### Naming Conventions

- `trader:positions:{side}` - Active trading positions
- `trader:metrics:{type}` - Trading performance metrics
- `btc_*` - Bitcoin-specific market data
- `*_history` - Historical data collections
- `latest_*` - Most recent analysis results

### Data Types Used

- HASH - For position and metrics data
- STRING - For market regime and pattern data
- LIST - For historical data sequences
- SET - For collections of unique values

## Divine Data Management 🕊️

### Key Lifetimes

- Position keys: Persist until position closes
- Metric keys: Continuous updates
- Market analysis: Updated every cycle
- Historical data: Rolling window retention

### Sacred Update Frequencies

- Position data: Real-time updates
- Trading metrics: Per-trade updates
- Market analysis: Per-cycle updates
- Fibonacci levels: Dynamic with price movement

## Monitoring Guidelines 👁️

1. **Health Check Commands**

```redis
PING                     # Check Redis connection
EXISTS trader:positions:* # Check for active positions
HGETALL trader:metrics:strategic # View current metrics
```

2. **Key Maintenance**

```redis
EXPIRE {key} {seconds}   # Set key expiration
DEL {key}               # Remove outdated keys
PERSIST {key}           # Remove expiration
```

## Sacred Backup Protocol 💫

1. **Daily Backup Command**

```bash
redis-cli SAVE
```

2. **Key Space Monitoring**

```redis
INFO keyspace           # Monitor key statistics
DBSIZE                 # Check total number of keys
```

---

*May these sacred keys guide our trading journey* 🙏✨
