
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


# Bitget Futures API Guide for AI-Driven Trading Bots

## 1. Introduction to Bitget Futures API

The Bitget platform offers a comprehensive suite of cryptocurrency trading services, with a significant focus on futures trading, all of which are accessible through a well-documented Application Programming Interface (API). This API is specifically designed to facilitate programmatic interaction with the exchange, enabling developers to build automated trading systems, perform detailed data acquisition, and integrate various services such as copy trading functionalities.

Within its futures trading offerings, Bitget supports three distinct product types:

- **USDT-M Futures**: Contracts are margined and settled in USDT
- **USDC-M Futures**: Contracts with margin and settlement in USDC
- **Coin-M Futures**: Utilize the underlying cryptocurrency as margin and for settlement

Bitget provides dedicated demo trading environments for each of these contract types, identified by the prefixes 'S' for simulated trading: SUSDT-FUTURES, SCOIN-FUTURES, and SUSDC-FUTURES. Every Bitget account is provisioned with demo coins, and users can leverage the Account List API, specifying these demo product types, to check their simulated balances.

The Bitget API's capabilities extend to program trading and data acquisition, directly aligning with the requirements for building automated trading bots driven by advanced AI models. The API documentation is logically organized into key sections such as Market, Account, Position, Trade, Trigger Order, and Websocket.

**Key Insights:**

- The variety in contract types allows for strategic selection based on the desired exposure to specific stablecoins or cryptocurrencies
- The simulated trading environment is invaluable for testing and refining AI models without risking actual capital
- The explicit mention of "program trading" suggests that Bitget anticipates and supports algorithmic trading strategies

## 2. Getting Started with the API

The initial step towards utilizing the Bitget Futures API for automated trading involves obtaining and managing the necessary API keys. This process begins with logging into a Bitget account via the web interface, after which users can navigate to the API Key Management section located within their user center.

Users can apply for and create API keys, with each Bitget User ID (UID) capable of generating up to 10 distinct API keys. A significant security feature is the ability to configure permissions for each API key, allowing for either read-only access, suitable for data retrieval, or read/write access, which is essential for a trading bot to execute trades.

During the API key creation process, users are prompted to set a Passphrase, which acts as an additional layer of security. It is critical to securely store this Passphrase, as it cannot be retrieved if forgotten, necessitating the recreation of the API key.

Accessing the Bitget API involves different authentication mechanisms:

- The **public interface** (configuration information and market data) does not require authentication
- The **private interface** (order and account management) mandates that every request be digitally signed

For REST API requests that require authentication, specific HTTP headers must be included:

- `ACCESS-KEY`: The API Key itself
- `ACCESS-SIGN`: The generated signature
- `ACCESS-TIMESTAMP`: Timestamp of the request in milliseconds since the Epoch
- `ACCESS-PASSPHRASE`: The user-defined Passphrase
- For all POST requests, the `Content-Type` header must be set to `application/json`

Bitget provides Software Development Kits (SDKs) such as the python-bitget library, available for installation using pip: `pip install python-bitget`.

**Key Insights:**

- Creating multiple API keys with granular permissions is a vital security best practice
- The non-retrievable nature of the Passphrase underscores the importance of secure storage
- Binding API keys to specific IP addresses significantly reduces the risk of unauthorized access
- The availability of a well-maintained Python SDK significantly simplifies the process of interacting with the Bitget API

## 3. Core Trading Operations (REST API)

The Bitget Futures API provides a comprehensive set of functionalities for managing trading activities through its RESTful interface.

### Placing Orders

Endpoint: `/api/mix/v1/order/placeOrder` or `/api/v2/mix/order/place-order`

Required parameters:

- `symbol`: Trading pair symbol
- `marginCoin`: Currency used for margin
- `size`: Order size
- `side`: Direction of the order (e.g., open_long, open_short, close_long, close_short)
- `orderType`: Either limit or market

Optional parameters:

- `price`: For limit orders
- `timeInForceValue`: Controls how long the order remains active (e.g., normal, post_only, fok, ioc)
- `clientOid`: Unique client-generated order ID
- `reduceOnly`: Relevant in 'single_hold' mode to ensure that the order only reduces an existing position
- Preset take-profit and stop-loss prices

Rate limit: 10 requests per second per User ID (UID), with a stricter limit of 1 request per second for traders.

### Cancelling Orders

Endpoint: `/api/mix/v1/order/cancel-order` or `/api/v2/mix/order/cancel-order`

Required parameters:

- `symbol`: Trading pair symbol
- `marginCoin`: Currency used for margin
- Either `orderId` or `clientOid`

For batch cancellation: `/api/mix/v1/order/batch-cancel-orders`
For cancelling all open orders for a specific trading symbol: `/api/mix/v1/order/cancel-all-orders`

Rate limit: 10 requests per second per UID.

### Modifying Orders

Endpoint: `/api/mix/v1/order/modifyOrder` or `/api/v2/mix/order/modify-order`

Required parameters:

- Either `orderId` or `clientOid`
- `symbol`: Trading pair symbol
- `newClientOid`: Mandatory when modifying size or price

Optional parameters:

- `size`, `price`, `presetTakeProfitPrice`, `presetStopLossPrice`

Important note: Changing the size or price will result in the cancellation of the original order and the asynchronous placement of a new order.

Rate limit: 10 requests per second per UID.

### Advanced Order Types

#### Plan Orders (Trigger Orders)

Endpoint: `/api/mix/v1/plan/placePlan` or `/api/v2/mix/order/place-plan-order`

Key parameters:

- `symbol`, `marginCoin`, `size`
- Optional `executePrice` (not required for market orders)
- `triggerPrice`: Activates the order
- `side`: Direction
- `orderType`: limit or market
- `triggerType`: Whether the trigger is based on the market_price or the fill_price

Modification: `/api/mix/v1/plan/modifyPlan` or `/api/v2/mix/order/modify-plan-order`
Cancellation: `/api/mix/v1/plan/cancelPlan` or `/api/v2/mix/order/cancel-plan-order`

#### Stop Orders (Take-Profit and Stop-Loss)

Endpoint: `/api/mix/v1/plan/placeTPSL` or `/api/v2/mix/order/place-tpsl-order`

Essential parameters:

- `symbol`, `marginCoin`
- `planType`: Either "profit_plan" for take-profit or "loss_plan" for stop-loss
- `triggerPrice`
- `holdSide`: Whether the position is "long" or "short"

Trailing stop orders: `/api/mix/v1/plan/placeTrailStop`
Position-level TP/SL: `/api/mix/v1/plan/placePositionsTPSL`

**Key Insights:**

- The granularity of order placement parameters allows for the implementation of various trading strategies
- The clientOid parameter is important for ensuring that the same order is not placed multiple times
- Rate limits require careful consideration in the design of the AI model and the bot's execution logic
- The asynchronous nature of modifying the price or size of an order is a critical detail for the bot's logic
- Plan orders are invaluable for implementing strategies that aim to enter or exit positions at predetermined price levels
- The availability of trailing stop orders offers an advanced risk management technique

## 4. Market Data Feeds (REST & WebSocket API)

For AI-driven trading bots, access to both real-time and historical market data is crucial.

### WebSocket API Channels

The WebSocket API is well-suited for real-time market data delivery due to its efficiency and low latency.

Public channels:

- **Tickers**: Latest traded price, best bid and ask prices, and 24-hour trading volume (updated every 150ms)
- **Candlesticks**: OHLCV data for various time intervals (updated every 500ms)
- **Order Book**: Real-time order book data at different levels of depth (updated every 100-200ms)
- **Trades**: Data about recently executed trades as they occur
- **New Trades**: Initial snapshot of 50 recent trades, followed by real-time updates

Private channels (requiring authentication):

- Real-time updates on account information, positions, orders, and plan orders

### REST API for Historical Data

REST endpoints for historical data:

- `/api/mix/v1/market/candles` or `/api/v2/mix/market/candles`
- `/api/mix/v1/market/history-candles` or `/api/v2/mix/market/history-candles`
- `/api/mix/v1/market/fills-history` or `/api/v2/mix/market/fills-history`
- `/api/mix/v1/market/history-index-candles` or `/api/v2/mix/market/history-index-candles`
- `/api/mix/v1/market/history-mark-candles` or `/api/v2/mix/market/history-mark-candles`
- `/api/mix/v1/market/history-fund-rate` or `/api/v2/mix/market/history-fund-rate`

### Contract Specifications

Endpoints for contract information:

- `/api/mix/v1/market/contracts` or `/api/v2/mix/market/contracts`
- `/api/mix/v1/market/symbol-leverage` or `/api/v2/mix/market/query-position-lever`
- `/api/mix/v1/market/queryPositionLever` or `/api/v2/mix/market/query-position-lever`
- `/api/mix/v1/market/open-limit`

**Key Insights:**

- Lower latency of WebSocket is essential for AI models that need to react quickly to market movements
- The availability of diverse WebSocket channels caters to the varying data requirements of different AI trading strategies
- Historical market data is fundamental for training and backtesting AI trading models
- Programmatically accessing contract specifications is essential for the trading bot to correctly interpret market data

## 5. Account and Position Management (REST API)

For an AI-powered trading bot to function effectively, it must have the ability to access and manage account information and trading positions.

### Account Balances

Endpoints:

- `/api/mix/v1/account/account` or `/api/v2/mix/account/account`: Asset information for a single futures account
- `/api/mix/v1/account/accounts` or `/api/v2/mix/account/accounts`: Asset information for all futures accounts
- `/api/mix/v1/account/sub-account-assets` or `/api/v2/mix/account/sub-account-assets`: Asset information for sub-accounts
- `/api/mix/v1/account/bill` or `/api/v2/mix/account/bill`: Detailed history of all account transactions

### Position Information

Endpoints:

- `/api/mix/v1/position/single-position` or `/api/v2/mix/position/single-position`: Information for a specific open position
- `/api/mix/v1/position/all-position` or `/api/v2/mix/position/all-position`: Information for all currently open positions
- `/api/mix/v1/position/history-position` or `/api/v2/mix/position/history-position`: Historical position data

### Risk Parameter Management

Endpoints:

- `/api/mix/v1/account/set-leverage` or `/api/v2/mix/account/set-leverage`: Change the leverage for a specific trading symbol
- `/api/mix/v1/account/set-margin` or `/api/v2/mix/account/set-margin`: Adjust the margin allocated to a specific position
- `/api/mix/v1/account/set-auto-margin` or `/api/v2/mix/account/set-auto-margin`: Toggle automatic margin supplement
- `/api/mix/v1/account/set-margin-mode` or `/api/v2/mix/account/set-margin-mode`: Switch between different margin modes
- `/api/mix/v1/account/set-position-mode` or `/api/v2/mix/account/set-position-mode`: Change the position mode

**Key Insights:**

- Monitoring account balances is fundamental for ensuring sufficient margin
- Access to sub-account balances is useful for employing different strategies across multiple accounts
- The account bill provides an essential audit trail of all trading activities
- Knowing the current open positions is vital for tracking market exposure and making informed decisions
- Programmatic control over leverage allows the AI model to dynamically adjust its risk exposure

## 6. API Limitations and Best Practices

When developing an AI-powered trading bot, it is crucial to be aware of API limitations and to adhere to recommended best practices.

### Rate Limits

- Overall rate limit for the REST API: 6000 requests per IP address per minute
- Place Order endpoint: 10 requests per second per UID
- Public market information interfaces: 20 requests per second per IP address
- Exceeding frequency limits results in HTTP status code 429 ("Too Many Requests")

### Error Handling

- Standard HTTP status codes: 200 (success), 4xx and 5xx (errors)
- Common error codes: 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 429 (Too Many Requests), 500 (Internal Server Error)
- API response body includes specific error information with "code" and "msg" fields

### Security Best Practices

- Enable two-factor authentication (2FA) on the Bitget account
- Set up Fund code and PIN code for additional security
- Store API Key, Secret Key, and Passphrase securely (avoid hardcoding)
- Grant only necessary permissions for the bot's intended trading activities
- Regularly rotate API keys
- Monitor API key usage for suspicious activity
- Bind API keys to specific IP addresses
- Use HTTPS for all communication with the Bitget API

**Key Insights:**

- The bot needs to manage its request frequency for different functionalities separately
- The combination of HTTP status codes and specific error codes offers a detailed way to diagnose and handle API errors
- Implementing security measures diligently is crucial for protecting the user's account and funds

## 7. Utilizing the WebSocket API for Real-time Trading

For AI-powered trading bots that require immediate access to market data and low-latency updates, the Bitget WebSocket API offers a powerful solution.

### Connection and Authentication

- The Bitget API documentation provides detailed instructions on initiating a WebSocket connection
- For private channels, authentication is required
- A "ping/pong" mechanism is recommended to ensure the connection remains active

### Channel Subscription

Public channels (no authentication required):

- `ticker`: Real-time price updates
- `candle`: Streaming candlestick data
- `depth`: Real-time order book updates
- `trades`: Information on recently executed trades

Private channels (authentication required):

- `account`: Balance changes
- `positions`: Updates on open positions
- `orders`: Real-time order status changes
- `planOrder`: Notifications related to triggered or modified plan orders

**Key Insights:**

- The ability to selectively subscribe to only the necessary channels minimizes bandwidth usage
- The separation of public and private channels ensures market data can be accessed efficiently
- The bot's architecture must be designed to efficiently handle the continuous stream of data and events

## 8. Considerations for AI Model Integration

Integrating an advanced AI model with the Bitget Futures API requires careful consideration of several key aspects.

### Data Requirements

- Historical market data for training (time series data on price, volume, order book, etc.)
- Real-time market data via WebSocket API for making informed trading decisions
- Account and position data for monitoring performance and managing risk

### Latency Considerations

- WebSocket API for high-frequency trading models requiring immediate reaction
- REST API for less time-sensitive operations (e.g., fetching historical data, placing conditional orders)

### Order Execution Logic

- Translation of AI model's trading signals into actionable API calls
- Handling different order types (market, limit, plan, stop)
- Error handling for potential API errors

### Risk Management

- Setting limits on position sizes
- Utilizing stop-loss orders
- Managing leverage
- Dynamically adjusting risk parameters based on market conditions

**Key Insights:**

- The Bitget API provides access to all necessary data types for AI trading
- The trading bot serves as the mechanism to enforce risk controls programmatically
- The AI model can potentially adapt its risk parameters based on real-time data

## 9. Conclusion and Recommendations

The Bitget Futures API presents a comprehensive platform for developing sophisticated AI-powered trading bots, with strengths in its extensive set of endpoints, support for various futures contract types, robust order management capabilities, wealth of market data, and features for managing risk parameters.

### Recommendations

1. Thoroughly familiarize yourself with the Bitget Futures API documentation
2. Leverage the official Python SDK (python-bitget) to streamline API interactions
3. Implement robust error handling and logging mechanisms
4. Pay close attention to API rate limits and design the bot's API call frequency accordingly
5. Prioritize the security of your Bitget account and API keys
6. Utilize the demo trading environment extensively during development and testing
7. For low-latency trading strategies, utilize the WebSocket API
8. Design the bot's order execution logic to accurately translate the AI model's trading signals
9. Integrate the risk management features provided by the Bitget API
10. Continuously monitor the bot's performance and API usage after deployment

**Important Note**: Always verify that you're using the correct endpoint structure, particularly for futures trading which requires the `/mix` prefix in most endpoints.
