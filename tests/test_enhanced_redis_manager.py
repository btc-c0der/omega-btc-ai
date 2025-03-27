#!/usr/bin/env python3
"""
OMEGA BTC AI - Enhanced Redis Manager Tests
===========================================

Unit and integration tests for the Enhanced Redis Manager with failover capabilities.
Tests the following functionality:
- Connection management for primary and failover Redis
- Automatic failover when primary Redis fails
- Data synchronization between Redis instances
- Error handling during Redis operations

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
"""

import os
import time
import json
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock, call

# Import module to test
from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager, DEFAULT_BATCH_SIZE

# Test constants
TEST_PRIMARY_HOST = "test.redis.host"
TEST_PRIMARY_PORT = 6379
TEST_FAILOVER_HOST = "localhost"
TEST_FAILOVER_PORT = 6380
TEST_KEY = "test_key"
TEST_VALUE = "test_value"
TEST_PRIORITY_KEYS = ["key1", "key2", "key3"]

# =====================================
# Fixtures
# =====================================

@pytest.fixture
def mock_redis_module():
    """Create a mock for the entire redis.asyncio module."""
    with patch('omega_ai.utils.enhanced_redis_manager.redis', autospec=True) as mock_redis:
        yield mock_redis

@pytest.fixture
def mock_primary_redis():
    """Create a mock for primary Redis client."""
    client = AsyncMock()
    client.ping.return_value = True
    client.get.return_value = TEST_VALUE
    client.set.return_value = True
    client.lpush.return_value = 10
    client.ltrim.return_value = True
    client.publish.return_value = 1
    client.exists.return_value = True
    client.type.return_value = "string"
    client.scan.return_value = (0, TEST_PRIORITY_KEYS)
    return client

@pytest.fixture
def mock_failover_redis():
    """Create a mock for failover Redis client."""
    client = AsyncMock()
    client.ping.return_value = True
    client.get.return_value = TEST_VALUE
    client.set.return_value = True
    client.lpush.return_value = 10
    client.ltrim.return_value = True
    client.publish.return_value = 1
    client.exists.return_value = True
    client.type.return_value = "string"
    client.scan.return_value = (0, TEST_PRIORITY_KEYS)
    return client

@pytest.fixture
async def redis_manager(mock_redis_module, mock_primary_redis, mock_failover_redis):
    """Create a test instance of EnhancedRedisManager with mocked Redis clients."""
    # Configure environment variables
    os.environ["REDIS_HOST"] = TEST_PRIMARY_HOST
    os.environ["REDIS_PORT"] = str(TEST_PRIMARY_PORT)
    os.environ["FAILOVER_REDIS_HOST"] = TEST_FAILOVER_HOST
    os.environ["FAILOVER_REDIS_PORT"] = str(TEST_FAILOVER_PORT)
    
    # Mock Redis class to return our mock clients
    mock_redis_module.Redis.side_effect = [mock_primary_redis, mock_failover_redis]
    
    # Create the Redis manager
    manager = EnhancedRedisManager(
        use_failover=True,
        sync_on_reconnect=True,
        priority_keys=TEST_PRIORITY_KEYS
    )
    
    # Initialize connections
    await manager.connect()
    
    # Verify Redis clients are set correctly
    assert manager.primary_redis is mock_primary_redis
    assert manager.failover_redis is mock_failover_redis
    
    yield manager
    
    # Clean up
    await manager.close()
    
    # Reset environment variables
    del os.environ["REDIS_HOST"]
    del os.environ["REDIS_PORT"]
    del os.environ["FAILOVER_REDIS_HOST"]
    del os.environ["FAILOVER_REDIS_PORT"]

# =====================================
# Connection Tests
# =====================================

@pytest.mark.asyncio
async def test_connect_both_successful(redis_manager):
    """Test successful connection to both primary and failover Redis."""
    # Already connected in fixture, verify state
    assert redis_manager.primary_connected is True
    assert redis_manager.failover_connected is True
    assert redis_manager.current_redis is redis_manager.primary_redis
    assert redis_manager.using_failover is False

@pytest.mark.asyncio
async def test_connect_primary_failure():
    """Test connection when primary Redis fails."""
    with patch('omega_ai.utils.enhanced_redis_manager.redis', autospec=True) as mock_redis:
        # Configure primary Redis to fail
        primary_redis = AsyncMock()
        primary_redis.ping.return_value = False
        
        # Configure failover Redis to succeed
        failover_redis = AsyncMock()
        failover_redis.ping.return_value = True
        
        mock_redis.Redis.side_effect = [primary_redis, failover_redis]
        
        # Set environment variables
        os.environ["REDIS_HOST"] = TEST_PRIMARY_HOST
        os.environ["REDIS_PORT"] = str(TEST_PRIMARY_PORT)
        os.environ["FAILOVER_REDIS_HOST"] = TEST_FAILOVER_HOST
        os.environ["FAILOVER_REDIS_PORT"] = str(TEST_FAILOVER_PORT)
        
        # Create manager and connect
        manager = EnhancedRedisManager(use_failover=True)
        result = await manager.connect()
        
        # Verify connection state
        assert result is True
        assert manager.primary_connected is False
        assert manager.failover_connected is True
        assert manager.current_redis is failover_redis
        assert manager.using_failover is True
        
        # Clean up
        await manager.close()
        del os.environ["REDIS_HOST"]
        del os.environ["REDIS_PORT"]
        del os.environ["FAILOVER_REDIS_HOST"]
        del os.environ["FAILOVER_REDIS_PORT"]

@pytest.mark.asyncio
async def test_connect_both_failure():
    """Test connection when both Redis instances fail."""
    with patch('omega_ai.utils.enhanced_redis_manager.redis', autospec=True) as mock_redis:
        # Configure both Redis clients to fail
        primary_redis = AsyncMock()
        primary_redis.ping.return_value = False
        
        failover_redis = AsyncMock()
        failover_redis.ping.return_value = False
        
        mock_redis.Redis.side_effect = [primary_redis, failover_redis]
        
        # Set environment variables
        os.environ["REDIS_HOST"] = TEST_PRIMARY_HOST
        os.environ["REDIS_PORT"] = str(TEST_PRIMARY_PORT)
        os.environ["FAILOVER_REDIS_HOST"] = TEST_FAILOVER_HOST
        os.environ["FAILOVER_REDIS_PORT"] = str(TEST_FAILOVER_PORT)
        
        # Create manager and connect
        manager = EnhancedRedisManager(use_failover=True)
        result = await manager.connect()
        
        # Verify connection state
        assert result is False
        assert manager.primary_connected is False
        assert manager.failover_connected is False
        assert manager.current_redis is None
        
        # Clean up
        await manager.close()
        del os.environ["REDIS_HOST"]
        del os.environ["REDIS_PORT"]
        del os.environ["FAILOVER_REDIS_HOST"]
        del os.environ["FAILOVER_REDIS_PORT"]

@pytest.mark.asyncio
async def test_connect_no_failover():
    """Test connection with failover disabled."""
    with patch('omega_ai.utils.enhanced_redis_manager.redis', autospec=True) as mock_redis:
        # Configure primary Redis to fail
        primary_redis = AsyncMock()
        primary_redis.ping.return_value = False
        
        mock_redis.Redis.side_effect = [primary_redis]
        
        # Set environment variables
        os.environ["REDIS_HOST"] = TEST_PRIMARY_HOST
        os.environ["REDIS_PORT"] = str(TEST_PRIMARY_PORT)
        
        # Create manager with failover disabled
        manager = EnhancedRedisManager(use_failover=False)
        result = await manager.connect()
        
        # Verify connection state
        assert result is False
        assert manager.primary_connected is False
        assert manager.current_redis is None
        
        # Clean up
        await manager.close()
        del os.environ["REDIS_HOST"]
        del os.environ["REDIS_PORT"]

# =====================================
# Failover Tests
# =====================================

@pytest.mark.asyncio
async def test_ping_primary_failure(redis_manager):
    """Test ping with primary Redis failure."""
    # Configure primary Redis to fail
    redis_manager.primary_redis.ping.return_value = False
    
    # Ping should trigger failover
    result = await redis_manager.ping()
    
    # Verify failover occurred
    assert result is True
    assert redis_manager.primary_connected is False
    assert redis_manager.current_redis is redis_manager.failover_redis
    assert redis_manager.using_failover is True
    assert redis_manager.last_failover_time is not None

@pytest.mark.asyncio
async def test_ping_both_failure(redis_manager):
    """Test ping with both Redis instances failing."""
    # Configure both Redis instances to fail
    redis_manager.primary_redis.ping.return_value = False
    redis_manager.failover_redis.ping.return_value = False
    
    # Ping should fail
    result = await redis_manager.ping()
    
    # Verify result
    assert result is False
    assert redis_manager.primary_connected is False
    assert redis_manager.current_redis is None

@pytest.mark.asyncio
async def test_try_reconnect_primary(redis_manager):
    """Test reconnection to primary Redis."""
    # Set initial state to using failover
    redis_manager.using_failover = True
    redis_manager.current_redis = redis_manager.failover_redis
    redis_manager.primary_connected = False
    
    # Configure primary Redis to succeed on reconnect
    redis_manager.primary_redis.ping.return_value = True
    
    # Mock _sync_data_to_primary to avoid actual sync
    redis_manager._sync_data_to_primary = AsyncMock()
    
    # Attempt to reconnect
    result = await redis_manager.try_reconnect_primary()
    
    # Verify reconnection
    assert result is True
    assert redis_manager.primary_connected is True
    assert redis_manager.current_redis is redis_manager.primary_redis
    assert redis_manager.using_failover is False
    
    # Verify data sync was called
    redis_manager._sync_data_to_primary.assert_called_once()

@pytest.mark.asyncio
async def test_try_reconnect_primary_failure(redis_manager):
    """Test failed reconnection to primary Redis."""
    # Set initial state to using failover
    redis_manager.using_failover = True
    redis_manager.current_redis = redis_manager.failover_redis
    redis_manager.primary_connected = False
    
    # Configure primary Redis to fail on reconnect
    redis_manager.primary_redis.ping.return_value = False
    
    # Attempt to reconnect
    result = await redis_manager.try_reconnect_primary()
    
    # Verify reconnection failed
    assert result is False
    assert redis_manager.primary_connected is False
    assert redis_manager.current_redis is redis_manager.failover_redis
    assert redis_manager.using_failover is True
    assert redis_manager.reconnection_attempts == 1

# =====================================
# Data Synchronization Tests
# =====================================

@pytest.mark.asyncio
async def test_sync_data_to_primary(redis_manager):
    """Test data synchronization from failover to primary Redis."""
    # Mock _sync_key to avoid implementation details
    redis_manager._sync_key = AsyncMock()
    
    # Configure scan to return keys in batches
    redis_manager.failover_redis.scan.side_effect = [
        ("123", ["key1", "key4", "key5"]),  # First batch
        (0, ["key6", "key7"])               # Second batch
    ]
    
    # Run sync
    await redis_manager._sync_data_to_primary()
    
    # Verify all keys were synced
    assert redis_manager._sync_key.call_count == 8  # 3 priority keys + 5 scanned keys
    
    # Verify priority keys were synced first
    priority_calls = [call(key) for key in TEST_PRIORITY_KEYS]
    redis_manager._sync_key.assert_has_calls(priority_calls, any_order=False)

@pytest.mark.asyncio
async def test_sync_key_string(redis_manager):
    """Test synchronization of string keys."""
    # Configure Redis clients for string key
    redis_manager.failover_redis.exists.return_value = True
    redis_manager.failover_redis.type.return_value = "string"
    redis_manager.failover_redis.get.return_value = TEST_VALUE
    
    # Run sync
    await redis_manager._sync_key(TEST_KEY)
    
    # Verify operations
    redis_manager.failover_redis.exists.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.type.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.get.assert_called_once_with(TEST_KEY)
    redis_manager.primary_redis.set.assert_called_once_with(TEST_KEY, TEST_VALUE)

@pytest.mark.asyncio
async def test_sync_key_list(redis_manager):
    """Test synchronization of list keys."""
    # Configure Redis clients for list key
    test_list = ["item1", "item2", "item3"]
    redis_manager.failover_redis.exists.return_value = True
    redis_manager.failover_redis.type.return_value = "list"
    redis_manager.failover_redis.lrange.return_value = test_list
    
    # Run sync
    await redis_manager._sync_key(TEST_KEY)
    
    # Verify operations
    redis_manager.failover_redis.exists.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.type.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.lrange.assert_called_once_with(TEST_KEY, 0, -1)
    redis_manager.primary_redis.delete.assert_called_once_with(TEST_KEY)
    redis_manager.primary_redis.rpush.assert_called_once_with(TEST_KEY, *test_list)

@pytest.mark.asyncio
async def test_sync_key_hash(redis_manager):
    """Test synchronization of hash keys."""
    # Configure Redis clients for hash key
    test_hash = {"field1": "value1", "field2": "value2"}
    redis_manager.failover_redis.exists.return_value = True
    redis_manager.failover_redis.type.return_value = "hash"
    redis_manager.failover_redis.hgetall.return_value = test_hash
    
    # Run sync
    await redis_manager._sync_key(TEST_KEY)
    
    # Verify operations
    redis_manager.failover_redis.exists.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.type.assert_called_once_with(TEST_KEY)
    redis_manager.failover_redis.hgetall.assert_called_once_with(TEST_KEY)
    redis_manager.primary_redis.hmset.assert_called_once_with(TEST_KEY, test_hash)

@pytest.mark.asyncio
async def test_sync_key_error(redis_manager):
    """Test error handling during key synchronization."""
    # Configure failover Redis to raise an exception
    redis_manager.failover_redis.exists.side_effect = Exception("Redis error")
    
    # Run sync (should not raise exception)
    await redis_manager._sync_key(TEST_KEY)
    
    # Verify error was handled
    redis_manager.failover_redis.exists.assert_called_once_with(TEST_KEY)

# =====================================
# Redis Operation Tests
# =====================================

@pytest.mark.asyncio
async def test_get_cached_success(redis_manager):
    """Test get_cached with successful Redis operation."""
    # Configure Redis client
    redis_manager.current_redis.get.return_value = TEST_VALUE
    
    # Run operation
    result = await redis_manager.get_cached(TEST_KEY)
    
    # Verify result
    assert result == TEST_VALUE
    redis_manager.current_redis.get.assert_called_once_with(TEST_KEY)

@pytest.mark.asyncio
async def test_get_cached_with_failover(redis_manager):
    """Test get_cached with failover during operation."""
    # Configure Redis ping to trigger failover
    redis_manager.ping = AsyncMock(side_effect=lambda: redis_manager.using_failover)
    
    # Run operation
    result = await redis_manager.get_cached(TEST_KEY)
    
    # Verify operation used failover Redis
    assert redis_manager.using_failover is True
    assert result is None  # Return None because we mocked ping to change using_failover but didn't setup the current_redis

@pytest.mark.asyncio
async def test_set_cached_success(redis_manager):
    """Test set_cached with successful Redis operation."""
    # Configure Redis client
    redis_manager.current_redis.set.return_value = True
    
    # Run operation
    result = await redis_manager.set_cached(TEST_KEY, TEST_VALUE)
    
    # Verify result
    assert result is True
    redis_manager.current_redis.set.assert_called_once_with(TEST_KEY, TEST_VALUE, ex=None)

@pytest.mark.asyncio
async def test_set_cached_with_expiration(redis_manager):
    """Test set_cached with expiration time."""
    # Configure Redis client
    redis_manager.current_redis.set.return_value = True
    
    # Run operation with expiration
    expiration = 3600  # 1 hour
    result = await redis_manager.set_cached(TEST_KEY, TEST_VALUE, ex=expiration)
    
    # Verify result
    assert result is True
    redis_manager.current_redis.set.assert_called_once_with(TEST_KEY, TEST_VALUE, ex=expiration)

@pytest.mark.asyncio
async def test_publish_success(redis_manager):
    """Test publish with successful Redis operation."""
    # Configure Redis client
    channel = "test_channel"
    message = "test_message"
    redis_manager.current_redis.publish.return_value = 5  # 5 subscribers
    
    # Run operation
    result = await redis_manager.publish(channel, message)
    
    # Verify result
    assert result == 5
    redis_manager.current_redis.publish.assert_called_once_with(channel, message)

@pytest.mark.asyncio
async def test_lpush_success(redis_manager):
    """Test lpush with successful Redis operation."""
    # Configure Redis client
    redis_manager.current_redis.lpush.return_value = 10  # List length after push
    
    # Run operation
    result = await redis_manager.lpush(TEST_KEY, TEST_VALUE)
    
    # Verify result
    assert result == 10
    redis_manager.current_redis.lpush.assert_called_once_with(TEST_KEY, TEST_VALUE)

@pytest.mark.asyncio
async def test_ltrim_success(redis_manager):
    """Test ltrim with successful Redis operation."""
    # Configure Redis client
    redis_manager.current_redis.ltrim.return_value = True
    
    # Run operation
    result = await redis_manager.ltrim(TEST_KEY, 0, 999)
    
    # Verify result
    assert result is True
    redis_manager.current_redis.ltrim.assert_called_once_with(TEST_KEY, 0, 999)

# =====================================
# Comprehensive Scenarios
# =====================================

@pytest.mark.asyncio
async def test_complete_failover_scenario(redis_manager):
    """Test a complete failover scenario from start to finish."""
    # Step 1: Start with normal operation
    assert redis_manager.using_failover is False
    assert redis_manager.current_redis is redis_manager.primary_redis
    
    # Step 2: Trigger primary failure
    redis_manager.primary_redis.ping.return_value = False
    redis_manager.primary_redis.get.side_effect = Exception("Connection refused")
    result = await redis_manager.ping()
    
    # Verify failover occurred
    assert result is True
    assert redis_manager.using_failover is True
    assert redis_manager.current_redis is redis_manager.failover_redis
    assert redis_manager.last_failover_time is not None
    
    # Step 3: Continue operations on failover Redis
    redis_manager.failover_redis.get.return_value = TEST_VALUE
    cached_value = await redis_manager.get_cached(TEST_KEY)
    assert cached_value == TEST_VALUE
    redis_manager.failover_redis.get.assert_called_with(TEST_KEY)
    
    # Step 4: Primary Redis comes back online
    redis_manager.primary_redis.ping.return_value = True
    redis_manager._sync_data_to_primary = AsyncMock()
    
    # Step 5: Reconnect to primary
    result = await redis_manager.try_reconnect_primary()
    
    # Verify reconnection
    assert result is True
    assert redis_manager.using_failover is False
    assert redis_manager.current_redis is redis_manager.primary_redis
    
    # Verify data sync was performed
    redis_manager._sync_data_to_primary.assert_called_once()
    
    # Step 6: Continue operations on primary Redis
    redis_manager.primary_redis.get.return_value = TEST_VALUE
    redis_manager.primary_redis.get.side_effect = None
    cached_value = await redis_manager.get_cached(TEST_KEY)
    assert cached_value == TEST_VALUE
    redis_manager.primary_redis.get.assert_called_with(TEST_KEY)

# Main test runner
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 