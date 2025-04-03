# Getting Started with BitGet Position Analyzer Bot

This guide will help you quickly set up and start using the BitGet Position Analyzer Bot.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- Access to a BitGet account with API keys
- Basic understanding of cryptocurrency trading concepts
- The Omega Bot Farm repository cloned locally

## Installation

1. Clone the repository if you haven't already:

   ```bash
   git clone https://github.com/yourusername/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Install the required dependencies:

   ```bash
   pip install -r src/omega_bot_farm/requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the project root:

   ```
   BITGET_API_KEY=your_api_key
   BITGET_SECRET_KEY=your_api_secret
   BITGET_PASSPHRASE=your_passphrase
   USE_TESTNET=True  # Set to False for production
   ```

## Basic Usage

### Standalone Mode

You can run the BitGet Position Analyzer Bot in standalone mode:

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Initialize with environment variables
analyzer = BitgetPositionAnalyzerB0t(use_testnet=True)

# Or initialize with explicit credentials
analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase",
    use_testnet=True
)

# Get current positions
positions = await analyzer.get_positions()

# Print the positions
print(positions)
```

### Integration with Other Bots

To use the BitGet Position Analyzer Bot with other bots:

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
from src.omega_bot_farm.trading.b0ts.ccxt.ccxt_strategic_trader import CCXTStrategicTraderB0t

# Initialize the analyzer
analyzer = BitgetPositionAnalyzerB0t(use_testnet=True)

# Initialize the strategic trader
trader = CCXTStrategicTraderB0t(exchange_id="bitget", symbol="BTCUSDT")

# Get position analysis
positions = await analyzer.get_positions()

# Use the analysis for trading decisions
if positions["account"]["harmony_score"] > 0.8:
    # High harmony score indicates balanced positions
    await trader.place_order("limit", "buy", amount=0.01, price=45000)
```

### Command Line Interface

You can also run the bot from the command line:

```bash
python -m src.omega_bot_farm.trading.b0ts --bot bitget_analyzer --exchange bitget
```

## Key Features

### Position Analysis

```python
# Get all positions
positions = await analyzer.get_positions()

# Analyze a specific position
position = positions["positions"][0]
analysis = analyzer.analyze_position(position)

print(f"Position Side: {position['side']}")
print(f"Position Size: {position['contracts']} contracts")
print(f"Position Value: ${position['notional']}")
print(f"Unrealized PnL: ${position['unrealizedPnl']}")
print(f"Risk Level: {analysis['risk_level']}")
print(f"Harmony Score: {analysis['harmony_score']}")
```

### Fibonacci Analysis

```python
# Generate Fibonacci levels for a price range
fib_levels = analyzer.generate_fibonacci_levels(
    high_price=50000,
    low_price=40000,
    current_price=45000
)

print("Fibonacci Retracement Levels:")
for level, price in fib_levels["retracements"].items():
    print(f"{level}: ${price}")

print("\nFibonacci Extension Levels:")
for level, price in fib_levels["extensions"].items():
    print(f"{level}: ${price}")
```

### Position Harmony

```python
# Calculate harmony score for a set of positions
harmony_score = analyzer.calculate_position_harmony(positions["positions"])
print(f"Overall Position Harmony: {harmony_score}")

# Get recommendations based on harmony analysis
recommendations = analyzer.generate_portfolio_recommendations()
for rec in recommendations:
    print(f"Recommendation: {rec['action']} {rec['symbol']} {rec['amount']}")
```

## Next Steps

Now that you have the basic setup, you can:

1. Explore the [API Reference](./api_reference.md) for detailed information on all available methods
2. Learn about the [Fibonacci Analysis Methodology](./fibonacci_analysis.md) used by the bot
3. Understand the [Harmony Calculations](./harmony_calculations.md) that drive position sizing
4. Configure advanced settings using the [Configuration Guide](./configuration.md)
5. Integrate with other systems using the [Integration Guide](./integration_guide.md)

## Troubleshooting

If you encounter issues:

- Check your API keys and ensure they have the correct permissions
- Verify that you're connected to the correct network (testnet vs. mainnet)
- Consult the [Troubleshooting Guide](./troubleshooting.md) for common issues
- Review the logs for detailed error messages

## Support

If you need further assistance:

- Check the [GitHub Issues](https://github.com/yourusername/omega-btc-ai/issues) for existing problems
- Join our Discord community for real-time support
- Contact our support team at <support@example.com>
