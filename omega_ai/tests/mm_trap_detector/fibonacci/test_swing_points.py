
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
🌌 OMEGA RASTA SWING POINT DETECTION TESTS 🌌
============================================

Tests for the divine swing point detection functionality.
May the golden ratio be with you! 🚀
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

class TestSwingPoints:
    """Test suite for swing point detection."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_divine_swing_point_detection(self, mock_redis, detector):
        """Test the divine swing point detection with enhanced validation."""
        # Initialize with some price data
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 42100.0, 42200.0, 42300.0, 42400.0, 42500.0, 42600.0]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Verify swing points are initialized
        assert detector.recent_swing_high is not None, "Swing high should be initialized"
        assert detector.recent_swing_low is not None, "Swing low should be initialized"
        
        # Add a new swing high
        new_high = 42750.0
        detector.update_price_data(new_high, base_time.replace(hour=8))
        
        # Verify swing high was updated
        assert detector.recent_swing_high == new_high, "Swing high should be updated"
        
        # Add a new swing low
        new_low = 41950.0
        detector.update_price_data(new_low, base_time.replace(hour=9))
        
        # Verify swing low was updated
        assert detector.recent_swing_low == new_low, "Swing low should be updated"
        
        print(f"{GREEN}✓ Divine swing point detection verified!{RESET}")
        print(f"{GREEN}✓ Swing high: ${detector.recent_swing_high:,.2f}{RESET}")
        print(f"{GREEN}✓ Swing low: ${detector.recent_swing_low:,.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_enhanced_swing_point_detection(self, mock_redis, detector):
        """Test the enhanced swing point detection with rolling window."""
        # Initialize with price data
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 42100.0, 42200.0, 42300.0, 42400.0, 42500.0, 42600.0]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Add a new swing high with confirmation
        new_high = 42750.0
        for i in range(3):  # Add 3 confirmations
            detector.update_price_data(new_high, base_time.replace(hour=8+i))
            detector.update_price_data(new_high - 100, base_time.replace(hour=9+i))
        
        # Verify swing high was updated
        assert detector.recent_swing_high == new_high, "Swing high should be updated"
        
        # Add a new swing low with confirmation
        new_low = 41950.0
        for i in range(3):  # Add 3 confirmations
            detector.update_price_data(new_low, base_time.replace(hour=12+i))
            detector.update_price_data(new_low + 100, base_time.replace(hour=13+i))
        
        # Verify swing low was updated
        assert detector.recent_swing_low == new_low, "Swing low should be updated"
        
        print(f"{GREEN}✓ Enhanced swing point detection verified!{RESET}")
        print(f"{GREEN}✓ Swing high: ${detector.recent_swing_high:,.2f}{RESET}")
        print(f"{GREEN}✓ Swing low: ${detector.recent_swing_low:,.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_small_price_range(self, mock_redis, detector):
        """Test handling of small price ranges."""
        # Initialize with very close prices
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 42001.0, 42002.0, 42003.0, 42004.0]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Verify swing points are not set due to small range
        assert detector.recent_swing_high is None, "Swing high should not be set for small range"
        assert detector.recent_swing_low is None, "Swing low should not be set for small range"
        
        print(f"{GREEN}✓ Small price range handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_equal_swing_points(self, mock_redis, detector):
        """Test handling of equal swing points."""
        # Initialize with equal prices
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 42000.0, 42000.0, 42000.0, 42000.0]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Verify swing points are not set due to equal prices
        assert detector.recent_swing_high is None, "Swing high should not be set for equal prices"
        assert detector.recent_swing_low is None, "Swing low should not be set for equal prices"
        
        print(f"{GREEN}✓ Equal swing points handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_missing_swing_points(self, mock_redis, detector):
        """Test handling of missing swing points."""
        # Initialize with no price data
        assert detector.recent_swing_high is None, "Swing high should be None initially"
        assert detector.recent_swing_low is None, "Swing low should be None initially"
        
        # Add single price
        base_time = datetime.now(timezone.utc)
        detector.update_price_data(42000.0, base_time)
        
        # Verify swing points are set to the single price
        assert detector.recent_swing_high == 42000.0, "Swing high should be set to single price"
        assert detector.recent_swing_low == 42000.0, "Swing low should be set to single price"
        
        print(f"{GREEN}✓ Missing swing points handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_invalid_timestamp_handling(self, mock_redis, detector):
        """Test handling of invalid timestamps."""
        # Test None timestamp
        with pytest.raises(ValueError, match="Timestamp cannot be None"):
            detector.update_price_data(42000.0, None)
        
        # Test invalid timestamp type
        with pytest.raises(ValueError, match="Invalid timestamp type"):
            detector.update_price_data(42000.0, "invalid")
        
        print(f"{GREEN}✓ Invalid timestamp handling verified!{RESET}") 