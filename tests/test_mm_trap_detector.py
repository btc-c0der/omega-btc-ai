import unittest
from datetime import datetime, timezone
from omega_ai.monitor.monitor_market_trends import detect_possible_mm_traps

class TestMMTrapDetector(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.test_timeframe = "15min"
        self.test_price_move = 100.0  # $100 price move

    def test_bull_trap_detection(self):
        """Test detection of bull traps."""
        # Test case 1: Strong bullish trend with large price change
        trend = "Strongly Bullish"
        price_change = 2.0  # 2% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertEqual(trap_type, "Bull Trap")
        self.assertGreater(confidence, 0.3)

        # Test case 2: Moderate bullish trend with small price change
        trend = "Moderately Bullish"
        price_change = 0.5  # 0.5% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)

    def test_bear_trap_detection(self):
        """Test detection of bear traps."""
        # Test case 1: Strong bearish trend with large price change
        trend = "Strongly Bearish"
        price_change = -2.0  # -2% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertEqual(trap_type, "Bear Trap")
        self.assertGreater(confidence, 0.3)

        # Test case 2: Moderate bearish trend with small price change
        trend = "Moderately Bearish"
        price_change = -0.5  # -0.5% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)

    def test_neutral_trend_no_trap(self):
        """Test that neutral trends don't trigger traps."""
        trend = "Neutral"
        price_change = 1.5  # 1.5% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertIsNone(trap_type)
        self.assertEqual(confidence, 0.0)

    def test_confidence_calculation(self):
        """Test confidence calculation for different price changes."""
        # Test case 1: Large price change
        trend = "Strongly Bullish"
        price_change = 5.0  # 5% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertEqual(trap_type, "Bull Trap")
        self.assertEqual(confidence, 1.0)  # Should be capped at 1.0

        # Test case 2: Medium price change
        price_change = 3.0  # 3% change
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertEqual(trap_type, "Bull Trap")
        self.assertLess(confidence, 1.0)
        self.assertGreater(confidence, 0.5)

    def test_threshold_conditions(self):
        """Test trap detection thresholds."""
        # Test case 1: Just above threshold
        trend = "Strongly Bullish"
        price_change = 1.51  # Just above 1.5% threshold
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertEqual(trap_type, "Bull Trap")

        # Test case 2: Just below threshold
        price_change = 1.49  # Just below 1.5% threshold
        trap_type, confidence = detect_possible_mm_traps(
            self.test_timeframe,
            trend,
            price_change,
            self.test_price_move
        )
        self.assertIsNone(trap_type)

if __name__ == '__main__':
    unittest.main() 