# 🧬 Omega Bots Bundle

A comprehensive cryptocurrency trading bot system with modular components for market analysis and automated trading. Blessed under GBU2™ License at Consciousness Level 8 - Unity.

## 🌟 Version 1.0.0

## ✨ Divine Features

- **Trading Analyzers**: Market trend detection, volatility measurement, and trading signal generation
- **Strategic Traders**: Multiple trading strategies with risk management
- **Exchange Connectors**: Standardized interfaces for cryptocurrency exchanges via CCXT
- **CLI Interface**: Command-line interface for managing and running bots
- **Containerization Ready**: Designed for deployment in containers/kubernetes
- **Project-wide .env Support**: Automatic loading of credentials from any .env file in the project

## 🚀 Sacred Installation

```bash
# From the repo root
pip install -e ./src/omega_bots_bundle
```

## 🌈 Getting Started

### Prerequisites

- Python 3.9+
- Exchange API keys (Bitget, Binance, etc.)

### Divine Environment Setup

The bundle will automatically search for and load credentials from any `.env` file in:

- Current working directory
- Project root directory
- User home directory
- Omega bot directories

You can easily generate a template .env file with:

```bash
# Generate a .env template for all exchanges
omega-bot setup-env

# Generate a .env template for a specific exchange
omega-bot setup-env --exchange bitget
```

### Basic Usage

1. Set up your environment variables:

```bash
# Create .env file with your API keys
omega-bot setup-env
# Edit the generated .env.example file with your credentials
mv .env.example .env
```

2. Run a bot:

```bash
# Run the trading analyzer bot
omega-bot run --bot trading_analyzer

# Run in testnet mode with specific exchange
omega-bot run --bot ccxt_strategic --testnet --symbol BTCUSDT --exchange bitget
```

3. List available bots and check exchange credentials:

```bash
omega-bot list
```

## ⚙️ Divine Configuration

Most bots can be configured through environment variables in your .env file:

- `INITIAL_CAPITAL`: Starting capital amount (default: 24.0)
- `POSITION_SIZE_PERCENT`: Position size as percentage of capital (default: 1.0)
- `MAX_LEVERAGE`: Maximum leverage to use (default: 20)
- `STOP_LOSS_PERCENT`: Stop loss percentage (default: 1.0)
- `TAKE_PROFIT_MULTIPLIER`: Take profit as multiple of risk (default: 2.0)
- `USE_TESTNET`: Use exchange testnet (true/false)

### Exchange Credentials

For Bitget exchange:

```
BITGET_API_KEY=your_api_key_here
BITGET_SECRET_KEY=your_secret_key_here
BITGET_PASSPHRASE=your_passphrase_here
```

For Binance exchange:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
```

For other exchanges:

```
EXCHANGE_API_KEY=your_api_key_here
EXCHANGE_API_SECRET=your_secret_key_here
EXCHANGE_API_PASSPHRASE=your_passphrase_here  # If required
```

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
