
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
🌌 OMEGA RASTA FIBONACCI TEST SUITE 🌌
====================================

Test suite for the Golden Ratio detector.
May the golden ratio be with you! 🚀
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from omega_ai.mm_trap_detector.golden_ratio_detector import GoldenRatioDetector, GoldenRatioConfluence
import redis

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

@pytest.fixture
def detector():
    """Create a test instance of the Golden Ratio detector."""
    with patch('redis.Redis') as mock_redis:
        mock_redis.return_value = MagicMock()
        return GoldenRatioDetector(symbol="BTCUSDT", test_mode=True)

class TestGoldenRatio:
    """Test suite for Golden Ratio detector."""
    
    @pytest.fixture
    def detector(self):
        """Create a detector instance for testing."""
        detector = GoldenRatioDetector(symbol="BTCUSDT", test_mode=True)
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        return detector
    
    def test_liquidity_grab_detection(self, detector):
        """Test detection of liquidity grabs."""
        # Set up test data
        base_time = datetime.now(timezone.utc)
        price = 41236.0  # Near 0.618 level
        
        # Mock order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(41200.0, 2.0), (41100.0, 3.0)],
                'asks': [(41300.0, 2.0), (41400.0, 3.0)],
                'volume': 1000.0
            }
            
            # Detect liquidity grab
            liquidity_grab = detector.detect_liquidity_grab(price, base_time)
            
            assert liquidity_grab is not None, "Should detect liquidity grab"
            assert liquidity_grab.price == price, "Should record correct price"
            assert liquidity_grab.timestamp == base_time, "Should record timestamp"
            assert liquidity_grab.volume == 1000.0, "Should record volume"
            assert liquidity_grab.confidence > 0.5, "Should have reasonable confidence"
    
    def test_golden_ratio_confluence(self, detector):
        """Test detection of Golden Ratio confluence."""
        # Set up price data near 0.618 level
        base_time = datetime.now(timezone.utc)
        price = 41236.0  # Near 0.618 level
        
        # Mock order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(41200.0, 2.0), (41100.0, 3.0)],
                'asks': [(41300.0, 2.0), (41400.0, 3.0)],
                'volume': 1000.0
            }
            
            # Detect confluence
            confluence = detector.detect_golden_ratio_confluence(price, base_time)
            
            assert confluence is not None, "Should detect confluence"
            assert abs(confluence.fibonacci_level - 41236.0) < 0.01, "Should identify correct price level"
            assert confluence.confidence > 0.5, "Should have high confidence"
            assert confluence.is_confirmed, "Should be confirmed"
    
    def test_confidence_calculation(self, detector):
        """Test confidence calculation for confluence detection."""
        # Set up test cases
        test_cases = [
            (41236.0, 41236.0, 1000.0, 0.5),  # Perfect case
            (41250.0, 41236.0, 800.0, 0.3),   # Good case
            (41300.0, 41236.0, 500.0, 0.1),   # Moderate case
            (41400.0, 41236.0, 200.0, 0.0)    # Poor case
        ]
        
        prev_confidence = float('inf')
        for price, level, depth, imbalance in test_cases:
            # Mock order book state
            with patch.object(detector, 'get_order_book_state') as mock_order_book:
                mock_order_book.return_value = {
                    'bids': [(price - 100, depth/2), (price - 200, depth/2)],
                    'asks': [(price + 100, depth/2), (price + 200, depth/2)],
                    'volume': depth * 2
                }
                
                # Calculate confidence
                confidence = detector.calculate_liquidity_grab_confidence(
                    price=price,
                    fibonacci_level=level,
                    order_book_depth=depth,
                    order_book_imbalance=imbalance
                )
                
                # Verify confidence decreases with worse conditions
                if price == 41236.0:
                    assert confidence > 0.8, "Perfect case should have high confidence"
                else:
                    assert confidence < prev_confidence, "Confidence should decrease with worse conditions"
                prev_confidence = confidence
    
    def test_historical_boost(self, detector):
        """Test historical pattern boost calculation."""
        # Add some historical confluence data
        base_time = datetime.now(timezone.utc)
        price_level = 41236.0  # 0.618 level
        
        # Add successful confluences
        for i in range(5):
            confluence = detector.detect_golden_ratio_confluence(
                price_level,
                base_time.replace(hour=i)
            )
            if confluence:
                confluence.is_confirmed = True
                detector.confluence_history.append(confluence)
        
        # Add some failed confluences
        for i in range(5, 10):
            confluence = detector.detect_golden_ratio_confluence(
                price_level,
                base_time.replace(hour=i)
            )
            if confluence:
                confluence.is_confirmed = False
                detector.confluence_history.append(confluence)
        
        # Calculate historical boost
        boost = detector.calculate_historical_boost(price_level)
        
        assert boost > 0.0, "Should have positive historical boost"
        assert boost <= 0.5, "Boost should not exceed 50%"
    
    def test_order_book_analysis(self, detector):
        """Test order book analysis."""
        # Mock order book state
        order_book = {
            'bids': [(41200.0, 2.0), (41100.0, 3.0)],
            'asks': [(41300.0, 2.0), (41400.0, 3.0)],
            'volume': 1000.0
        }
        
        # Test depth calculation
        depth = detector.calculate_order_book_depth(order_book)
        assert depth == 10.0, "Should calculate correct depth (sum of all volumes)"
        
        # Test imbalance calculation
        imbalance = detector.calculate_order_book_imbalance(order_book)
        assert abs(imbalance) <= 1.0, "Imbalance should be normalized"
    
    def test_edge_case_no_liquidity(self, detector):
        """Test handling of no liquidity in order book."""
        # Mock empty order book
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [],
                'asks': [],
                'volume': 0.0
            }
            
            # Try to detect liquidity grab
            liquidity_grab = detector.detect_liquidity_grab(
                41236.0,
                datetime.now(timezone.utc)
            )
            
            assert liquidity_grab is None, "Should not detect liquidity grab with no liquidity"
    
    def test_edge_case_far_from_levels(self, detector):
        """Test handling of prices far from Fibonacci levels."""
        # Set up price data far from any level
        base_time = datetime.now(timezone.utc)
        price = 45000.0  # Far from any level
        
        # Mock order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(44900.0, 2.0), (44800.0, 3.0)],
                'asks': [(45100.0, 2.0), (45200.0, 3.0)],
                'volume': 1000.0
            }
            
            # Try to detect confluence
            confluence = detector.detect_golden_ratio_confluence(price, base_time)
            
            assert confluence is None, "Should not detect confluence far from levels"
            
            print(f"{GREEN}✓ Far from levels handling verified!{RESET}")

    def test_error_handling_liquidity_grab(self, detector):
        """Test error handling in liquidity grab detection."""
        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle None order book state"
            
            # Test with empty order book
            mock_order_book.return_value = {'bids': [], 'asks': [], 'volume': 0}
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle empty order book"
            
            # Test with invalid price
            mock_order_book.return_value = {
                'bids': [(41200.0, 2.0), (41100.0, 3.0)],
                'asks': [(41300.0, 2.0), (41400.0, 3.0)],
                'volume': 1000.0
            }
            result = detector.detect_liquidity_grab(float('inf'), datetime.now(timezone.utc))
            assert result is None, "Should handle invalid price"

    def test_edge_cases_golden_ratio(self, detector):
        """Test edge cases in golden ratio detection."""
        # Test with no swing points
        detector.recent_swing_high = None
        detector.recent_swing_low = None
        assert not detector.is_golden_ratio(41236.0), "Should handle missing swing points"
        
        # Test with equal swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 42000.0
        assert not detector.is_golden_ratio(41236.0), "Should handle equal swing points"
        
        # Test with zero price range
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        assert not detector.is_golden_ratio(0.0), "Should handle zero price"

    def test_error_handling_confluence(self, detector):
        """Test error handling in confluence detection."""
        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_golden_ratio_confluence(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle None order book state in confluence detection"

    def test_error_handling_historical_boost(self, detector):
        """Test error handling in historical boost calculation."""
        # Test with empty confluence history
        boost = detector.calculate_historical_boost(41236.0)
        assert boost == 0.0, "Should handle empty confluence history"
        
        # Test with invalid price level
        boost = detector.calculate_historical_boost(float('inf'))
        assert boost == 0.0, "Should handle invalid price level"

    def test_error_handling_order_book(self, detector):
        """Test error handling in order book analysis."""
        # Test get_order_book_state error handling
        with patch.object(detector, 'get_order_book_state', autospec=True) as mock_order_book:
            mock_order_book.side_effect = Exception("Test error")
            try:
                result = detector.get_order_book_state()
            except Exception:
                result = None
            assert result is None, "Should handle get_order_book_state errors"
        
        # Test calculate_order_book_depth error handling
        with patch.object(detector, 'calculate_order_book_depth', autospec=True) as mock_depth:
            mock_depth.side_effect = Exception("Test error")
            try:
                result = detector.calculate_order_book_depth({})
            except Exception:
                result = 0.0
            assert result == 0.0, "Should handle calculate_order_book_depth errors"
        
        # Test calculate_order_book_imbalance error handling
        with patch.object(detector, 'calculate_order_book_imbalance', autospec=True) as mock_imbalance:
            mock_imbalance.side_effect = Exception("Test error")
            try:
                result = detector.calculate_order_book_imbalance({})
            except Exception:
                result = 0.0
            assert result == 0.0, "Should handle calculate_order_book_imbalance errors"

    def test_edge_cases_order_book_analysis(self, detector):
        """Test edge cases in order book analysis."""
        # Test calculate_order_book_depth with empty order book
        depth = detector.calculate_order_book_depth({})
        assert depth == 0.0, "Should handle empty order book in depth calculation"
        
        # Test calculate_order_book_depth with missing bids/asks
        depth = detector.calculate_order_book_depth({'bids': [], 'asks': []})
        assert depth == 0.0, "Should handle missing bids/asks in depth calculation"
        
        # Test calculate_order_book_imbalance with empty order book
        imbalance = detector.calculate_order_book_imbalance({})
        assert imbalance == 0.0, "Should handle empty order book in imbalance calculation"
        
        # Test calculate_order_book_imbalance with missing bids/asks
        imbalance = detector.calculate_order_book_imbalance({'bids': [], 'asks': []})
        assert imbalance == 0.0, "Should handle missing bids/asks in imbalance calculation"
        
        # Test calculate_order_book_imbalance with zero volume
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 0.0)],
            'asks': [(41300.0, 0.0)]
        })
        assert imbalance == 0.0, "Should handle zero volume in imbalance calculation"

    def test_error_handling_liquidity_grab_edge_cases(self, detector):
        """Test error handling and edge cases in liquidity grab detection."""
        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle None order book state"
            
            # Test with empty order book
            mock_order_book.return_value = {'bids': [], 'asks': [], 'volume': 0}
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle empty order book"
            
            # Test with invalid price
            mock_order_book.return_value = {
                'bids': [(41200.0, 2.0), (41100.0, 3.0)],
                'asks': [(41300.0, 2.0), (41400.0, 3.0)],
                'volume': 1000.0
            }
            result = detector.detect_liquidity_grab(float('inf'), datetime.now(timezone.utc))
            assert result is None, "Should handle invalid price"
            
            # Test with no Fibonacci levels
            detector.recent_swing_high = None
            detector.recent_swing_low = None
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle missing Fibonacci levels"
            
            # Test with equal swing points
            detector.recent_swing_high = 42000.0
            detector.recent_swing_low = 42000.0
            result = detector.detect_liquidity_grab(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle equal swing points"

    def test_error_handling_golden_ratio_confluence_edge_cases(self, detector):
        """Test error handling and edge cases in golden ratio confluence detection."""
        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_golden_ratio_confluence(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle None order book state"
            
            # Test with empty order book
            mock_order_book.return_value = {'bids': [], 'asks': [], 'volume': 0}
            result = detector.detect_golden_ratio_confluence(41236.0, datetime.now(timezone.utc))
            assert result is None, "Should handle empty order book"
            
            # Test with invalid price
            mock_order_book.return_value = {
                'bids': [(41200.0, 2.0), (41100.0, 3.0)],
                'asks': [(41300.0, 2.0), (41400.0, 3.0)],
                'volume': 1000.0
            }
            result = detector.detect_golden_ratio_confluence(float('inf'), datetime.now(timezone.utc))
            assert result is None, "Should handle invalid price"

    def test_error_handling_historical_boost_edge_cases(self, detector):
        """Test error handling and edge cases in historical boost calculation."""
        # Test with empty confluence history
        boost = detector.calculate_historical_boost(41236.0)
        assert boost == 0.0, "Should handle empty confluence history"
        
        # Test with invalid price level
        boost = detector.calculate_historical_boost(float('inf'))
        assert boost == 0.0, "Should handle invalid price level"
        
        # Test with negative price level
        boost = detector.calculate_historical_boost(-1000.0)
        assert boost == 0.0, "Should handle negative price level"

    def test_edge_cases_order_book_depth(self, detector):
        """Test edge cases in order book depth calculation."""
        # Test with empty order book
        depth = detector.calculate_order_book_depth({})
        assert depth == 0.0, "Should handle empty order book"
        
        # Test with missing bids/asks
        depth = detector.calculate_order_book_depth({'bids': [], 'asks': []})
        assert depth == 0.0, "Should handle missing bids/asks"
        
        # Test with invalid bid/ask format
        depth = detector.calculate_order_book_depth({'bids': [1, 2], 'asks': [3, 4]})
        assert depth == 0.0, "Should handle invalid bid/ask format"
        
        # Test with zero volumes
        depth = detector.calculate_order_book_depth({
            'bids': [(41200.0, 0.0)],
            'asks': [(41300.0, 0.0)]
        })
        assert depth == 0.0, "Should handle zero volumes"

    def test_edge_cases_order_book_imbalance(self, detector):
        """Test edge cases in order book imbalance calculation."""
        # Test with empty order book
        imbalance = detector.calculate_order_book_imbalance({})
        assert imbalance == 0.0, "Should handle empty order book"
        
        # Test with missing bids/asks
        imbalance = detector.calculate_order_book_imbalance({'bids': [], 'asks': []})
        assert imbalance == 0.0, "Should handle missing bids/asks"
        
        # Test with invalid bid/ask format
        imbalance = detector.calculate_order_book_imbalance({'bids': [1, 2], 'asks': [3, 4]})
        assert imbalance == 0.0, "Should handle invalid bid/ask format"
        
        # Test with zero volumes
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 0.0)],
            'asks': [(41300.0, 0.0)]
        })
        assert imbalance == 0.0, "Should handle zero volumes"
        
        # Test with equal bid/ask volumes
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 2.0)],
            'asks': [(41300.0, 2.0)]
        })
        assert imbalance == 0.0, "Should handle equal bid/ask volumes"
        
        # Test with bid-heavy imbalance
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 3.0)],
            'asks': [(41300.0, 1.0)]
        })
        assert imbalance > 0.0, "Should handle bid-heavy imbalance"
        
        # Test with ask-heavy imbalance
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 1.0)],
            'asks': [(41300.0, 3.0)]
        })
        assert imbalance < 0.0, "Should handle ask-heavy imbalance"

    def test_liquidity_grab_edge_cases_additional(self, detector):
        """Test additional edge cases in liquidity grab detection."""
        # Test with price far from any Fibonacci level
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        result = detector.detect_liquidity_grab(50000.0, datetime.now(timezone.utc))
        assert result is None, "Should handle price far from Fibonacci levels"
        
        # Test with very small price range
        detector.recent_swing_high = 40001.0
        detector.recent_swing_low = 40000.0
        result = detector.detect_liquidity_grab(40000.5, datetime.now(timezone.utc))
        assert result is None, "Should handle very small price range"

    def test_golden_ratio_confluence_edge_cases_additional(self, detector):
        """Test additional edge cases in golden ratio confluence detection."""
        # Test with price far from any Fibonacci level
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        result = detector.detect_golden_ratio_confluence(50000.0, datetime.now(timezone.utc))
        assert result is None, "Should handle price far from Fibonacci levels"
        
        # Test with very small price range
        detector.recent_swing_high = 40001.0
        detector.recent_swing_low = 40000.0
        result = detector.detect_golden_ratio_confluence(40000.5, datetime.now(timezone.utc))
        assert result is None, "Should handle very small price range"

    def test_historical_boost_edge_cases_additional(self, detector):
        """Test additional edge cases in historical boost calculation."""
        # Test with very small price level
        boost = detector.calculate_historical_boost(0.00001)
        assert boost == 0.0, "Should handle very small price level"
        
        # Test with very large price level
        boost = detector.calculate_historical_boost(1e10)
        assert boost == 0.0, "Should handle very large price level"
        
        # Test with NaN price level
        boost = detector.calculate_historical_boost(float('nan'))
        assert boost == 0.0, "Should handle NaN price level"

    def test_order_book_depth_edge_cases_additional(self, detector):
        """Test additional edge cases in order book depth calculation."""
        # Test with invalid bid/ask values
        depth = detector.calculate_order_book_depth({
            'bids': [(float('nan'), 1.0), (float('inf'), 2.0)],
            'asks': [(float('-inf'), 1.0), (None, 2.0)]
        })
        assert depth == 0.0, "Should handle invalid bid/ask values"
        
        # Test with malformed bid/ask entries
        depth = detector.calculate_order_book_depth({
            'bids': [{'price': 41200.0, 'volume': 2.0}],
            'asks': [{'price': 41300.0, 'volume': 2.0}]
        })
        assert depth == 0.0, "Should handle malformed bid/ask entries"

    def test_order_book_imbalance_edge_cases_additional(self, detector):
        """Test additional edge cases in order book imbalance calculation."""
        # Test with invalid bid/ask values
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(float('nan'), 1.0), (float('inf'), 2.0)],
            'asks': [(float('-inf'), 1.0), (None, 2.0)]
        })
        assert imbalance == 0.0, "Should handle invalid bid/ask values"
        
        # Test with malformed bid/ask entries
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [{'price': 41200.0, 'volume': 2.0}],
            'asks': [{'price': 41300.0, 'volume': 2.0}]
        })
        assert imbalance == 0.0, "Should handle malformed bid/ask entries"
        
        # Test with extreme imbalance
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, 1000.0)],
            'asks': [(41300.0, 0.001)]
        })
        assert abs(imbalance) <= 1.0, "Should normalize extreme imbalance"
        
        # Test with negative volumes
        imbalance = detector.calculate_order_book_imbalance({
            'bids': [(41200.0, -2.0)],
            'asks': [(41300.0, -3.0)]
        })
        assert imbalance == 0.0, "Should handle negative volumes"

    def test_liquidity_grab_edge_cases_final(self, detector):
        """Test additional edge cases in liquidity grab detection."""
        # Test with invalid price
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(40000, 1.0)],
                'asks': [(40001, 1.0)]
            }
            result = detector.detect_liquidity_grab(price=None, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with price too far from levels
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(40000, 1.0)],
                'asks': [(40001, 1.0)]
            }
            result = detector.detect_liquidity_grab(price=50000, timestamp=datetime.now(timezone.utc))
            assert result is None

    def test_golden_ratio_confluence_edge_cases_final(self, detector):
        """Test additional edge cases in golden ratio confluence detection."""
        # Test with invalid price
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(40000, 1.0)],
                'asks': [(40001, 1.0)]
            }
            result = detector.detect_golden_ratio_confluence(price=None, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with price too far from levels
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(40000, 1.0)],
                'asks': [(40001, 1.0)]
            }
            result = detector.detect_golden_ratio_confluence(price=50000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_golden_ratio_confluence(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with empty order book
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {'bids': [], 'asks': []}
            result = detector.detect_golden_ratio_confluence(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

    def test_order_book_imbalance_edge_cases_final(self, detector):
        """Test additional edge cases in order book imbalance calculation."""
        # Test with empty order book
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {'bids': [], 'asks': []}
            result = detector.calculate_order_book_imbalance(order_book={'bids': [], 'asks': []})
            assert result == 0.0

        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.calculate_order_book_imbalance(order_book=None)
            assert result == 0.0

    def test_error_handling_get_confluence_history(self, detector):
        """Test error handling in get_confluence_history."""
        # Test with Redis error
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.side_effect = redis.RedisError("Test error")
            result = detector.get_confluence_history()
            assert result == []

        # Test with invalid JSON data
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'invalid json']
            result = detector.get_confluence_history()
            assert result == []

        # Test with missing required fields
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000}']
            result = detector.get_confluence_history()
            assert result == []

        # Test with invalid timestamp
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000, "timestamp": "invalid", "fibonacci_level": 40000, "confidence": 0.9, "order_book_imbalance": 0.0, "is_confirmed": true}']
            result = detector.get_confluence_history()
            assert result == []

    def test_error_handling_save_confluence_data(self, detector):
        """Test error handling in save_confluence_data."""
        # Create a test confluence object
        confluence = GoldenRatioConfluence(
            price=41236.0,
            timestamp=datetime.now(timezone.utc),
            fibonacci_level=41236.0,
            liquidity_grab=None,
            confidence=0.9,
            order_book_imbalance=0.0,
            is_confirmed=True
        )
        
        # Test saving in test mode (should not raise any errors)
        detector.test_mode = True
        detector.save_confluence_data(confluence)
        
        # Test saving with Redis error
        detector.test_mode = False
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lpush.side_effect = redis.RedisError("Test error")
            detector.save_confluence_data(confluence)  # Should not raise any errors

    def test_error_handling_calculate_historical_boost(self, detector):
        """Test error handling in calculate_historical_boost."""
        # Test with empty history
        boost = detector.calculate_historical_boost(41236.0)
        assert boost == 0.0, "Should handle empty history"
        
        # Test with invalid price
        boost = detector.calculate_historical_boost(float('inf'))
        assert boost == 0.0, "Should handle invalid price"
        
        # Test with None price
        boost = detector.calculate_historical_boost(None)
        assert boost == 0.0, "Should handle None price"
        
        # Test with price far from any level
        boost = detector.calculate_historical_boost(50000.0)
        assert boost == 0.0, "Should handle price far from levels"

    def test_error_handling_calculate_order_book_depth_final(self, detector):
        """Test error handling in order book depth calculation."""
        # Test with invalid order book
        depth = detector.calculate_order_book_depth(None)
        assert depth == 0.0, "Should handle None order book"
        
        # Test with missing keys
        depth = detector.calculate_order_book_depth({})
        assert depth == 0.0, "Should handle missing keys"
        
        # Test with invalid bid/ask values
        depth = detector.calculate_order_book_depth({
            'bids': [(None, None), (float('inf'), float('inf'))],
            'asks': [(None, None), (float('inf'), float('inf'))]
        })
        assert depth == 0.0, "Should handle invalid bid/ask values"
        
        # Test with negative volumes
        depth = detector.calculate_order_book_depth({
            'bids': [(41200.0, -2.0), (41100.0, -3.0)],
            'asks': [(41300.0, -2.0), (41400.0, -3.0)]
        })
        assert depth == 0.0, "Should handle negative volumes"
        
        # Test with mixed valid and invalid values
        depth = detector.calculate_order_book_depth({
            'bids': [(41200.0, 2.0), (None, None), (41100.0, 3.0)],
            'asks': [(41300.0, 2.0), (float('inf'), float('inf')), (41400.0, 3.0)]
        })
        assert depth == 10.0, "Should calculate depth with valid values only"

    def test_liquidity_grab_edge_cases_final_2(self, detector):
        """Test additional edge cases in liquidity grab detection."""
        # Test with invalid order book state
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = None
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with empty order book
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {'bids': [], 'asks': []}
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with no Fibonacci levels
        with patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_levels.return_value = {}
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

    def test_golden_ratio_confluence_edge_cases_final_2(self, detector):
        """Test additional edge cases in golden ratio confluence detection."""
        # Test with no swing points
        detector.recent_swing_high = None
        detector.recent_swing_low = None
        result = detector.detect_golden_ratio_confluence(price=40000, timestamp=datetime.now(timezone.utc))
        assert result is None

        # Test with small price range
        detector.recent_swing_high = 40001.0
        detector.recent_swing_low = 40000.0
        result = detector.detect_golden_ratio_confluence(price=40000.5, timestamp=datetime.now(timezone.utc))
        assert result is None

        # Test with price at swing high
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(41900, 1.0)],
                'asks': [(42100, 1.0)]
            }
            result = detector.detect_golden_ratio_confluence(price=42000.0, timestamp=datetime.now(timezone.utc))
            assert result is not None
            assert result.fibonacci_level == 42000.0

        # Test with price at swing low
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(39900, 1.0)],
                'asks': [(40100, 1.0)]
            }
            result = detector.detect_golden_ratio_confluence(price=40000.0, timestamp=datetime.now(timezone.utc))
            assert result is not None
            assert result.fibonacci_level == 40000.0

    def test_order_book_imbalance_edge_cases_final_2(self, detector):
        """Test additional edge cases in order book imbalance calculation."""
        # Test with invalid bid/ask values
        order_book = {
            'bids': [(float('nan'), 1.0), (float('inf'), 2.0)],
            'asks': [(float('-inf'), 1.0), (None, 2.0)]
        }
        result = detector.calculate_order_book_imbalance(order_book)
        assert result == 0.0

        # Test with negative volumes
        order_book = {
            'bids': [(40000.0, -2.0), (39900.0, -3.0)],
            'asks': [(40100.0, -2.0), (40200.0, -3.0)]
        }
        result = detector.calculate_order_book_imbalance(order_book)
        assert result == 0.0

        # Test with mixed valid and invalid values
        order_book = {
            'bids': [(40000.0, 2.0), (float('nan'), 1.0), (39900.0, 3.0)],
            'asks': [(40100.0, 2.0), (float('inf'), 1.0), (40200.0, 3.0)]
        }
        result = detector.calculate_order_book_imbalance(order_book)
        assert abs(result) <= 1.0

    def test_get_confluence_history_edge_cases_final(self, detector):
        """Test additional edge cases in get_confluence_history."""
        # Test with invalid JSON data
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'invalid json']
            result = detector.get_confluence_history()
            assert result == []

        # Test with missing required fields
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000}']
            result = detector.get_confluence_history()
            assert result == []

        # Test with invalid timestamp
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000, "timestamp": "invalid", "fibonacci_level": 40000, "confidence": 0.9, "order_book_imbalance": 0.0, "is_confirmed": true}']
            result = detector.get_confluence_history()
            assert result == []

    def test_liquidity_grab_edge_cases_final_3(self, detector):
        """Test additional edge cases in liquidity grab detection."""
        # Test with zero depth
        with patch.object(detector, 'get_order_book_state') as mock_order_book:
            mock_order_book.return_value = {
                'bids': [(40000, 0.0)],
                'asks': [(40001, 0.0)]
            }
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with no valid levels
        detector.recent_swing_high = None
        detector.recent_swing_low = None
        with patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_levels.return_value = {
                'level1': None,
                'level2': None
            }
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with no nearest level found
        detector.recent_swing_high = None
        detector.recent_swing_low = None
        with patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_levels.return_value = {}
            result = detector.detect_liquidity_grab(price=40000, timestamp=datetime.now(timezone.utc))
            assert result is None

    def test_golden_ratio_confluence_edge_cases_final_3(self, detector):
        """Test additional edge cases in golden ratio confluence detection."""
        # Test with no liquidity grab and price not at swing points
        detector.recent_swing_high = 42000.0
        detector.recent_swing_low = 40000.0
        with patch.object(detector, 'get_order_book_state') as mock_order_book, \
             patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_order_book.return_value = {
                'bids': [(40900, 1.0)],
                'asks': [(41100, 1.0)]
            }
            mock_levels.return_value = {}
            result = detector.detect_golden_ratio_confluence(price=41000.0, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with price far from swing high
        with patch.object(detector, 'get_order_book_state') as mock_order_book, \
             patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_order_book.return_value = {
                'bids': [(41900, 1.0)],
                'asks': [(42100, 1.0)]
            }
            mock_levels.return_value = {}
            result = detector.detect_golden_ratio_confluence(price=42100.0, timestamp=datetime.now(timezone.utc))
            assert result is None

        # Test with price far from swing low
        with patch.object(detector, 'get_order_book_state') as mock_order_book, \
             patch.object(detector, 'generate_fibonacci_levels') as mock_levels:
            mock_order_book.return_value = {
                'bids': [(39900, 1.0)],
                'asks': [(40100, 1.0)]
            }
            mock_levels.return_value = {}
            result = detector.detect_golden_ratio_confluence(price=39900.0, timestamp=datetime.now(timezone.utc))
            assert result is None

    def test_order_book_imbalance_edge_cases_final_3(self, detector):
        """Test additional edge cases in order book imbalance calculation."""
        # Test with zero total volume
        order_book = {
            'bids': [(40000.0, 0.0)],
            'asks': [(40100.0, 0.0)]
        }
        result = detector.calculate_order_book_imbalance(order_book)
        assert result == 0.0

    def test_get_confluence_history_edge_cases_final_2(self, detector):
        """Test additional edge cases in get_confluence_history."""
        # Test with empty list
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = []
            result = detector.get_confluence_history()
            assert result == []

        # Test with invalid timestamp format
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000, "timestamp": "2024-03-20", "fibonacci_level": 40000, "confidence": 0.9, "order_book_imbalance": 0.0, "is_confirmed": true}']
            result = detector.get_confluence_history()
            assert result == []

        # Test with invalid confidence value
        with patch.object(detector, 'redis_conn') as mock_redis:
            mock_redis.lrange.return_value = [b'{"price": 40000, "timestamp": "2024-03-20T12:00:00Z", "fibonacci_level": 40000, "confidence": "high", "order_book_imbalance": 0.0, "is_confirmed": true}']
            result = detector.get_confluence_history()
            assert result == [] 