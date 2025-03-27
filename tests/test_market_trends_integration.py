import unittest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from omega_ai.monitor.monitor_market_trends import (
    MarketTrendAnalyzer,
    detect_possible_mm_traps,
    check_fibonacci_alignment,
    redis_conn
)

class TestMarketTrendsIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.analyzer = MarketTrendAnalyzer()
        self.test_timeframe = "15min"
        self.test_price = 80000.0
        self.test_volume = 1000.0
        
        # Mock Redis data
        self.redis_mock = MagicMock()
        self.redis_mock.get.side_effect = lambda key: {
            "last_btc_price": str(self.test_price),
            "last_btc_volume": str(self.test_volume),
            "abs_price_change_history": ["0.5", "0.7", "0.3", "0.4"]
        }.get(key)
        
        # Mock trend analysis
        self.trend_mock = MagicMock()
        self.trend_mock.return_value = ("Strongly Bullish", 2.0)
        
        # Mock Fibonacci data
        self.fib_mock = MagicMock()
        self.fib_mock.return_value = {
            "61.8%": 80000.0,
            "50.0%": 75000.0,
            "38.2%": 70000.0
        }

    @patch('redis.StrictRedis')
    def test_market_trend_analysis_with_trap_detection(self, redis_mock):
        """Test market trend analysis with integrated trap detection."""
        redis_mock.return_value = self.redis_mock
        
        with patch('omega_ai.monitor.monitor_market_trends.analyze_price_trend', self.trend_mock):
            with patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels', self.fib_mock):
                results = self.analyzer.analyze_trends()
                
                # Verify basic trend analysis
                self.assertIn("15min", results)
                self.assertEqual(results["15min"]["trend"], "Strongly Bullish")
                self.assertEqual(results["15min"]["change"], 2.0)
                
                # Verify trap detection
                trap_type, confidence = detect_possible_mm_traps(
                    self.test_timeframe,
                    results["15min"]["trend"],
                    results["15min"]["change"],
                    abs(results["15min"]["change"])
                )
                self.assertEqual(trap_type, "Bull Trap")
                self.assertGreater(confidence, 0.3)

    @patch('omega_ai.monitor.monitor_market_trends.redis_conn')
    @patch('omega_ai.monitor.monitor_market_trends.get_current_fibonacci_levels')
    def test_fibonacci_alignment_with_trap_detection(self, get_fib_mock, redis_mock):
        """Test Fibonacci alignment detection with trap detection."""
        redis_mock.get.return_value = str(self.test_price)
        get_fib_mock.return_value = {
            "61.8%": 80000.0,  # Exact match with test price
            "50.0%": 75000.0,
            "38.2%": 70000.0
        }
        
        alignment = check_fibonacci_alignment()
        
        # Verify Fibonacci alignment
        self.assertIsNotNone(alignment)
        self.assertEqual(alignment["type"], "GOLDEN_RATIO")
        self.assertEqual(alignment["level"], "61.8%")
        self.assertEqual(alignment["price"], 80000.0)
        self.assertEqual(alignment["distance_pct"], 0.0)
        self.assertEqual(alignment["confidence"], 1.0)

    @patch('redis.StrictRedis')
    def test_market_regime_determination(self, redis_mock):
        """Test market regime determination with trap detection."""
        redis_mock.return_value = self.redis_mock
        
        # Mock trend analysis for market regime
        with patch('omega_ai.monitor.monitor_market_trends.analyze_price_trend', self.trend_mock):
            regime = self.analyzer.determine_market_regime()
            
            # Verify market regime
            self.assertIsNotNone(regime)
            self.assertIn("Volatility", regime)
            self.assertIn("Bullish", regime)

    @patch('redis.StrictRedis')
    def test_volatility_calculation(self, redis_mock):
        """Test volatility calculation with trap detection."""
        redis_mock.return_value = self.redis_mock
        
        volatility = self.analyzer.calculate_volatility()
        
        # Verify volatility calculation
        self.assertIsNotNone(volatility)
        self.assertGreater(volatility, 0.0)
        self.assertLess(volatility, 1.0)

    @patch('redis.StrictRedis')
    def test_trap_detection_with_different_conditions(self, redis_mock):
        """Test trap detection with various market conditions."""
        redis_mock.return_value = self.redis_mock
        
        # Test case 1: Strong bull trap
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            "Strongly Bullish",
            5.0,
            4000.0
        )
        self.assertEqual(trap_type, "Bull Trap")
        self.assertEqual(confidence, 1.0)
        
        # Test case 2: Moderate bear trap
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            "Moderately Bearish",
            -3.0,
            -2400.0
        )
        self.assertEqual(trap_type, "Bear Trap")
        self.assertGreater(confidence, 0.5)
        self.assertLess(confidence, 1.0)
        
        # Test case 3: No trap (insufficient price change)
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            "Strongly Bullish",
            1.0,
            800.0
        )
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)

if __name__ == '__main__':
    unittest.main() 