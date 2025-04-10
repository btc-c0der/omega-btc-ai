
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


# BitGet Sub-Account Support

This document describes how to use sub-accounts with the BitGet trading system to achieve full separation of trading activities and risk management.

## Overview

Sub-accounts allow you to create separate trading accounts under your main BitGet account, each with its own:

- Balance
- Margin
- Trading history
- Risk parameters

This is particularly useful for:

- Running multiple trading strategies independently
- Isolating risk between different trading approaches
- Managing separate capital allocations
- Testing different trading parameters

## Setup

### 1. Create Sub-Accounts

You can create sub-accounts using the BitGet trader:

```python
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Initialize the main account trader
trader = BitGetTrader(
    profile_type="strategic",
    use_testnet=True,  # Use testnet for testing
    api_version="v2"
)

# Create sub-accounts for different trading strategies
trader.create_sub_account("scalping_trader", "password123")
trader.create_sub_account("aggressive_trader", "password456")
trader.create_sub_account("strategic_trader", "password789")
```

### 2. Transfer Funds

Transfer funds to each sub-account:

```python
# Transfer 1000 USDT to the scalping trader
trader.transfer_to_sub_account("scalping_trader", 1000.0)

# Transfer 2000 USDT to the aggressive trader
trader.transfer_to_sub_account("aggressive_trader", 2000.0)

# Transfer 3000 USDT to the strategic trader
trader.transfer_to_sub_account("strategic_trader", 3000.0)
```

### 3. Initialize Traders with Sub-Accounts

Create separate trader instances for each sub-account:

```python
# Scalping trader
scalping_trader = BitGetTrader(
    profile_type="scalper",
    use_testnet=True,
    api_version="v2",
    sub_account_name="scalping_trader"
)

# Aggressive trader
aggressive_trader = BitGetTrader(
    profile_type="aggressive",
    use_testnet=True,
    api_version="v2",
    sub_account_name="aggressive_trader"
)

# Strategic trader
strategic_trader = BitGetTrader(
    profile_type="strategic",
    use_testnet=True,
    api_version="v2",
    sub_account_name="strategic_trader"
)
```

## Available Methods

### Sub-Account Management

```python
# Get list of all sub-accounts
sub_accounts = trader.get_sub_accounts()

# Get balance for a specific sub-account
balance = trader.get_sub_account_balance("scalping_trader")

# Transfer funds to a sub-account
trader.transfer_to_sub_account("scalping_trader", 1000.0)

# Transfer funds from a sub-account
trader.transfer_from_sub_account("scalping_trader", 500.0)
```

### Trading with Sub-Accounts

All trading operations (orders, positions, etc.) automatically use the specified sub-account:

```python
# Place an order using the scalping trader
scalping_trader.place_order(
    symbol="BTCUSDT",
    side="buy",
    order_type="market",
    quantity=0.01
)

# Get positions for the aggressive trader
positions = aggressive_trader.get_positions()

# Get balance for the strategic trader
balance = strategic_trader.get_account_balance()
```

## Best Practices

1. **Naming Convention**
   - Use clear, descriptive names for sub-accounts
   - Include strategy type in the name (e.g., "scalping_trader_1")
   - Add version numbers if you have multiple instances of the same strategy

2. **Risk Management**
   - Set appropriate position sizes for each sub-account
   - Monitor risk parameters separately for each account
   - Use different leverage settings based on strategy

3. **Monitoring**
   - Track PnL separately for each sub-account
   - Monitor margin levels independently
   - Set up separate alerts for each account

4. **Testing**
   - Always test sub-account functionality on testnet first
   - Verify fund transfers with small amounts
   - Test trading operations with minimal position sizes

## Example Setup

Here's a complete example of setting up three different trading strategies with sub-accounts:

```python
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

def setup_trading_system():
    # Initialize main account
    main_trader = BitGetTrader(
        profile_type="strategic",
        use_testnet=True,
        api_version="v2"
    )
    
    # Create sub-accounts
    sub_accounts = [
        ("scalping_trader", "password123", 1000.0),
        ("aggressive_trader", "password456", 2000.0),
        ("strategic_trader", "password789", 3000.0)
    ]
    
    # Create accounts and transfer funds
    for name, password, amount in sub_accounts:
        main_trader.create_sub_account(name, password)
        main_trader.transfer_to_sub_account(name, amount)
    
    # Create trader instances
    traders = {
        "scalping": BitGetTrader(
            profile_type="scalper",
            use_testnet=True,
            api_version="v2",
            sub_account_name="scalping_trader"
        ),
        "aggressive": BitGetTrader(
            profile_type="aggressive",
            use_testnet=True,
            api_version="v2",
            sub_account_name="aggressive_trader"
        ),
        "strategic": BitGetTrader(
            profile_type="strategic",
            use_testnet=True,
            api_version="v2",
            sub_account_name="strategic_trader"
        )
    }
    
    return traders

# Usage
traders = setup_trading_system()

# Scalping trader operations
scalping_trader = traders["scalping"]
scalping_trader.place_order(
    symbol="BTCUSDT",
    side="buy",
    order_type="market",
    quantity=0.01
)

# Aggressive trader operations
aggressive_trader = traders["aggressive"]
aggressive_trader.place_order(
    symbol="BTCUSDT",
    side="buy",
    order_type="market",
    quantity=0.05
)

# Strategic trader operations
strategic_trader = traders["strategic"]
strategic_trader.place_order(
    symbol="BTCUSDT",
    side="buy",
    order_type="market",
    quantity=0.1
)
```

## Testing

Run the sub-account tests to verify functionality:

```bash
pytest omega_ai/trading/exchanges/tests/test_sub_accounts.py -v
```

## Notes

- Sub-accounts are only available on the mainnet
- Each sub-account requires its own API key with appropriate permissions
- Monitor API rate limits across all sub-accounts
- Keep track of sub-account passwords securely
- Consider implementing a password management system for production use
