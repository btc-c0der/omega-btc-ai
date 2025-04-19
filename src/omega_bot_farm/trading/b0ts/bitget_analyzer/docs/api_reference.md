
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


# BitGet Position Analyzer Bot API Reference

This document provides a comprehensive reference for all methods, properties, and functionality of the BitGet Position Analyzer Bot.

## Table of Contents

- [Initialization](#initialization)
- [Core Methods](#core-methods)
- [Position Analysis](#position-analysis)
- [Fibonacci Analysis](#fibonacci-analysis)
- [Harmony Calculations](#harmony-calculations)
- [Portfolio Management](#portfolio-management)
- [Account Statistics](#account-statistics)
- [Utility Methods](#utility-methods)
- [Error Handling](#error-handling)
- [Response Objects](#response-objects)

## Initialization

### Constructor

```python
BitgetPositionAnalyzerB0t(
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    api_passphrase: Optional[str] = None,
    use_testnet: bool = False,
    position_history_length: int = 10
)
```

**Parameters:**

- `api_key` (Optional[str]): BitGet API key. If None, will use BITGET_API_KEY environment variable.
- `api_secret` (Optional[str]): BitGet API secret. If None, will use BITGET_SECRET_KEY environment variable.
- `api_passphrase` (Optional[str]): BitGet API passphrase. If None, will use BITGET_PASSPHRASE environment variable.
- `use_testnet` (bool): Whether to use BitGet testnet. Default is False.
- `position_history_length` (int): Number of position snapshots to keep in history. Default is 10.

**Example:**

```python
# Using environment variables
analyzer = BitgetPositionAnalyzerB0t(use_testnet=True)

# Using explicit credentials
analyzer = BitgetPositionAnalyzerB0t(
    api_key="your_api_key",
    api_secret="your_api_secret",
    api_passphrase="your_passphrase",
    use_testnet=True,
    position_history_length=15
)
```

## Core Methods

### get_positions

```python
async def get_positions() -> Dict[str, Any]
```

Fetches current positions from BitGet exchange.

**Returns:**
A dictionary containing:

- `success` (bool): Whether the request was successful
- `positions` (List[Dict]): List of current positions
- `timestamp` (str): Current timestamp
- `connection` (str): Connection status
- `changes` (Dict): Position changes since last check
- `account` (Dict): Account statistics

**Example:**

```python
positions = await analyzer.get_positions()
print(f"Found {len(positions['positions'])} active positions")
```

### analyze_position

```python
def analyze_position(position: Dict[str, Any]) -> Dict[str, Any]
```

Analyzes a single position for risk, harmony, and Fibonacci levels.

**Parameters:**

- `position` (Dict[str, Any]): The position to analyze

**Returns:**
A dictionary containing:

- `position_id` (str): Position identifier
- `symbol` (str): Trading symbol
- `side` (str): Position side (long or short)
- `size` (float): Position size
- `entry_price` (float): Average entry price
- `current_price` (float): Current market price
- `unrealized_pnl` (float): Unrealized profit/loss
- `risk_level` (str): Position risk level (Low, Medium, High)
- `risk_score` (float): Numerical risk score (0-100)
- `harmony_score` (float): Position harmony score (0-1)
- `fibonacci_levels` (Dict): Relevant Fibonacci levels
- `recommendations` (List): List of recommendations

**Example:**

```python
positions = await analyzer.get_positions()
if positions["positions"]:
    analysis = analyzer.analyze_position(positions["positions"][0])
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"Harmony Score: {analysis['harmony_score']}")
```

## Position Analysis

### analyze_all_positions

```python
def analyze_all_positions(positions: List[Dict[str, Any]]) -> Dict[str, Any]
```

Analyzes all positions for portfolio-wide insights.

**Parameters:**

- `positions` (List[Dict[str, Any]]): List of positions to analyze

**Returns:**
A dictionary containing:

- `total_positions` (int): Total number of positions
- `long_positions` (int): Number of long positions
- `short_positions` (int): Number of short positions
- `total_exposure` (float): Total position exposure
- `long_exposure` (float): Long position exposure
- `short_exposure` (float): Short position exposure
- `long_short_ratio` (float): Ratio of long to short exposure
- `highest_risk_position` (Dict): Position with highest risk
- `overall_risk_score` (float): Overall portfolio risk score
- `overall_harmony_score` (float): Overall portfolio harmony score
- `portfolio_recommendations` (List): List of portfolio-wide recommendations

**Example:**

```python
positions = await analyzer.get_positions()
portfolio_analysis = analyzer.analyze_all_positions(positions["positions"])
print(f"Long/Short Ratio: {portfolio_analysis['long_short_ratio']}")
print(f"Overall Harmony: {portfolio_analysis['overall_harmony_score']}")
```

### _detect_position_changes

```python
def _detect_position_changes(positions: List[Dict[str, Any]]) -> Dict[str, Any]
```

Detects changes in positions since the last check.

**Parameters:**

- `positions` (List[Dict[str, Any]]): Current positions

**Returns:**
A dictionary containing:

- `new_positions` (List[Dict]): Newly opened positions
- `closed_positions` (List[Dict]): Recently closed positions
- `modified_positions` (List[Dict]): Positions with changes in size or leverage
- `unchanged_positions` (List[Dict]): Positions without changes

**Example:**

```python
positions = await analyzer.get_positions()
changes = analyzer._detect_position_changes(positions["positions"])
print(f"New positions: {len(changes['new_positions'])}")
print(f"Closed positions: {len(changes['closed_positions'])}")
```

## Fibonacci Analysis

### generate_fibonacci_levels

```python
def generate_fibonacci_levels(
    high_price: float,
    low_price: float,
    current_price: float = None,
    extended_levels: bool = False
) -> Dict[str, Dict[str, float]]
```

Generates Fibonacci retracement and extension levels for a price range.

**Parameters:**

- `high_price` (float): The highest price in the range
- `low_price` (float): The lowest price in the range
- `current_price` (float, optional): The current price. If None, will not calculate relative position.
- `extended_levels` (bool): Whether to include extended Fibonacci levels. Default is False.

**Returns:**
A dictionary containing:

- `retracements` (Dict[str, float]): Fibonacci retracement levels
- `extensions` (Dict[str, float]): Fibonacci extension levels
- `current_level` (str, optional): Current price relative to Fibonacci levels
- `next_support` (float, optional): Next support level based on current price
- `next_resistance` (float, optional): Next resistance level based on current price

**Example:**

```python
fib_levels = analyzer.generate_fibonacci_levels(
    high_price=50000,
    low_price=40000,
    current_price=45000,
    extended_levels=True
)

print("Retracement Levels:")
for level, price in fib_levels["retracements"].items():
    print(f"{level}: ${price}")
```

### identify_fibonacci_patterns

```python
def identify_fibonacci_patterns(
    price_data: List[float],
    window_size: int = 100
) -> List[Dict[str, Any]]
```

Identifies Fibonacci patterns in historical price data.

**Parameters:**

- `price_data` (List[float]): Historical price data
- `window_size` (int): Window size for pattern detection. Default is 100.

**Returns:**
A list of dictionaries containing:

- `pattern_type` (str): The type of pattern detected
- `start_index` (int): Start index of the pattern
- `end_index` (int): End index of the pattern
- `strength` (float): Pattern strength score
- `levels` (Dict): Fibonacci levels for the pattern

**Example:**

```python
# Get historical price data
price_data = [/* historical prices */]

# Identify patterns
patterns = analyzer.identify_fibonacci_patterns(price_data)
for pattern in patterns:
    print(f"Pattern: {pattern['pattern_type']}, Strength: {pattern['strength']}")
```

## Harmony Calculations

### calculate_position_harmony

```python
def calculate_position_harmony(positions: List[Dict[str, Any]]) -> float
```

Calculates the harmony score for a set of positions based on golden ratio principles.

**Parameters:**

- `positions` (List[Dict[str, Any]]): List of positions

**Returns:**
A float representing the harmony score (0-1), where 1 is perfect harmony.

**Example:**

```python
positions = await analyzer.get_positions()
harmony_score = analyzer.calculate_position_harmony(positions["positions"])
print(f"Position Harmony Score: {harmony_score:.2f}")
```

### _calculate_harmony_score

```python
def _calculate_harmony_score() -> float
```

Calculates the overall harmony score based on current account metrics.

**Returns:**
A float representing the harmony score (0-1).

**Example:**

```python
positions = await analyzer.get_positions()
harmony_score = positions["account"]["harmony_score"]
print(f"Account Harmony Score: {harmony_score:.2f}")
```

## Portfolio Management

### generate_portfolio_recommendations

```python
def generate_portfolio_recommendations() -> List[Dict[str, Any]]
```

Generates recommendations for portfolio adjustments based on current positions and harmony principles.

**Returns:**
A list of dictionaries containing:

- `action` (str): Recommended action (buy, sell, hold)
- `symbol` (str): Trading symbol
- `amount` (float): Recommended amount
- `price` (float, optional): Recommended price
- `reason` (str): Reason for the recommendation
- `priority` (int): Recommendation priority (1-10)

**Example:**

```python
recommendations = analyzer.generate_portfolio_recommendations()
for rec in recommendations:
    print(f"{rec['action'].upper()} {rec['symbol']} - {rec['reason']}")
```

### calculate_optimal_position_size

```python
def calculate_optimal_position_size(
    symbol: str,
    account_balance: float,
    risk_percentage: float = 1.0,
    leverage: float = 1.0
) -> Dict[str, float]
```

Calculates the optimal position size based on account balance and risk parameters.

**Parameters:**

- `symbol` (str): Trading symbol
- `account_balance` (float): Current account balance
- `risk_percentage` (float): Percentage of balance to risk. Default is 1.0.
- `leverage` (float): Position leverage. Default is 1.0.

**Returns:**
A dictionary containing:

- `position_size` (float): Optimal position size in base currency
- `contract_size` (float): Position size in contracts
- `risk_amount` (float): Amount at risk
- `max_loss` (float): Maximum potential loss
- `liquidation_price` (float, optional): Estimated liquidation price

**Example:**

```python
optimal_size = analyzer.calculate_optimal_position_size(
    symbol="BTCUSDT",
    account_balance=10000,
    risk_percentage=2.0,
    leverage=3.0
)
print(f"Optimal Position Size: {optimal_size['position_size']} BTC")
print(f"Contract Size: {optimal_size['contract_size']} contracts")
```

## Account Statistics

### update_account_statistics

```python
def update_account_statistics() -> Dict[str, float]
```

Updates and returns current account statistics.

**Returns:**
A dictionary containing:

- `balance` (float): Account balance
- `equity` (float): Account equity
- `available` (float): Available balance
- `margin` (float): Used margin
- `unrealized_pnl` (float): Unrealized profit/loss
- `margin_ratio` (float): Margin ratio
- `long_exposure` (float): Total long exposure
- `short_exposure` (float): Total short exposure
- `exposure_ratio` (float): Exposure to equity ratio

**Example:**

```python
stats = analyzer.update_account_statistics()
print(f"Account Balance: ${stats['balance']}")
print(f"Unrealized PnL: ${stats['unrealized_pnl']}")
```

### _calculate_long_short_ratio

```python
def _calculate_long_short_ratio() -> float
```

Calculates the ratio of long to short exposure.

**Returns:**
A float representing the long/short ratio.

**Example:**

```python
positions = await analyzer.get_positions()
long_short_ratio = positions["account"]["long_short_ratio"]
print(f"Long/Short Ratio: {long_short_ratio:.2f}")
```

### _calculate_exposure_to_equity_ratio

```python
def _calculate_exposure_to_equity_ratio() -> float
```

Calculates the ratio of total position exposure to account equity.

**Returns:**
A float representing the exposure/equity ratio.

**Example:**

```python
positions = await analyzer.get_positions()
exposure_ratio = positions["account"]["exposure_to_equity_ratio"]
print(f"Exposure/Equity Ratio: {exposure_ratio:.2f}")
```

## Utility Methods

### _initialize_exchange

```python
def _initialize_exchange() -> None
```

Initializes the exchange service or direct CCXT client.

**Example:**

```python
analyzer = BitgetPositionAnalyzerB0t()
analyzer._initialize_exchange()  # Usually called automatically
```

### _update_position_history

```python
def _update_position_history(positions: List[Dict[str, Any]]) -> None
```

Updates the internal position history with the latest positions.

**Parameters:**

- `positions` (List[Dict[str, Any]]): Current positions

**Example:**

```python
positions = await analyzer.get_positions()
analyzer._update_position_history(positions["positions"])
```

## Error Handling

The BitGet Position Analyzer Bot implements comprehensive error handling:

- Connection errors are caught and logged
- API errors are handled with appropriate fallbacks
- Rate limiting is respected and handled gracefully

**Example of handling errors:**

```python
try:
    positions = await analyzer.get_positions()
    
    if "error" in positions:
        print(f"Error: {positions['error']}")
    else:
        # Process positions
        pass
except Exception as e:
    print(f"An error occurred: {e}")
```

## Response Objects

### Position Object

```json
{
  "info": {},          // Original exchange response
  "id": "123456",      // Position ID
  "symbol": "BTCUSDT", // Trading symbol
  "contracts": 0.5,    // Position size in contracts
  "contractSize": 1,   // Contract size
  "side": "long",      // Position side (long or short)
  "notional": 20000,   // Notional value
  "leverage": 10,      // Position leverage
  "entryPrice": 40000, // Average entry price
  "markPrice": 41000,  // Current mark price
  "liquidationPrice": 36000, // Liquidation price
  "initialMargin": 2000,     // Initial margin
  "initialMarginPercentage": 0.1, // Initial margin as percentage
  "maintenanceMargin": 200,       // Maintenance margin
  "maintenanceMarginPercentage": 0.01, // Maintenance margin as percentage
  "unrealizedPnl": 500,      // Unrealized profit/loss
  "realizedPnl": 0,          // Realized profit/loss
  "marginType": "isolated",  // Margin type (isolated or cross)
  "datetime": "2023-01-01T00:00:00.000Z", // Position creation time
  "lastUpdateTimestamp": 1641000000000    // Last update timestamp
}
```

### Account Statistics Object

```json
{
  "balance": 10000,             // Account balance
  "equity": 10500,              // Account equity
  "total_position_value": 20000, // Total position value
  "total_pnl": 500,             // Total unrealized PnL
  "long_exposure": 15000,       // Long exposure
  "short_exposure": 5000,       // Short exposure
  "long_short_ratio": 3.0,      // Long/short ratio
  "exposure_to_equity_ratio": 1.9, // Exposure to equity ratio
  "harmony_score": 0.85         // Harmony score
}
```

### Fibonacci Levels Object

```json
{
  "retracements": {
    "0.0": 50000,   // 0% retracement (high)
    "0.236": 47640, // 23.6% retracement
    "0.382": 46090, // 38.2% retracement
    "0.5": 45000,   // 50% retracement
    "0.618": 43910, // 61.8% retracement
    "0.786": 42140, // 78.6% retracement
    "1.0": 40000    // 100% retracement (low)
  },
  "extensions": {
    "1.0": 50000,   // 100% extension
    "1.272": 52720, // 127.2% extension
    "1.414": 54140, // 141.4% extension
    "1.618": 56180, // 161.8% extension
    "2.0": 60000,   // 200% extension
    "2.618": 66180  // 261.8% extension
  },
  "current_level": "0.5", // Current price level
  "next_support": 43910,  // Next support level
  "next_resistance": 47640 // Next resistance level
}
```

### Recommendation Object

```json
{
  "action": "buy",       // Action to take
  "symbol": "BTCUSDT",   // Trading symbol
  "amount": 0.1,         // Amount to buy/sell
  "price": 45000,        // Recommended price
  "reason": "Fibonacci support level reached", // Reason for recommendation
  "priority": 8,         // Priority (1-10)
  "target_price": 48000, // Target price
  "stop_loss": 43000     // Stop loss price
}
```
