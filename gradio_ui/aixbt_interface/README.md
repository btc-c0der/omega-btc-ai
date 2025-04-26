# AIXBT Neural Analysis Interface

Web-based interface for AIXBT market analysis and trading, featuring real-time visualization and neural pattern detection.

## Features

- Real-time BTC price monitoring
- Market maker trap detection with probability meter
- Neural matrix pattern analysis
- Multi-timeframe market analysis
- Advanced visualization with volume profile and order flow

## Components

1. **Price Feed**: Real-time price and volume monitoring
2. **Trap Meter**: Market maker trap detection with component breakdown
3. **Market Data**: Technical analysis and order book visualization
4. **Neural Matrix**: Pattern recognition and market regime detection
5. **Visualization**: Advanced charting with pattern highlighting

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with Redis connection details:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_SSL=false
```

## Usage

Run the interface:
```bash
./start.sh
```

Or manually:
```bash
python app.py
```

## Redis Keys

The interface uses the following Redis keys:

### Market Data
- `btc_market_data`: Current market data
- `btc_price_history`: Historical price data
- `btc_market_analysis`: Technical analysis results
- `btc_visualization_data`: Chart visualization data

### Trap Detection
- `current_trap_data`: Current trap probability analysis
- `trap_probability_history`: Historical trap probabilities

### Neural Analysis
- `btc_neural_analysis`: Neural pattern analysis results
- `btc_pattern_correlation`: Pattern correlation matrix
- `btc_regime_data`: Market regime detection data

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request