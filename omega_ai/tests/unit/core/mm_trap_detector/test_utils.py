"""
🎯 0M3G4 TR4P D3T3CT0R - T3ST UT1L1T13S 🎯
=====================================

Shared test utilities for the Market Maker Trap Detection System.
May your tests be clean and your coverage high! 🧪

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any, Optional
import json
import time
import websockets
import redis
from influxdb_client.client.influxdb_client import InfluxDBClient

# ANSI color codes for styled output
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    mock = Mock(spec=redis.Redis)
    mock.get.return_value = "1000.0"
    mock.hget.return_value = "50000.0"
    mock.hset.return_value = True
    mock.rpush.return_value = True
    mock.lrange.return_value = []
    mock.ltrim.return_value = True
    return mock

@pytest.fixture
def mock_influxdb():
    """Create a mock InfluxDB client."""
    mock = Mock(spec=InfluxDBClient)
    mock.write_api.return_value.write.return_value = True
    return mock

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket connection."""
    mock = Mock(spec=websockets.client.WebSocketClientProtocol)
    mock.send.return_value = None
    mock.recv.return_value = json.dumps({"btc_price": 50000.0})
    return mock

@pytest.fixture
def mock_order_book():
    """Create a mock order book."""
    return {
        "bids": [
            {"price": 50000.0, "size": 1.0},
            {"price": 49999.0, "size": 100.0},
            {"price": 49998.0, "size": 1.0}
        ],
        "asks": [
            {"price": 50001.0, "size": 1.0},
            {"price": 50002.0, "size": 100.0},
            {"price": 50003.0, "size": 1.0}
        ]
    }

@pytest.fixture
def mock_trades():
    """Create mock trade data."""
    return [
        {"price": 50000.0, "size": 1.0, "side": "buy", "timestamp": time.time()},
        {"price": 50000.0, "size": 1.0, "side": "sell", "timestamp": time.time() + 0.1},
        {"price": 50000.0, "size": 1.0, "side": "buy", "timestamp": time.time() + 0.2},
        {"price": 50000.0, "size": 1.0, "side": "sell", "timestamp": time.time() + 0.3}
    ]

@pytest.fixture
def mock_exchange_prices():
    """Create mock exchange prices."""
    return {
        "binance": {"price": 50000.0, "volume": 1000.0},
        "coinbase": {"price": 49900.0, "volume": 1000.0},
        "kraken": {"price": 50100.0, "volume": 1000.0}
    }

def create_trap_detection(
    trap_type: str,
    price: float,
    volume: float,
    confidence: float = 0.85
) -> Dict[str, Any]:
    """Create a trap detection dictionary."""
    return {
        "type": trap_type,
        "confidence": confidence,
        "price": price,
        "volume": volume,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "price_change_pct": 0.01,
            "last_price": price * 0.99
        }
    }

def simulate_price_update(
    detector: Any,
    price: float,
    volume: Optional[float] = None
) -> None:
    """Simulate a price update on the detector."""
    detector.process_price_update(price, volume)

def verify_trap_detection(
    detector: Any,
    trap_type: str,
    price: float,
    volume: float
) -> bool:
    """Verify that a trap was detected with the correct parameters."""
    if not detector.trap_history:
        return False
    
    last_trap = detector.trap_history[-1]
    return (
        last_trap.type.value == trap_type and
        last_trap.price == price and
        last_trap.volume == volume
    )

def print_test_header(test_name: str) -> None:
    """Print a formatted test header."""
    print(f"\n{MAGENTA}Testing {test_name}...{RESET}")

def print_test_result(success: bool, message: str) -> None:
    """Print a formatted test result."""
    color = GREEN if success else RED
    print(f"  • {color}{message}{RESET}") 