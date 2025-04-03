# Omega Bot Farm - Trading Bots

This directory contains the trading bot implementations for the Omega Bot Farm. The bots are designed to be run as containerized applications in a Kubernetes environment or locally for development.

## Available Bots

- **CCXT Strategic Trader**: A strategic trading bot that connects to cryptocurrency exchanges via CCXT.

## Running Bots

### Prerequisites

- Python 3.9+
- Required packages (see `requirements.txt` in project root)
- Trading exchange API credentials (BitGet by default)

### Configuration

Bots can be configured through environment variables or `.env` file in the project root. Important configuration options:

```
# BitGet API Credentials
BITGET_API_KEY=your_api_key
BITGET_SECRET_KEY=your_secret_key
BITGET_PASSPHRASE=your_passphrase

# Trading Parameters
SYMBOL=BTCUSDT
TRADING_SYMBOL=BTCUSDT_UMCBL
INITIAL_CAPITAL=24.0
POSITION_SIZE_PERCENT=1.0 
STOP_LOSS_PERCENT=1.0
TAKE_PROFIT_MULTIPLIER=2.0
MAX_LEVERAGE=20
USE_TESTNET=true

# Redis (for bot communication)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Running Locally

You can run bots directly from the command line:

```bash
# Navigate to project root
cd /path/to/omega-btc-ai

# Run CCXT Strategic Trader
python -m src.omega_bot_farm.trading.bots --bot ccxt_strategic --symbol BTCUSDT --interval 60
```

### Command-line Options

- `--bot`: Bot type to run (`ccxt_strategic`, `aggressive`, `cosmic`, `scalper`)
- `--symbol`: Trading symbol (default from env or "BTCUSDT")
- `--interval`: Trading cycle interval in seconds (default 60)
- `--exchange`: Exchange ID to use (default "bitget")

## CCXT Strategic Trader

The CCXT Strategic Trader (`CCXTStrategicTraderB0t`) combines strategic trading approach with live exchange connectivity through CCXT for real trading operations.

### Features

- Connects to 120+ cryptocurrency exchanges through CCXT
- Implements strategic trading psychology with trend analysis
- Supports stop-loss and take-profit mechanisms
- Connects to Redis for inter-bot communication
- Can be deployed in Kubernetes

### Trading Strategy

The CCXT Strategic Trader uses the following approach:

1. **Trend Analysis**: Identifies market trends using multiple time frames
2. **Pattern Recognition**: Looks for specific patterns like higher lows in uptrends
3. **Confirmation**: Requires strong trend confirmation before entering trades
4. **Risk Management**: Uses stop-loss, take-profit, and position sizing
5. **Emotional State**: Factors in the bot's "emotional state" for decision making

### Exit Conditions

The bot will exit positions when:

- Stop-loss is triggered (configurable percent loss)
- Take-profit target is reached (configurable multiplier of stop-loss)
- Market trend reverses against the position

## Architecture

The bots utilize the following components:

- `trading_analyzer_b0t.py`: Market analysis tools
- `trader_base_b0t.py`: Base trader functionality
- `ccxt_b0t.py`: Exchange connectivity via CCXT
- `redis_client.py`: Inter-bot communication

## Development

### Adding a New Bot

1. Create a new bot class that extends `TraderProfile`
2. Implement required methods like `update_market_data` and `should_enter_trade`
3. Add the bot type to the `__main__.py` command-line options
4. Create a Kubernetes deployment file in `kubernetes/deployments/`

### Running Tests

```bash
# From project root
pytest src/omega_bot_farm/tests/trading/bots/
```

## Kubernetes Deployment

See `kubernetes/deployments/ccxt-strategic-trader.yaml` for an example deployment configuration.

## License

This project is licensed under the MIT License.
