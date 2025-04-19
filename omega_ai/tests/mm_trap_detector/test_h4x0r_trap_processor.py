
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
🎯 H4X0R TR4P PR0C3SS0R T3ST SU1T3 🎯
=====================================

L33t tests for the Market Maker Trap Queue Processor.
May your queues be fast and your latency low! 🚀

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import pytest
import redis
import json
import time
from unittest.mock import patch, MagicMock
from omega_ai.mm_trap_detector.mm_trap_consumer import TrapProcessor
from omega_ai.mm_trap_detector.mm_trap_processor import (
    process_mm_trap,
    print_header, print_section, print_price_update, print_analysis_result,
    print_movement_tag, print_alert
)
from omega_ai.mm_trap_detector.high_frequency_detector import (
    HighFrequencyTrapDetector,
    SCHUMANN_THRESHOLD,
    MIN_TRAPS_FOR_HF_MODE,
    BACK_TO_BACK_WINDOW
)
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector

# ANSI color codes for h4x0r style output
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def _run_detector_once(mock_sleep):
    """Helper function to run one iteration of the detector."""
    # Save original sleep function
    original_sleep = time.sleep
    
    # Replace sleep with mock during execution
    time.sleep = mock_sleep
    
    # Set flag to exit after one iteration
    process_mm_trap._test_single_run = True
    
    try:
        # Call the main processor function once
        process_mm_trap()
    finally:
        # Restore original sleep function
        time.sleep = original_sleep
        # Reset the test flag
        process_mm_trap._test_single_run = False
    
    # Assert that sleep was called (to prevent infinite loop in tests)
    mock_sleep.assert_called_once()
    # Reset mock for next call
    mock_sleep.reset_mock()

class TestH4x0rTrapProcessor:
    """🔥 L33t tests for the trap processing system."""
    
    @pytest.fixture
    def processor(self):
        """Create a fresh processor instance for each test."""
        return TrapProcessor()
    
    @pytest.fixture
    def mock_redis_manager(self):
        """Setup mock Redis manager."""
        with patch('omega_ai.mm_trap_detector.mm_trap_consumer.redis_manager') as mock:
            mock.client = MagicMock()
            yield mock
            
    @pytest.fixture
    def mock_redis(self):
        """Divine Redis mock for isolated testing."""
        mock_redis_client = MagicMock(spec=redis.Redis)
        
        # Mock data store
        data_store = {}
        lists_store = {}
        
        # Mock get method
        def mock_get(key):
            return data_store.get(key)
        
        # Mock set method
        def mock_set(key, value):
            data_store[key] = value
            return True
        
        # Mock rpush method
        def mock_rpush(key, value):
            if key not in lists_store:
                lists_store[key] = []
            lists_store[key].append(value)
            return len(lists_store[key])
        
        # Mock lrange method
        def mock_lrange(key, start, end):
            if key not in lists_store:
                return []
            if start < 0:
                start = max(0, len(lists_store[key]) + start)
            if end < 0:
                end = max(0, len(lists_store[key]) + end + 1)
            else:
                end = min(len(lists_store[key]), end + 1)
            return lists_store[key][start:end]
        
        # Mock ltrim method
        def mock_ltrim(key, start, end):
            if key not in lists_store:
                return True
            if start < 0:
                start = max(0, len(lists_store[key]) + start)
            if end < 0:
                end = max(0, len(lists_store[key]) + end + 1)
            else:
                end = min(len(lists_store[key]), end + 1)
            lists_store[key] = lists_store[key][start:end]
            return True
        
        # Mock hset method
        def mock_hset(key, mapping=None, **kwargs):
            if key not in data_store:
                data_store[key] = {}
            if mapping:
                data_store[key].update(mapping)
            else:
                data_store[key].update(kwargs)
            return True
        
        # Assign mocks
        mock_redis_client.get = MagicMock(side_effect=mock_get)
        mock_redis_client.set = MagicMock(side_effect=mock_set)
        mock_redis_client.rpush = MagicMock(side_effect=mock_rpush)
        mock_redis_client.lrange = MagicMock(side_effect=mock_lrange)
        mock_redis_client.ltrim = MagicMock(side_effect=mock_ltrim)
        mock_redis_client.hset = MagicMock(side_effect=mock_hset)
        
        # Provide access to internal stores for test verification
        mock_redis_client._data_store = data_store
        mock_redis_client._lists_store = lists_store
        
        return mock_redis_client

    @pytest.fixture
    def mock_omega_algo(self):
        """Divine OmegaAlgo mock for predictable test behavior."""
        mock_algo = MagicMock()
        mock_algo.calculate_dynamic_threshold.return_value = 300.0
        mock_algo.is_fibo_organic.return_value = "Organic Movement (High Confidence)"
        mock_algo.analyze_multi_timeframe_trends.return_value = {
            "1min": "bullish",
            "5min": "bullish",
            "15min": "neutral",
            "1h": "bullish"
        }
        return mock_algo

    @pytest.fixture
    def setup_price_environment(self):
        """Divine fixture to setup redis price environment."""
        def _setup(current_price, prev_price=None, mock_redis=None):
            if mock_redis is None:
                return
                
            mock_redis.get.side_effect = None
            mock_redis.reset_mock()
            
            def get_redis_value(key):
                if key == "last_btc_price":
                    return str(current_price)
                elif key == "prev_btc_price" and prev_price is not None:
                    return str(prev_price)
                elif key == "last_btc_volume":
                    return "1000"
                return None
                
            mock_redis.get.side_effect = get_redis_value
            mock_redis.lrange.return_value = []
        
        return _setup

    def test_h4x0r_batch_processing(self, processor, mock_redis_manager):
        """⚡ Test processing a batch of trap events with maximum l33tness."""
        print(f"\n{MAGENTA}Testing B4TCH PR0C3SS1NG...{RESET}")
        
        test_batch = [
            json.dumps({
                'type': 'Stealth Accumulation',
                'confidence': 0.85,
                'price': 42000.0
            }),
            json.dumps({
                'type': 'Stop Hunt',
                'confidence': 0.92,
                'price': 43100.0
            }),
            json.dumps({
                'type': 'Liquidity Grab',
                'confidence': 0.78,
                'price': 41900.0
            })
        ]
        
        successful, errors = processor.process_batch(test_batch)
        
        assert successful == 3, "Should process all traps in batch"
        assert errors == 0, "Should have no processing errors"
        assert processor.stats["processed"] == 3, "Stats should track processed traps"
        
        print(f"{GREEN}✓ B4TCH PR0C3SS1NG successful!{RESET}")
    
    def test_3rr0r_handling(self, processor, mock_redis_manager):
        """💀 Test handling of corrupt/invalid trap data."""
        print(f"\n{MAGENTA}Testing 3RR0R H4NDL1NG...{RESET}")
        
        test_batch = [
            "invalid json",
            json.dumps({
                'type': 'Valid Trap',
                'confidence': 0.85,
                'price': 42000.0
            }),
            "more invalid json"
        ]
        
        successful, errors = processor.process_batch(test_batch)
        
        assert successful == 1, "Should process valid trap"
        assert errors == 2, "Should handle invalid data gracefully"
        assert processor.stats["errors"] == 2, "Stats should track errors"
        
        print(f"{GREEN}✓ 3RR0R H4NDL1NG successful!{RESET}")
    
    def test_qu3u3_processing(self, processor, mock_redis_manager):
        """🔄 Test queue processing with rate limiting."""
        print(f"\n{MAGENTA}Testing QU3U3 PR0C3SS1NG...{RESET}")
        
        # Setup queue with test data
        test_data = [
            json.dumps({
                'type': 'Trap 1',
                'confidence': 0.85,
                'price': 42000.0
            }),
            json.dumps({
                'type': 'Trap 2',
                'confidence': 0.92,
                'price': 42100.0
            })
        ]
        
        mock_redis_manager.client.lrange.return_value = test_data
        
        # Process queue
        processor.process_queue()
        
        # Verify processing
        assert processor.stats["processed"] == 2, "Should process all queue items"
        assert processor.stats["errors"] == 0, "Should have no processing errors"
        
        print(f"{GREEN}✓ QU3U3 PR0C3SS1NG successful!{RESET}")
    
    def test_st4ts_tracking(self, processor, mock_redis_manager):
        """📊 Test statistics tracking and reporting."""
        print(f"\n{MAGENTA}Testing ST4TS TR4CK1NG...{RESET}")
        
        # Process some test data
        test_batch = [
            json.dumps({
                'type': 'Trap 1',
                'confidence': 0.85,
                'price': 42000.0
            }),
            json.dumps({
                'type': 'Trap 2',
                'confidence': 0.92,
                'price': 42100.0
            })
        ]
        
        processor.process_batch(test_batch)
        
        # Verify stats
        assert processor.stats["processed"] == 2, "Should track processed items"
        assert processor.stats["errors"] == 0, "Should track errors"
        assert processor.stats["last_processed"] is not None, "Should track last processed time"
        
        print(f"{GREEN}✓ ST4TS TR4CK1NG successful!{RESET}")
    
    def test_r3dis_integration(self, mock_redis_manager, processor):
        """🔌 Test Redis integration and data persistence."""
        print(f"\n{MAGENTA}Testing R3D1S 1NT3GR4T10N...{RESET}")
        
        # Setup test data
        test_trap = {
            'type': 'Test Trap',
            'confidence': 0.85,
            'price': 42000.0
        }
        
        # Process trap
        processor.process_trap(json.dumps(test_trap))
        
        # Verify Redis interactions
        mock_redis_manager.client.rpush.assert_called()
        mock_redis_manager.client.ltrim.assert_called()
        
        print(f"{GREEN}✓ R3D1S 1NT3GR4T10N successful!{RESET}")

if __name__ == "__main__":
    print("🚀 Running H4X0R TR4P PR0C3SS0R Test Suite...")
    pytest.main([__file__, "-v"]) 