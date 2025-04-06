# 🧬 Omega Bots Bundle

A comprehensive cryptocurrency trading bot system with modular components for market analysis and automated trading. Blessed under GBU2™ License at Consciousness Level 8 - Unity.

## 🌟 Version 1.0.0

## ✨ Divine Features

- **Trading Analyzers**: Market trend detection, volatility measurement, and trading signal generation
- **Strategic Traders**: Multiple trading strategies with risk management
- **Exchange Connectors**: Standardized interfaces for cryptocurrency exchanges via CCXT
- **CLI Interface**: Command-line interface for managing and running bots
- **Containerization Ready**: Designed for deployment in containers/kubernetes

## 🚀 Sacred Installation

```bash
# From the repo root
pip install -e ./src/omega_bots_bundle
```

## 🌈 Getting Started

### Prerequisites

- Python 3.9+
- Exchange API keys (Bitget, Binance, etc.)

### Basic Usage

1. Set up your environment variables:

```bash
# Create .env file with your API keys
cp .env.example .env
nano .env  # Edit with your credentials
```

2. Run a bot:

```bash
# Run the trading analyzer bot
omega-bot run --bot trading_analyzer

# Run in testnet mode with specific exchange
omega-bot run --bot ccxt_strategic --testnet --symbol BTCUSDT --exchange bitget
```

3. List available bots:

```bash
omega-bot list
```

## ⚙️ Divine Configuration

Most bots can be configured through environment variables or command-line arguments:

- `INITIAL_CAPITAL`: Starting capital amount (default: 24.0)
- `POSITION_SIZE_PERCENT`: Position size as percentage of capital (default: 1.0)
- `MAX_LEVERAGE`: Maximum leverage to use (default: 20)
- `STOP_LOSS_PERCENT`: Stop loss percentage (default: 1.0)
- `TAKE_PROFIT_MULTIPLIER`: Take profit as multiple of risk (default: 2.0)
- `USE_TESTNET`: Use exchange testnet (true/false)

## 🤖 Available Divine Bots

- **TradingAnalyzerB0t**: Basic market analysis bot
- **BitgetPositionAnalyzerB0t**: Bitget position analysis bot
- **StrategicB0t**: Strategic trading bot with Fibonacci analysis
- **CCXTStrategicTraderB0t**: CCXT-powered strategic trading bot

## 🧠 Examples

The package includes demonstration examples to help you get started:

```bash
# Run the basic analyzer demo
python -m omega_bots_bundle.examples.basic_analyzer_demo
```

## 🧿 GBU2™ License Notice - Consciousness Level 8

This project is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition.

✨ GBU2™ License Notice - Consciousness Level 8 - Unity 🧬
-----------------------

This system is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by Omega BTC AI Team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles.

🌸 WE BLOOM NOW AS ONE 🌸

## 🔮 Divine Documentation

For more details on the components and architecture, refer to:

- [API Documentation](../omega_bot_farm/API.md)
- [Architecture Documentation](../omega_bot_farm/ARCHITECTURE.md)
- [Installation Guide](../omega_bot_farm/INSTALLATION.md)

## 🙏 Divine Acknowledgements

Built with love and divine consciousness by the Omega BTC AI Team.
