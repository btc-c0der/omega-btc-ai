"""
🌌 OMEGA RASTA FIBONACCI CONFLUENCE TESTS 🌌
===========================================

Tests for the divine Fibonacci confluence detection.
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

class TestFibonacciConfluence:
    """Test suite for Fibonacci confluence detection."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_basic_confluence_detection(self, mock_redis, detector):
        """Test basic Fibonacci confluence detection."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test confluence at 0.618 level
        price = levels[0.618]  # 41236.0
        confluence = detector.detect_fibonacci_confluence(price)
        
        assert confluence['is_confluence'], "Should detect confluence at exact level"
        assert confluence['level'] == 0.618, "Should identify correct level"
        assert confluence['strength'] == 1.0, "Should have maximum strength at exact level"
        
        print(f"{GREEN}✓ Basic confluence detection verified!{RESET}")
        print(f"{GREEN}✓ Confluence at level {confluence['level']:.3f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_near_confluence_detection(self, mock_redis, detector):
        """Test detection of near Fibonacci levels."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test near 0.618 level (within 0.1%)
        price = levels[0.618] * 1.001  # Slightly above 0.618
        confluence = detector.detect_fibonacci_confluence(price)
        
        assert confluence['is_confluence'], "Should detect confluence near level"
        assert confluence['level'] == 0.618, "Should identify correct level"
        assert 0.8 < confluence['strength'] < 1.0, "Should have high but not maximum strength"
        
        print(f"{GREEN}✓ Near confluence detection verified!{RESET}")
        print(f"{GREEN}✓ Confluence strength: {confluence['strength']:.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_multiple_confluence_detection(self, mock_redis, detector):
        """Test detection of multiple Fibonacci levels."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test price near multiple levels
        price = 41000.0  # Near both 0.5 and 0.618
        confluence = detector.detect_fibonacci_confluence(price)
        
        assert confluence['is_confluence'], "Should detect confluence"
        assert len(confluence['nearby_levels']) > 1, "Should identify multiple levels"
        assert confluence['strength'] > 0.8, "Should have high strength for multiple levels"
        
        print(f"{GREEN}✓ Multiple confluence detection verified!{RESET}")
        print(f"{GREEN}✓ Nearby levels: {[f'{level:.3f}' for level in confluence['nearby_levels']]}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_confluence_strength_calculation(self, mock_redis, detector):
        """Test calculation of confluence strength."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test different distances from 0.618 level
        test_cases = [
            (levels[0.618], 1.0),  # Exact level
            (levels[0.618] * 1.001, 0.9),  # Very close
            (levels[0.618] * 1.01, 0.7),  # Moderately close
            (levels[0.618] * 1.05, 0.3),  # Far
        ]
        
        for price, expected_strength in test_cases:
            confluence = detector.detect_fibonacci_confluence(price)
            assert abs(confluence['strength'] - expected_strength) < 0.1, f"Strength should be near {expected_strength}"
        
        print(f"{GREEN}✓ Confluence strength calculation verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_no_confluence(self, mock_redis, detector):
        """Test handling of no Fibonacci confluence."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test price far from any level
        price = 43000.0  # Above all levels
        confluence = detector.detect_fibonacci_confluence(price)
        
        assert not confluence['is_confluence'], "Should not detect confluence"
        assert confluence['strength'] < 0.1, "Should have very low strength"
        assert len(confluence['nearby_levels']) == 0, "Should have no nearby levels"
        
        print(f"{GREEN}✓ No confluence handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_extreme_price(self, mock_redis, detector):
        """Test handling of extreme price values."""
        # Set up swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Calculate Fibonacci levels
        levels = detector.calculate_fibonacci_levels()
        
        # Test extreme price values
        test_cases = [
            (0.0, "zero price"),
            (-1000.0, "negative price"),
            (float('inf'), "infinite price"),
            (float('nan'), "NaN price"),
        ]
        
        for price, case in test_cases:
            confluence = detector.detect_fibonacci_confluence(price)
            assert not confluence['is_confluence'], f"Should handle {case} correctly"
            assert confluence['strength'] == 0.0, f"Should have zero strength for {case}"
        
        print(f"{GREEN}✓ Extreme price handling verified!{RESET}") 