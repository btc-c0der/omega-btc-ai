import unittest
import sys
import os
import json
import redis
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timezone, timedelta

# Set up path for imports
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import modules to test
from omega_ai.db_manager.database import analyze_price_trend, insert_price_movement
from omega_ai.monitor.monitor_market_trends_fixed import detect_possible_mm_traps

class TestMarketTrendMonitor(unittest.TestCase):
    """Test cases for the market trends monitor functionality"""

    def setUp(self):
        """Set up test environment"""
        # Mock Redis
        self.redis_patcher = patch('redis.StrictRedis')
        self.mock_redis = self.redis_patcher.start()
        self.mock_redis_instance = MagicMock()
        self.mock_redis.return_value = self.mock_redis_instance
        
        # Also mock the redis_conn in the database module
        self.db_redis_patcher = patch('omega_ai.db_manager.database.redis_conn')
        self.mock_db_redis = self.db_redis_patcher.start()
        
        # Set up the mock to return None for cached trend data to force recalculation
        self.mock_db_redis.get.return_value = None

    def tearDown(self):
        """Clean up after tests"""
        self.redis_patcher.stop()
        self.db_redis_patcher.stop()

    @patch('omega_ai.db_manager.database.insert_trend_analysis', return_value=None)
    @patch('omega_ai.db_manager.database.fetch_multi_interval_movements')
    def test_analyze_price_trend_normal_data(self, mock_fetch, mock_insert):
        """Test price trend analysis with normal data"""
        # Setup mock data
        mock_fetch.return_value = [
            {'o': 58000.0, 'c': 60000.0, 'timestamp': datetime.now(timezone.utc).isoformat()},
            {'o': 57000.0, 'c': 58000.0, 'timestamp': datetime.now(timezone.utc).isoformat()}
        ]
        
        # Test
        trend, change = analyze_price_trend(15)
        
        # Assertions
        self.assertEqual(trend, "Strongly Bullish")
        self.assertAlmostEqual(change, 5.26, places=2)
        
    @patch('omega_ai.db_manager.database.insert_trend_analysis', return_value=None)
    @patch('omega_ai.db_manager.database.fetch_multi_interval_movements')
    def test_analyze_price_trend_missing_data(self, mock_fetch, mock_insert):
        """Test price trend analysis with missing data"""
        # Setup mock data - empty list
        mock_fetch.return_value = []
        
        # Test
        trend, change = analyze_price_trend(15)
        
        # Assertions
        self.assertEqual(trend, "Neutral")
        self.assertEqual(change, 0.0)
        
    @patch('omega_ai.db_manager.database.insert_trend_analysis', return_value=None)
    @patch('omega_ai.db_manager.database.fetch_multi_interval_movements')
    def test_analyze_price_trend_invalid_price(self, mock_fetch, mock_insert):
        """Test price trend analysis with invalid price data"""
        # Setup mock data with zero reference price
        mock_fetch.return_value = [
            {'o': 60000.0, 'c': 60000.0, 'timestamp': datetime.now(timezone.utc).isoformat()},
            {'o': 0.0, 'c': 60000.0, 'timestamp': datetime.now(timezone.utc).isoformat()}
        ]
        
        # Test
        trend, change = analyze_price_trend(15)
        
        # Assertions
        self.assertEqual(trend, "Invalid Price")
        self.assertEqual(change, 0.0)
        
    def test_detect_mm_traps_normal_data(self):
        """Test MM trap detection with normal data"""
        # Test strongly bearish trend
        trap_type, confidence = detect_possible_mm_traps(
            "15min", "Strongly Bearish", -3.5, 1200.0
        )
        
        # Assertions
        self.assertEqual(trap_type, "Bear Trap")
        self.assertGreater(confidence, 0.8)
        
        # Test strongly bullish trend
        trap_type, confidence = detect_possible_mm_traps(
            "15min", "Strongly Bullish", 4.2, 1500.0
        )
        
        # Assertions
        self.assertEqual(trap_type, "Bull Trap")
        self.assertGreater(confidence, 0.8)
        
    def test_detect_mm_traps_invalid_data(self):
        """Test MM trap detection with invalid data"""
        # Test with very small price change
        trap_type, confidence = detect_possible_mm_traps(
            "15min", "Slightly Bearish", -0.02, 1.5
        )
        
        # Assertions
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)
        
    def test_detect_mm_traps_unrealistic_change(self):
        """Test MM trap detection with unrealistic price change"""
        # Test with extremely large negative change
        trap_type, confidence = detect_possible_mm_traps(
            "15min", "Strongly Bearish", -40.0, 40.0
        )
        
        # Assertions - should still detect trap but we'll verify it's working
        self.assertEqual(trap_type, "Bear Trap")
        self.assertGreater(confidence, 0.8)
        
    @patch('omega_ai.db_manager.database.insert_trend_analysis', return_value=None)
    @patch('omega_ai.db_manager.database.fetch_multi_interval_movements')
    def test_trend_standardization(self, mock_fetch, mock_insert):
        """Test consistency of trend values across the system"""
        # Setup mock data for different trend scenarios
        mock_fetch.return_value = [
            {'o': 60000.0, 'c': 60000.0, 'timestamp': datetime.now(timezone.utc).isoformat()},
            {'o': 58000.0, 'c': 58000.0, 'timestamp': datetime.now(timezone.utc).isoformat()}
        ]
        
        # Test
        trend, change = analyze_price_trend(15)
        
        # Assertions - verify trend value is one of the standardized values
        self.assertIn(trend, ["Strongly Bullish", "Bullish", "Neutral", "Bearish", "Strongly Bearish", "No Data", "Invalid Price"])
        
    @patch('omega_ai.db_manager.database.redis_conn')
    def test_price_movement_decimal_places(self, mock_redis):
        """Test handling of price movement decimal places"""
        # Insert price movement with known values
        insert_price_movement(
            price=60000.123456789,  # Test with many decimal places
            volume=100.0,
            interval=5,
            change_pct=1.23456789,
            abs_change=723.123456789
        )
        
        # Check Redis calls
        mock_redis.set.assert_any_call("last_btc_price", "60000.123456789")
        mock_redis.lpush.assert_any_call("btc_movement_history", "60000.123456789,100.0")
        mock_redis.lpush.assert_any_call("btc_change_history", "1.23456789")
        mock_redis.lpush.assert_any_call("abs_price_change_history", "723.123456789")

if __name__ == '__main__':
    unittest.main() 