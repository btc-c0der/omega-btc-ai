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
from unittest.mock import patch, MagicMock, ANY
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
        """🌟 Test the sacred 0.618 (Golden Ratio) confluence detection."""
        print(f"\n{MAGENTA}Testing G0LD3N R4T10 confluence...{RESET}")
        
        # Setup price range with golden ratio retracement
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        current_price = 43090.0  # Exactly at 0.618 retracement (40000 + 5000 * 0.618)
        
        # Test confluence detection
        hit = fib_detector.check_fibonacci_level(current_price)
        
        assert hit is not None, "Should detect Fibonacci level hit"
        assert hit["level"] == 0.618, "Should detect golden ratio level"
        assert abs(hit["proximity"]) < 0.1, "Should be very close to the level"
        
        # Verify the hit was recorded in Redis
        mock_redis.zadd.assert_called_once()
        call_args = mock_redis.zadd.call_args[0]
        assert call_args[0] == "fibonacci:hits"
        
        # Extract and parse the JSON from the call
        json_str = list(call_args[1].keys())[0]
        hit_data = json.loads(json_str)
        
        # Verify the hit data
        assert hit_data["price"] == current_price
        assert hit_data["level"] == 0.618
        assert hit_data["label"] == "Golden Ratio"
        assert hit_data["is_uptrend"] is True
        assert "timestamp" in hit_data
        
        print(f"{GREEN}✓ G0LD3N R4T10 confluence detected!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_fractal_harmony_detection(self, mock_redis, fib_detector):
        """🔄 Test detection of fractal harmonics across timeframes."""
        print(f"\n{MAGENTA}Testing FR4CT4L H4RM0NY detection...{RESET}")
        
        # Setup multiple timeframe price movements
        prices = []
        base = 50000.0
        
        # Generate fractal pattern (self-similar at different scales)
        for scale in [1.0, 0.618, 0.382, 0.236]:
            move = 1000.0 * scale
            prices.extend([
                base + move,
                base - move * 0.382,
                base + move * 0.618
            ])
            base = prices[-1]
        
        # Feed prices into detector
        base_time = datetime.datetime.now(datetime.timezone.utc)
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
            
            # Check for Fibonacci hits at each level
            hit = fib_detector.check_fibonacci_level(price)
            if hit:
                print(f"{GREEN}🎯 Detected fractal at {hit['label']}{RESET}")
        
        # Verify we found multiple Fibonacci levels
        hits = []
        for call in mock_redis.zadd.call_args_list:
            args = call[0]  # Get positional arguments
            if len(args) >= 2:  # Should have key and mapping
                key = args[0]
                if "fibonacci:hits" in key:
                    # Get the first (and only) key from the mapping
                    hit_json = next(iter(args[1].keys()))
                    hits.append(json.loads(hit_json))
        
        assert len(hits) >= 3, "Should detect multiple fractal harmonics"
        
        print(f"{GREEN}✓ FR4CT4L H4RM0NY confirmed across timeframes!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_trap_confluence_boost(self, mock_redis, fib_detector):
        """⚡ Test confidence boosting when traps align with Fibonacci levels."""
        print(f"\n{MAGENTA}Testing TR4P C0NFLU3NC3 boost calculation...{RESET}")
        
        # Setup a trap at golden ratio level
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        trap_price = 43090.0  # Exactly at 0.618 retracement
        
        # Test confluence detection with a trap
        enhanced_confidence, fib_hit = fib_detector.detect_fibonacci_confluence(
            trap_type="Liquidity Grab",
            confidence=0.8,
            price_change=-2.5,
            current_price=trap_price
        )
        
        # Verify confidence boost
        assert enhanced_confidence > 0.8, "Should boost confidence"
        assert fib_hit is not None, "Should detect Fibonacci hit"
        assert fib_hit["level"] == 0.618, "Should be at golden ratio"
        assert fib_hit["label"] == "Golden Ratio", "Should have correct label"
        
        # Verify confluence was recorded
        mock_redis.zadd.assert_any_call("grafana:fibonacci_trap_confluences", ANY)
        
        # Extract and parse the JSON from the call
        call_args = mock_redis.zadd.call_args_list[-1][0]
        json_str = list(call_args[1].keys())[0]
        confluence_data = json.loads(json_str)
        
        # Verify the confluence data
        assert confluence_data["trap_type"] == "Liquidity Grab"
        assert abs(confluence_data["confidence"] - enhanced_confidence) < 0.001
        assert abs(confluence_data["price"] - trap_price) < 0.001
        assert confluence_data["price_change"] == -2.5
        assert confluence_data["fibonacci_level"] == "Golden Ratio"
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
        
        # Should return None for equal swing points
        hit = fib_detector.check_fibonacci_level(45000.0)
        assert hit is None, "Should not detect Fibonacci levels for equal swing points"
        
        print(f"{GREEN}✓ Equal swing points handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_extreme_price_movements(self, mock_redis, fib_detector):
        """🚀 Test handling of extreme price movements."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Extreme price movements...{RESET}")
        
        # Setup extreme price movements
        prices = [
            45000.0,  # Base
            90000.0,  # +100%
            45000.0,  # -50%
            90000.0,  # +100%
            45000.0,  # -50%
        ]
        
        # Feed prices with timestamps
        base_time = datetime.datetime.now(datetime.timezone.utc)
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
        
        # Verify swing points were detected correctly despite extreme movements
        assert fib_detector.recent_swing_high == 90000.0, "Failed to detect highest swing"
        assert fib_detector.recent_swing_low == 45000.0, "Failed to detect lowest swing"
        
        print(f"{GREEN}✓ Extreme price movement handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_missing_swing_points(self, mock_redis, fib_detector):
        """❓ Test handling of missing swing points."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Missing swing points...{RESET}")
        
        # Set swing points to None
        fib_detector.recent_swing_high = None
        fib_detector.recent_swing_low = None
        
        # Should return None when swing points are missing
        hit = fib_detector.check_fibonacci_level(45000.0)
        assert hit is None, "Should not detect Fibonacci levels without swing points"
        
        # Should return None when generating levels
        levels = fib_detector.generate_fibonacci_levels()
        assert levels is None, "Should not generate levels without swing points"
        
        print(f"{GREEN}✓ Missing swing points handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_edge_case_rapid_price_changes(self, mock_redis, fib_detector):
        """⚡ Test handling of rapid price changes."""
        print(f"\n{MAGENTA}Testing 3DG3 C4S3: Rapid price changes...{RESET}")
        
        # Setup rapid price changes
        prices = []
        base = 45000.0
        for i in range(100):  # 100 rapid changes
            # Alternate between small up and down movements
            change = 10.0 if i % 2 == 0 else -10.0
            prices.append(base + change)
            base = prices[-1]
        
        # Feed prices with very short time intervals
        base_time = datetime.datetime.now(datetime.timezone.utc)
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(seconds=i*2)  # 2-second intervals
            fib_detector.update_price_data(price, timestamp)
        
        # Verify detector handles rapid changes without errors
        assert fib_detector.recent_swing_high is not None, "Should detect swing high"
        assert fib_detector.recent_swing_low is not None, "Should detect swing low"
        
        print(f"{GREEN}✓ Rapid price change handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_swing_points(self, mock_redis, fib_detector):
        """🔧 Test error handling in swing point detection."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in swing points...{RESET}")
        
        # Simulate Redis errors
        mock_redis.set.side_effect = redis.RedisError("Redis error")
        
        # Test with valid price data
        prices = [45000.0, 46000.0, 45500.0]
        base_time = datetime.datetime.now(datetime.timezone.utc)
        
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
        
        # Verify detector continues despite Redis errors
        assert fib_detector.recent_swing_high is not None
        assert fib_detector.recent_swing_low is not None
        
        print(f"{GREEN}✓ Swing point error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_fibonacci_hits(self, mock_redis, fib_detector):
        """🎯 Test error handling in Fibonacci hit recording."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in Fibonacci hits...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Simulate Redis error
        mock_redis.zadd.side_effect = redis.RedisError("Redis error")
        
        # Test hit recording
        hit_data = {
            "level": 0.618,
            "price": 43090.0,
            "label": "Golden Ratio",
            "proximity": 0.001,
            "is_uptrend": True
        }
        
        # Should not raise exception
        fib_detector._record_fibonacci_hit(43090.0, hit_data)
        
        print(f"{GREEN}✓ Fibonacci hit error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_trap_confluence(self, mock_redis, fib_detector):
        """⚡ Test error handling in trap confluence detection."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in trap confluence...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Simulate Redis error
        mock_redis.zadd.side_effect = redis.RedisError("Redis error")
        
        # Test confluence detection
        confidence, fib_hit = fib_detector.detect_fibonacci_confluence(
            "Liquidity Grab",
            0.8,
            -2.5,
            43090.0
        )
        
        assert confidence is not None
        assert fib_hit is not None
        
        print(f"{GREEN}✓ Trap confluence error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_fibonacci_levels(self, mock_redis, fib_detector):
        """📊 Test error handling in Fibonacci level generation."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in Fibonacci levels...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Simulate Redis error
        mock_redis.set.side_effect = redis.RedisError("Redis error")
        
        # Test level generation
        levels = fib_detector.generate_fibonacci_levels()
        
        assert levels is not None
        assert "61.8%" in levels
        assert "50%" in levels
        
        print(f"{GREEN}✓ Fibonacci level error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_fractal_harmony(self, mock_redis, fib_detector):
        """🎨 Test error handling in fractal harmony detection."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in fractal harmony...{RESET}")
        
        # Setup test data
        fib_detector.recent_swing_high = 45000.0
        fib_detector.recent_swing_low = 40000.0
        
        # Add price history
        base_time = datetime.datetime.now(datetime.timezone.utc)
        for i in range(10):
            price = 42500.0 + (i * 100)
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
        
        # Test fractal detection
        harmonics = fib_detector.detect_fractal_harmony()
        
        assert isinstance(harmonics, list)
        
        print(f"{GREEN}✓ Fractal harmony error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_alignment_check(self, mock_redis, fib_detector):
        """🎯 Test error handling in alignment check."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in alignment check...{RESET}")
        
        # Test with missing price data
        mock_redis.get.return_value = None
        alignment = check_fibonacci_alignment()
        assert alignment is None
        
        # Test with invalid price data
        mock_redis.get.return_value = "invalid"
        alignment = check_fibonacci_alignment()
        assert alignment is None
        
        # Test with valid data but missing levels
        mock_redis.get.return_value = "43090"
        with patch('omega_ai.mm_trap_detector.fibonacci_detector.get_current_fibonacci_levels') as mock_get_levels:
            mock_get_levels.return_value = None
            alignment = check_fibonacci_alignment()
            assert alignment is None
        
        print(f"{GREEN}✓ Alignment check error handling verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_error_handling_update_fibonacci_data(self, mock_redis, fib_detector):
        """🔄 Test error handling in Fibonacci data update."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG in Fibonacci data update...{RESET}")
        
        # Test with invalid price
        with pytest.raises(ValueError):
            update_fibonacci_data(-1000.0)
        
        # Test with Redis error
        mock_redis.zadd.side_effect = redis.RedisError("Redis error")
        update_fibonacci_data(43090.0)  # Should not raise exception
        
        print(f"{GREEN}✓ Fibonacci data update error handling verified!{RESET}")

if __name__ == "__main__":
    print("🚀 Running Fibonacci Detector Test Suite...")
    pytest.main([__file__, "-v"]) 