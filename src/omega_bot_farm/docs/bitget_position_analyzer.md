
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


# BitGet Position Analyzer Bot

The BitgetPositionAnalyzerB0t is a specialized component within the Omega Bot Farm designed to monitor, analyze, and provide insights on BitGet exchange positions using Fibonacci-based mathematical principles.

## Overview

This bot connects to the BitGet exchange API to fetch position data and applies Fibonacci-based analysis to identify optimal entry/exit points, evaluate position harmony, and generate trading recommendations. The analyzer integrates with the Trading Analyzer architecture while adding specialized position monitoring capabilities.

## Key Features

1. **Position Monitoring**: Continuously tracks open positions on BitGet exchange
2. **Fibonacci Analysis**: Applies the golden ratio (φ ≈ 1.618) and Fibonacci retracement levels to calculate optimal take profit and stop loss targets
3. **Position Harmony**: Calculates a harmony score based on how well positions align with Fibonacci principles
4. **Change Detection**: Identifies and reports new, closed, or significantly changed positions
5. **Portfolio Recommendations**: Generates actionable recommendations based on position analysis

## Mathematical Foundation

The BitgetPositionAnalyzerB0t leverages several key mathematical constants:

- **Golden Ratio (φ)**: 1.618034... - A universal constant found throughout nature and markets
- **Inverse Golden Ratio (1/φ)**: 0.618034... - Used for retracement calculations
- **Fibonacci Sequence**: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ... - The ratio of consecutive numbers approaches φ
- **Fibonacci Retracement Levels**: 23.6%, 38.2%, 50%, 61.8%, 78.6% - Used to identify potential support and resistance

## Installation

### Prerequisites

- Python 3.8+
- CCXT library (`pip install ccxt`)
- BitGet API credentials

### Setup

```bash
# Install required dependencies
pip install ccxt pyyaml redis

# Set environment variables for API access
export BITGET_API_KEY="your_api_key"
export BITGET_SECRET_KEY="your_secret_key"
export BITGET_PASSPHRASE="your_passphrase"
```

## Usage

### Basic Usage

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
import asyncio

async def main():
    # Initialize the analyzer
    analyzer = BitgetPositionAnalyzerB0t()
    
    # Get and analyze all positions
    analysis = await analyzer.analyze_all_positions()
    
    # Print analysis results
    print(f"Total positions: {analysis['total_positions']}")
    print(f"Harmony score: {analysis['harmony_score']:.2f}")
    
    # Print recommendations
    for rec in analysis['recommendations']:
        print(f"- {rec}")

# Run the main function
asyncio.run(main())
```

### Configuration Options

When initializing the BitgetPositionAnalyzerB0t, you can configure several parameters:

```python
analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",               # BitGet API key
    api_secret="your_api_secret",         # BitGet API secret
    api_passphrase="your_passphrase",     # BitGet API passphrase
    use_testnet=True,                     # Use testnet instead of mainnet
    position_history_length=10            # Number of position snapshots to keep
)
```

## Position Analysis

The analyzer provides detailed analysis for each position:

### Fibonacci Levels

For each position, the bot calculates Fibonacci-based price levels:

```python
# Example output for a long BTC position with entry at $30,000
{
    "fibonacci_levels": {
        "0.0%": 30000.0,              # Entry price
        "23.6%": 37080.0,             # 23.6% extension
        "38.2%": 41460.0,             # 38.2% extension
        "50.0%": 45000.0,             # 50% extension
        "61.8%": 48540.0,             # Golden ratio (key target)
        "78.6%": 53580.0,             # 78.6% extension
        "100.0%": 60000.0,            # 100% extension (double entry)
        "161.8%": 78540.0,            # 1.618 extension (key target)
        "261.8%": 108540.0            # 2.618 extension (moonshot target)
    }
}
```

### Position Harmony

Each position receives a harmony score (0.0-1.0) based on:

1. **Size Harmony**: How closely the position size aligns with the golden ratio (0.618) of account equity
2. **Leverage Harmony**: Whether the position uses leverage close to Fibonacci numbers (1, 2, 3, 5, 8, 13, 21)
3. **PnL Contribution**: Whether the position is profitable

### Recommended Targets

The analyzer identifies the optimal profit targets and stop losses based on Fibonacci principles:

```python
{
    "recommended_take_profit": ("61.8%", 48540.0),  # Golden ratio target
    "recommended_stop_loss": ("38.2%", 18540.0)     # Common reversal level
}
```

## Portfolio Analysis

At the portfolio level, the BitgetPositionAnalyzerB0t evaluates:

### Account Statistics

```python
{
    "account_stats": {
        "balance": 10000.0,               # Account balance
        "equity": 10500.0,                # Balance + unrealized PnL
        "total_position_value": 6180.34,  # Total position exposure (golden ratio!)
        "total_pnl": 500.0,               # Total unrealized profit/loss
        "long_exposure": 3819.66,         # Long exposure (inverse golden ratio!)
        "short_exposure": 2360.68,        # Short exposure
        "long_short_ratio": 1.618,        # Long:Short ratio (golden ratio!)
        "exposure_to_equity_ratio": 0.618,# Exposure to equity (inverse golden ratio!)
        "harmony_score": 0.85             # Overall harmony score
    }
}
```

### Portfolio Harmony

The overall harmony score (0.0-1.0) is calculated based on:

1. **Long-Short Balance**: How closely the ratio of long to short exposure approaches the golden ratio (1.618)
2. **Exposure Level**: How closely the total exposure to equity ratio approaches the inverse golden ratio (0.618)
3. **PnL Contribution**: Overall profitability

### Recommendations

The analyzer generates actionable recommendations for portfolio management:

```
- Portfolio has good Fibonacci harmony. Maintain current balance.
- Consider taking profit on BTC/USDT:USDT long position with 8.3% gain.
- Consider adding a small short position to maintain golden ratio balance.
```

## Change Detection

The analyzer tracks position changes between updates:

```python
{
    "changes": {
        "new": [
            # New positions since last check
        ],
        "closed": [
            # Positions that were closed
        ],
        "changed": [
            # Positions with significant changes in size or PnL
        ]
    }
}
```

## Integration with Other Systems

### Redis Integration

The BitgetPositionAnalyzerB0t can publish analysis results to Redis for other systems to consume:

```python
# Configure Redis publishing
redis_client = RedisClient(host="localhost", port=6379)
redis_client.publish("position_analysis", json.dumps(analysis))
```

### Discord Notifications

Position changes and significant harmony shifts can trigger Discord notifications:

```python
# Send Discord notification for new position
webhook_url = "https://discord.com/api/webhooks/..."
discord_notifier.send_position_notification(webhook_url, new_position)
```

## Kubernetes Deployment

The BitgetPositionAnalyzerB0t can be deployed in Kubernetes using the provided configuration:

```bash
# Apply Kubernetes configuration
kubectl apply -f kubernetes/deployments/bitget-position-analyzer.yaml
```

This creates:

- A deployment running the analyzer
- A service exposing the analyzer API
- A ConfigMap with configuration settings
- A CronJob for generating daily position reports
- A PersistentVolumeClaim for storing reports

## Development and Extending

### Adding New Fibonacci Metrics

To add a new Fibonacci-based metric:

```python
def calculate_fibonacci_wave_count(self, prices: List[float]) -> int:
    """Calculate the Fibonacci wave count from price history."""
    # Implementation here
    return wave_count
```

### Customizing Harmony Calculation

The harmony score calculation can be customized by adjusting the weights:

```python
def _calculate_custom_harmony(self, position: Dict[str, Any], weights: Dict[str, float]) -> float:
    """Calculate custom harmony score with specified weights."""
    harmony = 0.5  # Base harmony
    
    # Apply custom weights to different factors
    # Implementation here
    
    return harmony
```

## Performance Considerations

- **API Rate Limits**: The analyzer respects BitGet API rate limits to avoid throttling
- **Caching**: Position data is cached to reduce API calls
- **Async Processing**: Async methods are used for non-blocking operation

## Frequently Asked Questions

**Q: Why use Fibonacci levels for analysis?**
A: Fibonacci levels are widely observed in markets as psychological price points where support and resistance often occur. The golden ratio (1.618) appears frequently in nature and trading.

**Q: How can I improve my harmony score?**
A: Adjust position sizes to approach the inverse golden ratio (0.618) of your equity, and maintain a long-to-short exposure ratio close to the golden ratio (1.618).

**Q: Can I use this with other exchanges?**
A: While currently optimized for BitGet, the analyzer can be extended to support other exchanges that have CCXT integration.

## Troubleshooting

**API Connection Issues**

```
{"error": "Exchange client not initialized"}
```

Solution: Verify your API credentials and network connectivity.

**Missing Position Data**

```
"positions": []
```

Solution: Ensure you have open positions on the account and the API key has permission to view them.

## License

This component is part of the Omega Bot Farm and follows the project's licensing terms.
