"""
🌌 OMEGA RASTA FIBONACCI DETECTOR TESTS 🌌
========================================

Tests for the divine Fibonacci detector functionality.
May the golden ratio be with you! 🚀
"""

import pytest
import redis
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock, ANY
from omega_ai.mm_trap_detector.fibonacci_detector import (
    FibonacciDetector, 
    fibonacci_detector,
    check_fibonacci_level,
    update_fibonacci_data,
    detect_fibonacci_confluence
)

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

@pytest.fixture
def fib_detector():
    """Create a divine Fibonacci detector instance."""
    detector = FibonacciDetector()
    detector.recent_swing_high = 42000.0
    detector.recent_swing_low = 42000.0
    return detector

class TestFibonacciDetector:
    """🌿 Divine tests for Fibonacci market harmonics."""
    
    @pytest.fixture
    def fib_detector(self):
        """Create a FibonacciDetector instance for testing."""
        detector = FibonacciDetector(test_mode=True)
        # Initialize with a wider range to allow for swing detection
        detector.recent_swing_high = 44000.0
        detector.recent_swing_low = 41000.0
        detector.confirmation_threshold = 2  # Lower threshold for testing
        return detector
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_divine_swing_point_detection(self, mock_redis, fib_detector):
        """🎯 Test detection of divine swing points in price movements with enhanced rolling window."""
        print(f"\n{MAGENTA}Testing D1V1N3 SW1NG P01NT detection with enhanced rolling window...{RESET}")
        
        # Initialize with base swing points
        fib_detector.recent_swing_high = 42000.0
        fib_detector.recent_swing_low = 42000.0
        
        # Setup test data with golden ratio vibes
        prices = [
            42000.0,  # Base
            42618.0,  # +1.47%
            43000.0,  # +0.9%
            43618.0,  # +1.44% (Fibonacci-like move)
            44144.0,  # +1.2% (New high)
            43500.0,  # -1.46%
            42500.0,  # -2.3% (Retracement)
            41500.0,  # -2.35% (New low)
            42100.0,  # +1.45%
            42300.0,  # +0.48%
        ]
        
        # Feed prices with timestamps and add confirmation points
        base_time = datetime.now(timezone.utc) - timedelta(hours=2)
        for i, price in enumerate(prices):
            # Add main price point
            timestamp = base_time + timedelta(minutes=i*30)
            fib_detector.update_price_data(price, timestamp)
            
            # Add confirmation points after potential swing points
            if price == 44144.0 or price == 41500.0:
                # Add 2 confirmation points after each potential swing point
                for j in range(1, 3):
                    confirm_time = timestamp + timedelta(minutes=j*15)
                    # For high point confirmations, use lower prices
                    if price == 44144.0:
                        fib_detector.update_price_data(price - 200, confirm_time)
                    # For low point confirmations, use higher prices
                    else:
                        fib_detector.update_price_data(price + 200, confirm_time)
        
        # Verify swing points were detected
        assert fib_detector.recent_swing_high == 44144.0, "Failed to detect highest swing"
        assert fib_detector.recent_swing_low == 41500.0, "Failed to detect lowest swing"
        
        # Verify swing points have significant difference (>0.5%)
        swing_diff_pct = (fib_detector.recent_swing_high - fib_detector.recent_swing_low) / fib_detector.recent_swing_low
        assert swing_diff_pct >= 0.005, "Swing points should have significant difference"
        
        # Verify Redis storage of swing points
        mock_redis.set.assert_any_call("fibonacci:swing_high", 44144.0)
        mock_redis.set.assert_any_call("fibonacci:swing_low", 41500.0)
        
        print(f"{GREEN}✓ Enhanced SW1NG P01NTS detected successfully with {len(prices)} price points!{RESET}")
        print(f"{GREEN}✓ Swing differential: {swing_diff_pct:.2%}{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_golden_ratio_confluence(self, mock_redis, fib_detector):
        """🌟 Test the sacred 0.618 (Golden Ratio) confluence detection."""
        print(f"\n{MAGENTA}Testing G0LD3N R4T10 confluence...{RESET}")
        
        # Mock Redis response for Fibonacci levels
        mock_levels = {
            "0% (Base)": 42000.0,
            "23.6%": 42472.0,
            "38.2%": 42763.0,
            "50%": 43000.0,
            "61.8%": 43090.0,
            "78.6%": 43572.0,
            "100%": 44144.0
        }
        mock_redis.get.return_value = json.dumps(mock_levels)
        
        # Test with a price near the golden ratio level (allow for tolerance)
        test_price = 43085.0  # Slightly below the exact level
        hit = fib_detector.check_fibonacci_level(test_price, mock_levels)
        
        assert hit is not None, "Should detect golden ratio hit"
        assert hit["level"] == 0.618, "Should be golden ratio level"
        assert hit["label"] == "61.8%", "Should have correct label"
        assert abs(hit["price"] - 43090.0) < 10.0, "Should be within tolerance of level"
        assert hit["is_uptrend"] is True, "Should detect uptrend"
        assert "timestamp" in hit, "Should include timestamp"
        
        # Verify the hit was recorded in Redis
        mock_redis.zadd.assert_called_once()
        call_args = mock_redis.zadd.call_args[0]
        assert call_args[0] == "fibonacci:hits"  # Updated key name
        
        # Extract and parse the JSON from the call
        json_str = list(call_args[1].keys())[0]
        hit_data = json.loads(json_str)
        
        # Verify the hit data
        assert abs(hit_data["price"] - 43090.0) < 10.0
        assert hit_data["level"] == 0.618
        assert hit_data["label"] == "61.8%"
        assert hit_data["is_uptrend"] is True
        assert "timestamp" in hit_data
        
        print(f"{GREEN}✓ G0LD3N R4T10 confluence detected!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fractal_harmony_detection(self, mock_redis, fib_detector):
        """🔄 Test detection of fractal harmonics across timeframes."""
        print(f"\n{MAGENTA}Testing FR4CT4L H4RM0NY detection...{RESET}")
        
        # Mock Redis response for Fibonacci levels
        mock_levels = {
            "0% (Base)": 42000.0,
            "23.6%": 42472.0,
            "38.2%": 42763.0,
            "50%": 43000.0,
            "61.8%": 43090.0,
            "78.6%": 43572.0,
            "100%": 44144.0
        }
        mock_redis.get.return_value = json.dumps(mock_levels)
        
        # Feed prices near (but not exactly at) Fibonacci levels
        base_time = datetime.now(timezone.utc) - timedelta(hours=2)
        test_prices = [
            (price, base_time + timedelta(minutes=i*60))  # 60-minute intervals
            for i, price in enumerate([
                42000.0,  # Base
                42470.0,  # Near 23.6%
                42760.0,  # Near 38.2%
                43005.0,  # Near 50%
                43085.0,  # Near 61.8%
                43570.0,  # Near 78.6%
                44140.0   # Near 100%
            ])
        ]
        
        hits = []
        for price, timestamp in test_prices:
            fib_detector.update_price_data(price, timestamp)
            # Add confirmation points
            for i in range(2):
                confirm_time = timestamp + timedelta(minutes=15 * (i+1))
                fib_detector.update_price_data(price, confirm_time)
            
            # Check for hit with some tolerance
            hit = fib_detector.check_fibonacci_level(price, mock_levels)
            if hit:
                hits.append(hit)
        
        assert len(hits) >= 3, "Should detect multiple fractal harmonics"
        assert any(hit["level"] == 0.618 for hit in hits), "Should detect golden ratio"
        assert any(hit["level"] == 0.5 for hit in hits), "Should detect 50% level"
        assert any(hit["level"] == 0.382 for hit in hits), "Should detect 38.2% level"
        
        print(f"{GREEN}✓ FR4CT4L H4RM0NY confirmed across timeframes!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_trap_confluence_boost(self, mock_redis, fib_detector):
        """⚡ Test confidence boosting when traps align with Fibonacci levels."""
        print(f"\n{MAGENTA}Testing TR4P C0NFLU3NC3 boost calculation...{RESET}")
        
        # Setup a trap at golden ratio level
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        trap_price = 43090.0  # Exactly at 0.618 retracement
        
        # Mock Redis to return proper JSON string for levels
        mock_levels = {
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
        mock_redis.get.return_value = json.dumps(mock_levels)
        
        # Test confluence detection with a trap
        enhanced_confidence, fib_hit = fib_detector.detect_fibonacci_confluence(
            trap_type="LIQUIDITY_GRAB",  # Updated to match valid trap types
            confidence=0.8,
            volume=1000.0,
            price=trap_price
        )
        
        # Verify confidence boost
        assert enhanced_confidence > 0.8, "Should boost confidence"
        assert fib_hit is not None, "Should detect Fibonacci hit"
        assert fib_hit["level"] == 0.618, "Should be at golden ratio"
        assert fib_hit["label"] == "61.8%", "Should have correct label"
        
        # Verify confluence was recorded
        mock_redis.zadd.assert_any_call("grafana:fibonacci_trap_confluences", ANY)
        
        # Extract and parse the JSON from the call
        call_args = mock_redis.zadd.call_args_list[-1][0]
        json_str = list(call_args[1].keys())[0]
        confluence_data = json.loads(json_str)
        
        # Verify the confluence data
        assert confluence_data["trap_type"] == "LIQUIDITY_GRAB"
        assert abs(confluence_data["confidence"] - enhanced_confidence) < 0.001
        assert abs(confluence_data["price"] - trap_price) < 0.001
        assert "price_change" in confluence_data
        assert confluence_data["fibonacci_level"] == "61.8%"
        assert abs(confluence_data["fib_price"] - 43090.0) < 0.001
        assert confluence_data["is_uptrend"] is True
        assert confluence_data["confluence_type"] == "GOLDEN RATIO"
        
        print(f"{GREEN}✓ TR4P C0NFLU3NC3 boost verified!{RESET}")
    
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
            "fibonacci:current_levels",  # Updated key name
            json.dumps(levels)
        )
        
        print(f"{GREEN}✓ D1V1N3 L3V3LS generated successfully!{RESET}")

if __name__ == "__main__":
    print("🚀 Running Fibonacci Detector Test Suite...")
    pytest.main([__file__, "-v"]) 