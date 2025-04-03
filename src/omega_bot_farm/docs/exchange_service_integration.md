# Exchange Service Integration Guide

This guide explains how to integrate the ExchangeService into your Omega Bot Farm bots to standardize exchange API interactions and remove duplicated code.

## Overview

The `ExchangeService` provides a centralized way to manage exchange connections, credentials, and operations. It handles multiple exchanges with a focus on BitGet, supports both mainnet and testnet environments, and provides unified error handling.

Benefits of using the `ExchangeService`:

- Centralized credential management
- Standardized error handling
- Consistent API for different exchanges
- DRY code across bots
- Easier testing with mock exchanges

## Basic Integration

### Step 1: Import the ExchangeService

```python
from src.omega_bot_farm.services.exchange_service import create_exchange_service, ExchangeService
```

### Step 2: Initialize the Service

```python
def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
    # Initialize exchange service
    self.exchange_service = create_exchange_service(
        exchange_id="bitget",  # or "binance", "bybit", etc.
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        use_testnet=use_testnet
    )
    
    # Get the underlying CCXT client if needed for direct operations
    self.exchange = self.exchange_service.get_exchange_client()
```

### Step 3: Use the Service for Exchange Operations

```python
async def get_positions(self):
    # Use the service to fetch positions
    positions = await self.exchange_service.fetch_positions()
    return positions

async def get_balance(self):
    # Use the service to fetch balance
    balance = await self.exchange_service.fetch_balance()
    return balance

async def place_order(self, symbol, order_type, side, amount, price=None):
    # Use the service to place an order
    order = await self.exchange_service.create_order(
        symbol=symbol,
        order_type=order_type,
        side=side,
        amount=amount,
        price=price
    )
    return order
```

## Complete Example

Here's a complete example of a bot that uses the ExchangeService:

```python
import logging
from typing import Dict, Any, Optional
from src.omega_bot_farm.services.exchange_service import create_exchange_service

logger = logging.getLogger("example_bot")

class ExampleBot:
    def __init__(self, 
                 exchange_id: str = "bitget",
                 api_key: Optional[str] = None, 
                 api_secret: Optional[str] = None,
                 api_passphrase: Optional[str] = None,
                 use_testnet: bool = False):
        
        # Initialize exchange service
        self.exchange_service = create_exchange_service(
            exchange_id=exchange_id,
            api_key=api_key,
            api_secret=api_secret,
            api_passphrase=api_passphrase,
            use_testnet=use_testnet
        )
        
        # Log initialization status
        if self.exchange_service.is_connected():
            logger.info(f"Connected to {exchange_id.upper()}")
        else:
            logger.error(f"Failed to connect to {exchange_id.upper()}")
    
    async def get_market_data(self) -> Dict[str, Any]:
        """Get market data."""
        if not self.exchange_service.is_connected():
            return {"error": "Exchange not connected"}
        
        try:
            # Get positions and balance
            positions = await self.exchange_service.fetch_positions()
            balance = await self.exchange_service.fetch_balance()
            
            # Process and return data
            return {
                "positions": positions,
                "balance": balance,
                "total_positions": len(positions)
            }
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return {"error": str(e)}
    
    async def execute_strategy(self, symbol: str) -> Dict[str, Any]:
        """Execute a simple strategy."""
        if not self.exchange_service.is_connected():
            return {"error": "Exchange not connected"}
        
        try:
            # Example strategy logic
            # In a real bot, this would contain actual trading logic
            order = await self.exchange_service.create_order(
                symbol=symbol,
                order_type="limit",
                side="buy",
                amount=0.01,
                price=30000.0
            )
            
            return {"order": order, "status": "executed"}
        except Exception as e:
            logger.error(f"Error executing strategy: {e}")
            return {"error": str(e)}
```

## Handling Multiple Exchanges

The ExchangeService supports multiple exchanges via the `exchange_id` parameter:

```python
# BitGet
bitget_service = create_exchange_service("bitget", api_key="...", api_secret="...", api_passphrase="...")

# Binance
binance_service = create_exchange_service("binance", api_key="...", api_secret="...")

# Bybit
bybit_service = create_exchange_service("bybit", api_key="...", api_secret="...")
```

## Graceful Fallback to Direct CCXT

When migrating existing bots, you can implement graceful fallback to direct CCXT if the ExchangeService isn't available:

```python
try:
    from src.omega_bot_farm.services.exchange_service import create_exchange_service
    EXCHANGE_SERVICE_AVAILABLE = True
except ImportError:
    EXCHANGE_SERVICE_AVAILABLE = False

def _initialize_exchange(self):
    """Initialize exchange client."""
    if EXCHANGE_SERVICE_AVAILABLE:
        # Use ExchangeService
        self.exchange_service = create_exchange_service(
            exchange_id="bitget",
            api_key=self.api_key,
            api_secret=self.api_secret,
            api_passphrase=self.api_passphrase,
            use_testnet=self.use_testnet
        )
        self.exchange = self.exchange_service.get_exchange_client()
    else:
        # Fallback to direct CCXT
        self.exchange = ccxt.bitget({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'password': self.api_passphrase,
            'options': {
                'defaultType': 'swap',
                'adjustForTimeDifference': True,
                'testnet': self.use_testnet,
            }
        })
```

## Testing with the ExchangeService

You can easily mock the ExchangeService for testing:

```python
import unittest
from unittest.mock import patch, MagicMock

class TestExampleBot(unittest.TestCase):
    @patch('src.omega_bot_farm.services.exchange_service.create_exchange_service')
    def test_bot_initialization(self, mock_create_service):
        # Create a mock service
        mock_service = MagicMock()
        mock_service.is_connected.return_value = True
        mock_service.get_exchange_client.return_value = MagicMock()
        
        # Configure the mock factory
        mock_create_service.return_value = mock_service
        
        # Initialize the bot
        from my_bot import MyBot
        bot = MyBot(api_key="test", api_secret="test")
        
        # Verify the service was called correctly
        mock_create_service.assert_called_once_with(
            exchange_id="bitget",
            api_key="test",
            api_secret="test",
            api_passphrase=None,
            use_testnet=False
        )
        
        # Verify the bot has the service
        self.assertEqual(bot.exchange_service, mock_service)
```

## Best Practices

1. **Always check connectivity**:

   ```python
   if not self.exchange_service.is_connected():
       return {"error": "Exchange not connected"}
   ```

2. **Use async/await consistently**:

   ```python
   # Correct
   positions = await self.exchange_service.fetch_positions()
   
   # Incorrect
   positions = self.exchange_service.fetch_positions()  # This returns a coroutine, not the positions
   ```

3. **Handle exceptions**:

   ```python
   try:
       positions = await self.exchange_service.fetch_positions()
   except Exception as e:
       logger.error(f"Error fetching positions: {e}")
       return {"error": str(e)}
   ```

4. **Access the raw CCXT client only when necessary**:

   ```python
   # Only if you need direct access to CCXT features not exposed by ExchangeService
   ccxt_client = self.exchange_service.get_exchange_client()
   ```

5. **Test both with and without the service**:
   Ensure your bot works even if the service is unavailable by implementing graceful fallback.

## Migration Guide

To migrate existing bots to use the ExchangeService:

1. Replace direct CCXT initialization with ExchangeService
2. Replace direct calls to CCXT methods with calls to ExchangeService methods
3. Add proper async/await handling
4. Update tests to mock ExchangeService instead of CCXT
5. Add graceful fallback for backward compatibility

By following these guidelines, you can improve code quality, reduce duplication, and ensure consistent exchange interaction across all bots in the Omega Bot Farm.
