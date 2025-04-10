
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


# BitgetPositionAnalyzerB0t

## Overview

`BitgetPositionAnalyzerB0t` is a specialized component of the Omega Bot Farm that monitors and analyzes BitGet exchange positions using Fibonacci-based principles. This bot provides deep insights into trading positions, calculates Fibonacci retracement levels, measures position harmony, and generates actionable recommendations for portfolio management.

The analyzer integrates with the trading analyzer architecture to provide a comprehensive view of positions and trading opportunities based on mathematically harmonious ratios found throughout nature and markets.

## Features

- **Position Monitoring**: Real-time tracking of all open positions on BitGet
- **Fibonacci Analysis**: Calculation of Fibonacci retracement/extension levels for each position
- **Position Harmony**: Score each position's alignment with the golden ratio principles
- **Change Detection**: Identify new, closed, or significantly changed positions
- **Portfolio Recommendations**: Generate actionable insights based on Fibonacci principles

## Mathematical Foundation

The analyzer uses several key mathematical constants and sequences:

- **Golden Ratio (φ)**: 1.618034... - The divine proportion found throughout nature
- **Inverse Golden Ratio**: 0.618034... - Used for retracements and position sizing
- **Fibonacci Sequence**: 1, 1, 2, 3, 5, 8, 13, 21... - Each number is the sum of the two preceding ones
- **Fibonacci Retracement Levels**: 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%, 161.8%, 261.8%

## Prerequisites

- Python 3.8+
- BitGet API credentials
- CCXT library
- ExchangeService from Omega Bot Farm (recommended)

## Installation

The `BitgetPositionAnalyzerB0t` is part of the Omega Bot Farm package. To use it, ensure you have the required dependencies:

```bash
# Install required dependencies
pip install ccxt pyyaml

# Clone the Omega Bot Farm repository
git clone https://github.com/your-org/omega-btc-ai.git
cd omega-btc-ai
```

## Configuration

The analyzer can be initialized with the following parameters:

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Initialize with explicit API credentials
analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase",
    use_testnet=False,  # Set to True for testing
    position_history_length=10  # Number of historical snapshots to keep
)

# Or use environment variables
# export BITGET_API_KEY="your_api_key"
# export BITGET_SECRET_KEY="your_api_secret"
# export BITGET_PASSPHRASE="your_passphrase"
analyzer = BitgetPositionAnalyzerB0t()
```

### Environment Variables

The analyzer uses the following environment variables if not provided explicitly:

- `BITGET_API_KEY`: Your BitGet API key
- `BITGET_SECRET_KEY`: Your BitGet API secret
- `BITGET_PASSPHRASE`: Your BitGet API passphrase

## Usage Examples

### Basic Position Analysis

```python
import asyncio
import json

async def analyze_positions():
    # Create analyzer
    analyzer = BitgetPositionAnalyzerB0t()
    
    # Get positions
    positions_data = await analyzer.get_positions()
    
    # Print positions
    print(json.dumps(positions_data, indent=2))

# Run the analysis
asyncio.run(analyze_positions())
```

### Comprehensive Portfolio Analysis

```python
import asyncio
import json

async def analyze_portfolio():
    # Create analyzer
    analyzer = BitgetPositionAnalyzerB0t()
    
    # Get comprehensive analysis
    analysis = analyzer.analyze_all_positions()
    
    # If analyze_all_positions returns a coroutine (when using exchange_service)
    if asyncio.iscoroutine(analysis):
        analysis = await analysis
    
    # Print harmony score
    print(f"Portfolio Harmony Score: {analysis.get('harmony_score', 0):.2f}")
    
    # Print recommendations
    print("\nRecommendations:")
    for rec in analysis.get('recommendations', []):
        print(f"- {rec}")
    
    # Print position analyses
    print("\nPosition Analyses:")
    for pos_analysis in analysis.get('position_analyses', []):
        position = pos_analysis.get('position', {})
        analysis_data = pos_analysis.get('analysis', {})
        
        print(f"\n{position.get('symbol')}: {position.get('side').upper()}")
        print(f"Entry Price: {position.get('entryPrice')}")
        print(f"Current Price: {position.get('markPrice')}")
        print(f"PnL: {position.get('unrealizedPnl')} ({analysis_data.get('pnl_percentage', 0):.2f}%)")
        
        # Print TP/SL recommendations
        tp = analysis_data.get('recommended_take_profit')
        sl = analysis_data.get('recommended_stop_loss')
        
        if tp:
            print(f"Recommended Take Profit: {tp[1]} ({tp[0]})")
        if sl:
            print(f"Recommended Stop Loss: {sl[1]} ({sl[0]})")

# Run the analysis
asyncio.run(analyze_portfolio())
```

## Fibonacci Analysis

The analyzer calculates Fibonacci levels for both long and short positions:

### For Long Positions

```
0.0%    = Entry Price
23.6%   = Entry Price * (1 + 0.236)
38.2%   = Entry Price * (1 + 0.382)
50.0%   = Entry Price * (1 + 0.5)
61.8%   = Entry Price * (1 + 0.618)  # Golden Ratio
78.6%   = Entry Price * (1 + 0.786)
100.0%  = Entry Price * 2
161.8%  = Entry Price * (1 + 1.618)  # Golden Ratio
261.8%  = Entry Price * (1 + 2.618)  # PHI³
```

### For Short Positions

```
0.0%    = Entry Price
23.6%   = Entry Price * (1 - 0.236)
38.2%   = Entry Price * (1 - 0.382)
50.0%   = Entry Price * (1 - 0.5)
61.8%   = Entry Price * (1 - 0.618)  # Golden Ratio
78.6%   = Entry Price * (1 - 0.786)
100.0%  = Entry Price * 0  # Zero
```

## Harmony Scoring

The analyzer calculates harmony scores for individual positions and the overall portfolio:

### Position Harmony Factors

- **Position Size Ratio**: How close the position size is to the inverse golden ratio (0.618) of account equity
- **Leverage Harmony**: How close the leverage is to a Fibonacci number (1, 2, 3, 5, 8, 13, 21)
- **PnL Contribution**: Positive PnL contributes to harmony

### Portfolio Harmony Factors

- **Long-Short Balance**: How close the long-short ratio is to the golden ratio or its inverse
- **Exposure Level**: How close the exposure-to-equity ratio is to the inverse golden ratio
- **PnL Contribution**: Positive overall PnL contributes to harmony

## Portfolio Recommendations

The analyzer generates recommendations based on:

- Overall portfolio harmony score
- Long-short balance compared to golden ratio
- Exposure level compared to equity
- Individual position PnL performance

Example recommendations:

- "Portfolio harmony is low. Consider rebalancing positions to improve Fibonacci alignment."
- "Long exposure (2.50x short) exceeds golden ratio. Consider reducing long positions."
- "Consider taking profit on BTC/USDT LONG position with 21.5% gain."

## Integration with ExchangeService

`BitgetPositionAnalyzerB0t` can use the Omega Bot Farm's `ExchangeService` for better code reuse and standardized exchange interactions:

```python
from src.omega_bot_farm.services.exchange_service import create_exchange_service

# Create exchange service
exchange_service = create_exchange_service(
    exchange_id="bitget",
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase"
)

# Pass to analyzer (custom implementation)
analyzer = BitgetPositionAnalyzerB0t()
analyzer.exchange_service = exchange_service
analyzer.exchange = exchange_service.get_exchange_client()
```

The analyzer automatically attempts to use the `ExchangeService` if available, with a fallback to direct CCXT integration if the service is not available.

## Error Handling

The analyzer implements comprehensive error handling:

- Connection failures are logged with specific error messages
- Missing API credentials generate appropriate warnings
- Function-specific errors are captured and reported without crashing the analyzer
- All errors are properly logged for debugging

## Advanced Applications

### Custom Harmony Metrics

You can extend the analyzer with custom harmony metrics:

```python
class CustomHarmonyAnalyzer(BitgetPositionAnalyzerB0t):
    def _calculate_harmony_score(self) -> float:
        # Get base harmony score
        base_harmony = super()._calculate_harmony_score()
        
        # Add custom harmony factors
        # Example: Market trend alignment
        market_trend_alignment = 0.1  # Custom calculation
        
        # Return adjusted harmony
        return min(1.0, base_harmony + market_trend_alignment)
```

### Integration with Trading Bots

The analyzer can be used to inform trading decisions:

```python
async def trading_strategy():
    analyzer = BitgetPositionAnalyzerB0t()
    analysis = await analyzer.analyze_all_positions()
    
    # Make decisions based on harmony score
    if analysis['harmony_score'] < 0.4:
        # Rebalance portfolio
        pass
    
    # Execute recommendations
    for rec in analysis['recommendations']:
        if "taking profit" in rec:
            # Close profitable positions
            pass
```

## Contributing

Contributions to the `BitgetPositionAnalyzerB0t` are welcome! Areas for improvement include:

- Additional Fibonacci-based metrics
- Integration with more exchanges
- Enhanced visualization of Fibonacci levels
- Optimized position recommendation algorithms

## License

`BitgetPositionAnalyzerB0t` is part of the Omega Bot Farm and is licensed under the terms specified in the project's LICENSE file.
