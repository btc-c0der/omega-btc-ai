# CCXT Integration for Omega Bot Farm

This document outlines how to integrate cryptocurrency exchanges with the Omega Bot Farm using the CCXT library.

## Overview

The Omega Bot Farm uses CCXT (CryptoCurrency eXchange Trading Library) to provide a unified interface for interacting with various cryptocurrency exchanges. The integration is designed to be:

- **Containerized**: Works seamlessly in Kubernetes pods
- **Environment-aware**: Configurable via environment variables
- **Fault-tolerant**: Handles connection issues gracefully
- **Standardized**: Provides consistent interface across exchanges

## Architecture

```
┌─────────────────────────┐
│      Trading Bots       │
│                         │
│ ┌─────────┐ ┌─────────┐ │
│ │Strategic│ │ Other   │ │
│ │  Bot    │ │  Bots   │ │
│ └────┬────┘ └────┬────┘ │
└──────┼───────────┼──────┘
       │           │
       ▼           ▼
┌─────────────────────────┐
│    ExchangeClientB0t    │
│                         │
│ ┌─────────────────────┐ │
│ │     CCXT Library    │ │
│ └─────────────────────┘ │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Cryptocurrency Exchanges│
│                         │
│ ┌───────┐ ┌───────────┐ │
│ │BitGet │ │ Binance   │ │
│ └───────┘ └───────────┘ │
└─────────────────────────┘
```

## Getting Started

### Prerequisites

- CCXT library: `pip install ccxt`
- API credentials for your target exchange

### Configuration

The ExchangeClientB0t can be configured through environment variables or constructor parameters:

| Environment Variable   | Description                               | Default   |
|------------------------|-------------------------------------------|-----------|
| EXCHANGE_ID            | CCXT exchange ID (e.g., 'bitget')         | 'bitget'  |
| EXCHANGE_API_KEY       | Exchange API key                          | None      |
| EXCHANGE_API_SECRET    | Exchange API secret                       | None      |
| EXCHANGE_API_PASSPHRASE| Exchange API passphrase (if required)     | None      |
| USE_TESTNET            | Whether to use testnet (true/false)       | 'true'    |

### Usage Examples

#### Basic Initialization

```python
from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t

# Initialize with environment variables
client = ExchangeClientB0t()

# Or with explicit parameters
client = ExchangeClientB0t(
    exchange_id="bitget",
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_password="your_passphrase",
    use_testnet=True
)

# Don't forget to initialize the client
await client.initialize()
```

#### Fetching Market Data

```python
# Get current ticker
ticker = await client.fetch_ticker("BTCUSDT")
print(f"Current BTC price: ${ticker['last']}")

# Get historical candles
candles = await client.fetch_ohlcv("BTCUSDT", timeframe="1h", limit=100)
for candle in candles:
    timestamp, open_price, high, low, close, volume = candle
    print(f"Time: {timestamp}, Close: {close}")
```

#### Trading Operations

```python
# Place a market buy order
order = await client.create_market_order(
    symbol="BTCUSDT",
    side="buy",
    amount=0.01  # BTC amount
)

# Place a limit sell order
order = await client.create_order(
    symbol="BTCUSDT",
    type="limit",
    side="sell",
    amount=0.01,
    price=50000.0
)

# Set leverage
result = await client.set_leverage("BTCUSDT", 3)

# Close a position
result = await client.close_position("BTCUSDT")
```

#### Fetching Account Information

```python
# Get account balance
balance = await client.fetch_balance()
print(f"USDT Balance: {balance['USDT']['free']}")

# Get open positions
positions = await client.fetch_positions("BTCUSDT")
for position in positions:
    print(f"Position: {position['side']} {position['contracts']} contracts")
```

#### Cleanup

```python
# Close the client when done
await client.close()
```

## Integration with Trading Bots

To integrate CCXT with a trading bot in the Omega Bot Farm:

1. Import the `ExchangeClientB0t` in your bot class:

```python
from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
```

2. Initialize the client in your bot's initialization:

```python
class MyTradingBot:
    def __init__(self):
        self.exchange = ExchangeClientB0t()
        
    async def start(self):
        await self.exchange.initialize()
        # Your trading logic here
```

3. Use the client for market operations in your bot's methods:

```python
async def analyze_market(self):
    ticker = await self.exchange.fetch_ticker("BTCUSDT")
    candles = await self.exchange.fetch_ohlcv("BTCUSDT")
    # Analyze data
    
async def execute_trade(self, signal):
    if signal == "buy":
        await self.exchange.create_market_order("BTCUSDT", "buy", 0.01)
    elif signal == "sell":
        await self.exchange.create_market_order("BTCUSDT", "sell", 0.01)
```

## Kubernetes Deployment

When deploying your trading bot with CCXT in Kubernetes, add these environment variables to your deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strategic-trader
  namespace: omega-bot-farm
spec:
  # ... other fields
  template:
    spec:
      containers:
      - name: strategic-trader
        image: omega-btc-ai/strategic-trader:latest
        env:
        - name: EXCHANGE_ID
          value: "bitget"
        - name: EXCHANGE_API_KEY
          valueFrom:
            secretKeyRef:
              name: exchange-credentials
              key: api-key
        - name: EXCHANGE_API_SECRET
          valueFrom:
            secretKeyRef:
              name: exchange-credentials
              key: api-secret
        - name: EXCHANGE_API_PASSPHRASE
          valueFrom:
            secretKeyRef:
              name: exchange-credentials
              key: passphrase
        - name: USE_TESTNET
          value: "false"  # Set to true for testing
```

## Supported Exchanges

CCXT supports over 120 cryptocurrency exchanges. The most commonly used with Omega Bot Farm include:

- BitGet
- Binance
- Bybit
- OKX
- Kucoin
- FTX

For the full list of supported exchanges, refer to the [CCXT documentation](https://github.com/ccxt/ccxt).

## Error Handling

The `ExchangeClientB0t` includes robust error handling:

- Methods return error dictionaries instead of raising exceptions
- Connection issues are logged and handled gracefully
- The client automatically checks if CCXT is installed

Example error handling:

```python
result = await client.create_market_order("BTCUSDT", "buy", 0.01)
if "error" in result:
    logging.error(f"Failed to place order: {result['error']}")
    # Handle error appropriately
else:
    logging.info(f"Order placed successfully: {result['id']}")
```

## Advanced Features

### Setting Custom Order Parameters

CCXT allows passing additional parameters to exchanges. For example, to place a post-only order:

```python
order = await client.create_order(
    symbol="BTCUSDT",
    type="limit",
    side="buy",
    amount=0.01,
    price=48000.0,
    params={"postOnly": True}
)
```

### Working with Multiple Exchanges

The `ExchangeClientB0t` can be initialized with different exchange IDs:

```python
# BitGet client
bitget_client = ExchangeClientB0t(exchange_id="bitget")

# Binance client
binance_client = ExchangeClientB0t(exchange_id="binance")
```

## Troubleshooting

Common issues and solutions:

1. **CCXT not installed**
   - Error: "CCXT library not installed. Exchange functionality will be limited."
   - Solution: Run `pip install ccxt` in your container

2. **Authentication failures**
   - Error: "Error initializing exchange: AuthenticationError"
   - Solution: Verify your API key, secret, and passphrase are correct

3. **Symbol format issues**
   - Error: "Error creating order: ExchangeError: market does not exist"
   - Solution: Check that your symbol formatting is correct for the exchange

4. **Rate limiting**
   - Error: "Error fetching ticker: DDoSProtection"
   - Solution: Add delay between API calls and use enableRateLimit=True

## Contributing

To extend or improve the CCXT integration:

1. Update the `ExchangeClientB0t` class with new methods
2. Add thorough error handling
3. Document new functionality
4. Write tests for the new functionality

## References

- [CCXT Official Documentation](https://github.com/ccxt/ccxt/wiki)
- [BitGet API Documentation](https://bitgetlimited.github.io/apidoc/en/mix/)
- [CCXT Exchange List](https://github.com/ccxt/ccxt#supported-cryptocurrency-exchange-markets)
