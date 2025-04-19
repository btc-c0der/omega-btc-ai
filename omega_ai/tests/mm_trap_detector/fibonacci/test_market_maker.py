
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
🌌 OMEGA RASTA MARKET MAKER TESTS 🌌
===================================

Tests for the divine market maker detection functionality.
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

class TestMarketMaker:
    """Test suite for market maker detection."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_market_maker_fakeout_detection(self, mock_redis, detector):
        """Test detection of market maker fakeouts."""
        # Set up price data with fakeout pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial price
            42500.0,  # First push up
            43000.0,  # Second push up
            43500.0,  # Third push up
            44000.0,  # Fake high
            43000.0,  # Sharp reversal
            42000.0,  # Continued reversal
            41000.0   # Target reached
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect market maker fakeout
        fakeout = detector.detect_market_maker_fakeout()
        
        assert fakeout['is_fakeout'], "Should detect market maker fakeout"
        assert fakeout['type'] == 'bullish', "Should identify bullish fakeout"
        assert fakeout['strength'] > 0.7, "Should have strong fakeout pattern"
        
        print(f"{GREEN}✓ Market maker fakeout detection verified!{RESET}")
        print(f"{GREEN}✓ Fakeout type: {fakeout['type']}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_wick_deviation_detection(self, mock_redis, detector):
        """Test detection of wick deviations."""
        # Set up price data with wick pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial price
            42500.0,  # Body high
            43000.0,  # Upper wick
            42500.0,  # Close
            42000.0,  # Next candle
            41500.0,  # Body low
            41000.0,  # Lower wick
            41500.0   # Close
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect wick deviation
        wick = detector.detect_wick_deviation()
        
        assert wick['has_deviation'], "Should detect wick deviation"
        assert wick['upper_deviation'] > 0, "Should identify upper wick"
        assert wick['lower_deviation'] > 0, "Should identify lower wick"
        
        print(f"{GREEN}✓ Wick deviation detection verified!{RESET}")
        print(f"{GREEN}✓ Upper deviation: {wick['upper_deviation']:.2f}{RESET}")
        print(f"{GREEN}✓ Lower deviation: {wick['lower_deviation']:.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_reversal_validation_at_fibonacci_levels(self, mock_redis, detector):
        """Test validation of reversals at Fibonacci levels."""
        # Set up price data with Fibonacci-based reversal
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial high
            41236.0,  # 0.618 retracement
            41000.0,  # Slight overshoot
            41500.0,  # Reversal
            42000.0   # Target reached
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Validate reversal
        reversal = detector.validate_reversal_at_fibonacci()
        
        assert reversal['is_valid'], "Should validate Fibonacci reversal"
        assert reversal['level'] == 0.618, "Should identify correct Fibonacci level"
        assert reversal['strength'] > 0.8, "Should have strong reversal pattern"
        
        print(f"{GREEN}✓ Fibonacci reversal validation verified!{RESET}")
        print(f"{GREEN}✓ Reversal level: {reversal['level']:.3f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_support_resistance_confirmation(self, mock_redis, detector):
        """Test confirmation of Fibonacci support/resistance levels."""
        # Set up price data with multiple tests of levels
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial high
            41236.0,  # First test of 0.618
            41500.0,  # Bounce
            41236.0,  # Second test of 0.618
            41500.0,  # Bounce
            41236.0,  # Third test of 0.618
            41500.0   # Bounce
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Confirm support/resistance
        confirmation = detector.confirm_fibonacci_levels()
        
        assert confirmation['has_confirmation'], "Should confirm Fibonacci levels"
        assert confirmation['level'] == 0.618, "Should identify confirmed level"
        assert confirmation['strength'] > 0.9, "Should have strong confirmation"
        
        print(f"{GREEN}✓ Fibonacci level confirmation verified!{RESET}")
        print(f"{GREEN}✓ Confirmed level: {confirmation['level']:.3f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_market_maker_trap_detection(self, mock_redis, detector):
        """Test detection of market maker traps."""
        # Set up price data with trap pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial price
            42500.0,  # First push
            43000.0,  # Second push
            43500.0,  # Trap high
            43000.0,  # Sharp reversal
            42500.0,  # Continued reversal
            42000.0,  # Target reached
            41500.0   # Further reversal
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect market maker trap
        trap = detector.detect_market_maker_trap()
        
        assert trap['is_trap'], "Should detect market maker trap"
        assert trap['type'] == 'bullish', "Should identify trap type"
        assert trap['strength'] > 0.8, "Should have strong trap pattern"
        
        print(f"{GREEN}✓ Market maker trap detection verified!{RESET}")
        print(f"{GREEN}✓ Trap type: {trap['type']}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_no_market_maker_pattern(self, mock_redis, detector):
        """Test handling of non-market maker patterns."""
        # Set up price data with no clear pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Random price movements
            43000.0,
            41000.0,
            44000.0,
            40000.0,
            45000.0,
            39000.0
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect market maker patterns
        fakeout = detector.detect_market_maker_fakeout()
        trap = detector.detect_market_maker_trap()
        
        assert not fakeout['is_fakeout'], "Should not detect fakeout in random pattern"
        assert not trap['is_trap'], "Should not detect trap in random pattern"
        
        print(f"{GREEN}✓ No market maker pattern handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_insufficient_data_for_trap(self, mock_redis, detector):
        """Test handling of insufficient data for trap detection."""
        # Set up minimal price data
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 41000.0]  # Only two points
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect market maker patterns
        fakeout = detector.detect_market_maker_fakeout()
        trap = detector.detect_market_maker_trap()
        
        assert not fakeout['is_fakeout'], "Should not detect fakeout with insufficient data"
        assert not trap['is_trap'], "Should not detect trap with insufficient data"
        
        print(f"{GREEN}✓ Insufficient data handling verified!{RESET}") 