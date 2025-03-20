"""
🌌 OMEGA RASTA FIBONACCI DETECTOR TEST SUITE 🌌
==============================================

Divine market analysis through Fibonacci sequence harmony testing.
May the golden ratio be with you! 🚀
"""

import pytest
import redis
import datetime
import json
import math
from unittest.mock import patch, MagicMock, ANY
from typing import Any, Optional, Dict
from omega_ai.mm_trap_detector.fibonacci_detector import (
    FibonacciDetector, 
    fibonacci_detector,
    check_fibonacci_level,
    update_fibonacci_data,
    detect_fibonacci_confluence,
    check_fibonacci_alignment
)

# ANSI color codes for h4x0r style output
GREEN = "\033[32m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

class TestFibonacciDetector:
    """🌿 Divine tests for Fibonacci market harmonics."""
    
    @pytest.fixture
    def fib_detector(self):
        """Create a fresh detector instance for each test."""
        return FibonacciDetector()
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_divine_swing_point_detection(self, mock_redis, fib_detector):
        """🎯 Test detection of divine swing points in price movements with enhanced rolling window."""
        print(f"\n{MAGENTA}Testing D1V1N3 SW1NG P01NT detection with enhanced rolling window...{RESET}")
        
        # Setup test data with golden ratio vibes and more price points for rolling window
        prices = [
            42000.0,  # Base
            42618.0,  # +1.47%
            43000.0,  # +0.9%
            43618.0,  # +1.44% (Fibonacci-like move)
            43500.0,  # -0.27%
            42500.0,  # -2.3% (Retracement)
            41987.0,  # -1.2% (Continued retracement)
            42100.0,  # +0.27%
            42600.0,  # +1.19%
            43200.0,  # +1.41%
            44144.0,  # +2.19% (New high)
            43900.0,  # -0.55%
            43200.0,  # -1.6%
            42618.0,  # -1.35% (Golden ratio retracement)
        ]
        
        # Feed prices with timestamps
        base_time = datetime.datetime.now(datetime.timezone.utc)
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
        
        # Verify swing points were detected
        assert fib_detector.recent_swing_high == 44144.0, "Failed to detect highest swing"
        assert fib_detector.recent_swing_low == 41987.0, "Failed to detect lowest swing"
        
        # Verify swing points have significant difference (>0.5%)
        swing_diff_pct = (fib_detector.recent_swing_high - fib_detector.recent_swing_low) / fib_detector.recent_swing_low
        assert swing_diff_pct >= 0.005, "Swing points should have significant difference"
        
        # Verify Redis storage of swing points
        mock_redis.set.assert_any_call("fibonacci:swing_high", 44144.0)
        mock_redis.set.assert_any_call("fibonacci:swing_low", 41987.0)
        
        print(f"{GREEN}✓ Enhanced SW1NG P01NTS detected successfully with {len(prices)} price points!{RESET}")
        print(f"{GREEN}✓ Swing differential: {swing_diff_pct:.2%}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_golden_ratio_confluence(self, mock_redis, fib_detector):
        """🎯 Test golden ratio confluence detection."""
        print(f"\n{MAGENTA}Testing G0LD3N R4T10 confluence...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        current_price = 43090.0  # 61.8% retracement
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 42500.0,
            "61.8%": 43090.0,  # Golden ratio level
            "78.6%": 43930.0,
            "100%": 45000.0,
            "127.2%": 46360.0,
            "161.8%": 48090.0
        }
        mock_redis.get.return_value = test_levels
        
        # Test golden ratio hit
        hit = fib_detector.check_fibonacci_level(current_price)
        assert hit is not None, "Should detect Fibonacci hit"
        assert hit["level"] == 0.618, "Should detect golden ratio level"
        assert hit["price"] == 43090.0, "Should match golden ratio price"
        assert hit["label"] == "61.8%", "Should have correct label"
        assert hit["proximity"] <= 0.005, "Should be within 0.5% tolerance"
        
        print(f"{GREEN}✓ Golden ratio confluence verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fractal_harmony_detection(self, mock_redis, fib_detector):
        """🎨 Test fractal harmony detection."""
        print(f"\n{MAGENTA}Testing FR4CT4L H4RM0NY detection...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 51000.0
        fib_detector.recent_swing_low = 49618.0  # 61.8% retracement
        price = 50000.0  # 50% retracement
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 49618.0,
            "23.6%": 49944.0,
            "38.2%": 50144.0,
            "50%": 50000.0,  # Target level
            "61.8%": 50856.0,
            "78.6%": 50712.0,
            "100%": 51000.0,
            "127.2%": 51288.0,
            "161.8%": 51618.0
        }
        mock_redis.get.return_value = test_levels
        
        # Test fractal hit
        hit = fib_detector.check_fibonacci_level(price)
        assert hit is not None, "Should detect Fibonacci hit"
        assert hit["level"] == 0.5, "Should detect 50% level"
        assert hit["price"] == 50000.0, "Should match 50% price"
        assert hit["label"] == "50%", "Should have correct label"
        assert hit["proximity"] <= 0.005, "Should be within 0.5% tolerance"
        
        print(f"{GREEN}🎯 Detected fractal at {hit['label']}{RESET}")
        print(f"{GREEN}✓ Fractal harmony detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_trap_confluence_boost(self, mock_redis, fib_detector):
        """⚡ Test trap confluence boost calculation."""
        print(f"\n{MAGENTA}Testing TR4P C0NFLU3NC3 boost calculation...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        current_price = 43090.0  # 61.8% retracement
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 42500.0,
            "61.8%": 43090.0,  # Golden ratio level
            "78.6%": 43930.0,
            "100%": 45000.0,
            "127.2%": 46360.0,
            "161.8%": 48090.0
        }
        mock_redis.get.return_value = test_levels
        
        # Test trap confluence boost
        enhanced_confidence, fib_hit = fib_detector.detect_fibonacci_confluence(
            trap_type="BULL_TRAP",
            confidence=0.8,
            volume=1000.0,
            price=43090.0
        )
        
        assert enhanced_confidence > 0.8, "Should boost confidence"
        assert fib_hit is not None, "Should detect Fibonacci hit"
        assert fib_hit["level"] == 0.618, "Should detect golden ratio level"
        
        print(f"{GREEN}✓ Trap confluence boost verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_divine_level_generation(self, mock_redis, fib_detector):
        """🎨 Test generation of all divine Fibonacci levels."""
        print(f"\n{MAGENTA}Testing D1V1N3 L3V3L generation...{RESET}")
        
        # Setup swing points
        fib_detector.recent_swing_high = 50000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Generate levels
        levels = fib_detector.generate_fibonacci_levels()
        
        # Verify all key levels are present
        assert "0% (Base)" in levels
        assert "23.6%" in levels
        assert "38.2%" in levels
        assert "50%" in levels
        assert "61.8%" in levels
        assert "78.6%" in levels
        assert "100%" in levels
        assert "127.2%" in levels
        assert "161.8%" in levels
        
        # Verify specific level calculations
        range_size = 10000.0  # 50000 - 40000
        assert levels["61.8%"] == pytest.approx(46180.0)  # 40000 + (10000 * 0.618)
        assert levels["50%"] == pytest.approx(45000.0)    # 40000 + (10000 * 0.5)
        
        # Verify Redis storage
        mock_redis.set.assert_called_with(
            "fibonacci:current_levels",
            json.dumps(levels)
        )
        
        print(f"{GREEN}✓ D1V1N3 L3V3LS generated successfully!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels')
    def test_fibonacci_alignment_check(self, mock_get_fib_levels, mock_redis):
        """🎯 Test the Fibonacci alignment check functionality."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 4L1GNM3NT check...{RESET}")
        
        # Setup test Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 45000.0,
            "61.8%": 43090.0,  # Golden ratio level
            "78.6%": 47860.0,
            "100%": 50000.0,
            "127.2%": 52720.0,
            "161.8%": 56180.0
        }
        
        # Mock the Fibonacci levels function to return our test data
        mock_get_fib_levels.return_value = test_levels
        
        # Mock Redis to return current price
        mock_redis.get.return_value = "43090"  # Price exactly at golden ratio level
        
        # Test alignment check
        alignment = check_fibonacci_alignment()
        
        # Verify alignment detection
        assert alignment is not None, "Should detect alignment"
        assert alignment["type"] == "GOLDEN_RATIO", "Should detect golden ratio alignment"
        assert alignment["level"] == "61.8%", "Should identify correct level"
        assert alignment["distance_pct"] < 0.1, "Should be very close to the level"
        assert alignment["confidence"] > 0.9, "Should have high confidence for golden ratio"
        assert "timestamp" in alignment, "Should include timestamp"
        
        print(f"{GREEN}✓ F1B0N4CC1 4L1GNM3NT detected at {alignment['level']} level!{RESET}")
        print(f"{GREEN}✓ Alignment confidence: {alignment['confidence']:.2f}{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_invalid_price(self, mock_redis, fib_detector):
        """🚫 Test error handling for invalid price inputs."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG for invalid prices...{RESET}")
        
        # Test with None price
        with pytest.raises(ValueError):
            fib_detector.update_price_data(None, datetime.datetime.now(datetime.timezone.utc))
        
        # Test with negative price
        with pytest.raises(ValueError):
            fib_detector.update_price_data(-1000.0, datetime.datetime.now(datetime.timezone.utc))
        
        # Test with zero price
        with pytest.raises(ValueError):
            fib_detector.update_price_data(0.0, datetime.datetime.now(datetime.timezone.utc))
        
        print(f"{GREEN}✓ Invalid price handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_error_handling(self, mock_redis, fib_detector):
        """🔌 Test handling of Redis connection errors."""
        print(f"\n{MAGENTA}Testing R3D1S 3RR0R H4NDL1NG...{RESET}")
        
        # Simulate Redis connection error
        mock_redis.set.side_effect = redis.ConnectionError("Connection refused")
        
        # Should not raise exception, just log error
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        fib_detector.generate_fibonacci_levels()
        
        print(f"{GREEN}✓ Redis error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_small_price_range(self, mock_redis, fib_detector):
        """📏 Test handling of very small price ranges."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Small price range...{RESET}")
        
        # Setup very small price range
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 44990.0  # Only $10 difference
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 44990.0,
            "23.6%": 44992.36,
            "38.2%": 44993.82,
            "50%": 44995.0,
            "61.8%": 44996.18,
            "78.6%": 44997.86,
            "100%": 45000.0,
            "127.2%": 45002.72,
            "161.8%": 45006.18
        }
        mock_redis.get.return_value = test_levels
        
        # Should return None for very small ranges
        hit = fib_detector.check_fibonacci_level(44995.0)
        assert hit is None, "Should not detect Fibonacci levels for very small ranges"
        
        print(f"{GREEN}✓ Small price range handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_equal_swing_points(self, mock_redis, fib_detector):
        """⚖️ Test handling of equal swing high and low."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Equal swing points...{RESET}")
        
        # Setup equal swing points
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 45000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 45000.0,
            "23.6%": 45000.0,
            "38.2%": 45000.0,
            "50%": 45000.0,
            "61.8%": 45000.0,
            "78.6%": 45000.0,
            "100%": 45000.0,
            "127.2%": 45000.0,
            "161.8%": 45000.0
        }
        mock_redis.get.return_value = test_levels
        
        # Should return None for equal swing points
        hit = fib_detector.check_fibonacci_level(45000.0)
        assert hit is None, "Should not detect Fibonacci levels for equal swing points"
        
        print(f"{GREEN}✓ Equal swing points handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_missing_swing_points(self, mock_redis, fib_detector):
        """❌ Test handling of missing swing points."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Missing swing points...{RESET}")
        
        # Setup missing swing points
        fib_detector.recent_swing_high = None
        fib_detector.recent_swing_low = None
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 45000.0,
            "23.6%": 46180.0,
            "38.2%": 46910.0,
            "50%": 47500.0,
            "61.8%": 48090.0,
            "78.6%": 48930.0,
            "100%": 50000.0,
            "127.2%": 51360.0,
            "161.8%": 53090.0
        }
        mock_redis.get.return_value = test_levels
        
        # Should return None for missing swing points
        hit = fib_detector.check_fibonacci_level(45000.0)
        assert hit is None, "Should not detect Fibonacci levels for missing swing points"
        
        print(f"{GREEN}✓ Missing swing points handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_trap_confluence(self, mock_redis, fib_detector):
        """🚫 Test error handling in trap confluence detection."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in trap confluence...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 42500.0,
            "61.8%": 43090.0,
            "78.6%": 43930.0,
            "100%": 45000.0,
            "127.2%": 46360.0,
            "161.8%": 48090.0
        }
        mock_redis.get.return_value = json.dumps(test_levels)
        
        # Test with invalid trap type
        enhanced_confidence, fib_hit = fib_detector.detect_fibonacci_confluence(
            trap_type="INVALID_TRAP",
            confidence=0.8,
            volume=1000.0,
            price=43090.0
        )
        
        assert enhanced_confidence == 0.8, "Should not modify confidence for invalid trap type"
        assert fib_hit is None, "Should not detect Fibonacci hit for invalid trap type"
        
        print(f"{GREEN}✓ Trap confluence error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_update_fibonacci_data_edge_cases(self, mock_redis, fib_detector):
        """🚫 Test error handling in Fibonacci data updates."""
        print(f"\n{MAGENTA}Testing UPD4T3 F1B0N4CC1 D4T4 edge cases...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 42500.0,
            "61.8%": 43090.0,
            "78.6%": 43930.0,
            "100%": 45000.0,
            "127.2%": 46360.0,
            "161.8%": 48090.0
        }
        mock_redis.get.return_value = json.dumps(test_levels)
        
        # Test with invalid price values
        with pytest.raises(ValueError):
            update_fibonacci_data(-1000.0)  # Should raise ValueError for negative price
        
        with pytest.raises(ValueError):
            update_fibonacci_data(float('inf'))  # Should raise ValueError for infinite price
        
        with pytest.raises(ValueError):
            update_fibonacci_data(float('nan'))  # Should raise ValueError for NaN price
        
        with pytest.raises(ValueError):
            update_fibonacci_data("invalid")  # Should raise ValueError for non-numeric price
        
        # Test with Redis error
        mock_redis.get.side_effect = redis.RedisError("Redis error")
        with pytest.raises(ValueError):
            update_fibonacci_data(45000.0)  # Should handle Redis error gracefully
        
        print(f"{GREEN}✓ Fibonacci data update error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_fibonacci_data_edge_cases(self, mock_redis, fib_detector):
        """🚫 Test error handling in Fibonacci data operations."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 D4T4 edge cases...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "23.6%": 41180.0,
            "38.2%": 41910.0,
            "50%": 42500.0,
            "61.8%": 43090.0,
            "78.6%": 43930.0,
            "100%": 45000.0,
            "127.2%": 46360.0,
            "161.8%": 48090.0
        }
        mock_redis.get.return_value = json.dumps(test_levels)
        
        # Test with invalid price values
        with pytest.raises(ValueError):
            fib_detector.update_fibonacci_data(-1000.0)  # Should raise ValueError for negative price
        
        with pytest.raises(ValueError):
            fib_detector.update_fibonacci_data(float('inf'))  # Should raise ValueError for infinite price
        
        with pytest.raises(ValueError):
            fib_detector.update_fibonacci_data(float('nan'))  # Should raise ValueError for NaN price
        
        with pytest.raises(ValueError):
            fib_detector.update_fibonacci_data("invalid")  # Should raise ValueError for non-numeric price
        
        # Test with Redis error
        mock_redis.get.side_effect = redis.RedisError("Redis error")
        with pytest.raises(ValueError):
            fib_detector.update_fibonacci_data(45000.0)  # Should handle Redis error gracefully
        
        print(f"{GREEN}✓ Fibonacci data error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_record_fibonacci_hit_success(self, mock_redis, fib_detector):
        """Test successful recording of Fibonacci hits."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 H1T recording...{RESET}")
        
        # Setup test data
        current_price = 43090.0
        hit_data = {
            "level": 0.618,
            "label": "61.8%",
            "proximity": 0.001,
            "is_uptrend": True
        }
        
        # Test recording
        fib_detector._record_fibonacci_hit(current_price, hit_data)
        
        # Verify Redis call
        mock_redis.zadd.assert_called_once()
        args = mock_redis.zadd.call_args[0]
        assert args[0] == "fibonacci:hits"
        
        print(f"{GREEN}✓ Fibonacci hit recording verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_record_fibonacci_hit_redis_error(self, mock_redis, fib_detector):
        """Test handling of Redis errors when recording Fibonacci hits."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 H1T recording error handling...{RESET}")
        
        # Setup Redis to raise error
        mock_redis.zadd.side_effect = redis.RedisError("Test Redis error")
        
        # Setup test data
        current_price = 43090.0
        hit_data = {
            "level": 0.618,
            "label": "61.8%",
            "proximity": 0.001,
            "is_uptrend": True
        }
        
        # Test recording - should not raise error
        fib_detector._record_fibonacci_hit(current_price, hit_data)
        
        print(f"{GREEN}✓ Fibonacci hit error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_detect_fibonacci_confluence_invalid_inputs(self, mock_redis, fib_detector):
        """Test Fibonacci confluence detection with invalid inputs."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 C0NFLU3NC3 invalid inputs...{RESET}")
        
        # Setup Redis mock to return valid Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "61.8%": 43090.0
        }
        mock_redis.get.return_value = json.dumps(test_levels)
        
        # Setup swing points
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Test invalid confidence
        confidence, hit = fib_detector.detect_fibonacci_confluence("BULL_TRAP", float('nan'), 1000.0, 43090.0)
        assert confidence == 0.0, "Invalid confidence should return 0.0"
        assert hit is None, "Invalid confidence should return no hit"
        
        # Test invalid trap type
        confidence, hit = fib_detector.detect_fibonacci_confluence("INVALID_TRAP", 0.8, 1000.0, 43090.0)
        assert confidence == 0.8, "Invalid trap type should return original confidence"
        assert hit is None, "Invalid trap type should return no hit"
        
        print(f"{GREEN}✓ Invalid input handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_detect_fibonacci_confluence_high_volume(self, mock_redis, fib_detector):
        """Test Fibonacci confluence detection with high volume."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 C0NFLU3NC3 with high volume...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "61.8%": 43090.0  # Golden ratio level
        }
        mock_redis.get.return_value = test_levels
        
        # Mock Redis zadd to prevent errors
        mock_redis.zadd.return_value = True
        
        # Test with high volume
        confidence, hit = fib_detector.detect_fibonacci_confluence(
            "BULL_TRAP",
            0.8,
            10000.0,  # High volume
            43090.0
        )
        
        assert confidence > 0.8, "High volume should boost confidence"
        assert hit is not None, "Should detect Fibonacci hit"
        assert hit["level"] == 0.618, "Should detect golden ratio level"
        
        print(f"{GREEN}✓ High volume confluence boost verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_check_fibonacci_level_invalid_format(self, mock_redis, fib_detector):
        """Test handling of invalid Fibonacci levels format in Redis."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 L3V3L invalid format handling...{RESET}")
        
        # Setup Redis mock to return invalid format
        mock_redis.get.return_value = ["invalid", "format"]  # List instead of dict
        
        # Test should raise ValueError
        with pytest.raises(ValueError, match="Error checking Fibonacci level: the JSON object must be str, bytes or bytearray, not list"):
            fib_detector.check_fibonacci_level(43090.0)
        
        print(f"{GREEN}✓ Invalid format handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_check_fibonacci_level_invalid_prices(self, mock_redis, fib_detector):
        """Test handling of invalid prices in Fibonacci levels."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 L3V3L invalid price handling...{RESET}")
        
        # Setup Redis to return levels with invalid prices
        test_levels = {
            "0% (Base)": float('inf'),
            "61.8%": float('nan'),
            "100%": "invalid"
        }
        mock_redis.get.return_value = test_levels
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Test with invalid prices - should skip invalid levels and continue
        result = fib_detector.check_fibonacci_level(43090.0)
        assert result is None, "Should handle invalid prices gracefully"
        
        print(f"{GREEN}✓ Invalid price handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_record_trap_fibonacci_confluence_success(self, mock_redis, fib_detector):
        """Test successful recording of trap Fibonacci confluence."""
        print(f"\n{MAGENTA}Testing TR4P F1B0N4CC1 C0NFLU3NC3 recording...{RESET}")
        
        # Setup test data
        trap_type = "BULL_TRAP"
        confidence = 0.85
        price = 43090.0
        level = 0.618
        fib_hit = {
            "label": "61.8%",
            "price": 43090.0,
            "is_uptrend": True
        }
        
        # Mock Redis zadd
        mock_redis.zadd.return_value = True
        
        # Test recording
        fib_detector._record_trap_fibonacci_confluence(trap_type, confidence, price, level, fib_hit)
        
        # Verify Redis call
        mock_redis.zadd.assert_called_once()
        args = mock_redis.zadd.call_args[0]
        assert args[0] == "grafana:fibonacci_trap_confluences"
        
        print(f"{GREEN}✓ Trap Fibonacci confluence recording verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_record_trap_fibonacci_confluence_redis_error(self, mock_redis, fib_detector):
        """Test handling of Redis errors when recording trap Fibonacci confluence."""
        print(f"\n{MAGENTA}Testing TR4P F1B0N4CC1 C0NFLU3NC3 error handling...{RESET}")
        
        # Setup Redis to raise error
        mock_redis.zadd.side_effect = redis.RedisError("Test Redis error")
        
        # Setup test data
        trap_type = "BULL_TRAP"
        confidence = 0.85
        price = 43090.0
        level = 0.618
        fib_hit = {
            "label": "61.8%",
            "price": 43090.0,
            "is_uptrend": True
        }
        
        # Test recording - should raise error
        with pytest.raises(redis.RedisError, match="Test Redis error"):
            fib_detector._record_trap_fibonacci_confluence(trap_type, confidence, price, level, fib_hit)
        
        print(f"{GREEN}✓ Trap Fibonacci confluence error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_detect_fibonacci_confluence_with_different_trap_types(self, mock_redis, fib_detector):
        """Test Fibonacci confluence detection with different trap types."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 C0NFLU3NC3 with different trap types...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Setup Redis mock to return Fibonacci levels
        test_levels = {
            "0% (Base)": 40000.0,
            "61.8%": 43090.0  # Golden ratio level
        }
        mock_redis.get.side_effect = lambda key: json.dumps(test_levels) if key == "fibonacci_levels" else None
        mock_redis.zadd.return_value = True
        
        # Test different trap types
        trap_types = ["BULL_TRAP", "BEAR_TRAP", "LIQUIDITY_GRAB", "STOP_HUNT"]
        for trap_type in trap_types:
            confidence, hit = fib_detector.detect_fibonacci_confluence(
                trap_type,
                0.8,
                1000.0,
                43090.0
            )
            
            assert confidence > 0.8, f"{trap_type} should boost confidence"
            assert hit is not None, f"{trap_type} should detect Fibonacci hit"
            assert hit["level"] == 0.618, f"{trap_type} should detect golden ratio level"
        
        print(f"{GREEN}✓ Different trap types verified!{RESET}")

    def test_generate_fibonacci_levels_edge_cases(self, fib_detector):
        """Test edge cases in Fibonacci level generation."""
        print(f"\n{MAGENTA}Testing F1B0N4CC1 L3V3L generation edge cases...{RESET}")
        
        # Test with no swing points
        fib_detector.recent_swing_high = None
        fib_detector.recent_swing_low = None
        levels = fib_detector.generate_fibonacci_levels()
        assert levels is None, "Should return None when no swing points"
        
        # Test with equal swing points
        fib_detector.recent_swing_high = 42000.0
        fib_detector.recent_swing_low = 42000.0
        levels = fib_detector.generate_fibonacci_levels()
        assert levels is None, "Should return None when swing points are equal"
        
        # Test with valid swing points
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        levels = fib_detector.generate_fibonacci_levels()
        assert levels is not None, "Should generate levels with valid swing points"
        assert "61.8%" in levels, "Should include golden ratio level"
        assert levels["61.8%"] == pytest.approx(43090.0), "Should calculate golden ratio level correctly"
        
        print(f"{GREEN}✓ Fibonacci level generation edge cases verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_enhanced_swing_point_detection(self, mock_redis, fib_detector):
        """Test enhanced swing point detection with rolling window."""
        print(f"\n{MAGENTA}Testing 3NH4NC3D SW1NG P01NT D3T3CT10N...{RESET}")
        
        # Setup test data with manipulative wicks and genuine swings
        # Format: (timestamp, price)
        price_data = [
            (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=i*5), price)
            for i, price in enumerate([
                42000.0,  # Base price
                42100.0,  # Slight upward movement
                42050.0,  # Slight retracement
                42200.0,  # Continued upward movement
                42150.0,  # Small pullback
                42300.0,  # New high
                42750.0,  # Sharp move up
                42500.0,  # Retracement
                42200.0,  # Continued retracement
                42000.0,  # Back to base
                41800.0,  # Breaking down
                41750.0,  # New low
                41900.0,  # Slight bounce
                41870.0,  # Small retracement
                42300.0,  # Strong bounce
                42200.0,  # Small pullback
                42050.0,  # Continued pullback
                42150.0,  # Small bounce
                42500.0,  # New high
                42700.0,  # Continued uptrend
                42680.0,  # Tiny wick (manipulation attempt)
                42690.0,  # Tiny wick (manipulation attempt)
                42750.0,  # New high
                42730.0,  # Small pullback
                42500.0   # Larger pullback
            ])
        ]
        
        # Reset detector state
        fib_detector.recent_swing_high = None
        fib_detector.recent_swing_low = None
        fib_detector.potential_swing_highs = []
        fib_detector.potential_swing_lows = []
        fib_detector.price_history = []
        
        # Feed price data
        for timestamp, price in price_data:
            fib_detector.update_price_data(price, timestamp)
        
        # Verify swing points after feeding all data
        assert fib_detector.recent_swing_high == 42750.0, "Should detect correct swing high"
        assert fib_detector.recent_swing_low == 41750.0, "Should detect correct swing low"
        
        # Verify swing high was stored in Redis
        mock_redis.set.assert_any_call("fibonacci:swing_high", 42750.0)
        mock_redis.set.assert_any_call("fibonacci:swing_low", 41750.0)
        
        # Verify that false wicks were filtered out (the tiny 42680.0 and 42690.0 wicks)
        found_manipulation = False
        for high in fib_detector.potential_swing_highs:
            if high["price"] in [42680.0, 42690.0] and high["confirmation_count"] > 0:
                found_manipulation = True
        assert not found_manipulation, "Should filter out manipulative wicks"
        
        # Verify significant swing difference
        swing_diff_pct = (fib_detector.recent_swing_high - fib_detector.recent_swing_low) / fib_detector.recent_swing_low
        assert swing_diff_pct >= fib_detector.min_swing_diff, "Swing points should have significant difference"
        
        print(f"{GREEN}✓ Enhanced swing point detection verified!{RESET}")
        print(f"{GREEN}✓ Detected High: ${fib_detector.recent_swing_high} | Low: ${fib_detector.recent_swing_low}{RESET}")
        print(f"{GREEN}✓ Swing difference: {swing_diff_pct:.2%}{RESET}")

if __name__ == "__main__":
    print("🚀 Running Fibonacci Detector Test Suite...")
    pytest.main([__file__, "-v"]) 