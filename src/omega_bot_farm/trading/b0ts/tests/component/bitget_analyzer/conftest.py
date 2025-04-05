"""
Pytest configuration for component tests.
"""
import json
import os
import pytest
from unittest.mock import MagicMock, patch

# Define fixture paths relative to this directory
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def mock_exchange_service():
    """
    Provides a mocked exchange service that returns predefined responses
    for component tests.
    """
    mock_service = MagicMock()
    
    # Configure default behavior for common methods
    mock_service.get_positions.return_value = [
        {
            "symbol": "BTCUSDT",
            "positionSide": "LONG",
            "position": 0.5,
            "entryPrice": 65000,
            "markPrice": 68000,
            "unrealizedProfit": 1500,
            "leverage": 10
        },
        {
            "symbol": "ETHUSDT",
            "positionSide": "SHORT",
            "position": 2.0,
            "entryPrice": 3500,
            "markPrice": 3400,
            "unrealizedProfit": 200,
            "leverage": 5
        }
    ]
    
    mock_service.get_account_balance.return_value = {
        "totalWalletBalance": 10000,
        "totalUnrealizedProfit": 1700,
        "totalMarginBalance": 11700,
        "availableBalance": 5000
    }
    
    mock_service.get_market_data.return_value = {
        "BTCUSDT": {
            "lastPrice": 68000,
            "24hChange": 2.5,
            "24hVolume": 1500000000
        },
        "ETHUSDT": {
            "lastPrice": 3400,
            "24hChange": -1.2,
            "24hVolume": 750000000
        }
    }
    
    return mock_service

@pytest.fixture
def mock_notification_service():
    """
    Provides a mocked notification service for testing components
    that send alerts.
    """
    mock_service = MagicMock()
    return mock_service

@pytest.fixture
def sample_position_data():
    """
    Returns sample position data for testing.
    """
    return {
        "positions": [
            {
                "symbol": "BTCUSDT",
                "positionSide": "LONG",
                "position": 0.5,
                "entryPrice": 65000,
                "markPrice": 68000,
                "unrealizedProfit": 1500,
                "leverage": 10,
                "liquidationPrice": 59000,
                "marginType": "ISOLATED"
            }
        ],
        "account": {
            "totalWalletBalance": 10000,
            "totalUnrealizedProfit": 1500,
            "totalMarginBalance": 11500,
            "availableBalance": 5000
        }
    }

@pytest.fixture
def fibonacci_analysis_result():
    """
    Returns sample Fibonacci analysis results.
    """
    return {
        "symbol": "BTCUSDT",
        "timeframe": "4h",
        "trend": "BULLISH",
        "fibonacci_levels": {
            "0": 68000,
            "0.236": 67200,
            "0.382": 66700,
            "0.5": 66000,
            "0.618": 65300,
            "0.786": 64600,
            "1": 64000
        },
        "current_price": 68000,
        "nearest_level": "0",
        "next_resistance": None,
        "next_support": "0.236"
    } 