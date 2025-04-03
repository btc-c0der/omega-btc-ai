# Omega Bot Farm

A containerized, Kubernetes-orchestrated trading bot system with Discord integration and cosmic influences.

## Overview

The Omega Bot Farm is a sophisticated trading system that deploys multiple trading bots with distinct psychological profiles and trading strategies. Each bot operates with its own decision-making process, risk tolerance, and emotional responses to market conditions.

The system is deployed in Kubernetes for scalability and resilience, and includes a Discord bot for real-time monitoring and command control.

## Features

- **Multiple Trading Personas**: Strategic, Aggressive, Scalper, Newbie, and Cosmic traders
- **Psychological Modeling**: Bots with emotional states that affect trading decisions
- **CCXT Integration**: Unified interface to 120+ cryptocurrency exchanges
- **Cosmic Influences**: Integration of Schumann resonance, moon phases, and other cosmic factors
- **Discord Integration**: Command and control via Discord with rich data visualization
- **Kubernetes Deployment**: Containerized, scalable architecture
- **Advanced Risk Management**: Sophisticated position sizing and exit strategies

## Architecture

The system consists of several components:

- **Trading Bots**: Independent containers running different trader personas
- **Exchange Connectivity**: CCXT integration for trading on various exchanges
- **Discord Bot**: User interface for monitoring and control
- **Redis**: Message queue for inter-service communication
- **Kubernetes**: Orchestration platform for container management

## Getting Started

### Prerequisites

- Docker
- Kubernetes cluster or minikube
- Redis instance
- Discord Bot Token
- Exchange API credentials
- CCXT library (`pip install ccxt`)

### Installation

1. Configure environment variables:

```bash
export DISCORD_TOKEN=your_discord_token
export EXCHANGE_ID=bitget
export EXCHANGE_API_KEY=your_api_key
export EXCHANGE_API_SECRET=your_api_secret
export EXCHANGE_API_PASSPHRASE=your_passphrase
```

2. Create Kubernetes secrets:

```bash
kubectl create secret generic discord-credentials \
  --from-literal=token=$DISCORD_TOKEN

kubectl create secret generic exchange-credentials \
  --from-literal=api-key=$EXCHANGE_API_KEY \
  --from-literal=api-secret=$EXCHANGE_API_SECRET \
  --from-literal=passphrase=$EXCHANGE_API_PASSPHRASE
```

3. Deploy Redis:

```bash
kubectl apply -f kubernetes/infrastructure/redis.yaml
```

4. Deploy trading bots:

```bash
kubectl apply -f kubernetes/deployments/strategic-trader.yaml
kubectl apply -f kubernetes/deployments/ccxt-strategic-trader.yaml
kubectl apply -f kubernetes/deployments/aggressive-trader.yaml
kubectl apply -f kubernetes/deployments/scalper-trader.yaml
kubectl apply -f kubernetes/deployments/cosmic-trader.yaml
```

5. Deploy Discord bot:

```bash
kubectl apply -f kubernetes/deployments/discord-bot.yaml
```

## Discord Commands

The Discord bot provides several commands for interacting with the trading bots:

- `/farm_status` - Get status of all trading bots in the farm
- `/start <bot_name>` - Start a specific trading bot
- `/stop <bot_name>` - Stop a specific trading bot
- `/stats <bot_name>` - View detailed statistics for a trading bot
- `/cosmic_influence` - View current cosmic influences on trading

## CCXT Integration

The Omega Bot Farm integrates with CCXT (CryptoCurrency eXchange Trading Library) to provide a unified interface for interacting with various cryptocurrency exchanges.

### Supported Exchanges

CCXT supports over 120 cryptocurrency exchanges, including:

- BitGet
- Binance
- Bybit
- OKX
- Kucoin
- FTX

### Exchange Configuration

The trading bots can be configured to work with different exchanges by setting the appropriate environment variables:

```yaml
env:
- name: EXCHANGE_ID
  value: "bitget"  # Can be any CCXT-supported exchange
- name: USE_TESTNET
  value: "true"    # Set to false for live trading
```

For more detailed information, see the [CCXT Integration Documentation](docs/ccxt_integration.md).

## Development

### Building from Source

1. Clone the repository:

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai/src/omega_bot_farm
```

2. Build Docker images:

```bash
docker build -t omega-btc-ai/ccxt-strategic-trader:latest -f docker/trading-bots/Dockerfile .
docker build -t omega-btc-ai/discord-bot:latest -f docker/discord-bot/Dockerfile .
```

### Project Structure

```
omega_bot_farm/
├── discord/               # Discord bot implementation
├── kubernetes/            # Kubernetes deployment configurations
├── trading/               # Trading components
│   ├── bots/              # Bot implementations for different personas
│   ├── core/              # Core trading functionality
│   ├── exchanges/         # Exchange integrations using CCXT
│   └── profiles/          # Trading profiles from existing codebase
├── analytics/             # Analytics and performance tracking
├── docker/                # Dockerfiles for containerization
├── docs/                  # Documentation
├── tests/                 # Test suite
├── config/                # Configuration files
└── utils/                 # Utility functions and helpers
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Built on the foundation of OmegaBTC AI trading components and integrates with CCXT for exchange connectivity.
