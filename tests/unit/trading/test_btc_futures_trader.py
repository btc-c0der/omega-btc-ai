
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

import os
import sys
import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add project root to path for module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.trading.btc_futures_trader import BtcFuturesTrader

@pytest.fixture
def mock_binance_client():
    """Mock Binance client for testing."""
    with patch('binance.client.Client') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance

def test_get_historical_data_empty_response(mock_binance_client):
    """Test get_historical_data method when Binance returns empty data."""
    # Arrange
    mock_binance_client.futures_klines.return_value = []
    trader = BtcFuturesTrader(api_key="test_key", api_secret="test_secret")
    
    # Act
    df = trader.get_historical_data(
        symbol="BTCUSDT",
        interval="1h",
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now()
    )
    
    # Assert
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == [
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
        'taker_buy_quote_volume', 'ignore'
    ]

def test_get_historical_data_with_data(mock_binance_client):
    """Test get_historical_data method with mock data from Binance."""
    # Arrange
    mock_data = [
        [
            1499040000000,      # Timestamp
            "8100.0",           # Open
            "8200.0",           # High
            "8000.0",           # Low
            "8150.0",           # Close
            "10.0",             # Volume
            1499644799999,      # Close time
            "80000.0",          # Quote volume
            100,                # Number of trades
            "5.0",              # Taker buy volume
            "40000.0",          # Taker buy quote volume
            "0"                 # Ignore
        ]
    ]
    mock_binance_client.futures_klines.return_value = mock_data
    trader = BtcFuturesTrader(api_key="test_key", api_secret="test_secret")
    
    # Act
    df = trader.get_historical_data(
        symbol="BTCUSDT",
        interval="1h",
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now()
    )
    
    # Assert
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 1
    assert list(df.columns) == [
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
        'taker_buy_quote_volume', 'ignore'
    ]
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])
    assert pd.api.types.is_float_dtype(df['open'])
    assert pd.api.types.is_float_dtype(df['high'])
    assert pd.api.types.is_float_dtype(df['low'])
    assert pd.api.types.is_float_dtype(df['close'])
    assert pd.api.types.is_float_dtype(df['volume'])
    
    # Check values
    assert df.iloc[0]['open'] == 8100.0
    assert df.iloc[0]['high'] == 8200.0
    assert df.iloc[0]['low'] == 8000.0
    assert df.iloc[0]['close'] == 8150.0
    assert df.iloc[0]['volume'] == 10.0

def test_get_historical_data_error_handling(mock_binance_client):
    """Test get_historical_data method error handling."""
    # Arrange
    mock_binance_client.futures_klines.side_effect = Exception("API Error")
    trader = BtcFuturesTrader(api_key="test_key", api_secret="test_secret")
    
    # Act
    df = trader.get_historical_data(
        symbol="BTCUSDT",
        interval="1h",
        start_time=datetime.now() - timedelta(days=1),
        end_time=datetime.now()
    )
    
    # Assert
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == [
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
        'taker_buy_quote_volume', 'ignore'
    ] 