"""
DIVINE MM TRAP PROCESSOR TESTS 🌿🔥

These sacred tests verify that the Market Maker Trap Processor properly detects
Babylon system manipulation tactics and protects traders with divine insight.

JAH BLESS THE TRUTHFUL MARKET VISION! 🙏
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
from omega_ai.mm_trap_detector.mm_trap_processor import (
    process_mm_trap,  # Main function to test
    print_header, print_section, print_price_update, print_analysis_result,
    print_movement_tag, print_alert
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
    def test_liquidity_grab_detection(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                    mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                    mock_redis, setup_price_environment):
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
        
        setup_price_environment(current_price, prev_price)
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for liquidity grab
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Liquidity Grab", "Should detect as Liquidity Grab"
        assert trap_call[3] == 0.9, "Liquidity Grab should have 0.9 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Liquidity Grab", 0.9, price_change_pct)
        
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
                assert mapping["type"] == "Liquidity Grab"
                assert float(mapping["confidence"]) == 0.9
                assert float(mapping["price"]) == current_price
                matched = True
                break
        assert matched, "Should store trap data in Redis for Grafana"
        
        print(f"  • {CYAN}Full Liquidity Grab detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('time.sleep')
    def test_half_liquidity_grab_detection(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                         mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                         mock_redis, setup_price_environment):
        """🌿 Test divine detection of half liquidity grab manipulation."""
        print(f"\n{GREEN}Testing HALF-LIQUIDITY GRAB detection...{RESET}")
        
        # Setup test data - medium price change to trigger half liquidity grab detection
        current_price = 100000.0
        prev_price = 99500.0  # $600 change, between half and full threshold
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 1000.0  # Full threshold
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        setup_price_environment(current_price, prev_price)
        
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
        
        print(f"  • {CYAN}Half-Liquidity Grab detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('time.sleep')
    def test_fake_pump_detection(self, mock_sleep, mock_send_alert, mock_register_trap, 
                              mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                              mock_redis, setup_price_environment):
        """🌿 Test divine detection of fake pump manipulation."""
        print(f"\n{GREEN}Testing FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase above PRICE_PUMP_THRESHOLD (0.02 = 2%)
        current_price = 60000.0
        prev_price = 58800.0  # 2.04% increase
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        setup_price_environment(current_price, prev_price)
        
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
        
        print(f"  • {CYAN}Fake Pump detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('time.sleep')
    def test_fake_dump_detection(self, mock_sleep, mock_send_alert, mock_register_trap, 
                             mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                             mock_redis, setup_price_environment):
        """🌿 Test divine detection of fake dump manipulation."""
        print(f"\n{GREEN}Testing FAKE DUMP detection...{RESET}")
        
        # Setup test data - price decrease below PRICE_DROP_THRESHOLD (-0.02 = -2%)
        current_price = 58800.0
        prev_price = 60000.0  # -2% decrease
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Potential Manipulation Pattern"
        
        setup_price_environment(current_price, prev_price)
        
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
        
        print(f"  • {CYAN}Fake Dump detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('time.sleep')
    def test_half_fake_pump_detection(self, mock_sleep, mock_send_alert, mock_register_trap, 
                                  mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                                  mock_redis, setup_price_environment):
        """🌿 Test divine detection of half-fake pump manipulation."""
        print(f"\n{GREEN}Testing HALF-FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase between 1% and PRICE_PUMP_THRESHOLD (2%)
        current_price = 60000.0
        prev_price = 59400.0  # 1.01% increase
        price_change_pct = (current_price - prev_price) / prev_price
        abs_change = abs(current_price - prev_price)
        
        # Configure mocks
        mock_omega_algo.calculate_dynamic_threshold.return_value = 2000.0  # Above our change
        mock_omega_algo.is_fibo_organic.return_value = "Mixed Pattern (Medium Confidence)"
        
        setup_price_environment(current_price, prev_price)
        
        # Run one loop of the trap detector
        _run_detector_once(mock_sleep)
        
        # Verify trap was detected
        mock_insert_trap.assert_called_once()
        trap_call = mock_insert_trap.call_args[0]
        
        # Divine assertions for half-fake pump
        assert trap_call[0] == current_price, "Trap should record current price"
        assert trap_call[1] == price_change_pct, "Trap should record correct price change percentage"
        assert trap_call[2] == "Half-Fake Pump", "Should detect as Half-Fake Pump"
        assert trap_call[3] == 0.5, "Half-Fake Pump should have 0.5 confidence"
        
        # Verify high-frequency detector was notified
        mock_register_trap.assert_called_once_with("Half-Fake Pump", 0.5, price_change_pct)
        
        # Verify alert was sent
        mock_send_alert.assert_called_once()
        
        print(f"  • {CYAN}Half-Fake Pump detection verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
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
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
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
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
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
    
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.redis_conn')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.OmegaAlgo')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_mm_trap')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.insert_subtle_movement')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.register_trap_detection')
    @patch('omega_ai.mm_trap_detector.mm_trap_processor.send_alert')
    @patch('time.sleep')
    def test_potential_fake_pump(self, mock_sleep, mock_send_alert, mock_register_trap, 
                              mock_insert_subtle, mock_insert_trap, mock_omega_algo, 
                              mock_redis, setup_price_environment):
        """🌿 Test divine detection of potential fake pump with organic pattern."""
        print(f"\n{GREEN}Testing POTENTIAL FAKE PUMP detection...{RESET}")
        
        # Setup test data - price increase above PRICE_PUMP_THRESHOLD (0.02 = 2