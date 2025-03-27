"""
🌌 OMEGA RASTA ERROR HANDLING TESTS 🌌
=====================================

Tests for the divine error handling functionality.
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

class TestErrorHandling:
    """Test suite for error handling."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_invalid_price_data(self, mock_redis, detector):
        """Test handling of invalid price data."""
        # Test None price
        with pytest.raises(ValueError, match="Price cannot be None"):
            detector.update_price_data(None, datetime.now(timezone.utc))
        
        # Test invalid price type
        with pytest.raises(ValueError, match="Price must be a number"):
            detector.update_price_data("invalid", datetime.now(timezone.utc))
        
        # Test NaN price
        with pytest.raises(ValueError, match="Price cannot be NaN"):
            detector.update_price_data(float('nan'), datetime.now(timezone.utc))
        
        # Test infinite price
        with pytest.raises(ValueError, match="Price cannot be infinite"):
            detector.update_price_data(float('inf'), datetime.now(timezone.utc))
        
        print(f"{GREEN}✓ Invalid price data handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_invalid_timestamp_data(self, mock_redis, detector):
        """Test handling of invalid timestamp data."""
        # Test None timestamp
        with pytest.raises(ValueError, match="Timestamp cannot be None"):
            detector.update_price_data(42000.0, None)
        
        # Test invalid timestamp type
        with pytest.raises(ValueError, match="Invalid timestamp type"):
            detector.update_price_data(42000.0, "invalid")
        
        # Test future timestamp
        future_time = datetime.now(timezone.utc).replace(year=2025)
        with pytest.raises(ValueError, match="Invalid timestamp: cannot be in the future"):
            detector.update_price_data(42000.0, future_time)
        
        # Test past timestamp before Unix epoch
        past_time = datetime(1969, 12, 31, tzinfo=timezone.utc)
        with pytest.raises(ValueError, match="Invalid timestamp: cannot be before Unix epoch"):
            detector.update_price_data(42000.0, past_time)
        
        print(f"{GREEN}✓ Invalid timestamp data handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_connection_error(self, mock_redis, detector):
        """Test handling of Redis connection errors."""
        # Simulate Redis connection error
        mock_redis.get.side_effect = Exception("Redis connection failed")
        
        # Test graceful handling of Redis error
        result = detector.get_fibonacci_data()
        assert result is None, "Should handle Redis error gracefully"
        
        print(f"{GREEN}✓ Redis connection error handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_invalid_swing_points(self, mock_redis, detector):
        """Test handling of invalid swing points."""
        # Test with None swing points
        detector.recent_swing_high = None
        detector.recent_swing_low = None
        
        with pytest.raises(ValueError, match="Swing points not initialized"):
            detector.calculate_fibonacci_levels()
        
        # Test with invalid swing point values
        detector.recent_swing_high = float('nan')
        detector.recent_swing_low = 40000.0
        
        with pytest.raises(ValueError, match="Invalid swing high"):
            detector.calculate_fibonacci_levels()
        
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = float('inf')
        
        with pytest.raises(ValueError, match="Invalid swing low"):
            detector.calculate_fibonacci_levels()
        
        print(f"{GREEN}✓ Invalid swing points handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_invalid_fibonacci_levels(self, mock_redis, detector):
        """Test handling of invalid Fibonacci levels."""
        # Set up valid swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        
        # Test with invalid level
        with pytest.raises(ValueError, match="Invalid Fibonacci level"):
            detector.detect_fibonacci_confluence(41000.0, invalid_level=2.5)
        
        # Test with invalid tolerance
        with pytest.raises(ValueError, match="Invalid tolerance value"):
            detector.detect_fibonacci_confluence(41000.0, tolerance=-0.1)
        
        print(f"{GREEN}✓ Invalid Fibonacci levels handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_empty_data(self, mock_redis, detector):
        """Test handling of empty data."""
        # Test with empty price history
        detector.price_history = []
        
        with pytest.raises(ValueError, match="Insufficient price data"):
            detector.update_price_data(42000.0, datetime.now(timezone.utc))
        
        # Test with empty Fibonacci data
        mock_redis.get.return_value = None
        
        result = detector.get_fibonacci_data()
        assert result is None, "Should handle empty Fibonacci data"
        
        print(f"{GREEN}✓ Empty data handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_corrupted_data(self, mock_redis, detector):
        """Test handling of corrupted data."""
        # Test with corrupted JSON data
        mock_redis.get.return_value = "invalid json"
        
        result = detector.get_fibonacci_data()
        assert result is None, "Should handle corrupted JSON data"
        
        # Test with corrupted price data
        detector.price_history = [float('nan')]
        
        with pytest.raises(ValueError, match="Invalid price data"):
            detector.update_price_data(42000.0, datetime.now(timezone.utc))
        
        print(f"{GREEN}✓ Corrupted data handling verified!{RESET}") 