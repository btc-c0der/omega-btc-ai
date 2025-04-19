
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


# Omega Bot Farm - API Documentation

## Overview

The Omega Bot Farm exposes several internal APIs for service communication and integration with external systems. This document outlines the available APIs, their endpoints, parameters, and expected responses.

## API Types

The system provides the following API types:

1. **Service APIs**: Internal APIs for communication between services
2. **Redis Pub/Sub Channels**: Event-based communication
3. **Exchange Integration APIs**: Wrappers around exchange APIs
4. **Discord Bot Commands**: User-facing command interface

## Service APIs

### Exchange Service API

The Exchange Service provides a unified interface for interacting with cryptocurrency exchanges.

#### Base URL

For internal service-to-service communication:

- Local: `http://localhost:5000/api/exchange`
- Docker: `http://exchange-service:5000/api/exchange`
- Kubernetes: `http://exchange-service.omega-bot-farm.svc.cluster.local/api/exchange`

#### Endpoints

##### GET /positions

Retrieves open positions from the exchange.

**Parameters**:

- `exchange` (query, string): Exchange name (default: "bitget")
- `symbol` (query, string, optional): Filter by symbol (e.g., "BTCUSDT")
- `limit` (query, integer, optional): Maximum number of positions to return

**Response**:

```json
{
  "positions": [
    {
      "symbol": "BTCUSDT",
      "size": 0.001,
      "side": "long",
      "entry_price": 50000.0,
      "mark_price": 51000.0,
      "unrealized_pnl": 1.0,
      "leverage": 10,
      "margin_mode": "isolated",
      "created_at": 1617293940
    }
  ],
  "exchange": "bitget",
  "timestamp": 1617294000
}
```

##### POST /order

Places a new order on the exchange.

**Request Body**:

```json
{
  "exchange": "bitget",
  "symbol": "BTCUSDT",
  "side": "buy",
  "type": "limit",
  "price": 50000.0,
  "amount": 0.001,
  "leverage": 10,
  "margin_mode": "isolated"
}
```

**Response**:

```json
{
  "order_id": "12345678",
  "symbol": "BTCUSDT",
  "status": "open",
  "price": 50000.0,
  "amount": 0.001,
  "filled": 0.0,
  "remaining": 0.001,
  "cost": 0.0,
  "timestamp": 1617294000
}
```

##### DELETE /order/{order_id}

Cancels an existing order.

**Parameters**:

- `order_id` (path, string): The ID of the order to cancel
- `exchange` (query, string): Exchange name (default: "bitget")
- `symbol` (query, string): Symbol of the order (e.g., "BTCUSDT")

**Response**:

```json
{
  "order_id": "12345678",
  "symbol": "BTCUSDT",
  "status": "canceled",
  "timestamp": 1617294000
}
```

### Analytics Service API

The Analytics Service provides market and position analysis.

#### Base URL

- Local: `http://localhost:5001/api/analytics`
- Docker: `http://analytics-service:5001/api/analytics`
- Kubernetes: `http://analytics-service.omega-bot-farm.svc.cluster.local/api/analytics`

#### Endpoints

##### POST /fibonacci-analysis

Performs Fibonacci analysis on a position or price range.

**Request Body**:

```json
{
  "symbol": "BTCUSDT",
  "high": 60000.0,
  "low": 30000.0,
  "current": 45000.0,
  "position_side": "long",
  "position_entry": 40000.0
}
```

**Response**:

```json
{
  "symbol": "BTCUSDT",
  "levels": {
    "0.0": 30000.0,
    "0.236": 37080.0,
    "0.382": 41460.0,
    "0.5": 45000.0,
    "0.618": 48540.0,
    "0.786": 53580.0,
    "1.0": 60000.0,
    "1.618": 78540.0
  },
  "closest_level": {
    "ratio": "0.382",
    "price": 41460.0,
    "distance_percent": 3.65
  },
  "position_analysis": {
    "entry_level_ratio": 0.333,
    "current_level_ratio": 0.5,
    "golden_ratio_alignment": 0.81,
    "recommendation": "Hold position - price near 0.5 Fibonacci level"
  },
  "timestamp": 1617294000
}
```

##### GET /market-sentiment

Retrieves current market sentiment analysis.

**Parameters**:

- `symbol` (query, string): Symbol to analyze (e.g., "BTCUSDT")
- `timeframe` (query, string, optional): Timeframe for analysis (default: "1d")

**Response**:

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1d",
  "sentiment": {
    "value": 0.65,
    "label": "Moderately Bullish",
    "indicators": {
      "rsi": {
        "value": 58,
        "interpretation": "Neutral"
      },
      "macd": {
        "value": 100.5,
        "interpretation": "Bullish"
      },
      "fibonacci_position": {
        "value": 0.382,
        "interpretation": "Support Level"
      }
    }
  },
  "cosmic_factors": {
    "mercury_retrograde": false,
    "moon_phase": "Waxing Gibbous",
    "influence": 0.2
  },
  "timestamp": 1617294000
}
```

## Redis Pub/Sub Channels

The system uses Redis Pub/Sub for event-based communication between services.

### Position Update Channel

**Channel**: `position:updates`

**Message Format**:

```json
{
  "event": "position:updated",
  "exchange": "bitget",
  "symbol": "BTCUSDT",
  "position": {
    "symbol": "BTCUSDT",
    "size": 0.001,
    "side": "long",
    "entry_price": 50000.0,
    "mark_price": 51000.0,
    "unrealized_pnl": 1.0,
    "leverage": 10,
    "margin_mode": "isolated",
    "created_at": 1617293940,
    "updated_at": 1617294000
  },
  "changes": {
    "mark_price": {
      "old": 50500.0,
      "new": 51000.0,
      "percent": 0.99
    },
    "unrealized_pnl": {
      "old": 0.5,
      "new": 1.0,
      "percent": 100.0
    }
  },
  "timestamp": 1617294000
}
```

### Market Alert Channel

**Channel**: `market:alerts`

**Message Format**:

```json
{
  "event": "market:alert",
  "symbol": "BTCUSDT",
  "alert_type": "price_target",
  "level": "info",
  "message": "BTC price has reached the 0.618 Fibonacci level at $48,540",
  "data": {
    "price": 48540.0,
    "fibonacci_level": 0.618,
    "previous_level": 0.5,
    "next_level": 0.786
  },
  "timestamp": 1617294000
}
```

### Bot Status Channel

**Channel**: `bot:status`

**Message Format**:

```json
{
  "event": "bot:status",
  "bot_id": "bitget-position-analyzer-1",
  "status": "running",
  "message": "Bot is analyzing positions",
  "metrics": {
    "positions_analyzed": 5,
    "alerts_generated": 2,
    "memory_usage": 128.5,
    "uptime_seconds": 3600
  },
  "timestamp": 1617294000
}
```

## Discord Bot Commands

The Discord Bot provides a command-based API for user interaction.

### Position Commands

#### !bitget-positions

Shows current BitGet positions.

**Usage**:

```
!bitget-positions [symbol]
```

**Parameters**:

- `symbol` (optional): Filter positions by symbol

**Response**:
A formatted message showing open positions with entry price, current price, PNL, and Fibonacci alignment.

#### /bitget-analyze

Analyzes BitGet positions with Fibonacci levels.

**Usage**:

```
/bitget-analyze symbol:BTCUSDT [detailed:true]
```

**Parameters**:

- `symbol`: Symbol to analyze
- `detailed` (optional): Whether to show detailed analysis

**Response**:
A formatted message with Fibonacci levels, position analysis, and recommendations.

### Insight Commands

#### /golden-wisdom

Provides trading wisdom based on Fibonacci principles.

**Usage**:

```
/golden-wisdom [topic:risk_management]
```

**Parameters**:

- `topic` (optional): Specific topic for wisdom

**Response**:
A message containing trading wisdom relevant to the current market conditions or specified topic.

#### /market-pulse

Gets the current market sentiment.

**Usage**:

```
/market-pulse symbol:BTCUSDT [timeframe:1h]
```

**Parameters**:

- `symbol`: Symbol to check
- `timeframe` (optional): Timeframe for analysis

**Response**:
A message with market sentiment analysis, key indicators, and cosmic influences.

## Integration Examples

### Python Service-to-Service Integration

```python
import requests
import json

def get_position_analysis(symbol):
    # Get positions from Exchange Service
    positions_url = "http://exchange-service:5000/api/exchange/positions"
    positions_response = requests.get(positions_url, params={"symbol": symbol})
    positions = positions_response.json()["positions"]
    
    if not positions:
        return {"error": "No positions found for symbol"}
    
    position = positions[0]
    
    # Get Fibonacci analysis from Analytics Service
    analysis_url = "http://analytics-service:5001/api/analytics/fibonacci-analysis"
    market_data = {
        "symbol": symbol,
        "high": position["recent_high"],
        "low": position["recent_low"],
        "current": position["mark_price"],
        "position_side": position["side"],
        "position_entry": position["entry_price"]
    }
    
    analysis_response = requests.post(analysis_url, json=market_data)
    analysis = analysis_response.json()
    
    return {
        "position": position,
        "analysis": analysis
    }
```

### Redis Pub/Sub Integration

```python
import redis
import json

class AlertSubscriber:
    def __init__(self, redis_host="redis", redis_port=6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.pubsub = self.redis.pubsub()
        
    def subscribe_to_alerts(self, callback):
        self.pubsub.subscribe("market:alerts")
        for message in self.pubsub.listen():
            if message["type"] == "message":
                alert = json.loads(message["data"])
                callback(alert)
                
    def start(self):
        self.subscribe_to_alerts(self.process_alert)
        
    def process_alert(self, alert):
        print(f"Alert received: {alert['message']}")
        # Process alert data
```

### Discord Bot Integration

```python
from discord.ext import commands
import requests

class FibonacciAnalyzer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="bitget-positions")
    async def get_positions(self, ctx, symbol=None):
        # Call Exchange Service API
        url = "http://exchange-service:5000/api/exchange/positions"
        params = {"symbol": symbol} if symbol else {}
        
        response = requests.get(url, params=params)
        positions = response.json()["positions"]
        
        # Format and send response
        message = "**Current BitGet Positions**\n\n"
        for position in positions:
            message += f"**{position['symbol']}**: {position['side'].upper()} {position['size']}\n"
            message += f"Entry: ${position['entry_price']:.2f} | Current: ${position['mark_price']:.2f}\n"
            message += f"PNL: ${position['unrealized_pnl']:.2f}\n\n"
            
        await ctx.send(message)
```

## API Security

All internal APIs should be secured using:

1. Network isolation (for containerized deployments)
2. API keys for service-to-service communication
3. Rate limiting to prevent abuse

External-facing APIs (Discord Bot) are secured through Discord's OAuth2 system.
