
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


# OMEGA BTC AI v1 - Advanced Crypto Trading System

![RASTA QA SHIELD](https://img.shields.io/badge/RASTA%20QA-BLESSED-52b788?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADWSURBVHgBrVNbDsFAFJ1JS3yCn4ifSkRYAR+srsTHd1dhB9iBHaywArEDgxdxkzYz7cykZoL4OMnNzD333HM7twC/QMn7KYKDwkPDQcHASkgI2oFL6OEGAhsMGUFwN6BIovFjpOUdO4eIdPwQMdLJPNZs3YnmrGLFBlPJspth5HxZ5QVqkJG7gK7rDTyfj0iKYzSgeOITDlCDdguKaZqw2+0Tz0GxXdvG8/LKtePIWGJll9AlDV2U0yTb7TSu9xdpsysEGjB37vGKikNEJkPtf+QcZ9pGzn+QvwG14CvkQBnwYgAAAABJRU5ErkJggg==)
[![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen.svg)](https://github.com/yourusername/omega-btc-ai/actions)

## System Overview

OMEGA BTC AI is an advanced cryptocurrency trading system that combines real-time market monitoring, AI-powered pattern recognition, and sophisticated trading strategies. The system specializes in detecting market maker traps (manipulation tactics) and executing optimized trading strategies in response.

### Core Features

- **Market Maker Trap Detection**: Identifies manipulation tactics such as liquidity grabs, stop hunts, and fake breakouts
- **Dual Position Trading**: Simultaneous long and short positions managed by different sub-accounts
- **Elite Exit Strategies**: Sophisticated exit decision-making based on multiple market factors
- **Real-time Monitoring**: WebSocket-based price feeds with sub-second updates
- **BitGet Exchange Integration**: Complete futures trading implementation with sub-account support
- **Advanced Fibonacci Analysis**: Multi-timeframe Fibonacci level calculation and confluence detection
- **Redis-powered Data Flow**: High-performance data synchronization between components

## Architecture

The OMEGA BTC AI system consists of several interacting components:

1. **Data Ingestion**
   - Real-time BTC price data from exchanges
   - Market data stored in Redis for immediate access
   - Historical data persisted to PostgreSQL

2. **Analysis Layer**
   - Market maker trap detection
   - Fibonacci level calculation
   - Pattern recognition
   - Multi-timeframe trend analysis

3. **Trading Layer**
   - BitGet integration for futures trading
   - Dual position traders (long and short)
   - Position management
   - Risk control

4. **Visualization**
   - Real-time performance dashboards
   - Trap pattern visualization
   - Position flow tracking

### Component Organization

The system is organized into multiple Python modules:

- `data_feed/`: Real-time price data ingestion
- `mm_trap_detector/`: Market manipulation detection
- `trading/strategies/`: Trading strategies implementation
- `trading/exchanges/`: Exchange-specific implementations
- `utils/`: Helper functions and utilities
- `alerts/`: Notification system (Telegram, etc.)
- `visualization/`: Data visualization components

## Trap-Aware Dual Position Traders

The flagship component of OMEGA BTC AI is the Trap-Aware Dual Position Traders system, which enhances traditional trading strategies with market maker trap awareness.

### How It Works

1. The system monitors real-time price data and calculates trap probability
2. When potential traps are detected, it adjusts trading parameters accordingly
3. Different trap types trigger different responses:
   - Bull traps → Reduce long risk, increase short risk
   - Bear traps → Reduce short risk, increase long risk
   - Liquidity grabs → Reduce risk on both sides
4. Elite exit strategies determine optimal exit points based on multiple factors

### Trap Types Detected

- **Bull Trap (🐂)**: False breakout above resistance to trap buyers
- **Bear Trap (🐻)**: False breakdown below support to trap sellers  
- **Liquidity Grab (💰)**: Sudden price movement to grab liquidity
- **Stop Hunt (🎯)**: Price pushed to common stop loss levels then reverses
- **Fake Pump (🚀)**: Artificial pump to create FOMO
- **Fake Dump (📉)**: Artificial dump to create panic selling

### Elite Exit Strategy

The system includes sophisticated exit strategies that consider:

1. Fibonacci retracement levels
2. Reversal pattern detection
3. Trap probability signals
4. Market regime analysis
5. Dynamic trailing stops
6. Risk management thresholds

### Balance Management and Account Limits

The system uses improved balance checking logic that:

1. Uses **free balance** (available funds) rather than total balance for account limit checks
2. Properly handles different types of balances reported by BitGet API:
   - **Free Balance**: Funds available for new trades
   - **Used Balance**: Funds locked as margin/collateral
   - **Total Balance**: Includes all above plus unrealized P&L and notional position values
3. Supports setting a minimum free balance requirement with the `--min-free-balance` parameter
4. Provides clear logging about current balance status

## Installation and Setup

### Prerequisites

- Python 3.8+
- Redis server
- PostgreSQL (optional, for historical data)
- BitGet API credentials

### Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (create .env file):

   ```
   # BitGet API Credentials
   BITGET_API_KEY=your_api_key
   BITGET_SECRET_KEY=your_secret_key
   BITGET_PASSPHRASE=your_passphrase
   
   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   
   # Telegram Alerts (optional)
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

## Usage

### Running the System

The main way to run the system is using the provided shell script:

```bash
./run_trap_aware_traders.sh
```

Or with custom parameters:

```bash
./run_trap_aware_traders.sh --symbol BTCUSDT --long-capital 150.0 --short-capital 200.0
```

### Available Parameters

- `--symbol`: Trading symbol (default: BTCUSDT)
- `--long-capital`: Initial capital for long trader (default: 150.0 USDT)
- `--short-capital`: Initial capital for short trader (default: 200.0 USDT)
- `--long-leverage`: Leverage for long positions (default: 11)
- `--short-leverage`: Leverage for short positions (default: 11)
- `--trap-probability-threshold`: Threshold for trap detection (default: 0.7)
- `--trap-alert-threshold`: Threshold for sending alerts (default: 0.8)
- `--min-free-balance`: Minimum free balance to maintain (default: 0.0 USDT)
- `--enable-elite-exits`: Enable elite exit strategies
- `--elite-exit-confidence`: Confidence threshold for exits (default: 0.7)

### Utility Scripts

Several utility scripts are provided for checking system status:

- **check_positions.py**: Display current open positions in both sub-accounts
- **check_balances.py**: Show detailed balance information for both sub-accounts
- **verify_credentials.py**: Validate BitGet API credentials
- **test_trap_probability.py**: Test the trap probability meter
- **check_trap_meter.py**: View current trap probability and components

### Monitoring the System

Monitor the system's operation through the log files:

```bash
tail -f trap_aware_debug_*.log
```

## Testing

The OMEGA BTC AI system includes comprehensive test suites for both backend and frontend components.

### Backend Tests

Run the backend tests using pytest:

```bash
pytest tests/
```

Run specific test categories:

```bash
pytest tests/unit/                       # Unit tests only
pytest tests/unit/trading/               # Trading module tests
pytest tests/integration/                # Integration tests
```

### Frontend Tests

For the Reggae Dashboard frontend (if installed):

```bash
cd omega_ai/visualizer/frontend/reggae-dashboard
npm test                                 # Run all tests
npm run test:watch                       # Run in watch mode
npm run test:coverage                    # Generate coverage report
```

### Test Data Generation

Generate test data for development and testing:

```bash
python tests/fixtures/create_test_trap_data.py --interval 2
```

Options:

- `--host`: Redis host (default: localhost)
- `--port`: Redis port (default: 6379)
- `--interval`: Update interval in seconds (default: 1.0)

## Recent Improvements

1. **Redis Fallback Enhancement**: Improved JSON handling for price data from Redis.
2. **BitGet Integration**: Full support for BitGet futures trading with sub-account management.
3. **Trap Awareness**: Integration of trap detection with trading strategies.
4. **Elite Exit Strategy**: Sophisticated exit decision-making based on multiple factors.
5. **Balance Management**: Improved free balance checking for better risk management.
6. **V2 Roadmap**: Created comprehensive roadmap for ZION TRAIN V2 release.

## V2 Roadmap Highlights (ZION TRAIN)

The upcoming ZION TRAIN V2 release focuses on:

1. **Core System Enhancements**
   - Type safety improvements
   - Module refactoring for classes exceeding 333 LoC
   - Improved architecture for trap detection algorithms

2. **Resilience & Stability**
   - Enhanced error handling with specific error classes
   - Graceful degradation for API failures
   - Improved Redis fallback mechanisms

3. **Performance Optimization**
   - Optimized trap detection algorithms
   - Parallel processing for non-dependent operations
   - Reduced memory footprint for high-frequency operations

4. **Advanced Features**
   - ML-based trap pattern recognition
   - Time-series analysis for improved accuracy
   - Dynamic position sizing based on volatility metrics

5. **Testing & Validation**
   - Expanded test suite with improved coverage
   - Backtesting framework with trap simulation
   - Performance metrics collection and analysis

## Divine Flow Principles

The project adheres to several key principles:

1. **Harmonic Development**
   - Code structure aligned with natural patterns of complexity
   - Balanced abstractions across the codebase

2. **Assembly Fibonacci**
   - Component relationships following Fibonacci sequence patterns
   - Natural scaling proportions in modules

3. **Golden Ratio Architecture**
   - 1.618 ratio balance between abstraction layers
   - Phi-based proportionality in core components

## Development Guidelines

1. **Test Driven Development**
   - Maintain test coverage above 75%
   - Roll back if coverage decreases

2. **Module Refactoring**
   - Refactor classes exceeding 333 LoC
   - Consider AI efficiency in refactoring

3. **Process Management**
   - Kill running processes before starting new ones
   - Start system flow from scratch for clean state
   - Ensure logs are in place for debugging
   - Run in-scope processes in foreground for analysis

4. **Code Quality**
   - Use GNU license in all files
   - Document major project decisions via RFC READMEs
   - Preserve existing functionality when processing new features

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis is running: `redis-cli ping`
   - Check connection parameters in `.env` file
   - Verify `REDIS_HOST` is set to `localhost` for local development

2. **BitGet API Issues**
   - Validate credentials using `verify_credentials.py`
   - Check API rate limits (BitGet has strict limits)
   - Ensure system clock is synchronized

3. **System Startup Issues**
   - Kill any running processes first: `pkill -f "python.*omega_ai"`
   - Start services in the correct order:
     1. Data feed
     2. WebSocket server
     3. MM trap consumer
     4. Trap probability meter
     5. Trap-aware traders

### Debugging Process

1. Check log files for specific errors
2. Run problematic components in foreground for direct observation
3. Use utility scripts to verify system state
4. Turn on DEBUG logging level for more verbose output

## License

This project is licensed under the GNU Affero General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is for educational and research purposes only. Trading cryptocurrencies carries a high level of risk, and may not be suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade cryptocurrencies you should carefully consider your investment objectives, level of experience, and risk appetite.

---

*OMEGA BTC AI - Divine Flow in Algorithmic Trading*
