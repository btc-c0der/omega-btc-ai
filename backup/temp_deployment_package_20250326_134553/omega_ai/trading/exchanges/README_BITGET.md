
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


# OMEGA BTC AI - BitGet Integration

![BitGet Integration](https://img.shields.io/badge/BitGet-Integration-52b788?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADWSURBVHgBrVNbDsFAFJ1JS3yCn4ifSkRYAR+srsTHd1dhB9iBHaywArEDgxdxkzYz7cykZoL4OMnNzD333HM7twC/QMn7KYKDwkPDQcHASkgI2oFL6OEGAhsMGUFwN6BIovFjpOUdO4eIdPwQMdLJPNZs3YnmrGLFBlPJspth5HxZ5QVqkJG7gK7rDTyfj0iKYzSgeOITDlCDdguKaZqw2+0Tz0GxXdvG8/LKtePIWGJll9AlDV2U0yTb7TSu9xdpsysEGjB37vGKikNEJkPtf+QcZ9pGzn+QvwG14CvkQBnwYgAAAABJRU5ErkJggg==)

## Overview

The BitGet integration for OMEGA BTC AI provides a robust interface for automated trading on the BitGet exchange. This integration supports both testnet and mainnet environments, offering a comprehensive set of features for position management, risk control, and market analysis.

## Features

### Core Trading Capabilities

- Market and limit order execution
- Position management with stop-loss and take-profit levels
- Multiple order types (market, limit, post_only, FOK, IOC)
- Support for both testnet and mainnet environments
- Real-time position tracking and PnL calculation

### Risk Management

- Dynamic position sizing based on account balance
- Configurable leverage settings
- Stop-loss and take-profit management
- Margin mode selection (crossed/isolated)
- Risk parameter customization per trader profile

### Market Data Access

- Real-time ticker data
- Order book depth analysis
- Recent trades history
- Position risk information
- Account balance monitoring

## Installation

1. Add BitGet API credentials to your `.env` file:

```bash
# Testnet
BITGET_TESTNET_API_KEY=your_testnet_api_key
BITGET_TESTNET_SECRET_KEY=your_testnet_secret_key
BITGET_TESTNET_PASSPHRASE=your_testnet_passphrase

# Mainnet
BITGET_MAINNET_API_KEY=your_mainnet_api_key
BITGET_MAINNET_SECRET_KEY=your_mainnet_secret_key
BITGET_MAINNET_PASSPHRASE=your_mainnet_passphrase
```

2. Import the BitGet trader in your code:

```python
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
```

## Usage

### Basic Setup

```python
# Initialize the BitGet trader with a specific profile
trader = BitGetTrader(
    profile_type="strategic",  # Options: strategic, aggressive, newbie, scalper
    api_key="your_api_key",
    secret_key="your_secret_key",
    passphrase="your_passphrase",
    use_testnet=True,  # Set to False for mainnet
    initial_capital=10000.0
)
```

### Placing Orders

```python
# Place a market order
order_response = trader.place_order(
    symbol="BTCUSDT_UMCBL",
    side="BUY",
    order_type="MARKET",
    quantity=0.01,
    leverage="20"
)

# Place a limit order
limit_order = trader.place_order(
    symbol="BTCUSDT_UMCBL",
    side="SELL",
    order_type="LIMIT",
    price=50000.0,
    quantity=0.01,
    leverage="20"
)
```

### Position Management

```python
# Get current positions
positions = trader.get_positions()

# Get position risk information
risk_info = trader.get_position_risk()

# Close a position
close_response = trader.close_position(
    symbol="BTCUSDT_UMCBL",
    side="LONG"
)
```

### Market Data

```python
# Get current ticker
ticker = trader.get_market_ticker("BTCUSDT_UMCBL")

# Get order book
orderbook = trader.get_orderbook("BTCUSDT_UMCBL", limit=100)

# Get recent trades
recent_trades = trader.get_recent_trades("BTCUSDT_UMCBL", limit=100)
```

## Trader Profiles

The BitGet integration supports multiple trader profiles, each with its own risk parameters and trading strategy:

1. **Strategic Trader**
   - Balanced risk approach
   - Focus on trend following
   - Moderate leverage usage

2. **Aggressive Trader**
   - Higher risk tolerance
   - Quick profit taking
   - Higher leverage usage

3. **Newbie Trader**
   - Conservative approach
   - Strict risk management
   - Lower leverage usage

4. **Scalper Trader**
   - Short-term trades
   - Quick entries and exits
   - Variable leverage based on volatility

## Error Handling

The integration includes comprehensive error handling for:

- API connection issues
- Invalid order parameters
- Insufficient balance
- Rate limiting
- Network timeouts

## Best Practices

1. **Testnet First**
   - Always test strategies on testnet before mainnet
   - Use testnet API keys for development
   - Validate risk parameters in a safe environment

2. **Risk Management**
   - Start with conservative position sizes
   - Use stop-loss orders for every trade
   - Monitor leverage levels carefully
   - Keep track of total exposure

3. **API Usage**
   - Implement rate limiting in your application
   - Cache market data when appropriate
   - Handle API errors gracefully
   - Monitor API key permissions

## Support

For issues related to the BitGet integration:

1. Check the [BitGet API Documentation](https://bitgetlimited.github.io/apidoc/en/spot)
2. Review the error messages in the logs
3. Contact the OMEGA BTC AI team for support

## Disclaimer

Trading cryptocurrencies carries significant risk. This integration is provided as-is without any guarantees. Always:

- Test thoroughly on testnet
- Start with small position sizes
- Monitor your positions actively
- Keep your API keys secure
- Never share your secret keys or passphrase

## Community & Support

### OMEGA BTC AI Community

- 🔗 [Discord Server](https://discord.gg/omega-btc-ai) - Real-time trade sharing and community discussions
- 🔗 [Telegram Channel](https://t.me/omega_btc_ai) - Instant alerts and market updates
- 🔗 [Twitter](https://twitter.com/omega_btc_ai) - Latest updates and trading insights
- 🔗 [GitHub Discussions](https://github.com/yourusername/omega-btc-ai/discussions) - Technical discussions and feature requests

### API Debug Reference Table

| Error Code | Description | Common Causes | Solution |
|------------|-------------|---------------|-----------|
| 40001 | Invalid API Key | Incorrect API key format or expired key | Check API key validity and format |
| 40002 | Invalid Signature | Incorrect signature generation | Verify timestamp and signature calculation |
| 40003 | Invalid Timestamp | Server time mismatch | Sync system time with NTP |
| 40004 | Invalid Request | Malformed request parameters | Check parameter types and values |
| 40005 | Rate Limit Exceeded | Too many requests | Implement request throttling |
| 40006 | Insufficient Balance | Not enough funds for order | Check account balance |
| 40007 | Invalid Leverage | Leverage value out of range | Verify leverage limits |
| 40008 | Invalid Order Type | Unsupported order type | Check order type documentation |
| 40009 | Invalid Symbol | Trading pair not supported | Verify symbol format |
| 40010 | Position Not Found | Position doesn't exist | Check position ID/status |

### Quick Debug Tips

1. **API Connection Issues**

   ```python
   # Test API connection
   try:
       trader = BitGetTrader(use_testnet=True)
       balance = trader.get_account_balance()
       print("Connection successful!")
   except Exception as e:
       print(f"Connection failed: {str(e)}")
   ```

2. **Signature Verification**

   ```python
   # Verify signature generation
   timestamp = str(int(time.time() * 1000))
   signature = trader._generate_signature(timestamp, "GET", "/api/account/balance")
   print(f"Generated signature: {signature}")
   ```

3. **Rate Limit Monitoring**

   ```python
   # Monitor rate limits
   response_headers = trader._make_request("GET", "/api/account/balance")
   remaining_requests = response_headers.get("X-RateLimit-Remaining")
   print(f"Remaining requests: {remaining_requests}")
   ```

### Community Guidelines

1. **Trade Sharing**
   - Use the `#trades` channel for sharing successful trades
   - Include entry/exit points and reasoning
   - Tag your profile type (e.g., `#strategic`, `#scalper`)

2. **Knowledge Exchange**
   - Share your trading strategies in `#strategies`
   - Discuss market analysis in `#analysis`
   - Ask technical questions in `#support`

3. **Code Sharing**
   - Share code snippets in `#code-snippets`
   - Use code blocks with proper formatting
   - Include context and explanation

### Getting Help

1. **Technical Support**
   - Check the [BitGet API Documentation](https://bitgetlimited.github.io/apidoc/en/spot)
   - Review the error messages in the logs
   - Search existing GitHub issues
   - Post in the Discord `#support` channel

2. **Trading Support**
   - Join strategy discussions in Discord
   - Share your trading journal
   - Get feedback from experienced traders
   - Participate in weekly trading reviews

Remember: The OMEGA BTC AI community is built on mutual respect and knowledge sharing. Always be helpful and constructive in your interactions!

## API Authentication and Signature Generation

### Updated Signature Generation

BitGet API requires a specific signature format for authentication. We've updated the signature generation code to follow BitGet's documentation more precisely:

```python
def generate_signature(secret_key, timestamp, method, request_path, body=None, params=None):
    """
    Generate BitGet API signature.
    
    Args:
        secret_key: Your API secret key
        timestamp: Timestamp in milliseconds
        method: HTTP method (GET, POST, etc.)
        request_path: API endpoint path
        body: Request body for POST requests
        params: Query parameters for GET requests
        
    Returns:
        Base64 encoded signature
    """
    # Ensure method is uppercase
    method = method.upper()
    
    # Start with timestamp + method + requestPath
    message = str(timestamp) + method + request_path
    
    # Add query string if present (for GET requests)
    if params and method == "GET":
        # Sort parameters by key
        sorted_params = sorted(params.items())
        # Create query string
        query_string = "&".join([f"{key}={value}" for key, value in sorted_params])
        # Add to message with question mark
        message += "?" + query_string
    
    # Add body for POST requests
    if body and method == "POST":
        if isinstance(body, dict):
            message += json.dumps(body)
        else:
            message += body
    
    # Create signature using HMAC-SHA256
    signature = base64.b64encode(
        hmac.new(
            secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode("utf-8")
    
    return signature
```

### Common API Authentication Issues

If you encounter `sign signature error` when working with BitGet API, check the following:

1. **API Key Permissions**: Ensure your API key has the correct permissions (read/trade/transfer)
2. **Parameter Order**: BitGet requires parameters to be sorted alphabetically by key
3. **Method Capitalization**: HTTP method must be uppercase (GET, POST, etc.)
4. **Timestamp Format**: Must be in milliseconds since epoch
5. **Query String Format**: For GET requests, parameters must be included in the signature with a `?` prefix
6. **Network Selection**: Make sure you're using the correct network (testnet vs. mainnet)

### Debugging Tools

We've added a debugging tool at `omega_ai/scripts/debug/bitget_signature_test.py` to help with API authentication issues. This tool:

- Compares different signature generation methods
- Tests basic API endpoints
- Provides detailed request/response information

To use it:

```bash
python omega_ai/scripts/debug/bitget_signature_test.py --testnet
```

See the [debugging tools README](../../scripts/debug/README.md) for more details.
