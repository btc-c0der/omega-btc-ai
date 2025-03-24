import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timezone

# Import the module to be tested
from omega_ai.monitor.market_trends_monitor_ai import AIEnhancedMarketTrendAnalyzer


class TestMarketTrendsMonitor(unittest.TestCase):
    """Test the AI Enhanced Market Trend Analyzer."""
    
    def setUp(self):
        """Set up the test environment."""
        # Disable real connections
        self.db_patcher = patch('omega_ai.db_manager.database.redis_conn')
        self.db_mock = self.db_patcher.start()
        
        self.fib_patcher = patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
        self.fib_mock = self.fib_patcher.start()
        
        # Mock Redis connection
        self.redis_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.redis_conn')
        self.redis_mock = self.redis_patcher.start()
        
        # Mock the get method
        self.redis_mock.get.side_effect = self._mock_redis_get
        self.redis_mock.lrange.return_value = ["0.5", "0.7", "0.3", "0.4"]
        
        # Mock the MarketTrendsModel
        self.model_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.MarketTrendsModel')
        self.model_mock = self.model_patcher.start()
        
        # Create a mock instance of MarketTrendsModel
        self.model_instance = MagicMock()
        self.model_mock.return_value = self.model_instance
        
        # Mock generate_predictions method
        self.model_instance.generate_predictions.return_value = self._mock_ai_predictions()
        
        # Mock analyze_price_trend
        self.analyze_trend_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.analyze_price_trend')
        self.analyze_trend_mock = self.analyze_trend_patcher.start()
        self.analyze_trend_mock.return_value = ("Bullish", 1.5)
        
        # Mock Fibonacci functions
        self.get_fib_levels_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.get_current_fibonacci_levels')
        self.get_fib_levels_mock = self.get_fib_levels_patcher.start()
        self.get_fib_levels_mock.return_value = self._mock_fibonacci_levels()
        
        self.check_fib_align_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.check_fibonacci_alignment')
        self.check_fib_align_mock = self.check_fib_align_patcher.start()
        self.check_fib_align_mock.return_value = self._mock_fibonacci_alignment()
        
        self.update_fib_patcher = patch('omega_ai.monitor.market_trends_monitor_ai.update_fibonacci_data')
        self.update_fib_mock = self.update_fib_patcher.start()
        
        # Create analyzer for testing
        self.analyzer = AIEnhancedMarketTrendAnalyzer()
    
    def tearDown(self):
        """Clean up after tests."""
        self.redis_patcher.stop()
        self.model_patcher.stop()
        self.analyze_trend_patcher.stop()
        self.get_fib_levels_patcher.stop()
        self.check_fib_align_patcher.stop()
        self.update_fib_patcher.stop()
        self.db_patcher.stop()
        self.fib_patcher.stop()
    
    def _mock_redis_get(self, key):
        """Mock Redis get method."""
        data = {
            "last_btc_price": "83000",
            "last_btc_volume": "5000",
            "abs_price_change_history": json.dumps(["0.5", "0.7", "0.3"])
        }
        return data.get(key)
    
    def _mock_ai_predictions(self):
        """Create mock AI predictions."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trend": {
                "trend": "Bullish",
                "confidence": 0.85
            },
            "price": {
                "price": 85000.0,
                "current_price": 83000.0,
                "pct_change": 2.4,
                "confidence": 0.75
            },
            "trap": {
                "trap_detected": False,
                "confidence": 0.92
            },
            "divine_wisdom": "The market follows the eternal dance of the Fibonacci sequence. Observe the pattern and flow with it."
        }
    
    def _mock_fibonacci_levels(self):
        """Create mock Fibonacci levels."""
        return {
            "0.0": 75000.0,
            "0.236": 76800.0,
            "0.382": 78100.0,
            "0.5": 79000.0,
            "0.618": 80000.0,
            "0.786": 81500.0,
            "1.0": 83000.0
        }
    
    def _mock_fibonacci_alignment(self):
        """Create mock Fibonacci alignment data."""
        return {
            "type": "GOLDEN_RATIO",
            "level": "0.618",
            "price": 80000.0,
            "distance_pct": 0.01,
            "confidence": 0.95,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def test_analyze_trends(self):
        """Test the analyze_trends method."""
        # Run the method
        results = self.analyzer.analyze_trends()
        
        # Check that results are as expected
        self.assertIn("current_price", results)
        self.assertEqual(results["current_price"], 83000.0)
        
        # Check timeframes
        self.assertIn("1min", results)
        self.assertIn("15min", results)
        
        # Check trend data
        self.assertEqual(results["15min"]["trend"], "Bullish")
        self.assertEqual(results["15min"]["change"], 1.5)
        
        # Check Fibonacci data
        self.assertIn("fibonacci_levels", results)
        self.assertIn("fibonacci_alignment", results)
        
        # Check AI predictions
        self.assertIn("ai_predictions", results)
        self.assertEqual(results["ai_predictions"]["trend"]["trend"], "Bullish")
        self.assertEqual(results["ai_predictions"]["price"]["price"], 85000.0)
    
    def test_calculate_volatility(self):
        """Test the calculate_volatility method."""
        # Calculate volatility
        volatility = self.analyzer.calculate_volatility()
        
        # Verify result
        self.assertEqual(volatility, 0.475)  # (0.5 + 0.7 + 0.3 + 0.4) / 4
    
    def test_determine_market_regime(self):
        """Test the determine_market_regime method."""
        # Mock calculate_volatility
        with patch.object(self.analyzer, 'calculate_volatility', return_value=0.7):
            # Get regime
            regime = self.analyzer.determine_market_regime()
            
            # Check result
            self.assertEqual(regime, "Moderate Volatility Bullish")
    
    def test_high_volatility_regime(self):
        """Test high volatility regime determination."""
        # Mock calculate_volatility for high volatility
        with patch.object(self.analyzer, 'calculate_volatility', return_value=1.5):
            # Get regime
            regime = self.analyzer.determine_market_regime()
            
            # Check result
            self.assertEqual(regime, "High Volatility Bullish")
    
    def test_low_volatility_regime(self):
        """Test low volatility regime determination."""
        # Mock calculate_volatility for low volatility
        with patch.object(self.analyzer, 'calculate_volatility', return_value=0.3):
            # Get regime
            regime = self.analyzer.determine_market_regime()
            
            # Check result
            self.assertEqual(regime, "Low Volatility Bullish")


if __name__ == '__main__':
    unittest.main() 