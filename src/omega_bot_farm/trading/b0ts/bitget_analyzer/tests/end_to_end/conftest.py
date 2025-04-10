
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

"""
Pytest configuration for end-to-end tests.

This module contains fixtures that set up the testing environment for
end-to-end tests of the Bitget position analyzer.
"""
import os
import json
import pytest
import logging
from unittest.mock import MagicMock, patch
from pathlib import Path

# Configure logging for end-to-end tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('e2e_tests')

# Define fixture paths relative to this directory
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures")

# Load test configuration
@pytest.fixture
def e2e_config():
    """Load test configuration from environment or defaults."""
    config_path = os.environ.get('E2E_CONFIG_PATH', 
                               os.path.join(FIXTURE_PATH, 'e2e_config.json'))
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        # Default configuration for tests
        config = {
            "use_mock_exchange": True,
            "test_symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
            "mock_data_path": os.path.join(FIXTURE_PATH, "mock_data"),
            "output_path": os.path.join(FIXTURE_PATH, "output"),
            "test_timeframes": ["15m", "1h", "4h", "1d"],
            "test_harmony_thresholds": [0.3, 0.5, 0.7, 0.9]
        }
    
    # Ensure output directory exists
    os.makedirs(config["output_path"], exist_ok=True)
    
    return config

@pytest.fixture
def mock_ccxt_bitget():
    """Create a mock CCXT Bitget exchange instance."""
    mock_exchange = MagicMock()
    
    # Configure the mock to return realistic data
    
    # Mock fetchMarkets
    markets_file = os.path.join(FIXTURE_PATH, "mock_data", "markets.json")
    if os.path.exists(markets_file):
        with open(markets_file, 'r') as f:
            mock_exchange.fetchMarkets.return_value = json.load(f)
    else:
        # Default mock markets data
        mock_exchange.fetchMarkets.return_value = [
            {"id": "BTCUSDT_UMCBL", "symbol": "BTCUSDT", "base": "BTC", "quote": "USDT", "active": True},
            {"id": "ETHUSDT_UMCBL", "symbol": "ETHUSDT", "base": "ETH", "quote": "USDT", "active": True},
            {"id": "SOLUSDT_UMCBL", "symbol": "SOLUSDT", "base": "SOL", "quote": "USDT", "active": True}
        ]
    
    # Mock fetchPositions
    positions_file = os.path.join(FIXTURE_PATH, "mock_data", "positions.json")
    if os.path.exists(positions_file):
        with open(positions_file, 'r') as f:
            mock_exchange.fetchPositions.return_value = json.load(f)
    else:
        # Default mock positions data
        mock_exchange.fetchPositions.return_value = [
            {
                "info": {"symbol": "BTCUSDT_UMCBL", "positionSide": "long"},
                "symbol": "BTCUSDT",
                "side": "long",
                "contracts": 0.5,
                "contractSize": 1,
                "entryPrice": 65000,
                "markPrice": 68000,
                "unrealizedPnl": 1500,
                "leverage": 10,
                "liquidationPrice": 59000,
                "marginType": "isolated",
                "marginMode": "isolated"
            }
        ]
    
    # Mock fetchBalance
    balance_file = os.path.join(FIXTURE_PATH, "mock_data", "balance.json")
    if os.path.exists(balance_file):
        with open(balance_file, 'r') as f:
            mock_exchange.fetchBalance.return_value = json.load(f)
    else:
        # Default mock balance data
        mock_exchange.fetchBalance.return_value = {
            "info": {},
            "USDT": {
                "free": 5000,
                "used": 5000,
                "total": 10000
            },
            "BTC": {
                "free": 0.1,
                "used": 0,
                "total": 0.1
            },
            "ETH": {
                "free": 1.5,
                "used": 0,
                "total": 1.5
            },
            "total": {
                "USDT": 10000,
                "unrealizedPnl": 1500
            }
        }
    
    # Mock fetchOHLCV for different timeframes
    def mock_fetch_ohlcv(symbol, timeframe='1h', since=None, limit=None, params={}):
        """Mock implementation of fetchOHLCV that returns data from fixture files."""
        filename = f"{symbol.replace('/', '_')}_{timeframe}.json"
        ohlcv_file = os.path.join(FIXTURE_PATH, "mock_data", "ohlcv", filename)
        
        if os.path.exists(ohlcv_file):
            with open(ohlcv_file, 'r') as f:
                data = json.load(f)
                
                # Handle since and limit parameters
                if since is not None and limit is not None:
                    # Filter and slice the data based on since and limit
                    filtered_data = [candle for candle in data if candle[0] >= since]
                    return filtered_data[:limit]
                elif limit is not None:
                    return data[:limit]
                else:
                    return data
        else:
            # Generate synthetic OHLCV data if file doesn't exist
            import time
            import random
            
            now = int(time.time() * 1000)
            base_price = 65000 if symbol == "BTCUSDT" else 3400 if symbol == "ETHUSDT" else 150
            
            # Create realistic price movements
            data = []
            for i in range(limit or 100):
                timestamp = now - (i * 60 * 60 * 1000)  # 1 hour candles
                close_price = base_price * (1 + random.uniform(-0.05, 0.05))
                open_price = close_price * (1 + random.uniform(-0.02, 0.02))
                high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.03))
                low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.03))
                volume = base_price * random.uniform(50, 500)
                
                data.append([timestamp, open_price, high_price, low_price, close_price, volume])
            
            return sorted(data, key=lambda x: x[0])
    
    mock_exchange.fetchOHLCV.side_effect = mock_fetch_ohlcv
    
    return mock_exchange

@pytest.fixture
def exchange_service(mock_ccxt_bitget, e2e_config):
    """Create an exchange service instance with the mock exchange."""
    # Import the actual exchange service
    try:
        from src.omega_bot_farm.trading.b0ts.bitget_analyzer.exchange_service import ExchangeService
        
        with patch('ccxt.bitget') as mock_bitget_class:
            mock_bitget_class.return_value = mock_ccxt_bitget
            
            # Create the service with the mocked exchange
            service = ExchangeService(
                api_key="test_key",
                api_secret="test_secret",
                passphrase="test_passphrase"
            )
            
            return service
    except ImportError:
        # Create a mock service if we can't import the actual one
        mock_service = MagicMock()
        
        # Configure the mock to return data from the mock exchange
        mock_service.get_positions.return_value = mock_ccxt_bitget.fetchPositions()
        mock_service.get_account_balance.return_value = mock_ccxt_bitget.fetchBalance()
        mock_service.get_markets.return_value = mock_ccxt_bitget.fetchMarkets()
        
        # Method to get OHLCV data
        mock_service.get_ohlcv.side_effect = lambda symbol, timeframe, limit=100: (
            mock_ccxt_bitget.fetchOHLCV(symbol, timeframe, limit=limit)
        )
        
        return mock_service

@pytest.fixture
def notification_service():
    """Create a notification service for end-to-end tests."""
    mock_service = MagicMock()
    
    # Track notifications for verification
    mock_service.notifications = []
    
    # Override send_notification to track calls
    original_send = mock_service.send_notification
    def tracked_send_notification(*args, **kwargs):
        mock_service.notifications.append((args, kwargs))
        return original_send(*args, **kwargs)
    
    mock_service.send_notification = tracked_send_notification
    
    return mock_service

@pytest.fixture
def position_analyzer_bot(exchange_service, notification_service, e2e_config):
    """Create a position analyzer bot instance for end-to-end testing."""
    try:
        from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import (
            BitgetPositionAnalyzerBot
        )
        
        # Create the bot with our test services
        bot = BitgetPositionAnalyzerBot(
            exchange_service=exchange_service,
            notification_service=notification_service,
            config={
                "test_mode": True,
                "symbols": e2e_config["test_symbols"],
                "timeframes": e2e_config["test_timeframes"],
                "risk_threshold": 0.1,
                "profit_target": 0.05,
                "harmony_threshold": 0.7,
                "output_path": e2e_config["output_path"]
            }
        )
        
        return bot
    except ImportError:
        # Create a mock bot if we can't import the actual one
        pytest.skip("BitgetPositionAnalyzerBot not available")
        return None 