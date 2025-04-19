
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
🌌 OMEGA RASTA FIBONACCI LEVEL TESTS 🌌
======================================

Tests for the divine Fibonacci level calculations.
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

class TestFibonacciLevels:
    """Test suite for Fibonacci level calculations."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_level_calculation(self, mock_redis, detector):
        """Test the calculation of Fibonacci levels."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Verify key Fibonacci levels
        assert 0.0 in levels, "0.0 level should be present"
        assert 0.236 in levels, "0.236 level should be present"
        assert 0.382 in levels, "0.382 level should be present"
        assert 0.5 in levels, "0.5 level should be present"
        assert 0.618 in levels, "0.618 level should be present"
        assert 0.786 in levels, "0.786 level should be present"
        assert 1.0 in levels, "1.0 level should be present"
        
        # Verify level values
        assert levels[0.0] == 40000.0, "0.0 level should be swing low"
        assert levels[1.0] == 42000.0, "1.0 level should be swing high"
        
        print(f"{GREEN}✓ Fibonacci level calculation verified!{RESET}")
        for level, price in levels.items():
            print(f"{GREEN}✓ Level {level:.3f}: ${price:,.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_level_validation(self, mock_redis, detector):
        """Test validation of Fibonacci levels."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Verify level ordering
        sorted_levels = sorted(levels.keys())
        assert sorted_levels == [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0], "Levels should be in ascending order"
        
        # Verify price ordering
        sorted_prices = sorted(levels.values())
        assert sorted_prices == [40000.0, 40472.0, 40764.0, 41000.0, 41236.0, 41528.0, 42000.0], "Prices should be in ascending order"
        
        print(f"{GREEN}✓ Fibonacci level validation verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_level_extensions(self, mock_redis, detector):
        """Test calculation of Fibonacci extensions."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels with extensions
        levels = detector.calculate_fibonacci_levels(include_extensions=True)
        
        # Verify extension levels
        assert 1.618 in levels, "1.618 extension should be present"
        assert 2.618 in levels, "2.618 extension should be present"
        assert 3.618 in levels, "3.618 extension should be present"
        
        # Verify extension values
        assert levels[1.618] == 43236.0, "1.618 extension should be calculated correctly"
        assert levels[2.618] == 45236.0, "2.618 extension should be calculated correctly"
        assert levels[3.618] == 47236.0, "3.618 extension should be calculated correctly"
        
        print(f"{GREEN}✓ Fibonacci level extensions verified!{RESET}")
        for level, price in levels.items():
            if level > 1.0:
                print(f"{GREEN}✓ Extension {level:.3f}: ${price:,.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_level_precision(self, mock_redis, detector):
        """Test precision of Fibonacci level calculations."""
        # Set up swing points with precise values
        detector.recent_swing_high = 42000.123456
        detector.recent_swing_low = 40000.123456
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Verify precision is maintained
        assert levels[0.0] == 40000.123456, "Swing low precision should be maintained"
        assert levels[1.0] == 42000.123456, "Swing high precision should be maintained"
        
        # Verify intermediate level precision
        assert levels[0.618] == 41236.123456, "0.618 level precision should be maintained"
        
        print(f"{GREEN}✓ Fibonacci level precision verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_zero_range(self, mock_redis, detector):
        """Test handling of zero price range."""
        # Set up equal swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 42000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Verify all levels are equal to the price
        for level, price in levels.items():
            assert price == 42000.0, f"Level {level} should equal price for zero range"
        
        print(f"{GREEN}✓ Zero range handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_negative_range(self, mock_redis, detector):
        """Test handling of negative price range."""
        # Set up reversed swing points
        detector.recent_swing_high = 40000.0
        detector.recent_swing_low = 42000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Verify levels are calculated correctly despite reversed range
        assert levels[0.0] == 42000.0, "0.0 level should be the lower price"
        assert levels[1.0] == 40000.0, "1.0 level should be the higher price"
        
        print(f"{GREEN}✓ Negative range handling verified!{RESET}") 