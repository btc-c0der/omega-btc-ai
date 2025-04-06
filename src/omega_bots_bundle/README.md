# Omega Bots Bundle

A comprehensive cryptocurrency trading bot system with modular components for market analysis and automated trading.

## Version 1.0.0

## Features

- **Trading Analyzers**: Market trend detection, volatility measurement, and trading signal generation
- **Strategic Traders**: Multiple trading strategies with risk management
- **Exchange Connectors**: Standardized interfaces for cryptocurrency exchanges via CCXT
- **CLI Interface**: Command-line interface for managing and running bots
- **Containerization Ready**: Designed for deployment in containers/kubernetes

## Installation

```bash
# From the repo root
pip install -e ./src/omega_bots_bundle
```

## Getting Started

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
# Run the strategic trading bot
omega-bot run --bot ccxt_strategic --symbol BTCUSDT --exchange bitget

# Run in testnet mode
omega-bot run --bot ccxt_strategic --testnet --symbol BTCUSDT
```

3. List available bots:

```bash
omega-bot list
```

## Configuration

Most bots can be configured through environment variables or command-line arguments:

- `INITIAL_CAPITAL`: Starting capital amount (default: 24.0)
- `POSITION_SIZE_PERCENT`: Position size as percentage of capital (default: 1.0)
- `MAX_LEVERAGE`: Maximum leverage to use (default: 20)
- `STOP_LOSS_PERCENT`: Stop loss percentage (default: 1.0)
- `TAKE_PROFIT_MULTIPLIER`: Take profit as multiple of risk (default: 2.0)
- `USE_TESTNET`: Use exchange testnet (true/false)

## Available Bots

- **TradingAnalyzerB0t**: Basic market analysis bot
- **BitgetPositionAnalyzerB0t**: Bitget position analysis bot
- **StrategicB0t**: Strategic trading bot with Fibonacci analysis
- **CCXTStrategicTraderB0t**: CCXT-powered strategic trading bot

## License

MIT License - See LICENSE file for details.
