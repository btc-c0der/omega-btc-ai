#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Live Feed v3 Tests
=====================================

Unit and integration tests for the BTC Live Feed v3 with enhanced Redis failover.
Tests the following functionality:
- Redis failover mechanisms
- Error handling and recovery
- Health monitoring
- Performance metrics

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.
"""

import os
import json
import time
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone

# Import modules to test
from omega_ai.data_feed.btc_live_feed_v3 import (
    BtcLiveFeedV3, 
    price_movement_indicator,
    check_required_packages,
    log_rasta,
    MockHighFrequencyTrapDetector
)
from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager

# Test Constants
TEST_PRICE = 45678.90
TEST_VOLUME = 1.2345
TEST_SAMPLE_MESSAGE = json.dumps({
    "e": "trade",
    "E": 1609459200000,
    "s": "BTCUSDT",
    "t": 123456789,
    "p": str(TEST_PRICE),
    "q": str(TEST_VOLUME),
    "b": 123456,
    "a": 123457,
    "T": 1609459200000,
    "m": True,
    "M": True
}).encode('utf-8')

# =====================================
# Fixtures
# =====================================

@pytest.fixture
def mock_redis_client():
    """Create a mock Redis client for testing."""
    redis_client = AsyncMock()
    redis_client.ping.return_value = True
    redis_client.get.return_value = "45678.90"
    redis_client.set.return_value = True
    redis_client.lpush.return_value = 10
    redis_client.ltrim.return_value = True
    redis_client.publish.return_value = 1
    redis_client.scan.return_value = (0, ["last_btc_price", "last_btc_update_time", "btc_movement_history"])
    return redis_client

@pytest.fixture
def mock_redis_manager(mock_redis_client):
    """Create a mock Redis manager for testing."""
    with patch('omega_ai.data_feed.btc_live_feed_v3.EnhancedRedisManager', autospec=True) as mock_manager:
        instance = mock_manager.return_value
        instance.primary_redis = mock_redis_client
        instance.failover_redis = mock_redis_client
        instance.current_redis = mock_redis_client
        instance.primary_connected = True
        instance.failover_connected = True
        instance.using_failover = False
        instance.use_failover = True
        
        # Mock methods
        instance.ping.return_value = True
        instance.get_cached.return_value = "45678.90"
        instance.set_cached.return_value = True
        instance.publish.return_value = 1
        instance.lpush.return_value = 10
        instance.ltrim.return_value = True
        instance.get_stats.return_value = {
            "primary_available": True,
            "failover_available": True,
            "using_failover": False,
            "reconnection_attempts": 0
        }
        instance.try_reconnect_primary.return_value = True
        
        yield instance

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket for testing."""
    websocket = AsyncMock()
    return websocket

@pytest.fixture
async def btc_feed(mock_redis_manager):
    """Create a test instance of BtcLiveFeedV3."""
    feed = BtcLiveFeedV3()
    feed.redis_manager = mock_redis_manager
    feed.is_running = True
    feed.websocket_connected = True
    feed.last_price = TEST_PRICE
    
    # Return the feed instance
    yield feed
    
    # Cleanup
    feed.is_running = False

# =====================================
# Tests for Utility Functions
# =====================================

def test_price_movement_indicator():
    """Test price movement indicator function."""
    assert price_movement_indicator(100.0, 150.0) == "📈"  # Price increased
    assert price_movement_indicator(150.0, 100.0) == "📉"  # Price decreased
    assert price_movement_indicator(100.0, 100.0) == "🔄"  # Price unchanged

@pytest.mark.asyncio
async def test_log_rasta():
    """Test log_rasta function."""
    with patch('omega_ai.data_feed.btc_live_feed_v3.logger') as mock_logger:
        await log_rasta("Test message")
        mock_logger.info.assert_called_once_with("🔱 OMEGA BTC AI - Test message")

def test_check_required_packages():
    """Test check_required_packages function."""
    # Test with all packages available
    with patch('omega_ai.data_feed.btc_live_feed_v3.__import__', return_value=True):
        assert check_required_packages() is True
    
    # Test with missing package
    def mock_import(name):
        if name == "websockets":
            raise ImportError("Package not found")
        return True
    
    with patch('omega_ai.data_feed.btc_live_feed_v3.__import__', side_effect=mock_import):
        with patch('omega_ai.data_feed.btc_live_feed_v3.logger') as mock_logger:
            assert check_required_packages() is False
            mock_logger.error.assert_called_once()

# =====================================
# Tests for MockHighFrequencyTrapDetector
# =====================================

def test_mock_trap_detector():
    """Test the mock trap detector."""
    detector = MockHighFrequencyTrapDetector()
    now = datetime.now(timezone.utc)
    
    # Test initial state
    assert len(detector.prices) == 0
    
    # Test update_price_data
    detector.update_price_data(TEST_PRICE, now)
    assert len(detector.prices) == 1
    assert detector.prices[0][0] == TEST_PRICE
    assert detector.prices[0][1] == now
    
    # Test limit of 100 entries
    for i in range(110):
        detector.update_price_data(TEST_PRICE + i, now)
    assert len(detector.prices) == 100
    
    # Test detect_trap
    trap_result = detector.detect_trap()
    assert trap_result["trapDetected"] is False
    assert trap_result["confidence"] == 0.0
    assert trap_result["trapType"] == "NONE"

# =====================================
# Tests for BtcLiveFeedV3
# =====================================

@pytest.mark.asyncio
async def test_feed_initialization():
    """Test BtcLiveFeedV3 initialization."""
    with patch('omega_ai.data_feed.btc_live_feed_v3.EnhancedRedisManager') as mock_redis_manager:
        # Test with default parameters
        feed = BtcLiveFeedV3()
        assert feed.is_running is False
        assert feed.websocket_connected is False
        assert feed.last_price == 0.0
        
        # Verify EnhancedRedisManager was initialized with correct params
        mock_redis_manager.assert_called_once()
        args, kwargs = mock_redis_manager.call_args
        assert kwargs["use_failover"] is True
        assert kwargs["sync_on_reconnect"] is True
        assert kwargs["retry_interval"] == 60
        assert "last_btc_price" in kwargs["priority_keys"]
        
        # Test with custom parameters
        feed = BtcLiveFeedV3(use_failover=False, sync_on_reconnect=False)
        args, kwargs = mock_redis_manager.call_args_list[1]
        assert kwargs["use_failover"] is False
        assert kwargs["sync_on_reconnect"] is False

@pytest.mark.asyncio
async def test_handle_message(btc_feed):
    """Test message handling with automatic failover."""
    # Mock successful Redis operations
    await btc_feed._handle_message(TEST_SAMPLE_MESSAGE)
    
    # Verify Redis operations were called
    assert btc_feed.redis_manager.set_cached.call_count >= 2
    assert btc_feed.redis_manager.lpush.call_count >= 1
    assert btc_feed.redis_manager.ltrim.call_count >= 1
    assert btc_feed.redis_manager.publish.call_count >= 1
    
    # Verify metrics were updated
    assert btc_feed.performance_metrics["total_messages_processed"] == 1
    assert btc_feed.performance_metrics["successful_redis_operations"] > 0
    assert btc_feed.last_price == TEST_PRICE

@pytest.mark.asyncio
async def test_handle_message_with_redis_error(btc_feed):
    """Test message handling with Redis errors."""
    # Configure Redis operations to fail
    btc_feed.redis_manager.set_cached.side_effect = Exception("Redis connection error")
    
    # Handle message should not raise exception
    await btc_feed._handle_message(TEST_SAMPLE_MESSAGE)
    
    # Verify metrics were updated correctly
    assert btc_feed.performance_metrics["failed_redis_operations"] > 0
    assert btc_feed.performance_metrics["total_messages_processed"] == 1

@pytest.mark.asyncio
async def test_redis_reconnect_task(btc_feed):
    """Test the Redis reconnection task."""
    # Mock Redis manager methods
    btc_feed.redis_manager.try_reconnect_primary.return_value = True
    
    # Create a task that runs for a short time
    async def mock_run_reconnect():
        btc_feed.last_redis_reconnect_attempt = 0
        await btc_feed._run_redis_reconnect_task()
    
    # Run the task for a short period then cancel
    task = asyncio.create_task(mock_run_reconnect())
    await asyncio.sleep(0.1)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    # Verify the reconnect method was called
    btc_feed.redis_manager.try_reconnect_primary.assert_called()

@pytest.mark.asyncio
async def test_check_health(btc_feed):
    """Test the health check function."""
    health_data = await btc_feed.check_health()
    
    # Verify health data contains expected fields
    assert "redis_connected" in health_data
    assert "websocket_connected" in health_data
    assert "last_price" in health_data
    assert "uptime" in health_data
    assert "messages_processed" in health_data
    assert "redis_stats" in health_data
    assert "status" in health_data
    
    # Verify status is healthy when everything is connected
    assert health_data["status"] == "healthy"
    
    # Test degraded status
    btc_feed.websocket_connected = False
    health_data = await btc_feed.check_health()
    assert health_data["status"] == "degraded"
    
    # Test unhealthy status
    btc_feed.redis_manager.ping.return_value = False
    health_data = await btc_feed.check_health()
    assert health_data["status"] == "unhealthy"

# =====================================
# Tests for Redis Failover
# =====================================

@pytest.mark.asyncio
async def test_redis_failover_scenario():
    """
    Test a complete Redis failover scenario.
    
    This test simulates:
    1. Primary Redis connection failing
    2. Automatic failover to local Redis
    3. Reconnection to primary Redis
    4. Synchronization of data
    """
    # Create mock Redis clients
    primary_redis = AsyncMock()
    failover_redis = AsyncMock()
    
    # Configure primary Redis to fail on first ping but succeed later
    primary_ping_responses = [False, False, True]
    primary_redis.ping = AsyncMock(side_effect=primary_ping_responses)
    
    # Configure failover Redis to always succeed
    failover_redis.ping.return_value = True
    
    # Create a patched EnhancedRedisManager
    with patch('omega_ai.utils.enhanced_redis_manager.redis.Redis') as mock_redis_class:
        # Configure Redis.Redis to return our mock clients
        mock_redis_class.side_effect = [primary_redis, failover_redis]
        
        # Create the Redis manager
        redis_manager = EnhancedRedisManager(
            use_failover=True,
            sync_on_reconnect=True
        )
        
        # Patch internal methods to avoid actual Redis operations
        redis_manager._sync_data_to_primary = AsyncMock()
        redis_manager._sync_key = AsyncMock()
        
        # Step 1: Connect to Redis - should connect to both primary and failover
        await redis_manager.connect()
        
        # Verify both Redis clients were created
        assert redis_manager.primary_redis is primary_redis
        assert redis_manager.failover_redis is failover_redis
        
        # Verify we're using primary Redis initially
        assert redis_manager.current_redis is primary_redis
        assert redis_manager.using_failover is False
        
        # Step 2: Simulate primary Redis failure
        result = await redis_manager.ping()
        
        # Verify failover occurred
        assert result is True  # Ping should succeed due to failover
        assert redis_manager.using_failover is True
        assert redis_manager.current_redis is failover_redis
        
        # Step 3: Reconnect to primary Redis
        # First attempt should fail
        result = await redis_manager.try_reconnect_primary()
        assert result is False
        assert redis_manager.using_failover is True
        
        # Second attempt should succeed
        result = await redis_manager.try_reconnect_primary()
        assert result is True
        assert redis_manager.using_failover is False
        assert redis_manager.current_redis is primary_redis
        
        # Verify data sync was called
        redis_manager._sync_data_to_primary.assert_called_once()

@pytest.mark.asyncio
async def test_redis_operations_with_failover(mock_redis_manager, btc_feed):
    """Test that Redis operations handle failover correctly."""
    # Configure Redis operations to fail on first attempt but succeed on failover
    def mock_ping_side_effect():
        # Switch to failover Redis
        if mock_redis_manager.using_failover:
            return True
        mock_redis_manager.using_failover = True
        mock_redis_manager.current_redis = mock_redis_manager.failover_redis
        return True
    
    mock_redis_manager.ping.side_effect = mock_ping_side_effect
    
    # Test message handling with Redis failover
    await btc_feed._handle_message(TEST_SAMPLE_MESSAGE)
    
    # Verify failover occurred
    assert mock_redis_manager.using_failover is True
    
    # Verify message was still processed
    assert btc_feed.performance_metrics["total_messages_processed"] == 1
    assert btc_feed.performance_metrics["successful_redis_operations"] > 0

# =====================================
# Integration Tests
# =====================================

@pytest.mark.asyncio
async def test_websocket_reconnection(btc_feed, mock_websocket):
    """Test WebSocket reconnection with exponential backoff."""
    # Configure websocket.connect to fail and then succeed
    connect_results = [
        Exception("Connection failed"),  # First attempt fails
        mock_websocket  # Second attempt succeeds
    ]
    
    with patch('omega_ai.data_feed.btc_live_feed_v3.websockets.connect') as mock_connect:
        mock_connect.side_effect = connect_results
        
        # Create a task that runs for a short time
        async def mock_run_price_feed():
            await btc_feed._run_price_feed()
        
        # Run the task for a short period then cancel
        task = asyncio.create_task(mock_run_price_feed())
        await asyncio.sleep(0.1)
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        # Verify reconnection attempts
        assert btc_feed.connection_attempts > 0
        assert btc_feed.performance_metrics["websocket_reconnections"] > 0

# Main test runner
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 