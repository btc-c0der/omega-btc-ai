import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock, call, AsyncMock
import asyncio
from datetime import datetime, UTC
from omega_ai.data_feed.btc_live_feed import BtcPriceFeed, PriceSource
import threading

# Define our stub functions that we'll test
def check_redis_health():
    """Stub function for Redis health check"""
    # This is a simplified version that doesn't actually check Redis
    return True

def update_redis(price, volume):
    """Stub function for updating Redis with BTC price data"""
    # Store both price and volume values separately
    redis_conn.set("last_btc_price", str(price))
    redis_conn.set("last_btc_volume", str(volume))
    
    # Store combined price and volume data in history
    combined_data = f"{price},{volume}"
    redis_conn.lpush("btc_movement_history", combined_data)
    redis_conn.ltrim("btc_movement_history", -100, -1)

def on_message(ws, message):
    """Stub function for WebSocket message handler"""
    data = json.loads(message)
    price = float(data["p"])
    volume = float(data["q"])
    update_redis(price, volume)

def save_btc_price_to_db(price, volume):
    """Stub function for saving price data to PostgreSQL"""
    pass

async def send_to_mm_websocket(price):
    """Stub function for sending data to MM WebSocket"""
    pass

# Define a redis_conn mock for our stubs
redis_conn = MagicMock()

class TestBtcPriceFeed:
    """Test suite for BtcPriceFeed class"""
    
    @pytest.fixture
    def btc_feed(self):
        """Fixture to create a BtcPriceFeed instance"""
        with patch('omega_ai.data_feed.btc_live_feed.RedisManager') as mock_redis:
            mock_redis.return_value.get_cached.return_value = "85000.50"
            mock_redis.return_value.ping.return_value = True
            feed = BtcPriceFeed()
            # Remove WebSocket initialization
            feed._ws = None
            feed._ws_thread = threading.Thread(target=lambda: None)  # Create a dummy thread
            return feed

    def test_initialization(self, btc_feed):
        """Test BtcPriceFeed initialization"""
        assert btc_feed.sources == [PriceSource.BINANCE, PriceSource.COINBASE]
        assert btc_feed.update_interval == 5.0
        assert btc_feed.last_price is None
        assert btc_feed.last_volume is None
        assert btc_feed.is_running is False
        assert btc_feed._ws is None

    def test_connect_websocket(self, btc_feed):
        """Test WebSocket connection setup"""
        with patch('omega_ai.data_feed.btc_live_feed.WebSocketApp') as mock_ws:
            btc_feed.connect_websocket()
            mock_ws.assert_called_once()
            assert btc_feed._ws is not None
            assert btc_feed._ws_thread is not None
            assert btc_feed._ws_thread.daemon is True

    def test_update_redis(self, btc_feed):
        """Test updating Redis with BTC price data"""
        # Create a mock Redis manager
        mock_redis_manager = MagicMock()
        
        # Mock the RedisManager class to return our mock instance
        with patch('omega_ai.data_feed.btc_live_feed.RedisManager', return_value=mock_redis_manager):
            # Create an instance of BtcPriceFeed
            btc_feed = BtcPriceFeed()
            
            # Test data
            test_price = 85000.5
            test_volume = 1.5
            
            # Mock get_cached to return None for prev_btc_price to ensure update happens
            mock_redis_manager.get_cached.return_value = None
            
            # Call update_redis
            btc_feed.update_redis(test_price, test_volume)
            
            # Verify Redis calls
            mock_redis_manager.set_cached.assert_any_call("last_btc_price", str(test_price))
            mock_redis_manager.set_cached.assert_any_call("last_btc_volume", str(test_volume))
            mock_redis_manager.lpush.assert_any_call("btc_movement_history", f"{test_price},{test_volume}")
            mock_redis_manager.ltrim.assert_any_call("btc_movement_history", -100, -1)

    def test_small_volume_handling(self, btc_feed):
        """Test handling of very small volume values"""
        with patch.object(btc_feed.redis_manager, 'get_cached') as mock_get:
            with patch.object(btc_feed.redis_manager, 'set_cached') as mock_set:
                # Mock previous price to be different
                mock_get.side_effect = lambda key: "84000.50" if key == "prev_btc_price" else "85000.50"
                btc_feed.update_redis(85000.50, 7e-05)
                mock_set.assert_any_call("last_btc_volume", "7e-05")

    def test_get_current_price(self, btc_feed):
        """Test getting current price"""
        with patch.object(btc_feed.redis_manager, 'get_cached') as mock_get:
            mock_get.return_value = "85000.50"
            price = btc_feed.get_current_price()
            assert price == 85000.50

    def test_get_price_history(self, btc_feed):
        """Test getting price history"""
        with patch.object(btc_feed.redis_manager, 'lrange') as mock_lrange:
            mock_lrange.return_value = ["85000.50,1.5", "85001.50,2.5"]
            history = btc_feed.get_price_history()
            assert len(history) == 2
            assert history[0]["price"] == 85000.50
            assert history[0]["volume"] == 1.5

    def test_start_stop(self, btc_feed):
        """Test starting and stopping the price feed"""
        with patch('threading.Thread') as mock_thread:
            btc_feed.start()
            assert btc_feed.is_running is True
            mock_thread.assert_called_once()
            
            btc_feed.stop()
            assert btc_feed.is_running is False 