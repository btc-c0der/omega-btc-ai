
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
    detect_fibonacci_confluence
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
        """🎯 Test detection of divine swing points in price movements."""
        print(f"\n{MAGENTA}Testing D1V1N3 SW1NG P01NT detection...{RESET}")
        
        # Setup test data with golden ratio vibes
        prices = [
            42000.0,  # Base
            43618.0,  # +3.85% (Fibonacci-like move)
            41987.0,  # Retracement
            44144.0,  # New high
            42618.0,  # Golden ratio retracement
        ]
        
        # Feed prices with timestamps
        base_time = datetime.datetime.now(datetime.UTC)
        for i, price in enumerate(prices):
            timestamp = base_time + datetime.timedelta(minutes=i*5)
            fib_detector.update_price_data(price, timestamp)
        
        # Verify swing points were detected
        assert fib_detector.recent_swing_high == 44144.0, "Failed to detect highest swing"
        assert fib_detector.recent_swing_low == 41987.0, "Failed to detect lowest swing"
        
        # Verify Redis storage of swing points
        mock_redis.set.assert_any_call("fibonacci:swing_high", 44144.0)
        mock_redis.set.assert_any_call("fibonacci:swing_low", 41987.0)
        
        print(f"{GREEN}✓ SW1NG P01NTS detected successfully!{RESET}")
    
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
        base_time = datetime.datetime.now(datetime.UTC)
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

if __name__ == "__main__":
    print("🚀 Running Fibonacci Detector Test Suite...")
    pytest.main([__file__, "-v"]) 