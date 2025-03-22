# OMEGA BTC AI - Divine Alignment Dashboard v2

> "This assembly is not mechanical—it's rhythmic. Let's tune it as if each opcode had intention."

The Divine Alignment Dashboard is a visualization and analysis tool that provides insights into Bitcoin's price movements based on golden ratio and Fibonacci principles, now enhanced with trader personas that embody different trading strategies.

## Features

- **Golden Ratio Visualization**: View Bitcoin price charts with golden ratio and Fibonacci overlays
- **Divine Alignment Analysis**: Track how closely BTC price aligns with golden ratio levels
- **Fibonacci Crossing Detection**: Get alerts when price crosses significant Fibonacci levels
- **Trade Recommendations**: Receive trade signals based on golden ratio alignment
- **Market Data Analysis**: See key support/resistance levels and momentum indicators
- **Trader Personas**: Understand different trading strategies through personified traders
- **Performance Metrics**: Track win rates, profits, and drawdown for each trader persona

## New in v2: Trader Personas

The dashboard now features four distinct trader personas, each with their own personality, trading style, and performance characteristics:

1. **Strategic Trader** - Methodical and disciplined with a focus on Fibonacci levels
2. **Aggressive Trader** - Bold and decisive, seeking high-leverage opportunities
3. **Scalper Trader** - Quick and nimble, exploiting small golden ratio divergences
4. **Divine Harmonizer** - Intuitive and balanced, seeking universal alignment across markets

Each persona provides a unique lens through which to view market movements and potential trading strategies.

## Installation

### Prerequisites

- Python 3.7+
- Flask
- ccxt
- matplotlib
- numpy
- pandas

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/username/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the divine dashboard:

   ```bash
   cd sandbox/divine
   python start_divine_dashboard.py
   ```

The dashboard will be available at <http://localhost:5051/divine>

## API Endpoints

The dashboard exposes several API endpoints:

- **GET /api/golden_status**: Current golden ratio alignment status and BTC price
- **GET /api/trading_data**: Combined trading data including signals and recommendations
- **GET /api/generate**: Generate new golden ratio chart (POST)
- **GET /api/trader_personas**: Data about different trader personas and their strategies

## Testing

Run the tests for the trader personas functionality:

```bash
cd sandbox/divine
python -m pytest test_trader_personas.py -v
```

## Technical Details

### Architecture

The Divine Alignment Dashboard is built using:

- **Flask**: Backend API server
- **HTML/CSS/JavaScript**: Frontend dashboard
- **ccxt**: Cryptocurrency exchange API integration
- **matplotlib**: Golden ratio chart visualization

### Trader Personas Implementation

Trader personas are implemented as a data model that captures different aspects of trading personalities:

- **Personality**: Character traits and approach to trading
- **Style**: Specific trading methodologies employed
- **Risk Level**: Comfort with market volatility and potential losses
- **Favorite Pattern**: Preferred chart patterns or technical indicators
- **Current Position**: Example of typical position management
- **Performance Metrics**: Quantitative measures of trading success

This personification allows users to identify with different trading styles and understand how each approach might perform in various market conditions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- The OMEGA BTC AI team
- Fibonacci, for the mathematical sequence that guides our trading
- The divine harmony of the markets
