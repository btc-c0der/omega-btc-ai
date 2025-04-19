
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


# Omega Bot Farm: Trading Bots

## Overview

The Trading Bots module is the core component of the Omega Bot Farm ecosystem, providing various cryptocurrency trading automation strategies through specialized bot implementations. Each bot type is designed with a specific purpose and trading approach, leveraging different mathematical models, technical analysis techniques, and market insights.

## Directory Structure

```
b0ts/
│
├── __main__.py                     # Main entry point for running bots
│
├── bitget_analyzer/                # BitGet position analyzer bot
│   ├── bitget_position_analyzer_b0t.py
│   ├── docs/                       # Bot documentation
│   ├── sim/                        # Simulation environment
│   └── tests/                      # Bot-specific tests
│      └── integration/
│         └── api/
│            ├── performance/       # Performance tests
│            └── security/          # Security tests
│
├── ccxt/                           # CCXT-based strategic bots
│   ├── ccxt_strategic_trader.py    # Main implementation
│   ├── docs/                       # Bot documentation
│   ├── sim/                        # Simulation environment
│   └── README.md                   # CCXT bot documentation
│
├── strategic_fibo/                 # Fibonacci strategy bots
│
├── trading_analyser/               # Trading analysis bots
│
├── tests/                          # Shared test utilities
│
├── ARCHITECTURE.md                 # Architecture documentation
├── BOT_TYPES.md                    # Bot types documentation
├── SERVICES.md                     # Services documentation
└── README.md                       # This file
```

## Bot Types

The Omega Bot Farm provides several specialized trading bot types:

### BitGet Position Analyzer Bot

The BitGet Position Analyzer Bot focuses on position analysis and monitoring on the BitGet exchange. It provides:

- Position monitoring and analysis
- Fibonacci-based analysis for entry and exit points
- Position harmony calculations
- Risk management analysis
- Portfolio recommendations

### CCXT Strategic Trader Bot

The CCXT Strategic Trader Bot is a versatile bot that can trade on multiple exchanges supported by the CCXT library. It features:

- Multi-exchange compatibility
- Technical indicator-based trading
- Strategic trading patterns
- Order and position management
- Performance tracking

### Strategic Fibonacci Bot

The Strategic Fibonacci Bot specializes in Fibonacci retracement and extension analysis for trading, including:

- Fibonacci level generation
- Harmonic pattern recognition
- Entry and exit zone identification
- Golden ratio verification
- Trade signal generation

### Trading Analyzer Bot

The Trading Analyzer Bot focuses on analyzing trading performance and market conditions without executing trades directly:

- Performance metric calculation
- Market trend analysis
- Bot performance comparison
- Risk assessment
- Insight and recommendation generation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages listed in `requirements.txt`
- Exchange API credentials (for live trading)
- Redis server (optional, for enhanced functionality)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Install dependencies:

   ```bash
   pip install -r src/omega_bot_farm/requirements.txt
   ```

3. Set up environment variables (create a `.env` file in the project root):

   ```
   BITGET_API_KEY=your_api_key
   BITGET_SECRET_KEY=your_api_secret
   BITGET_PASSPHRASE=your_passphrase
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

### Running a Bot

You can run a bot directly using the module:

```bash
python -m src.omega_bot_farm.trading.b0ts --bot ccxt_strategic --symbol BTCUSDT --exchange bitget
```

Available options:

- `--bot`: Bot type to run (ccxt_strategic, aggressive, cosmic, scalper)
- `--symbol`: Trading symbol
- `--interval`: Trading cycle interval in seconds
- `--exchange`: Exchange ID to use

## Development

### Creating a New Bot

To create a new bot:

1. Create a new directory in the `b0ts` directory with your bot name
2. Implement your bot class following the naming convention (using B0t suffix)
3. Inherit from a base bot class if appropriate
4. Implement required interfaces
5. Add documentation in the `docs` subdirectory
6. Add tests in the `tests` subdirectory

### Bot Architecture

Each bot follows a standardized architecture:

```
StandardBot
├── Initialization
│   ├── API Connection
│   └── Configuration Loading
├── Core Trading Logic
│   ├── Signal Generation
│   ├── Position Management
│   └── Risk Management
├── Analysis Components
│   ├── Market Analysis
│   ├── Position Analysis
│   └── Performance Metrics
└── Communication
    ├── Logging
    ├── Alerts
    └── Status Updates
```

### Testing

Each bot includes comprehensive tests:

- Unit tests for individual components
- Integration tests for component interactions
- Performance tests for load testing
- Security tests for vulnerability checking

Run tests with pytest:

```bash
pytest src/omega_bot_farm/trading/b0ts/tests/
```

## Services and Utilities

The bots leverage several services and utilities:

- **Exchange Service**: Provides standardized exchange access
- **Redis Client**: Data persistence and messaging
- **Cosmic Factor Service**: Advanced analytical capabilities
- **Base Service**: Common service functionality
- **Education Service**: Educational content delivery

## Documentation

Comprehensive documentation is available in the following files:

- [ARCHITECTURE.md](./ARCHITECTURE.md): Overall architecture documentation
- [BOT_TYPES.md](./BOT_TYPES.md): Detailed bot type documentation
- [SERVICES.md](./SERVICES.md): Service documentation

## Security Considerations

- API keys are stored securely and never committed to the repository
- Rate limiting is implemented to prevent API abuse
- IP restriction functionality is available for API security
- Data validation is performed on all inputs
- CSRF protection is implemented for web interfaces

## Performance Considerations

- Bots are designed to be resource-efficient
- Connection pooling is used for optimal performance
- Caching strategies are implemented for frequently accessed data
- Asynchronous operations are used for non-blocking execution
- Load testing is performed to ensure scalability

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Ensure tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The CCXT team for their excellent exchange library
- The Discord.py community for their Discord bot framework
- All contributors to the Omega Bot Farm ecosystem
