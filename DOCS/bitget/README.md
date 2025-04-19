
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


# BitGet Integration for OmegaBTC AI

This module provides integration with the BitGet cryptocurrency exchange for our trader profile system. It allows you to execute trades on BitGet while maintaining the psychological and risk management characteristics of different trader profiles.

## Features

- Integration with BitGet's testnet and mainnet APIs
- Support for all trader profiles (Strategic, Aggressive, Newbie, Scalper)
- Automatic position sizing and risk management
- Stop-loss and take-profit order management
- Trade history tracking and PnL calculation
- Psychological state tracking and adaptation

## Prerequisites

1. Python 3.7 or higher
2. BitGet account (testnet or mainnet)
3. BitGet API credentials (API key, secret key, and passphrase)

## Installation

1. Install the required Python packages:

```bash
pip install requests
```

2. Set up your BitGet API credentials as environment variables:

For testnet:

```bash
export BITGET_TESTNET_API_KEY="your_testnet_api_key"
export BITGET_TESTNET_SECRET_KEY="your_testnet_secret_key"
export BITGET_TESTNET_PASSPHRASE="your_testnet_passphrase"
```

For mainnet:

```bash
export BITGET_API_KEY="your_mainnet_api_key"
export BITGET_SECRET_KEY="your_mainnet_secret_key"
export BITGET_PASSPHRASE="your_mainnet_passphrase"
```

## Usage

### Basic Usage

```python
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Initialize a strategic trader
trader = BitGetTrader(
    profile_type="strategic",
    api_key="your_api_key",
    secret_key="your_secret_key",
    passphrase="your_passphrase",
    use_testnet=True,  # Use testnet for testing
    initial_capital=10000.0
)

# Create market context
market_context = {
    "price": 50000.0,  # Current BTC price
    "trend": "bullish",
    "volatility": 0.02,
    "volume": 1000000,
    "timestamp": datetime.now()
}

# Execute a trade
position = trader.execute_trade(market_context)

# Update positions with new price
trader.update_positions(51000.0)

# Get trade history
history = trader.get_trade_history()

# Get total PnL
total_pnl = trader.get_total_pnl()
```

### Available Trader Profiles

1. **Strategic Trader**
   - Uses Fibonacci levels and market structure
   - Moderate risk management
   - Patient entry and exit points
   - 2% risk per trade

2. **Aggressive Trader**
   - High-risk, high-reward approach
   - Quick entries and exits
   - Higher leverage usage
   - 5% risk per trade

3. **Newbie Trader**
   - Conservative approach
   - Strict risk management
   - Limited leverage
   - 0.5% risk per trade

4. **Scalper Trader**
   - Quick, small profit trades
   - Tight stop losses
   - High frequency trading
   - 1% risk per trade

### Risk Management

Each trader profile implements its own risk management rules:

- Position sizing based on account balance and risk parameters
- Stop-loss placement based on volatility and market conditions
- Take-profit levels based on risk:reward ratios
- Leverage limits based on market conditions

### Example Script

See `examples/bitget_trader_example.py` for a complete example showing how to:

1. Initialize different trader profiles
2. Execute trades
3. Update positions
4. Track trade history and PnL

## Important Notes

1. **Testnet Usage**
   - Always test your strategies on the testnet first
   - Testnet provides simulated trading environment
   - No real funds are at risk

2. **Risk Warning**
   - Cryptocurrency trading is highly risky
   - Past performance does not guarantee future results
   - Use proper risk management and position sizing

3. **API Rate Limits**
   - Be mindful of BitGet's API rate limits
   - Implement appropriate delays between requests
   - Monitor your API usage

4. **Error Handling**
   - The module includes basic error handling
   - Monitor logs for API errors and trade execution issues
   - Implement additional error handling as needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
