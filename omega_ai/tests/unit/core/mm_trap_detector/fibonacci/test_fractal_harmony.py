"""
🌌 OMEGA RASTA FRACTAL HARMONY TESTS 🌌
=====================================

Tests for the divine fractal harmony detection.
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

class TestFractalHarmony:
    """Test suite for fractal harmony detection."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_basic_fractal_harmony(self, mock_redis, detector):
        """Test basic fractal harmony detection."""
        # Set up price data with fractal pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial high
            41000.0,  # First retracement
            41500.0,  # First bounce
            40500.0,  # Second retracement
            41250.0,  # Second bounce
            40250.0,  # Third retracement
            41000.0   # Third bounce
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert harmony['is_harmonic'], "Should detect fractal harmony"
        assert harmony['strength'] > 0.7, "Should have strong harmonic pattern"
        assert len(harmony['fractal_points']) >= 3, "Should identify multiple fractal points"
        
        print(f"{GREEN}✓ Basic fractal harmony detection verified!{RESET}")
        print(f"{GREEN}✓ Harmony strength: {harmony['strength']:.2f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fibonacci_fractal_harmony(self, mock_redis, detector):
        """Test Fibonacci-based fractal harmony detection."""
        # Set up price data with Fibonacci-based fractal pattern
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial high
            41236.0,  # 0.618 retracement
            41618.0,  # 0.382 bounce
            40818.0,  # 0.786 retracement
            41409.0,  # 0.236 bounce
            40609.0,  # 0.886 retracement
            41236.0   # 0.618 bounce
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert harmony['is_harmonic'], "Should detect Fibonacci-based harmony"
        assert harmony['strength'] > 0.8, "Should have very strong harmonic pattern"
        assert harmony['fibonacci_ratio'] == 0.618, "Should identify golden ratio"
        
        print(f"{GREEN}✓ Fibonacci fractal harmony detection verified!{RESET}")
        print(f"{GREEN}✓ Fibonacci ratio: {harmony['fibonacci_ratio']:.3f}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_nested_fractal_harmony(self, mock_redis, detector):
        """Test detection of nested fractal patterns."""
        # Set up price data with nested fractal patterns
        base_time = datetime.now(timezone.utc)
        prices = [
            42000.0,  # Initial high
            41000.0,  # First retracement
            41500.0,  # First bounce
            40500.0,  # Second retracement
            41250.0,  # Second bounce
            40250.0,  # Third retracement
            41000.0,  # Third bounce
            40000.0,  # Fourth retracement
            40800.0,  # Fourth bounce
            39800.0,  # Fifth retracement
            40600.0   # Fifth bounce
        ]
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert harmony['is_harmonic'], "Should detect nested fractal harmony"
        assert harmony['strength'] > 0.8, "Should have strong nested pattern"
        assert len(harmony['nested_patterns']) > 1, "Should identify multiple nested patterns"
        
        print(f"{GREEN}✓ Nested fractal harmony detection verified!{RESET}")
        print(f"{GREEN}✓ Number of nested patterns: {len(harmony['nested_patterns'])}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fractal_harmony_strength(self, mock_redis, detector):
        """Test calculation of fractal harmony strength."""
        # Set up price data with varying harmony strength
        base_time = datetime.now(timezone.utc)
        test_cases = [
            # Perfect harmony
            [42000.0, 41236.0, 41618.0, 40818.0, 41409.0],
            # Strong harmony
            [42000.0, 41300.0, 41700.0, 40900.0, 41500.0],
            # Moderate harmony
            [42000.0, 41400.0, 41800.0, 41000.0, 41600.0],
            # Weak harmony
            [42000.0, 41500.0, 41900.0, 41100.0, 41700.0]
        ]
        
        for prices in test_cases:
            # Reset price history
            detector.price_history = []
            
            # Update price data
            for i, price in enumerate(prices):
                timestamp = base_time.replace(hour=i)
                detector.update_price_data(price, timestamp)
            
            # Detect fractal harmony
            harmony = detector.detect_fractal_harmony()
            
            # Verify strength decreases with less perfect patterns
            if prices == test_cases[0]:
                assert harmony['strength'] > 0.9, "Perfect pattern should have high strength"
            elif prices == test_cases[1]:
                assert 0.7 < harmony['strength'] < 0.9, "Strong pattern should have good strength"
            elif prices == test_cases[2]:
                assert 0.5 < harmony['strength'] < 0.7, "Moderate pattern should have medium strength"
            else:
                assert 0.3 < harmony['strength'] < 0.5, "Weak pattern should have low strength"
        
        print(f"{GREEN}✓ Fractal harmony strength calculation verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_no_harmony(self, mock_redis, detector):
        """Test handling of non-harmonic price patterns."""
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
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert not harmony['is_harmonic'], "Should not detect harmony in random pattern"
        assert harmony['strength'] < 0.3, "Should have very low strength"
        assert len(harmony['fractal_points']) < 3, "Should identify few fractal points"
        
        print(f"{GREEN}✓ No harmony detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_insufficient_data(self, mock_redis, detector):
        """Test handling of insufficient price data."""
        # Set up minimal price data
        base_time = datetime.now(timezone.utc)
        prices = [42000.0, 41000.0]  # Only two points
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert not harmony['is_harmonic'], "Should not detect harmony with insufficient data"
        assert harmony['strength'] == 0.0, "Should have zero strength"
        assert len(harmony['fractal_points']) < 3, "Should identify few fractal points"
        
        print(f"{GREEN}✓ Insufficient data handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_constant_price(self, mock_redis, detector):
        """Test handling of constant price data."""
        # Set up constant price data
        base_time = datetime.now(timezone.utc)
        prices = [42000.0] * 7  # Same price repeated
        
        # Update price data
        for i, price in enumerate(prices):
            timestamp = base_time.replace(hour=i)
            detector.update_price_data(price, timestamp)
        
        # Detect fractal harmony
        harmony = detector.detect_fractal_harmony()
        
        assert not harmony['is_harmonic'], "Should not detect harmony in constant price"
        assert harmony['strength'] == 0.0, "Should have zero strength"
        assert len(harmony['fractal_points']) == 0, "Should identify no fractal points"
        
        print(f"{GREEN}✓ Constant price handling verified!{RESET}") 