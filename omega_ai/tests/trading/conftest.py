"""
OMEGA BTC AI - Trading Test Configuration
=======================================

Divine test configuration for trading modules with self-healing integration.
Ensures proper test environment and divine execution.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import asyncio
import logging
from typing import Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timezone
from omega_ai.trading.exchanges.ai_self_healing import AISelfHealing

# Configure divine logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Terminal colors for blessed output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create divine event loop for async tests."""
    logger.info(f"{GREEN}Creating divine event loop{RESET}")
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def mock_api_client() -> AsyncGenerator[Mock, None]:
    """Create divine mock API client."""
    logger.info(f"{GREEN}Creating divine mock API client{RESET}")
    client = Mock()
    client.get_market_ticker = AsyncMock(return_value={"last": 50000.0})
    client.get_positions = AsyncMock(return_value=[])
    client.place_order = AsyncMock(return_value={"orderId": "123"})
    client.close_position = AsyncMock(return_value={"status": "CLOSED"})
    yield client

@pytest.fixture(scope="session")
def mock_telegram_client() -> Mock:
    """Create divine mock Telegram client."""
    logger.info(f"{GREEN}Creating divine mock Telegram client{RESET}")
    client = Mock()
    client.send_message = AsyncMock(return_value={"message_id": 123})
    return client

@pytest.fixture(scope="session")
def mock_market_data() -> dict:
    """Create divine mock market data."""
    logger.info(f"{GREEN}Creating divine mock market data{RESET}")
    return {
        "BTCUSDT": {
            "last": 50000.0,
            "bid": 49999.0,
            "ask": 50001.0,
            "volume": 100.0
        }
    }

@pytest.fixture(scope="session")
def mock_trader_config() -> dict:
    """Create divine mock trader configuration."""
    logger.info(f"{GREEN}Creating divine mock trader configuration{RESET}")
    return {
        "initial_capital": 24.0,
        "symbol": "BTCUSDT",
        "testnet": True,
        "update_interval": 1.0
    }

@pytest.fixture(scope="session")
def mock_risk_metrics() -> dict:
    """Create divine mock risk metrics."""
    logger.info(f"{GREEN}Creating divine mock risk metrics{RESET}")
    return {
        "sharpe_ratio": 1.5,
        "max_drawdown": 0.1,
        "win_rate": 0.6,
        "total_pnl": 2.4
    }

@pytest.fixture(scope="session")
def mock_position_data() -> dict:
    """Create divine mock position data."""
    logger.info(f"{GREEN}Creating divine mock position data{RESET}")
    return {
        "positions": [
            {
                "symbol": "BTCUSDT",
                "size": 0.001,
                "entry_price": 50000.0,
                "unrealized_pnl": 0.1
            }
        ]
    }

@pytest.fixture(scope="session")
def mock_order_data() -> dict:
    """Create divine mock order data."""
    logger.info(f"{GREEN}Creating divine mock order data{RESET}")
    return {
        "orderId": "123",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "price": 50000.0,
        "quantity": 0.001,
        "status": "FILLED"
    }

@pytest.fixture(scope="session")
def mock_error_responses() -> dict:
    """Create divine mock error responses."""
    logger.info(f"{GREEN}Creating divine mock error responses{RESET}")
    return {
        "rate_limit": Exception("Rate limit exceeded"),
        "api_error": Exception("API Error"),
        "position_error": Exception("Position update error"),
        "order_error": Exception("Order placement error")
    }

@pytest.fixture(scope="session")
def self_healing():
    """Create divine self-healing instance."""
    return AISelfHealing() 