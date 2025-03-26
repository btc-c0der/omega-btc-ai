"""
DIVINE MM TRAP DETECTOR TESTS 🌿🔥

These sacred tests verify that the Market Maker Trap Detector properly detects
Babylon system manipulation tactics and protects traders with divine insight.

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏

H4X0R M0D3 4CT1V4T3D - 3L1T3 TR4P D3T3CT10N 🎯
"""

import pytest
import redis
import json
import time
import datetime
from unittest.mock import patch, MagicMock, call
import numpy as np
from omega_ai.tests.mm_trap_detector.test_helpers import _run_detector_once

# Add project root to path for divine module accessibility
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Import the module under test with divine blessings
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector  # Main class to test

from omega_ai.mm_trap_detector.high_frequency_detector import (
    HighFrequencyTrapDetector,
    SCHUMANN_THRESHOLD,
    MIN_TRAPS_FOR_HF_MODE,
    BACK_TO_BACK_WINDOW
)

# Terminal colors for divine test output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# =============== DIVINE FIXTURES ===============

@pytest.fixture
def mock_redis():
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
        # Handle negative indices
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
        # Handle negative indices
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
        
        # Handle both mapping parameter and kwargs
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
def mock_omega_algo():
    """Divine OmegaAlgo mock for predictable test behavior."""
    mock_algo = MagicMock()
    
    # Set up mock behaviors
    mock_algo.calculate_dynamic_threshold.return_value = 300.0  # Default threshold
    mock_algo.is_fibo_organic.return_value = "Organic Movement (High Confidence)"  # Default analysis
    mock_algo.analyze_multi_timeframe_trends.return_value = {
        "1min": "bullish",
        "5min": "bullish",
        "15min": "neutral",
        "1h": "bullish"
    }
    
    return mock_algo

@pytest.fixture
def mock_db():
    """Divine database mock for isolation."""
    mock_db = MagicMock()
    mock_db.insert_mm_trap.return_value = True
    mock_db.insert_subtle_movement.return_value = True
    return mock_db

@pytest.fixture
def mock_hf_detector():
    """Divine high-frequency detector mock."""
    mock_detector = MagicMock()
    mock_detector.register_trap_detection.return_value = True
    return mock_detector

@pytest.fixture
def mock_alerts():
    """Divine alerts orchestrator mock."""
    mock_alerts = MagicMock()
    mock_alerts.send_alert.return_value = True
    return mock_alerts

@pytest.fixture
def setup_price_environment():
    """Divine fixture to setup redis price environment."""
    def _setup(current_price, prev_price=None, mock_redis=None):
        if mock_redis is None:
            return  # Can't setup without mock_redis
            
        # Clear any previous side effects
        mock_redis.get.side_effect = None
        mock_redis.reset_mock()
        
        # Configure get() to return proper values for different keys
        def get_redis_value(key):
            if key == "last_btc_price":
                return str(current_price)
            elif key == "prev_btc_price" and prev_price is not None:
                return str(prev_price)
            elif key == "last_btc_volume":
                return "1000"  # Default test volume
            return None
            
        mock_redis.get.side_effect = get_redis_value
        
        # For lrange calls, return empty list by default
        mock_redis.lrange.return_value = []
    
    return _setup

# =============== DIVINE TEST CLASSES ===============

class TestMMTrapDetector:
    """Divine tests for Market Maker Trap Detector."""
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    async def test_liquidity_grab_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                    mock_insert_subtle, mock_register_trap, mock_send_alert,
                                    mock_sleep):
        """🌿 Test divine detection of full liquidity grab manipulation."""
        print(f"\n{GREEN}Testing LIQUIDITY GRAB detection...{RESET}")
        
        # Setup test data - large price change to trigger liquidity grab detection
        current_price = 60000.0
        prev_price = 59000.0  # $1000 change, above threshold
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 500.0  # Set threshold below our change
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Create detector instance
        detector = MMTrapDetector()
        detector.prev_btc_price = prev_price
        detector.current_btc_price = current_price
        
        # Run one loop of the trap detector
        await detector.process_price_update(current_price)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for liquidity grab
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Liquidity Grab", "Should detect as Liquidity Grab"
        assert trap_call[3] == 0.9, "Liquidity Grab should have 0.9 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once()
        register_call = mock_register_trap.call_args[0]
        assert register_call[0] == current_price, "Should register current price"
        assert register_call[1] == 1000.0, "Should register correct volume"
        assert register_call[2] == price_change_pct, "Should register correct price change"
        
        print(f"{GREEN}✅ Liquidity Grab Detection Test Passed{RESET}\n")
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_half_liquidity_grab_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                         mock_insert_subtle, mock_register_trap, mock_send_alert,
                                         mock_sleep):
        """🌿 Test divine detection of half liquidity grab manipulation."""
        print(f"\n{GREEN}Testing HALF-LIQUIDITY GRAB detection...{RESET}")
        
        # Setup test data - medium price change to trigger half liquidity grab detection
        current_price = 100000.0
        prev_price = 99400.0  # $600 change, above half threshold of $500
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0  # Full threshold
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for half liquidity grab
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Half-Liquidity Grab", "Should detect as Half-Liquidity Grab"
        assert trap_call[3] == 0.7, "Half-Liquidity Grab should have 0.7 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Half-Liquidity Grab", 0.7, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        # Verify data was stored in Redis for Grafana
        mock_redis.hset.assert_called()
        calls = mock_redis.hset.call_args_list
        matched = False
        for call_obj in calls:
            key = call_obj[0][0]
            if "mm_trap:" in key:
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Half-Liquidity Grab"
                assert float(mapping["confidence"]) == 0.7
                assert float(mapping["price"]) == current_price
                matched = True
                break
        assert matched, "Should store trap data in Redis for Grafana"
        
        print(f"  • {CYAN}Half-Liquidity Grab detection verified!{RESET}")
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_fake_pump_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """🌿 Test divine detection of fake pump manipulation."""
        print(f"\n{GREEN}Testing FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase above PRICE_PUMP_THRESHOLD (0.02 = 2%)
        current_price = 30000.0
        prev_price = 29400.0  # 2.04% increase but only $600 absolute change
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for fake pump
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Fake Pump", "Should detect as Fake Pump"
        assert trap_call[3] == 0.85, "Fake Pump should have 0.85 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Fake Pump", 0.85, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        # Verify data was stored in Redis for Grafana
        mock_redis.hset.assert_called()
        calls = mock_redis.hset.call_args_list
        matched = False
        for call_obj in calls:
            key = call_obj[0][0]
            if "mm_trap:" in key:
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Fake Pump"
                assert float(mapping["confidence"]) == 0.85
                assert float(mapping["price"]) == current_price
                matched = True
                break
        assert matched, "Should store trap data in Redis for Grafana"
        
        print(f"  • {CYAN}Fake Pump detection verified!{RESET}")
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_fake_dump_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """🌿 Test divine detection of fake dump manipulation."""
        print(f"\n{GREEN}Testing FAKE DUMP detection...{RESET}")
        
        # Setup test data - price decrease below PRICE_DROP_THRESHOLD (-0.02 = -2%)
        current_price = 29300.0
        prev_price = 30000.0  # -2.33% decrease with $700 absolute change
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Manipulation Trap Pattern"
    
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for fake dump
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Fake Dump", "Should detect as Fake Dump"
        assert trap_call[3] == 0.85, "Fake Dump should have 0.85 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Fake Dump", 0.85, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        # Verify data was stored in Redis for Grafana
        mock_redis.hset.assert_called()
        calls = mock_redis.hset.call_args_list
        matched = False
        for call_obj in calls:
            key = call_obj[0][0]
            if "mm_trap:" in key:
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Fake Dump"
                assert float(mapping["confidence"]) == 0.85
                assert float(mapping["price"]) == current_price
                matched = True
                break
        assert matched, "Should store trap data in Redis for Grafana"
        
        print(f"  • {CYAN}Fake Dump detection verified!{RESET}")
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_half_fake_pump_detection(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                    mock_insert_subtle, mock_register_trap, mock_send_alert,
                                    mock_sleep):
        """🌿 Test divine detection of half-fake pump manipulation."""
        print(f"\n{GREEN}Testing HALF-FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase between 1% and PRICE_PUMP_THRESHOLD (2%)
        current_price = 30000.0
        prev_price = 29700.0  # 1.01% increase but only $300 absolute change
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Mixed Pattern (Medium Confidence)"
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"1000"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for half fake pump
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Half-Fake Pump", "Should detect as Half-Fake Pump"
        assert trap_call[3] == 0.5, "Half-Fake Pump should have 0.5 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Half-Fake Pump", 0.5, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        # Verify data was stored in Redis for Grafana
        mock_redis.hset.assert_called()
        calls = mock_redis.hset.call_args_list
        matched = False
        for call_obj in calls:
            key = call_obj[0][0]
            if "mm_trap:" in key:
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Half-Fake Pump"
                assert float(mapping["confidence"]) == 0.5
                assert float(mapping["price"]) == current_price
                matched = True
                break
        assert matched, "Should store trap data in Redis for Grafana"
        
        print(f"  • {CYAN}Half-Fake Pump detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('time.sleep')
    def test_organic_movement_no_trap(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                   mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                   mock_redis, setup_price_environment):
        """🌿 Test divine recognition of organic price movement with no trap."""
        print(f"\n{GREEN}Testing ORGANIC MOVEMENT recognition...{RESET}")
        
        # Setup test data - small price change, organic movement
        current_price = 60000.0
        prev_price = 59900.0  # Small 0.17% increase
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0  # Way above our change
        mock_omega_algo.is_fibo_organic.return_value = "Organic Movement (High Confidence)"
        
        setup_price_environment(current_price, prev_price)
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify no trap was detected
        mock_insert_trap.assert_not_called()
        
        # Verify high-frequency detector was not notified
        mock_register_trap.assert_not_called()
        
        # Verify no alert was sent
        mock_send_alert.assert_not_called()
        
        # Verify subtle movement was recorded
        mock_insert_subtle.assert_called()
        
        # Verify organic data was stored in Redis
        organic_stored = False
        for call_obj in mock_redis.hset.call_args_list:
            key = call_obj[0][0]
            if "organic_move:" in key:
                organic_stored = True
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Organic"
                assert mapping["confidence"] == "0.8"  # High confidence
                break
                
        assert organic_stored, "Should store organic movement data in Redis"
        
        print(f"  • {CYAN}Organic movement correctly identified (no false positives)!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('time.sleep')

    def test_fibonacci_metrics_storage(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                    mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                    mock_redis, setup_price_environment):
        """🌿 Test divine storage of Fibonacci metrics for analytics."""
        print(f"\n{GREEN}Testing FIBONACCI METRICS storage...{RESET}")
        
        # Setup test data
        current_price = 60000.0
        prev_price = 59900.0
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0
        mock_omega_algo.is_fibo_organic.return_value = "Organic Movement (High Confidence)"
        
        setup_price_environment(current_price, prev_price)
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify Fibonacci metrics were stored in Redis
        # Check fib_match_history list append
        mock_redis.rpush.assert_any_call("fib_match_history", 1)  # 1 = Organic
        
        # Check dynamic threshold history
        mock_redis.rpush.assert_any_call("price_volatility_history", 1000.0)
        
        # Check latest movement analysis
        mock_redis.set.assert_any_call("latest_movement_analysis", "Organic Movement (High Confidence)")
        
        print(f"  • {CYAN}Fibonacci metrics storage verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('time.sleep')
    def test_initial_price_handling(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                 mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                 mock_redis, setup_price_environment):
        """🌿 Test divine handling of initial price with no previous price."""
        print(f"\n{GREEN}Testing INITIAL PRICE handling...{RESET}")
        
        # Setup test data - only current price, no previous price
        current_price = 60000.0
        
        # Mock Redis to return empty list for price history
        mock_redis.lrange.return_value = []
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0
        mock_omega_algo.is_fibo_organic.return_value = "Organic Movement (Medium Confidence)"
        
        setup_price_environment(current_price, mock_redis=mock_redis)  # No prev_price
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify the code handles missing previous price gracefully
        # by creating a slightly different initial price
        
        # Verify subtle movement was recorded with a valid previous price
        mock_insert_subtle.assert_called()

        # Get keyword arguments from the call
        args, kwargs = mock_insert_subtle.call_args

        # Verify prev_price is present and properly set
        assert 'prev_price' in kwargs, "prev_price should be in the arguments"
        assert kwargs['prev_price'] is not None, "Should create a valid previous price"
        assert kwargs['prev_price'] != current_price, "Previous price should differ from current"

        # Optional: Verify price equals current_price
        assert kwargs['price'] == current_price, "Current price should be passed correctly"
        
        # Verify we update Redis with the current price for next time
        mock_redis.set.assert_any_call("prev_btc_price", current_price)
        
        print(f"  • {CYAN}Initial price handling verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('time.sleep')
    def test_potential_fake_pump(self, mock_sleep, mock_send_alert, mock_register_trap, 
                              mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                              mock_redis, setup_price_environment):
        """🌿 Test divine detection of potential fake pump with organic pattern."""
        print(f"\n{GREEN}Testing POTENTIAL FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase above PRICE_PUMP_THRESHOLD (0.02 = 2%)
        current_price = 30000.0
        prev_price = 29400.0  # 2.04% increase but only $600 absolute change
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        setup_price_environment(current_price, prev_price)
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify no trap was detected
        mock_insert_trap.assert_not_called()
        
        # Verify high-frequency detector was not notified
        mock_register_trap.assert_not_called()
        
        # Verify no alert was sent
        mock_send_alert.assert_not_called()
        
        # Verify subtle movement was recorded
        mock_insert_subtle.assert_called()
        
        # Verify organic data was stored in Redis
        organic_stored = False
        for call_obj in mock_redis.hset.call_args_list:
            key = call_obj[0][0]
            if "organic_move:" in key:
                organic_stored = True
                mapping = call_obj[1]["mapping"]
                assert mapping["type"] == "Organic"
                assert mapping["confidence"] == "0.8"  # High confidence
                break
                
        assert organic_stored, "Should store organic movement data in Redis"
        
        print(f"  • {CYAN}Organic movement correctly identified (no false positives)!{RESET}")
    
    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_stealth_accumulation_pattern(self, mock_redis, mock_omega_algo, mock_insert_trap,
                                      mock_insert_subtle, mock_register_trap, mock_send_alert,
                                      mock_sleep):
        """🕵️ Test detection of stealth accumulation patterns by whales."""
        print(f"\n{CYAN}Testing ST34LTH 4CCUMUL4T10N detection...{RESET}")
        
        # Setup test data - subtle price changes with increasing volume
        current_price = 50000.0
        prev_price = 49950.0  # Small price change
        
        # Configure mocks for stealth pattern
        mock_omega_algo.calculate_dynamic_threshold.return_value = 100.0
        mock_omega_algo.is_fibo_organic.return_value = "Potential Stealth Pattern"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            "1min": "neutral",
            "5min": "neutral",
            "15min": "bullish",
            "1h": "bullish"
        }
        
        # Configure Redis mock with increasing volume pattern
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"5000"  # Higher than usual volume
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        _run_detector_once(mock_sleep)
        
        # Verify subtle movement was detected
        mock_insert_subtle.assert_called_once()
        movement_call = mock_insert_subtle.call_args[0]
        
        # Verify pattern characteristics
        assert movement_call[0] == current_price, "Should record current price"
        assert movement_call[2] == "Stealth Accumulation", "Should detect stealth pattern"
        assert movement_call[3] >= 0.7, "Should have high confidence due to volume"

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_fractal_trap_pattern(self, mock_redis, mock_omega_algo, mock_insert_trap,
                               mock_insert_subtle, mock_register_trap, mock_send_alert,
                               mock_sleep):
        """🌀 Test detection of fractal trap patterns (self-similar price movements)."""
        print(f"\n{MAGENTA}Testing FR4CT4L TR4P P4TT3RN detection...{RESET}")
        
        # Setup test data - fractal pattern (similar movements at different scales)
        current_price = 55000.0
        prev_price = 54500.0
        
        # Configure mocks for fractal analysis
        mock_omega_algo.calculate_dynamic_threshold.return_value = 400.0
        mock_omega_algo.is_fibo_organic.return_value = "Fractal Pattern Detected"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            "1min": "bullish",
            "5min": "bullish",
            "15min": "bullish",
            "1h": "neutral"
        }
        
        # Configure Redis mock with fractal pattern data
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"2500"
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Verify fractal characteristics
        assert trap_call[0] == current_price, "Should record current price"
        assert trap_call[2] == "Fractal Trap", "Should detect fractal pattern"
        assert trap_call[3] >= 0.85, "Should have high confidence for fractal pattern"

    @patch('time.sleep')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.send_alert')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_detector.redis_conn')
    def test_time_dilation_trap(self, mock_redis, mock_omega_algo, mock_insert_trap,
                             mock_insert_subtle, mock_register_trap, mock_send_alert,
                             mock_sleep):
        """⌛ Test detection of time-based manipulation (weekend/off-hours traps)."""
        print(f"\n{YELLOW}Testing T1M3 D1L4T10N TR4P detection...{RESET}")
        
        # Setup test data - weekend movement
        current_price = 52000.0
        prev_price = 51500.0
        
        # Configure mocks for time-based analysis
        mock_omega_algo.calculate_dynamic_threshold.return_value = 300.0
        mock_omega_algo.is_fibo_organic.return_value = "Time-Based Pattern"
        mock_omega_algo.analyze_multi_timeframe_trends.return_value = {
            "1min": "bearish",
            "5min": "neutral",
            "15min": "bullish",
            "1h": "neutral"
        }
        
        # Configure Redis mock with weekend data
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "last_btc_volume":
                return b"800"  # Lower weekend volume
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Simulate weekend timestamp
        current_time = datetime.datetime.now()
        if current_time.weekday() < 5:  # If not weekend
            current_time = current_time + datetime.timedelta(days=(6 - current_time.weekday()))
        
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = current_time
            
            # Run detector
            _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Verify time-based characteristics
        assert trap_call[0] == current_price, "Should record current price"
        assert trap_call[2] == "Time Dilation Trap", "Should detect time-based pattern"
        assert trap_call[3] >= 0.75, "Should have good confidence for time pattern"

class TestHighFrequencyTrapDetector:
    """🌿 Divine tests for High Frequency Trap Detector."""
    
    @pytest.fixture
    def hf_detector(self):
        """Create a fresh HF detector instance for each test."""
        return HighFrequencyTrapDetector()
    
    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_schumann_resonance_spike_detection(self, mock_redis, hf_detector):
        """🌌 Test detection of Schumann resonance spikes during price movements."""
        print(f"\n{MAGENTA}Testing SCHUM4NN R3S0N4NC3 SP1K3 detection...{RESET}")
        
        # Setup test data - high Schumann resonance with price movement
        schumann_value = SCHUMANN_THRESHOLD + 5.0  # Above threshold
        current_price = 50000.0
        prev_price = 49900.0  # 0.2% change
        
        # Configure Redis mock
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "schumann_resonance":
                return str(schumann_value).encode()
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        hf_mode_active = hf_detector.detect_high_freq_trap_mode(
            latest_price=current_price,
            schumann_resonance=schumann_value
        )
        
        # Verify HF mode was activated
        assert hf_mode_active, "HF mode should activate with Schumann spike"
        
        print(f"  • {CYAN}Schumann resonance spike detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_volatility_acceleration_detection(self, mock_redis, hf_detector):
        """⚡ Test detection of volatility acceleration patterns."""
        print(f"\n{YELLOW}Testing V0L4T1L1TY 4CC3L3R4T10N detection...{RESET}")
        
        # Setup test data - high short-term volatility
        current_price = 55000.0
        prev_price = 54000.0
        
        # Configure Redis mock with volatility data
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "volatility_1min":
                return b"2.5"  # High 1-min volatility
            elif key == "volatility_5min":
                return b"1.0"  # Lower 5-min volatility
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        hf_mode_active = hf_detector.detect_high_freq_trap_mode(latest_price=current_price)
        
        # Verify HF mode was activated
        assert hf_mode_active, "HF mode should activate with volatility acceleration"
        
        print(f"  • {CYAN}Volatility acceleration detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_back_to_back_trap_detection(self, mock_redis, hf_detector):
        """🔄 Test detection of back-to-back trap patterns."""
        print(f"\n{BLUE}Testing B4CK-2-B4CK TR4P detection...{RESET}")
        
        # Setup test data - multiple recent traps
        current_time = datetime.datetime.now(datetime.UTC)
        
        # Register multiple traps within the window
        for i in range(MIN_TRAPS_FOR_HF_MODE + 1):
            trap_time = current_time - datetime.timedelta(seconds=i*10)
            hf_detector.register_trap_event(
                "Test Trap",
                0.9,
                0.02,
                from_detector=False,
                timestamp=trap_time
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
        hf_mode_active = hf_detector.detect_high_freq_trap_mode()
        
        # Verify HF mode was activated
        assert hf_mode_active, "HF mode should activate with multiple recent traps"
        
        print(f"  • {CYAN}Back-to-back trap detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_direct_liquidity_grab_detection(self, mock_redis, hf_detector):
        """💧 Test detection of direct liquidity grabs."""
        print(f"\n{RED}Testing D1R3CT L1QU1D1TY GR4B detection...{RESET}")
        
        # Setup test data - high volatility and acceleration
        current_price = 60000.0
        prev_price = 58800.0  # 2% change
        
        # Configure Redis mock with volatility data
        def get_side_effect(key):
            if key == "last_btc_price":
                return str(current_price).encode()
            elif key == "prev_btc_price":
                return str(prev_price).encode()
            elif key == "volatility_1min":
                return b"0.5"  # High volatility
            elif key == "volatility_acceleration":
                return b"0.3"  # High acceleration
            return None
        mock_redis.get.side_effect = get_side_effect
        
        # Run detector
        hf_mode_active = hf_detector.detect_high_freq_trap_mode(latest_price=current_price)
        
        # Verify HF mode was activated
        assert hf_mode_active, "HF mode should activate with direct liquidity grab"
        
        # Verify grab was detected with high confidence
        grab_type, confidence = hf_detector.detect_liquidity_grabs(current_price)
        assert grab_type == "Volatility Liquidity Grab"
        assert confidence > 0.7
        
        print(f"  • {CYAN}Direct liquidity grab detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn')
    def test_simulation_mode_handling(self, mock_redis, hf_detector):
        """🎮 Test handling of simulation mode data."""
        print(f"\n{MAGENTA}Testing S1MUL4T10N M0D3 handling...{RESET}")
    
        # Setup test data for simulation
        sim_price = 45000.0
        sim_prev_price = 44100.0
        
        # Configure mock Redis with simulation data
        mock_data = {
            "sim_last_btc_price": str(sim_price).encode(),
            "sim_prev_btc_price": str(sim_prev_price).encode(),
            "sim_volatility_1min": b"0.4",
            "volatility_1min": b"0.3",
            "volatility_5min": b"0.2",
            "schumann_resonance": b"7.83"
        }
        
        def get_side_effect(key):
            return mock_data.get(key)
            
        mock_redis.get.side_effect = get_side_effect
        
        # Initialize price history for the detector
        hf_detector.price_history_1min.append((datetime.datetime.now(datetime.UTC), sim_prev_price))
        hf_detector.price_history_1min.append((datetime.datetime.now(datetime.UTC), sim_price))
        hf_detector.price_history_5min.append((datetime.datetime.now(datetime.UTC), sim_prev_price))
        hf_detector.price_history_5min.append((datetime.datetime.now(datetime.UTC), sim_price))
    
        # Run detector in simulation mode
        hf_mode_active, multiplier = hf_detector.detect_high_freq_trap_mode(
            latest_price=sim_price,
            simulation_mode=True
        )
    
        # Verify simulation data was used
        mock_redis.get.assert_any_call("sim_last_btc_price")
        mock_redis.get.assert_any_call("sim_volatility_1min")
        
        # Verify the detector used simulation mode data
        assert not hf_mode_active, "Should not activate HF mode with normal simulation data"
        assert multiplier == 1.0, "Should return default multiplier"
        
        print(f"{GREEN}✓ S1MUL4T10N M0D3 handling verified!{RESET}")