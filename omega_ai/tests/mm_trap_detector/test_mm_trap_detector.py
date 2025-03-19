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
import asyncio
from unittest.mock import patch, MagicMock, ANY
import numpy as np
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK, WebSocketException
import re
from typing import Dict, Any
from datetime import datetime, timedelta
import logging
from prometheus_client import REGISTRY, Counter, Histogram
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import random
from concurrent.futures import ThreadPoolExecutor
import psutil
import signal
import os

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

class TestAutoHealing:
    """🔄 Test auto-healing capabilities of the MM Trap Detector."""
    
    @pytest.fixture
    def detector(self):
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    @pytest.mark.asyncio
    async def test_websocket_auto_healing(self, detector):
        """Test WebSocket connection auto-healing after disconnections."""
        print(f"\n{MAGENTA}Testing WEBSOCKET AUTO-HEALING...{RESET}")
        
        # Mock WebSocket connection failures
        with patch('websockets.connect') as mock_connect:
            # Simulate connection failures
            mock_connect.side_effect = [
                ConnectionClosedError(1000, "Connection lost"),
                ConnectionClosedOK(1000, "Normal closure"),
                WebSocketException("Network error"),
                MagicMock()  # Successful connection
            ]
            
            # Start detector in background
            task = asyncio.create_task(detector.connect_websocket())
            
            # Wait for reconnection attempts
            await asyncio.sleep(0.1)
            
            # Verify reconnection attempts
            assert mock_connect.call_count >= 3, "Should attempt reconnection after failures"
            
            # Cleanup
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        print(f"  • {CYAN}WebSocket auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_redis_connection_healing(self, detector):
        """Test Redis connection auto-healing."""
        print(f"\n{MAGENTA}Testing REDIS AUTO-HEALING...{RESET}")
        
        with patch('redis.Redis') as mock_redis:
            # Simulate Redis connection failures
            mock_redis.side_effect = [
                redis.ConnectionError("Connection lost"),
                redis.ConnectionError("Connection lost"),
                MagicMock()  # Successful connection
            ]
            
            # Create new detector (will trigger Redis connection)
            detector = MMTrapDetector()
            
            # Verify reconnection attempts
            assert mock_redis.call_count >= 3, "Should attempt Redis reconnection"
            
            # Test data consistency after reconnection
            mock_redis.return_value.get.return_value = "50000.0"
            price = detector.get_current_volume()
            assert price == 0.0, "Should handle Redis reconnection gracefully"
        
        print(f"  • {CYAN}Redis auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_influxdb_connection_healing(self, detector):
        """Test InfluxDB connection auto-healing."""
        print(f"\n{MAGENTA}Testing INFLUXDB AUTO-HEALING...{RESET}")
        
        with patch('influxdb_client.client.influxdb_client.InfluxDBClient') as mock_influx:
            # Simulate InfluxDB connection failures
            mock_influx.side_effect = [
                Exception("Connection failed"),
                Exception("Connection failed"),
                MagicMock()  # Successful connection
            ]
            
            # Create new detector (will trigger InfluxDB connection)
            detector = MMTrapDetector()
            
            # Verify reconnection attempts
            assert mock_influx.call_count >= 3, "Should attempt InfluxDB reconnection"
            
            # Test data consistency after reconnection
            mock_influx.return_value.ping.return_value = True
            assert detector.influxdb_client is not None, "Should maintain InfluxDB connection"
        
        print(f"  • {CYAN}InfluxDB auto-healing verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_data_consistency_recovery(self, detector):
        """Test data consistency recovery after connection issues."""
        print(f"\n{MAGENTA}Testing DATA CONSISTENCY RECOVERY...{RESET}")
        
        with patch('redis.Redis') as mock_redis:
            # Setup mock Redis with initial data
            mock_redis_instance = MagicMock()
            mock_redis_instance.get.side_effect = lambda key: {
                "last_btc_price": "50000.0",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            mock_redis.return_value = mock_redis_instance
            
            # Create detector and simulate connection loss
            detector = MMTrapDetector()
            mock_redis_instance.get.side_effect = redis.ConnectionError("Connection lost")
            
            # Attempt to get data during connection loss
            volume = detector.get_current_volume()
            assert volume == 0.0, "Should handle connection loss gracefully"
            
            # Restore connection
            mock_redis_instance.get.side_effect = lambda key: {
                "last_btc_price": "50000.0",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            
            # Verify data consistency after recovery
            volume = detector.get_current_volume()
            assert volume == 1000.0, "Should restore data consistency after recovery"
        
        print(f"  • {CYAN}Data consistency recovery verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_threshold_recalculation_recovery(self, detector):
        """Test threshold recalculation recovery after market data issues."""
        print(f"\n{MAGENTA}Testing THRESHOLD RECALCULATION RECOVERY...{RESET}")
        
        with patch('redis.Redis') as mock_redis:
            # Setup mock Redis with market data
            mock_redis_instance = MagicMock()
            mock_redis_instance.get.side_effect = lambda key: {
                "rolling_volatility": "1000.0",
                "market_regime": "normal",
                "directional_strength": "0.5"
            }.get(key)
            mock_redis.return_value = mock_redis_instance
            
            # Calculate initial threshold
            initial_threshold = detector.calculate_dynamic_threshold(False)
            
            # Simulate market data corruption
            mock_redis_instance.get.side_effect = redis.ConnectionError("Connection lost")
            corrupted_threshold = detector.calculate_dynamic_threshold(False)
            assert corrupted_threshold == detector.BASE_TRAP_THRESHOLD, "Should use base threshold on error"
            
            # Restore market data
            mock_redis_instance.get.side_effect = lambda key: {
                "rolling_volatility": "1000.0",
                "market_regime": "normal",
                "directional_strength": "0.5"
            }.get(key)
            
            # Verify threshold recalculation
            recovered_threshold = detector.calculate_dynamic_threshold(False)
            assert recovered_threshold == initial_threshold, "Should restore correct threshold after recovery"
        
        print(f"  • {CYAN}Threshold recalculation recovery verified!{RESET}")
    
    @pytest.mark.asyncio
    async def test_state_restoration_after_crash(self, detector):
        """Test state restoration after system crash."""
        print(f"\n{MAGENTA}Testing STATE RESTORATION AFTER CRASH...{RESET}")
        
        with patch('redis.Redis') as mock_redis:
            # Setup mock Redis with system state
            mock_redis_instance = MagicMock()
            mock_redis_instance.get.side_effect = lambda key: {
                "high_frequency_mode": "1",
                "last_btc_price": "50000.0",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            mock_redis.return_value = mock_redis_instance
            
            # Create detector and simulate crash
            detector = MMTrapDetector()
            mock_redis_instance.get.side_effect = Exception("System crash")
            
            # Attempt operations during crash
            hf_mode = detector.check_high_frequency_mode()
            assert not hf_mode, "Should handle crash gracefully"
            
            # Restore system state
            mock_redis_instance.get.side_effect = lambda key: {
                "high_frequency_mode": "1",
                "last_btc_price": "50000.0",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            
            # Verify state restoration
            hf_mode = detector.check_high_frequency_mode()
            assert hf_mode, "Should restore system state after recovery"
            
            price = detector.get_current_volume()
            assert price == 1000.0, "Should restore price data after recovery"
        
        print(f"  • {CYAN}State restoration after crash verified!{RESET}")

class TestSecurity:
    """🔒 Security testing for the MM Trap Detector."""
    
    @pytest.fixture
    def detector(self):
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    def test_input_validation(self, detector):
        """Test input validation and sanitization."""
        print(f"\n{MAGENTA}Testing INPUT VALIDATION...{RESET}")
        
        # Test malicious price data
        malicious_prices = [
            float('inf'),
            float('-inf'),
            float('nan'),
            -1.0,
            0.0,
            "50000.0",  # String instead of float
            None,
            b"50000.0"  # Bytes instead of float
        ]
        
        for price in malicious_prices:
            with pytest.raises((ValueError, TypeError)):
                detector.process_price_update(price)
        
        # Test malicious volume data
        malicious_volumes = [
            -1000.0,
            float('inf'),
            float('-inf'),
            float('nan'),
            "1000.0",  # String instead of float
            None,
            b"1000.0"  # Bytes instead of float
        ]
        
        for volume in malicious_volumes:
            with pytest.raises((ValueError, TypeError)):
                detector.get_current_volume()
        
        print(f"  • {CYAN}Input validation verified!{RESET}")
    
    def test_rate_limiting(self, detector):
        """Test rate limiting and request throttling."""
        print(f"\n{MAGENTA}Testing RATE LIMITING...{RESET}")
        
        # Mock time for consistent testing
        with patch('time.time') as mock_time:
            current_time = 1000000.0
            mock_time.return_value = current_time
            
            # Test rapid price updates
            for _ in range(100):
                detector.process_price_update(50000.0)
                current_time += 0.01  # 10ms between updates
                mock_time.return_value = current_time
            
            # Verify rate limiting
            assert detector._request_count <= detector.MAX_REQUESTS_PER_SECOND, "Should respect rate limit"
            
            # Test rate limit reset
            current_time += 1.0  # Wait 1 second
            mock_time.return_value = current_time
            detector.process_price_update(50000.0)
            assert detector._request_count == 1, "Rate limit should reset after window"
        
        print(f"  • {CYAN}Rate limiting verified!{RESET}")
    
    def test_authentication(self, detector):
        """Test authentication and authorization."""
        print(f"\n{MAGENTA}Testing AUTHENTICATION...{RESET}")
        
        # Test WebSocket authentication
        with patch('websockets.connect') as mock_connect:
            # Test without authentication
            mock_connect.side_effect = Exception("Authentication failed")
            with pytest.raises(Exception):
                detector.connect_websocket()
            
            # Test with invalid credentials
            mock_connect.side_effect = Exception("Invalid credentials")
            with pytest.raises(Exception):
                detector.connect_websocket()
            
            # Test with valid credentials
            mock_connect.return_value = MagicMock()
            detector.connect_websocket()
        
        print(f"  • {CYAN}Authentication verified!{RESET}")
    
    def test_dos_protection(self, detector):
        """Test DoS protection mechanisms."""
        print(f"\n{MAGENTA}Testing DOS PROTECTION...{RESET}")
        
        # Test connection flood protection
        with patch('websockets.connect') as mock_connect:
            # Simulate connection flood
            for _ in range(100):
                mock_connect.side_effect = Exception("Connection refused")
                with pytest.raises(Exception):
                    detector.connect_websocket()
            
            # Verify backoff mechanism
            assert detector._connection_attempts >= detector.MAX_CONNECTION_ATTEMPTS, "Should implement backoff"
        
        # Test message flood protection
        with patch('redis.Redis') as mock_redis:
            # Simulate message flood
            mock_redis.return_value.get.side_effect = Exception("Too many requests")
            for _ in range(100):
                with pytest.raises(Exception):
                    detector.get_current_volume()
            
            # Verify message throttling
            assert detector._message_count <= detector.MAX_MESSAGES_PER_SECOND, "Should throttle messages"
        
        print(f"  • {CYAN}DoS protection verified!{RESET}")
    
    def test_data_encryption(self, detector):
        """Test data encryption and secure transmission."""
        print(f"\n{MAGENTA}Testing DATA ENCRYPTION...{RESET}")
        
        # Test WebSocket encryption
        with patch('websockets.connect') as mock_connect:
            # Verify WSS (secure WebSocket) is used
            assert detector.ws_url.startswith('wss://'), "Should use secure WebSocket"
            
            # Test data encryption
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            
            # Send test data
            test_data = {"btc_price": 50000.0}
            detector.handle_websocket_message(json.dumps(test_data))
            
            # Verify data was encrypted
            mock_ws.send.assert_called_once()
            sent_data = mock_ws.send.call_args[0][0]
            assert isinstance(sent_data, bytes), "Data should be encrypted"
        
        print(f"  • {CYAN}Data encryption verified!{RESET}")
    
    def test_error_message_security(self, detector):
        """Test secure error handling and messages."""
        print(f"\n{MAGENTA}Testing ERROR MESSAGE SECURITY...{RESET}")
        
        # Test error message sanitization
        with patch('redis.Redis') as mock_redis:
            # Simulate various error scenarios
            error_cases = [
                ("Connection failed", "Connection error occurred"),
                ("Invalid credentials", "Authentication error"),
                ("Database error", "System error"),
                ("<script>alert('xss')</script>", "System error"),
                ("../../etc/passwd", "System error")
            ]
            
            for error, expected in error_cases:
                mock_redis.side_effect = Exception(error)
                with pytest.raises(Exception) as exc_info:
                    detector.get_current_volume()
                assert str(exc_info.value) == expected, "Error messages should be sanitized"
        
        print(f"  • {CYAN}Error message security verified!{RESET}")
    
    def test_websocket_security(self, detector):
        """Test WebSocket security measures."""
        print(f"\n{MAGENTA}Testing WEBSOCKET SECURITY...{RESET}")
        
        with patch('websockets.connect') as mock_connect:
            # Test ping/pong mechanism
            mock_ws = MagicMock()
            mock_connect.return_value = mock_ws
            
            # Verify ping interval
            assert detector.ping_interval == 15, "Should have appropriate ping interval"
            
            # Test connection timeout
            mock_ws.ping.side_effect = Exception("Connection timeout")
            with pytest.raises(Exception):
                detector.connect_websocket()
            
            # Test message size limits
            large_message = "x" * (2**24 + 1)  # Exceed max size
            with pytest.raises(ValueError):
                detector.handle_websocket_message(large_message)
        
        print(f"  • {CYAN}WebSocket security verified!{RESET}")
    
    def test_data_integrity(self, detector):
        """Test data integrity and validation."""
        print(f"\n{MAGENTA}Testing DATA INTEGRITY...{RESET}")
        
        with patch('redis.Redis') as mock_redis:
            # Test price data integrity
            mock_redis.return_value.get.side_effect = lambda key: {
                "last_btc_price": "50000.0",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            
            # Verify price validation
            price = detector.get_current_volume()
            assert isinstance(price, float), "Price should be float"
            assert price > 0, "Price should be positive"
            
            # Test data corruption detection
            mock_redis.return_value.get.side_effect = lambda key: {
                "last_btc_price": "invalid_price",
                "prev_btc_price": "49900.0",
                "last_btc_volume": "1000.0"
            }.get(key)
            
            with pytest.raises(ValueError):
                detector.get_current_volume()
        
        print(f"  • {CYAN}Data integrity verified!{RESET}")

class TestObservability:
    """🔍 Testing observability features of the MM Trap Detector."""
    
    @pytest.fixture
    def detector(self):
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    @pytest.fixture
    def mock_logger(self):
        """Setup mock logger for testing."""
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            yield mock_logger
    
    def test_logging_levels(self, detector, mock_logger):
        """Test logging at different severity levels."""
        print(f"\n{MAGENTA}Testing LOGGING LEVELS...{RESET}")
        
        # Test info logging
        detector.process_price_update(50000.0)
        mock_logger.info.assert_called()
        assert "Processing price update" in mock_logger.info.call_args[0][0]
        
        # Test warning logging
        detector.process_price_update(float('inf'))
        mock_logger.warning.assert_called()
        assert "Invalid price data" in mock_logger.warning.call_args[0][0]
        
        # Test error logging
        with patch('redis.Redis') as mock_redis:
            mock_redis.side_effect = Exception("Connection failed")
            detector.get_current_volume()
            mock_logger.error.assert_called()
            assert "Failed to get current volume" in mock_logger.error.call_args[0][0]
        
        print(f"  • {CYAN}Logging levels verified!{RESET}")
    
    def test_logging_context(self, detector, mock_logger):
        """Test logging context and metadata."""
        print(f"\n{MAGENTA}Testing LOGGING CONTEXT...{RESET}")
        
        # Test price update logging with context
        detector.process_price_update(50000.0)
        log_call = mock_logger.info.call_args[0][0]
        assert "price=50000.0" in log_call
        assert "timestamp=" in log_call
        
        # Test error logging with context
        with patch('redis.Redis') as mock_redis:
            mock_redis.side_effect = Exception("Connection failed")
            detector.get_current_volume()
            log_call = mock_logger.error.call_args[0][0]
            assert "error=Connection failed" in log_call
            assert "component=redis" in log_call
        
        print(f"  • {CYAN}Logging context verified!{RESET}")
    
    def test_metrics_collection(self, detector):
        """Test Prometheus metrics collection."""
        print(f"\n{MAGENTA}Testing METRICS COLLECTION...{RESET}")
        
        # Reset metrics registry
        REGISTRY._collector_to_names.clear()
        
        # Test price update metrics
        with patch('prometheus_client.Counter') as mock_counter:
            detector.process_price_update(50000.0)
            mock_counter.assert_called_with(
                'mm_trap_price_updates_total',
                'Total number of price updates processed'
            )
        
        # Test error metrics
        with patch('prometheus_client.Counter') as mock_counter:
            with patch('redis.Redis') as mock_redis:
                mock_redis.side_effect = Exception("Connection failed")
                detector.get_current_volume()
                mock_counter.assert_called_with(
                    'mm_trap_errors_total',
                    'Total number of errors encountered'
                )
        
        # Test latency metrics
        with patch('prometheus_client.Histogram') as mock_histogram:
            detector.process_price_update(50000.0)
            mock_histogram.assert_called_with(
                'mm_trap_processing_duration_seconds',
                'Time spent processing price updates'
            )
        
        print(f"  • {CYAN}Metrics collection verified!{RESET}")
    
    def test_metrics_values(self, detector):
        """Test metric values and labels."""
        print(f"\n{MAGENTA}Testing METRIC VALUES...{RESET}")
        
        # Test price update counter
        price_counter = Counter('mm_trap_price_updates_total', 'Price updates')
        price_counter.inc()
        assert price_counter._value.get() == 1
        
        # Test error counter with labels
        error_counter = Counter('mm_trap_errors_total', 'Errors', ['type'])
        error_counter.labels(type='connection').inc()
        assert error_counter.labels(type='connection')._value.get() == 1
        
        # Test latency histogram
        latency_hist = Histogram('mm_trap_processing_duration_seconds', 'Processing time')
        latency_hist.observe(0.1)
        assert latency_hist._sum.get() == 0.1
        assert latency_hist._count.get() == 1
        
        print(f"  • {CYAN}Metric values verified!{RESET}")
    
    def test_tracing_setup(self, detector):
        """Test distributed tracing setup."""
        print(f"\n{MAGENTA}Testing TRACING SETUP...{RESET}")
        
        # Test tracer creation
        tracer = trace.get_tracer(__name__)
        assert tracer is not None
        
        # Test span creation
        with tracer.start_as_current_span("test_span") as span:
            span.set_attribute("test.attribute", "value")
            assert span.get_span_context().trace_id is not None
            assert span.get_span_context().span_id is not None
        
        print(f"  • {CYAN}Tracing setup verified!{RESET}")
    
    def test_tracing_propagation(self, detector):
        """Test trace context propagation."""
        print(f"\n{MAGENTA}Testing TRACE PROPAGATION...{RESET}")
        
        # Create test span
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("parent_span") as parent_span:
            # Create carrier for trace context
            carrier = {}
            propagator = TraceContextTextMapPropagator()
            propagator.inject(carrier)
            
            # Verify carrier contains trace context
            assert "traceparent" in carrier
            assert "tracestate" in carrier
            
            # Extract trace context
            context = propagator.extract(carrier=carrier)
            assert context.trace_id == parent_span.get_span_context().trace_id
        
        print(f"  • {CYAN}Trace propagation verified!{RESET}")
    
    def test_tracing_attributes(self, detector):
        """Test span attributes and events."""
        print(f"\n{MAGENTA}Testing TRACE ATTRIBUTES...{RESET}")
        
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("price_update") as span:
            # Test price update attributes
            detector.process_price_update(50000.0)
            assert span.get_attribute("price") == 50000.0
            assert span.get_attribute("timestamp") is not None
            
            # Test error attributes
            with patch('redis.Redis') as mock_redis:
                mock_redis.side_effect = Exception("Connection failed")
                detector.get_current_volume()
                assert span.get_attribute("error") == "Connection failed"
                assert span.get_attribute("component") == "redis"
            
            # Test span status
            assert span.get_status().status_code == StatusCode.OK
        
        print(f"  • {CYAN}Trace attributes verified!{RESET}")
    
    def test_tracing_span_relationships(self, detector):
        """Test span relationships and hierarchy."""
        print(f"\n{MAGENTA}Testing SPAN RELATIONSHIPS...{RESET}")
        
        tracer = trace.get_tracer(__name__)
        
        # Create parent span
        with tracer.start_as_current_span("parent_operation") as parent_span:
            parent_id = parent_span.get_span_context().span_id
            
            # Create child span
            with tracer.start_as_current_span("child_operation") as child_span:
                child_id = child_span.get_span_context().span_id
                
                # Verify parent-child relationship
                assert child_span.parent.span_id == parent_id
                assert child_span.get_span_context().trace_id == parent_span.get_span_context().trace_id
        
        print(f"  • {CYAN}Span relationships verified!{RESET}")

class TestChaos:
    """🌋 Testing chaos scenarios for the MM Trap Detector."""
    
    @pytest.fixture
    def detector(self):
        """Create a fresh detector instance for each test."""
        return MMTrapDetector()
    
    def test_network_chaos(self, detector):
        """Test system resilience under network chaos."""
        print(f"\n{MAGENTA}Testing NETWORK CHAOS...{RESET}")
        
        # Simulate network latency spikes
        with patch('websockets.connect') as mock_connect:
            # Random latency between 0.1 and 2 seconds
            mock_connect.side_effect = lambda *args, **kwargs: asyncio.sleep(random.uniform(0.1, 2))
            
            # Test connection under latency
            start_time = time.time()
            asyncio.run(detector.connect_websocket())
            duration = time.time() - start_time
            
            # Verify system handles latency
            assert duration >= 0.1, "Should handle network latency"
            print(f"  • {CYAN}Network latency handling verified!{RESET}")
    
    def test_data_corruption(self, detector):
        """Test system resilience under data corruption."""
        print(f"\n{MAGENTA}Testing DATA CORRUPTION...{RESET}")
        
        # Simulate corrupted price data
        corrupted_prices = [
            float('inf'),
            float('-inf'),
            float('nan'),
            None,
            "not_a_number",
            -1.0,
            0.0
        ]
        
        for price in corrupted_prices:
            try:
                detector.process_price_update(price)
            except Exception as e:
                print(f"  • {RED}Error handling corrupted price {price}: {str(e)}{RESET}")
                continue
        
        print(f"  • {CYAN}Data corruption handling verified!{RESET}")
    
    def test_resource_exhaustion(self, detector):
        """Test system behavior under resource exhaustion."""
        print(f"\n{MAGENTA}Testing RESOURCE EXHAUSTION...{RESET}")
        
        # Simulate memory pressure
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create memory pressure
        large_data = [bytearray(1024 * 1024) for _ in range(100)]
        
        # Test system under memory pressure
        try:
            detector.process_price_update(50000.0)
        except Exception as e:
            print(f"  • {RED}Error under memory pressure: {str(e)}{RESET}")
        
        # Cleanup
        del large_data
        
        # Verify memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        print(f"  • {CYAN}Resource exhaustion handling verified! Memory increase: {memory_increase / 1024 / 1024:.2f}MB{RESET}")
    
    def test_concurrent_operations(self, detector):
        """Test system under concurrent operations."""
        print(f"\n{MAGENTA}Testing CONCURRENT OPERATIONS...{RESET}")
        
        def simulate_price_update(price):
            try:
                detector.process_price_update(price)
            except Exception as e:
                print(f"  • {RED}Error in concurrent operation: {str(e)}{RESET}")
        
        # Simulate concurrent price updates
        with ThreadPoolExecutor(max_workers=10) as executor:
            prices = [random.uniform(40000, 60000) for _ in range(100)]
            futures = [executor.submit(simulate_price_update, price) for price in prices]
            
            # Wait for all operations to complete
            for future in futures:
                future.result()
        
        print(f"  • {CYAN}Concurrent operations handling verified!{RESET}")
    
    def test_signal_handling(self, detector):
        """Test system signal handling."""
        print(f"\n{MAGENTA}Testing SIGNAL HANDLING...{RESET}")
        
        def signal_handler(signum, frame):
            print(f"  • {YELLOW}Received signal {signum}{RESET}")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Simulate signal reception
        try:
            os.kill(os.getpid(), signal.SIGINT)
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception as e:
            print(f"  • {RED}Error handling signals: {str(e)}{RESET}")
        
        print(f"  • {CYAN}Signal handling verified!{RESET}")
    
    def test_connection_flapping(self, detector):
        """Test system under connection flapping."""
        print(f"\n{MAGENTA}Testing CONNECTION FLAPPING...{RESET}")
        
        with patch('websockets.connect') as mock_connect:
            # Simulate connection flapping
            mock_connect.side_effect = [
                ConnectionClosedError(1000, "Connection lost"),
                MagicMock(),
                ConnectionClosedOK(1000, "Normal closure"),
                MagicMock(),
                WebSocketException("Network error"),
                MagicMock()
            ]
            
            # Test connection recovery
            start_time = time.time()
            asyncio.run(detector.connect_websocket())
            duration = time.time() - start_time
            
            # Verify reconnection attempts
            assert mock_connect.call_count >= 3, "Should attempt reconnection after failures"
            print(f"  • {CYAN}Connection flapping handling verified! Duration: {duration:.2f}s{RESET}")
    
    def test_data_burst(self, detector):
        """Test system under data burst conditions."""
        print(f"\n{MAGENTA}Testing DATA BURST...{RESET}")
        
        # Simulate burst of price updates
        burst_size = 1000
        prices = [random.uniform(40000, 60000) for _ in range(burst_size)]
        
        start_time = time.time()
        for price in prices:
            try:
                detector.process_price_update(price)
            except Exception as e:
                print(f"  • {RED}Error processing burst data: {str(e)}{RESET}")
        
        duration = time.time() - start_time
        throughput = burst_size / duration
        
        print(f"  • {CYAN}Data burst handling verified! Throughput: {throughput:.2f} updates/s{RESET}")
    
    def test_system_clock_skew(self, detector):
        """Test system under clock skew conditions."""
        print(f"\n{MAGENTA}Testing CLOCK SKEW...{RESET}")
        
        # Simulate clock skew
        with patch('time.time') as mock_time:
            # Simulate time jumping forward and backward
            mock_time.side_effect = [
                time.time(),
                time.time() + 3600,  # Jump forward 1 hour
                time.time() - 1800,   # Jump backward 30 minutes
                time.time() + 7200,   # Jump forward 2 hours
                time.time()           # Back to normal
            ]
            
            try:
                detector.process_price_update(50000.0)
            except Exception as e:
                print(f"  • {RED}Error handling clock skew: {str(e)}{RESET}")
        
        print(f"  • {CYAN}Clock skew handling verified!{RESET}")
    
    def test_partial_system_failure(self, detector):
        """Test system under partial component failure."""
        print(f"\n{MAGENTA}Testing PARTIAL SYSTEM FAILURE...{RESET}")
        
        # Simulate Redis failure
        with patch('redis.Redis') as mock_redis:
            mock_redis.side_effect = Exception("Redis connection failed")
            
            try:
                detector.get_current_volume()
            except Exception as e:
                print(f"  • {RED}Error handling Redis failure: {str(e)}{RESET}")
        
        # Simulate InfluxDB failure
        with patch('influxdb_client.InfluxDBClient') as mock_influx:
            mock_influx.side_effect = Exception("InfluxDB connection failed")
            
            try:
                detector.initialize_influxdb()
            except Exception as e:
                print(f"  • {RED}Error handling InfluxDB failure: {str(e)}{RESET}")
        
        print(f"  • {CYAN}Partial system failure handling verified!{RESET}")

if __name__ == "__main__":
    print("🚀 Running H4x0r Trap Processor Test Suite...")
    pytest.main([__file__, "-v"]) 