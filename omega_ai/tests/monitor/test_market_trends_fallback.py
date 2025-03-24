import unittest
import json
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from omega_ai.monitor.monitor_market_trends import detect_possible_mm_traps, monitor_market_trends

class TestMarketTrendsFallback(unittest.TestCase):
    """Test the fallback mechanisms for market trends analysis when data is missing."""

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.logger')
    def test_trap_detection_with_no_data_candle_fallback(self, mock_logger, mock_redis):
        """Test MM trap detection when trend is 'No Data' but candle data is available."""
        # Mock the Redis connection for candle data
        mock_redis.get.side_effect = [
            json.dumps({
                'o': 50000,  # Open price
                'c': 52000,  # Close price (4% increase)
                'h': 52500,  # High
                'l': 49800,  # Low
                'v': 1000,   # Volume
                't': 1615882800000  # Timestamp
            }),
            None  # For any other get call
        ]
        
        # Call the trap detection with No Data trend
        trap_type, confidence = detect_possible_mm_traps("15min", "No Data", 0.0, 0.0)
        
        # Verify the function inferred a trend and returned a trap detection
        self.assertEqual(trap_type, "Bull Trap")
        self.assertGreaterEqual(confidence, 0.3)
        
        # Verify appropriate log messages
        mock_logger.warning.assert_not_called()  # Should not log any warnings

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.logger')
    def test_trap_detection_with_no_data_movement_fallback(self, mock_logger, mock_redis):
        """Test MM trap detection when trend is 'No Data' and falls back to movement history."""
        # Mock Redis to return no candle data but movement history
        mock_redis.get.side_effect = [
            None,  # No candle data
            "85000"  # last_btc_price
        ]
        mock_redis.lrange.return_value = ["80000,1500"]  # Previous price, volume
        
        # Call the trap detection with No Data trend
        trap_type, confidence = detect_possible_mm_traps("15min", "No Data", 0.0, 0.0)
        
        # Verify Redis was queried for both candle and movement data
        mock_redis.get.assert_any_call("btc_candle_15min")
        mock_redis.get.assert_any_call("last_btc_price")
        mock_redis.lrange.assert_called_with("btc_movement_history", 0, 0)
        
        # Verify the function inferred a trend and returned a trap detection
        self.assertEqual(trap_type, "Bull Trap")
        self.assertGreaterEqual(confidence, 0.3)

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.logger')
    def test_trap_detection_with_no_data_no_fallback(self, mock_logger, mock_redis):
        """Test MM trap detection when trend is 'No Data' and no fallback data is available."""
        # Mock Redis to return no data at all
        mock_redis.get.return_value = None
        mock_redis.lrange.return_value = []
        
        # Call the trap detection with No Data trend
        trap_type, confidence = detect_possible_mm_traps("15min", "No Data", 0.0, 0.0)
        
        # Verify the function returns no trap when no data is available
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)
        
        # Make sure get was called at least once
        self.assertTrue(mock_redis.get.called)

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.logger')
    def test_trap_detection_with_bear_trend_candle_fallback(self, mock_logger, mock_redis):
        """Test MM trap detection when trend is 'Bearish' using candle data."""
        # Mock the Redis connection for candle data
        mock_redis.get.return_value = json.dumps({
            'o': 50000,  # Open price
            'c': 48000,  # Close price (4% decrease)
            'h': 50100,  # High
            'l': 47500,  # Low
            'v': 1000,   # Volume
            't': 1615882800000  # Timestamp
        })
        
        # Call the trap detection with Bearish trend
        trap_type, confidence = detect_possible_mm_traps("15min", "Bearish", -4.0, 2000)
        
        # Verify the function identified a bear trap
        self.assertEqual(trap_type, "Bear Trap")
        self.assertGreaterEqual(confidence, 0.3)

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.get_current_fibonacci_levels')
    @patch('omega_ai.monitor.monitor_market_trends.update_fibonacci_data')
    @patch('omega_ai.monitor.monitor_market_trends.MarketTrendAnalyzer')
    @patch('omega_ai.monitor.monitor_market_trends.time')
    def test_monitor_startup_data_availability(self, mock_time, mock_analyzer, 
                                               mock_update_fib, mock_get_fib, mock_redis):
        """Test that monitor_market_trends properly checks data availability on startup."""
        # Set up mocks
        mock_time.sleep.side_effect = [None, Exception("Stop iteration")]  # Break after first iteration
        mock_redis.llen.return_value = 0  # No movement history
        mock_redis.get.return_value = "50000.0"  # BTC price available
        mock_get_fib.return_value = None  # No Fibonacci levels initially
        
        # Set up analyzer mock
        analyzer_instance = MagicMock()
        analyzer_instance.last_analysis_time = None
        analyzer_instance.analysis_interval = 5
        analyzer_instance.analyze_trends.return_value = {"current_price": 50000}
        mock_analyzer.return_value = analyzer_instance
        
        # Call the monitor function (will exit after first iteration due to mock)
        try:
            monitor_market_trends()
        except Exception as e:
            pass  # Expected exception to break the loop
            
        # Verify Redis was queried for movement history
        mock_redis.llen.assert_called_with("btc_movement_history")
        
        # Verify movement history was initialized with current price
        mock_redis.lpush.assert_called_with("btc_movement_history", "50000.0,0")
        
        # Verify candle data availability was checked
        self.assertTrue(mock_redis.get.call_count >= 6)  # At least 6 calls for different timeframes
        
        # Verify Fibonacci data was initialized with price 50000.0 (float)
        mock_update_fib.assert_called_with(50000.0)

if __name__ == '__main__':
    unittest.main() 