
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


# Trap Probability Meter

The Trap Probability Meter is a powerful tool that calculates and visualizes the probability of market maker traps forming in real-time. It combines various market indicators, price patterns, and historical data to provide a comprehensive assessment of potential market manipulation.

## Overview

Market maker traps are deliberate price manipulations designed to exploit trader psychology, often targeting stop-losses, liquidation points, or common technical analysis patterns. The Trap Probability Meter helps traders identify these potential traps before they fully develop, enabling better decision-making and risk management.

The tool displays:
- An overall trap probability meter (progress bar)
- Individual component meters showing what factors contribute to the probability
- Trap type prediction with confidence level
- Trend indicators showing if probability is increasing/decreasing

![Trap Probability Meter Screenshot](../assets/images/trap_probability_meter.png)

## Components Analyzed

The Trap Probability Meter analyzes several factors to calculate the overall trap probability:

| Component | Weight | Description |
|-----------|--------|-------------|
| Price Pattern | 25% | Identifies chart patterns associated with traps (Wyckoff, H&S, etc.) |
| Volume Spike | 20% | Detects unusual volume activity that may indicate manipulation |
| Fibonacci Level | 15% | Analyzes price proximity to key Fibonacci levels where traps often occur |
| Historical Match | 15% | Compares current conditions to historical trap patterns |
| Order Book | 15% | Analyzes order book imbalances and walls that may indicate manipulation |
| Market Regime | 10% | Considers the overall market context and its susceptibility to traps |

## Trap Types Detected

The meter can identify various types of market maker traps:

- **Liquidity Grab** (💰): Sudden price movement to grab liquidity at a key level
- **Stop Hunt** (🎯): Price pushed to common stop loss levels then reverses
- **Bull Trap** (🐂): False breakout above resistance to trap buyers
- **Bear Trap** (🐻): False breakdown below support to trap sellers
- **Fake Pump** (🚀): Artificial pump to create FOMO then dump
- **Fake Dump** (📉): Artificial dump to create panic selling then pump

## Usage

### Command-Line Interface

```bash
python -m omega_ai.tools.trap_probability_meter [options]
```

Options:
- `--interval SECONDS`: Check interval in seconds (default: 5)
- `--debug`: Show debug information
- `--no-color`: Disable colored output
- `--verbose`: Show detailed component information
- `--backtest DATE`: Run in backtest mode from a specific date (format: YYYY-MM-DD)

### Integration with Other Components

The Trap Probability Meter stores its data in Redis, making it accessible to other components of the Omega BTC AI system. You can access this data using the utility functions in `omega_ai.utils.trap_probability_utils`:

```python
from omega_ai.utils.trap_probability_utils import get_current_trap_probability

# Get the current trap probability
probability = get_current_trap_probability()

# Check if it's above a threshold
if probability > 0.7:
    print("High probability of trap formation!")
```

Available utility functions:
- `get_current_trap_probability()`: Get the current probability value
- `get_probability_components()`: Get individual component values
- `get_detected_trap_info()`: Get information about any detected traps
- `get_probability_trend()`: Get trend information over a specified time period
- `is_trap_likely()`: Quick check if a trap is likely based on current probability

## Testing

You can test the Trap Probability Meter with mock data using the included test script:

```bash
python scripts/test_trap_probability.py
```

This script:
1. Generates mock trap probability data
2. Stores it in Redis for the meter to access
3. Runs the trap probability meter to visualize the data

## Implementation Details

The Trap Probability Meter maintains a history of probability values to calculate trends. It also records detection metrics over time to help improve the model. The probabilities are calculated using a weighted combination of the individual components.

Data is stored in Redis under these keys:
- `current_trap_probability`: Current probability data (JSON)
- `trap_probability_history`: Historical probability data (list of JSON)
- `trap_detection_metrics`: Accuracy metrics for trap detection

## Future Enhancements

Planned enhancements for the Trap Probability Meter include:
- Machine learning model for improved trap detection
- Integration with alert systems for real-time notifications
- Customizable thresholds for different trading strategies
- Web UI for easier visualization and configuration
- Performance optimization for high-frequency trading scenarios 