
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


# Integrating Cosmic Factors with CCXT Strategic Trader

This guide explains how to integrate the CosmicFactorService with the CCXT Strategic Trader Bot for live trading environments.

## Overview

The CCXT Strategic Trader Bot can now leverage cosmic factors to enhance its trading decisions through the CosmicFactorService. This integration allows you to:

- Enable/disable cosmic influences in live trading
- Configure different weight parameters for each cosmic factor
- Compare trading performance with and without cosmic influences
- Fine-tune cosmic parameters based on market conditions

## Configuration

### Cosmic Factors Configuration File

Create a `cosmic_factors.yaml` file in your configuration directory:

```yaml
# Master switch for all cosmic factors
enabled: true  

# Individual cosmic factors
factors:
  moon_phase:
    enabled: true
    weight: 0.5  # 50% influence

  schumann_resonance:
    enabled: true
    weight: 0.3  # 30% influence

  market_liquidity:
    enabled: true
    weight: 1.0  # 100% influence

  global_sentiment:
    enabled: true
    weight: 0.8  # 80% influence

  mercury_retrograde:
    enabled: false  # Disabled
    weight: 0.0

  geographic_influence:
    enabled: true
    weight: 0.4  # 40% influence

  time_cycle:
    enabled: true
    weight: 0.6  # 60% influence

  circadian_rhythm:
    enabled: true
    weight: 0.5  # 50% influence

# Control which decision parameters can be affected by cosmic factors
application:
  risk_appetite: true
  confidence: true
  insight_level: true
  emotional_intensity: true
  position_size: true
  entry_threshold: true
  exit_impulse: true
```

### Environment Variables

To customize the cosmic factor integration, you can set these environment variables:

```
# Cosmic Factor Configuration
COSMIC_CONFIG_PATH=/path/to/your/cosmic_factors.yaml
TRADER_LATITUDE=40.7128  # New York
TRADER_LONGITUDE=-74.0060

# Trading Bot Configuration
SYMBOL=BTCUSDT
INITIAL_CAPITAL=1000
POSITION_SIZE_PERCENT=2.0
MAX_LEVERAGE=5
```

## Usage

### Initializing the CCXT Strategic Trader with Cosmic Factors

```python
from src.omega_bot_farm.trading.b0ts.ccxt.ccxt_strategic_trader import CCXTStrategicTraderB0t
import os

# Get cosmic config path from environment or use default
cosmic_config_path = os.environ.get("COSMIC_CONFIG_PATH", "config/cosmic_factors.yaml")

# Initialize the trader with cosmic factors
trader = CCXTStrategicTraderB0t(
    initial_capital=1000.0,
    name="Cosmic_CCXT_Trader",
    exchange_id="bitget",
    symbol="BTCUSDT",
    cosmic_config_path=cosmic_config_path
)

# Start the trader
await trader.initialize()
await trader.start_trading(interval_seconds=60)
```

### How Cosmic Factors Affect Trading Decisions

The CCXT Strategic Trader uses cosmic factors in three key decision points:

1. **Entry Decisions**: Cosmic factors can influence the confidence score and entry threshold
2. **Position Sizing**: Cosmic factors can adjust the size of positions based on current conditions
3. **Exit Decisions**: Cosmic factors influence exit impulse and threshold values

#### Example Entry Decision Flow

```
Market Analysis → Calculate Confirmation Score → Create Decision Object → 
Apply Cosmic Factors → Modified Confirmation Score → Trading Decision
```

#### Example Position Sizing Flow

```
Calculate Base Position Size → Create Decision Object → 
Apply Cosmic Factors → Modified Position Size → Execute Trade
```

## Docker Deployment

When deploying your CCXT Strategic Trader in Docker, mount your cosmic configuration file:

```yaml
version: '3'
services:
  ccxt-trader:
    image: omega-bot-farm/ccxt-trader:latest
    container_name: ccxt-cosmic-trader
    volumes:
      - ./config/cosmic_factors.yaml:/app/config/cosmic_factors.yaml
    environment:
      - INITIAL_CAPITAL=1000
      - EXCHANGE_ID=bitget
      - SYMBOL=BTCUSDT
      - BITGET_API_KEY=${BITGET_API_KEY}
      - BITGET_SECRET_KEY=${BITGET_SECRET_KEY}
      - BITGET_PASSPHRASE=${BITGET_PASSPHRASE}
      - USE_TESTNET=true
      - TRADER_LATITUDE=40.7128
      - TRADER_LONGITUDE=-74.0060
```

## Testing and Monitoring

### A/B Testing Cosmic Factors

To compare trading with and without cosmic factors:

1. Run two instances of the trader with same market and exchange settings
2. Enable cosmic factors on one instance and disable on the other
3. Monitor performance metrics between the two instances

### Monitoring Cosmic Influence

The trader's status includes information about cosmic factor service:

```python
status = trader.get_status_dict()
print(f"Cosmic service enabled: {status['cosmic_service_enabled']}")
```

### Logging Cosmic Influences

The trader logs cosmic influence information during operation:

```
INFO:ccxt_strategic_trader:Moon phase influence: 0.23 (waxing crescent)
INFO:ccxt_strategic_trader:Position size adjusted by cosmic factors: 0.01 BTC → 0.0115 BTC
INFO:ccxt_strategic_trader:Entry threshold adjusted by cosmic factors: 0.65 → 0.62
```

## Example Workflow

1. **Configuration**: Create and customize your cosmic_factors.yaml file
2. **Initialization**: Start the CCXT Strategic Trader with the cosmic config
3. **Market Data**: Trader collects market data and adds cosmic conditions
4. **Decision Making**: Trading decisions are influenced by cosmic factors
5. **Execution**: Trades are executed with cosmic-adjusted parameters
6. **Monitoring**: Track performance and adjust cosmic weights as needed

## Benefits in Live Trading

- **Reduced Emotional Bias**: Cosmic factors provide an external reference point for decisions
- **Systematic Approach**: All influences are quantified and configurable
- **Progressive Testing**: Gradually increase or decrease cosmic influence
- **Performance Attribution**: Analyze which cosmic factors contribute to success

## Common Configurations

### Conservative Cosmic Setting

```yaml
enabled: true
factors:
  moon_phase:
    enabled: true
    weight: 0.3  # Low influence
  # Other factors at low weights
```

### Aggressive Cosmic Setting

```yaml
enabled: true
factors:
  moon_phase:
    enabled: true
    weight: 0.9  # High influence
  # Other factors at high weights
```

### Market-Focused Setting

```yaml
enabled: true
factors:
  # Astronomical factors disabled
  moon_phase:
    enabled: false
    weight: 0.0
  mercury_retrograde:
    enabled: false
    weight: 0.0
  
  # Market factors enabled
  market_liquidity:
    enabled: true
    weight: 1.0
  global_sentiment:
    enabled: true
    weight: 1.0
```
