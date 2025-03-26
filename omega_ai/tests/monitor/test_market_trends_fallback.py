import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import os
import sys
import logging
from io import StringIO

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from omega_ai.monitor.monitor_market_trends import detect_possible_mm_traps, monitor_market_trends
from omega_ai.utils.test_redis_manager import TestRedisManager

class TestMarketTrendsFallback(unittest.TestCase):
    """Test cases for market trends fallback system."""
    
    def setUp(self):
        """Set up test environment."""
        self.redis_manager = TestRedisManager()
        
        # Patch Redis connections
        self.redis_patchers = [
            patch('omega_ai.monitor.monitor_market_trends.redis_conn', self.redis_manager.redis),
            patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn', self.redis_manager.redis),
            patch('omega_ai.db_manager.database.redis_conn', self.redis_manager.redis)
        ]
        
        # Start all patchers
        for patcher in self.redis_patchers:
            patcher.start()
        
        # Set up logging capture
        self.log_output = StringIO()
        self.log_handler = logging.StreamHandler(self.log_output)
        self.log_handler.setLevel(logging.WARNING)
        logging.getLogger().addHandler(self.log_handler)
        
        self._setup_test_data()
    
    def tearDown(self):
        """Clean up test environment."""
        # Stop all patchers
        for patcher in self.redis_patchers:
            patcher.stop()
        
        # Clean up logging
        logging.getLogger().removeHandler(self.log_handler)
        self.log_output.close()
        
        self.redis_manager._clear_test_data()
    
    def _setup_test_data(self):
        """Set up test data in Redis."""
        # Add test price data
        self.redis_manager.set_cached("last_btc_price", "50000.0")
        self.redis_manager.set_cached("btc_candle_15min", json.dumps({
            "price": 50000.0,
            "timestamp": datetime.now().isoformat()
        }))
        
        # Add test trend data
        self.redis_manager.set_cached("btc_trend_15min", json.dumps({
            "trend": "Bullish",
            "change": 2.1,
            "timestamp": datetime.now().isoformat()
        }))
        
        # Add test price history
        test_prices = [
            {"price": 50000.0, "volume": 100.0, "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat()},
            {"price": 51000.0, "volume": 150.0, "timestamp": (datetime.now() - timedelta(minutes=4)).isoformat()},
            {"price": 52000.0, "volume": 200.0, "timestamp": (datetime.now() - timedelta(minutes=3)).isoformat()},
            {"price": 53000.0, "volume": 180.0, "timestamp": (datetime.now() - timedelta(minutes=2)).isoformat()},
            {"price": 54000.0, "volume": 160.0, "timestamp": (datetime.now() - timedelta(minutes=1)).isoformat()},
            {"price": 55000.0, "volume": 140.0, "timestamp": datetime.now().isoformat()}
        ]
        for price_data in test_prices:
            self.redis_manager.lpush("btc_movement_history", json.dumps(price_data))
    
    def test_detect_possible_mm_traps_with_data(self):
        """Test detecting possible MM traps with available data."""
        traps = detect_possible_mm_traps(
            timeframe="15min",
            trend="Bullish",
            price_change_pct=2.1,
            price_move=1000.0
        )
        self.assertIsInstance(traps, tuple)
        self.assertEqual(len(traps), 2)
        self.assertEqual(traps[0], "Bull Trap")
        self.assertIsInstance(traps[1], float)
    
    def test_detect_possible_mm_traps_no_data(self):
        """Test detecting possible MM traps without data."""
        # Clear test data
        self.redis_manager._clear_test_data()
        traps = detect_possible_mm_traps(
            timeframe="15min",
            trend="No Data",
            price_change_pct=0.0,
            price_move=0.0
        )
        self.assertIsInstance(traps, tuple)
        self.assertEqual(len(traps), 2)
        self.assertIsNone(traps[0])
        self.assertEqual(traps[1], 0.0)
    
    def test_monitor_market_trends(self):
        """Test monitoring market trends with data."""
        with patch('time.sleep', side_effect=Exception("Stop iteration")):
            try:
                monitor_market_trends()
            except Exception as e:
                if str(e) != "Stop iteration":
                    raise
        
        # Verify trend data was processed
        trends = self.redis_manager.get_cached("btc_trend_15min")
        self.assertIsNotNone(trends)
        trend_data = json.loads(str(trends))
        self.assertIsInstance(trend_data, dict)
        self.assertIn("trend", trend_data)
        self.assertIn("change", trend_data)
        self.assertIn("timestamp", trend_data)
    
    def test_monitor_market_trends_no_data(self):
        """Test that monitor_market_trends handles missing data correctly."""
        # Clear all test data
        self.redis_manager._clear_test_data()
        
        # Verify no trend data exists
        for timeframe in ["15min", "5min", "1min", "30min", "60min", "240min"]:
            self.assertIsNone(self.redis_manager.get_cached(f"btc_trend_{timeframe}"))
        
        # Run the monitor
        with patch('time.sleep') as mock_sleep:
            mock_sleep.side_effect = KeyboardInterrupt
            try:
                monitor_market_trends()
            except KeyboardInterrupt:
                pass
        
        # Verify that no trend data was created
        for timeframe in ["15min", "5min", "1min", "30min", "60min", "240min"]:
            # Check both prefixed and unprefixed keys
            self.assertIsNone(self.redis_manager.get_cached(f"btc_trend_{timeframe}"))
            self.assertIsNone(self.redis_manager.redis.get(f"btc_trend_{timeframe}"))
        
        # Verify warning was logged
        self.assertIn("No current price available for analysis", self.log_output.getvalue())

if __name__ == '__main__':
    unittest.main() 