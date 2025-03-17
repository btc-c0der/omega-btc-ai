"""
🎯 0M3G4 TR4P PR0C3SS0R T3ST SU1T3 🎯
=====================================

L33t tests for the Market Maker Trap Queue Processor.
May your queues be fast and your latency low! 🚀

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
"""

import pytest
import redis
import json
import time
import datetime
from unittest.mock import patch, MagicMock, ANY
import numpy as np

# Add project root to path for divine module accessibility
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from omega_ai.mm_trap_detector.mm_trap_consumer import TrapProcessor, QUEUE_NAME
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
            "invalid_json{",
            json.dumps({'type': 'Valid Trap', 'confidence': 0.9, 'price': 42000.0}),
            b'\x80\x80\x80\x80'
        ]
        
        successful, errors = processor.process_batch(test_batch)
        
        assert successful == 1, "Should process valid traps"
        assert errors == 2, "Should count invalid traps"
        assert processor.stats["errors"] == 2, "Stats should track errors"
        
        print(f"{GREEN}✓ 3RR0R H4NDL1NG verified!{RESET}")
    
    def test_qu3u3_processing(self, processor, mock_redis_manager):
        """🔄 Test queue interaction and item removal."""
        print(f"\n{MAGENTA}Testing QU3U3 PR0C3SS1NG...{RESET}")
        
        mock_items = [
            json.dumps({'type': 'Stop Hunt', 'confidence': 0.95, 'price': 44000.0}),
            json.dumps({'type': 'Liquidity Grab', 'confidence': 0.88, 'price': 43500.0})
        ]
        mock_scores = [1234567890.0, 1234567891.0]
        
        # Set up mock to return items once then empty queue
        mock_redis_manager.client.zrange.side_effect = [mock_items, []]
        mock_redis_manager.client.zmscore.return_value = mock_scores
        
        # Patch the running flag to exit after processing
        with patch('omega_ai.mm_trap_detector.mm_trap_consumer.running', new=True):
            processor.run_consumer()
        
        mock_redis_manager.client.zrange.assert_called_with(QUEUE_NAME, 0, 49)
        mock_redis_manager.client.zmscore.assert_called_with(QUEUE_NAME, mock_items)
        mock_redis_manager.client.zremrangebyscore.assert_called_with(
            QUEUE_NAME, '-inf', mock_scores[1]
        )
        
        print(f"{GREEN}✓ QU3U3 PR0C3SS1NG verified!{RESET}")
    
    def test_st4ts_tracking(self, processor, mock_redis_manager):
        """📊 Test statistics collection and reporting."""
        print(f"\n{MAGENTA}Testing ST4TS TR4CK1NG...{RESET}")
    
        test_batch = [
            json.dumps({'type': 'Trap1', 'confidence': 0.9, 'price': 42000.0}),
            json.dumps({'type': 'Trap2', 'confidence': 0.85, 'price': 43000.0}),
            "invalid_data",
            b'\x80\x80\x80\x80'
        ]
    
        time.sleep(0.1)
        processor.process_batch(test_batch)
        time.sleep(0.1)
        processor.process_batch(test_batch[:1])
    
        assert processor.stats["processed"] == 3, "Should count all processed traps"
        assert processor.stats["errors"] == 2, "Should count all errors"
        assert processor.stats["processing_rate"] > 0, "Should calculate rate"
        assert isinstance(processor.stats["last_processed"], datetime.datetime)
        
        print(f"{GREEN}✓ ST4TS TR4CK1NG verified!{RESET}")
    
    def test_r3dis_integration(self, mock_redis_manager, processor):
        """🔌 Test Redis connection handling and recovery."""
        print(f"\n{MAGENTA}Testing R3D1S 1NT3GR4T10N...{RESET}")
    
        mock_redis_manager.client.zrange.side_effect = [
            redis.ConnectionError("Connection lost"),
            ["valid_trap_data"],
            []
        ]
    
        for _ in range(3):
            processor.run_consumer()
            time.sleep(0.1)
    
        assert mock_redis_manager.client.zrange.call_count == 3
        
        print(f"{GREEN}✓ R3D1S 1NT3GR4T10N verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_liquidity_grab_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                    mock_insert_subtle, mock_register_trap, mock_send_alert,
                                    mock_sleep):
        """🌿 Test divine detection of full liquidity grab manipulation."""
        print(f"\n{GREEN}Testing LIQUIDITY GRAB detection...{RESET}")
        
        current_price = 60000.0
        prev_price = 59000.0
        price_change_pct = (current_price - prev_price) / prev_price
        
        mock_omega_algo.calculate_dynamic_threshold.return_value = 500.0
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        _run_detector_once(mock_sleep)
        
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        assert trap_call[0] == current_price
        assert trap_call[1] == price_change_pct
        assert trap_call[2] == "Liquidity Grab"
        assert trap_call[3] == 0.9
        
        mock_register_trap.assert_called_once_with("Liquidity Grab", 0.9, price_change_pct)
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Full Liquidity Grab detection verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_fake_pump_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """🚀 Test divine detection of fake pump manipulation."""
        print(f"\n{GREEN}Testing F4K3 PUMP detection...{RESET}")
        
        current_price = 30000.0
        prev_price = 29400.0  # 2.04% increase
        price_change_pct = (current_price - prev_price) / prev_price
        
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        _run_detector_once(mock_sleep)
        
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        assert trap_call[0] == current_price
        assert trap_call[1] == price_change_pct
        assert trap_call[2] == "Fake Pump"
        assert trap_call[3] == 0.85
        
        mock_register_trap.assert_called_once_with("Fake Pump", 0.85, price_change_pct)
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Fake Pump detection verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_fake_dump_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """💥 Test divine detection of fake dump manipulation."""
        print(f"\n{RED}Testing F4K3 DUMP detection...{RESET}")
        
        current_price = 29300.0
        prev_price = 30000.0  # -2.33% decrease
        price_change_pct = (current_price - prev_price) / prev_price
        
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0
        mock_omega_algo.is_fibo_organic.return_value = "Manipulation Trap Pattern"
        
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        _run_detector_once(mock_sleep)
        
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        assert trap_call[0] == current_price
        assert trap_call[1] == price_change_pct
        assert trap_call[2] == "Fake Dump"
        assert trap_call[3] == 0.85
        
        mock_register_trap.assert_called_once_with("Fake Dump", 0.85, price_change_pct)
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Fake Dump detection verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_stealth_accumulation_pattern(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                      mock_insert_subtle, mock_register_trap, mock_send_alert,
                                      mock_sleep):
        """Test detection of stealth accumulation pattern."""
        print(f"\n{MAGENTA}Testing Stealth Accumulation Pattern...{RESET}")
        
        # Setup test data
        current_price = 45000.0
        prev_price = 44800.0
        volume = 1200.0
        price_change_pct = (current_price - prev_price) / prev_price
        
        # Configure Redis mock
        mock_redis.get.side_effect = lambda key: {
            'last_btc_price': str(current_price).encode(),
            'prev_btc_price': str(prev_price).encode(),
            'btc_volume': str(volume).encode()
        }.get(key)
        
        # Configure OmegaAlgo mock
        mock_omega_algo.calculate_dynamic_threshold.return_value = 300.0
        mock_omega_algo.is_fibo_organic.return_value = "Stealth Accumulation Pattern"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            '1h': 'Bullish',
            '4h': 'Bullish',
            '1d': 'Neutral'
        }
        
        # Run detector once
        _run_detector_once(mock_sleep)
        
        # Verify subtle movement was recorded
        movement_call = mock_insert_subtle.call_args[1]
        assert movement_call['price'] == current_price
        assert movement_call['prev_price'] == prev_price
        assert movement_call['movement_tag'] == "Stealth Accumulation"
        assert movement_call['volume'] == volume
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Assertions for stealth accumulation
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Stealth Accumulation", "Should detect as Stealth Accumulation"
        assert trap_call[3] == 0.75, "Stealth Accumulation should have 0.75 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Stealth Accumulation", 0.75, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Stealth Accumulation Pattern detection verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_fractal_trap_pattern(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """Test detection of fractal trap pattern."""
        print(f"\n{MAGENTA}Testing Fractal Trap Pattern...{RESET}")
        
        # Setup test data
        current_price = 48000.0
        prev_price = 47500.0
        volume = 2500.0
        price_change_pct = (current_price - prev_price) / prev_price
        
        # Configure Redis mock
        mock_redis.get.side_effect = lambda key: {
            'last_btc_price': str(current_price).encode(),
            'prev_btc_price': str(prev_price).encode(),
            'btc_volume': str(volume).encode()
        }.get(key)
        
        # Configure OmegaAlgo mock
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0  # Higher threshold to avoid liquidity grab
        mock_omega_algo.is_fibo_organic.return_value = "Fractal Pattern Detected"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            '1h': 'Bullish',
            '4h': 'Bullish',
            '1d': 'Bullish'
        }
        
        # Run detector once
        _run_detector_once(mock_sleep)
        
        # Verify subtle movement was recorded
        movement_call = mock_insert_subtle.call_args[1]
        assert movement_call['price'] == current_price
        assert movement_call['prev_price'] == prev_price
        assert movement_call['movement_tag'] == "Fractal Trap"
        assert movement_call['volume'] == volume
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Assertions for fractal trap
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Fractal Trap", "Should detect as Fractal Trap"
        assert trap_call[3] == 0.85, "Fractal Trap should have 0.85 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Fractal Trap", 0.85, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Fractal Trap Pattern detection verified!{RESET}")

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    def test_time_dilation_trap(self, mock_redis, mock_omega_algo, mock_insert_trap,
                             mock_insert_subtle, mock_register_trap, mock_send_alert,
                             mock_sleep):
        """Test detection of time dilation trap pattern."""
        print(f"\n{MAGENTA}Testing Time Dilation Trap Pattern...{RESET}")
        
        # Setup test data
        current_price = 46000.0
        prev_price = 45800.0
        volume = 800.0  # Lower weekend volume
        avg_volume = 2000.0  # Normal average daily volume
        price_change_pct = (current_price - prev_price) / prev_price
        
        # Configure Redis mock
        mock_redis.get.side_effect = lambda key: {
            'last_btc_price': str(current_price).encode(),
            'prev_btc_price': str(prev_price).encode(),
            'btc_volume': str(volume).encode(),
            'avg_daily_volume': str(avg_volume).encode()
        }.get(key)
        
        # Configure OmegaAlgo mock
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0  # Higher threshold to avoid liquidity grab
        mock_omega_algo.is_fibo_organic.return_value = "Time-Based Pattern"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            '1h': 'Bullish',
            '4h': 'Neutral',
            '1d': 'Bearish'
        }
        
        # Force weekend timestamp
        current_time = datetime.datetime.now()
        if current_time.weekday() < 5:  # If it's a weekday
            current_time = current_time + datetime.timedelta(days=(5 - current_time.weekday()))
        
        # Run detector once
        _run_detector_once(mock_sleep)
        
        # Verify subtle movement was recorded
        movement_call = mock_insert_subtle.call_args[1]
        assert movement_call['price'] == current_price
        assert movement_call['prev_price'] == prev_price
        assert movement_call['movement_tag'] == "Time Dilation Trap"
        assert movement_call['volume'] == volume
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Assertions for time dilation trap
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Time Dilation Trap", "Should detect as Time Dilation Trap"
        assert trap_call[3] == 0.8, "Time Dilation Trap should have 0.8 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Time Dilation Trap", 0.8, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Time Dilation Trap Pattern detection verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_schumann_resonance_spike(self, mock_redis):
        """🌌 Test detection of Schumann resonance spikes."""
        print(f"\n{MAGENTA}Testing SCHUM4NN R3S0N4NC3 SP1K3 detection...{RESET}")
        
        detector = HighFrequencyTrapDetector()
        schumann_value = SCHUMANN_THRESHOLD + 5.0
        current_price = 50000.0
        
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "schumann_resonance":
                return str(schumann_value).encode()
            return None
        mock_redis.get.side_effect = get_side_effect
        
        hf_mode_active = detector.detect_high_freq_trap_mode(
            latest_price=current_price,
            schumann_resonance=schumann_value
        )
        
        assert hf_mode_active, "HF mode should activate with Schumann spike"
        
        print(f"  • {CYAN}Schumann resonance spike detection verified!{RESET}")

    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_back_to_back_trap_detection(self, mock_redis):
        """🔄 Test detection of back-to-back trap patterns."""
        print(f"\n{BLUE}Testing B4CK-2-B4CK TR4P detection...{RESET}")
        
        detector = HighFrequencyTrapDetector()
        
        # Register multiple traps in sequence
        for i in range(MIN_TRAPS_FOR_HF_MODE + 1):
            time.sleep(0.1)  # Small delay between traps
            detector.register_trap_event(
                "Test Trap",
                0.9,
                0.02,
                from_detector=False
            )
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return b"50000.0"
            elif key == "prev_btc_price":
                return b"49900.0"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        hf_mode_active = detector.detect_high_freq_trap_mode()
        
        # Verify HF mode was activated
        assert hf_mode_active, "HF mode should activate with multiple recent traps"
        
        print(f"  • {CYAN}Back-to-back trap detection verified!{RESET}")

if __name__ == "__main__":
    print("🚀 Running H4x0r Trap Processor Test Suite...")
    pytest.main([__file__, "-v"]) 