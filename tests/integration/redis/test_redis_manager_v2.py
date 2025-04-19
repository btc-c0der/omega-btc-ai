
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

"""Tests for Redis Manager V2 functionality.

This test suite covers the enhanced features of the Redis Manager V2:
1. Connection pooling
2. Data serialization
3. Pub/sub management
4. Error handling
5. Health monitoring
6. Memory optimization
7. Performance tracking
8. Resource cleanup
"""

import pytest
import asyncio
import json
from datetime import datetime, UTC
from typing import Dict, Any, List
from omega_ai.mm_trap_detector.redis_manager_v2 import (
    RedisManagerV2, RedisConfig
)

# ---- Test Helpers ----

@pytest.fixture
def redis_config():
    """Create test Redis configuration."""
    return RedisConfig(
        host="localhost",
        port=6379,
        db=0,
        password=None,
        ssl=False,
        pool_size=2,
        pool_timeout=5,
        decode_responses=True,
        max_connections=10
    )

@pytest.fixture
async def redis_manager(redis_config):
    """Create Redis manager instance."""
    manager = RedisManagerV2(config=redis_config)
    yield manager
    await manager.close()

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_redis_v2_initialization(redis_manager):
    """Test Redis manager initialization."""
    assert redis_manager is not None
    assert redis_manager.pool is not None
    assert redis_manager.async_pool is not None

@pytest.mark.asyncio
async def test_redis_v2_connection_pool(redis_manager):
    """Test Redis connection pool functionality."""
    # Get multiple clients
    clients = []
    for _ in range(3):
        client = redis_manager.get_client()
        clients.append(client)
        assert client.ping()
    
    # Verify pool is working
    assert len(clients) == 3
    for client in clients:
        client.close()

@pytest.mark.asyncio
async def test_redis_v2_data_operations(redis_manager):
    """Test Redis data operations."""
    key = "test:key"
    value = {
        "name": "divine_test",
        "value": 42,
        "timestamp": datetime.now(UTC).isoformat()
    }
    
    # Set data
    await redis_manager.set_data(key, value)
    
    # Get data
    result = await redis_manager.get_data(key)
    assert result is not None
    assert result["name"] == "divine_test"
    assert result["value"] == 42
    
    # Delete data
    await redis_manager.delete_data(key)
    
    # Verify deletion
    result = await redis_manager.get_data(key)
    assert result is None

@pytest.mark.asyncio
async def test_redis_v2_pub_sub(redis_manager):
    """Test Redis pub/sub functionality."""
    channel = "test:channel"
    message = {
        "type": "test",
        "data": "divine_message",
        "timestamp": datetime.now(UTC).isoformat()
    }
    
    # Subscribe to channel
    pubsub = redis_manager.get_client().pubsub()
    pubsub.subscribe(channel)
    
    # Publish message
    await redis_manager.publish(channel, message)
    
    # Receive message
    received = pubsub.get_message(timeout=1)
    assert received is not None
    assert received["type"] == "message"
    assert received["channel"] == channel.encode()
    
    # Verify message content
    data = json.loads(received["data"])
    assert data["type"] == "test"
    assert data["data"] == "divine_message"
    
    # Cleanup
    pubsub.unsubscribe(channel)
    pubsub.close()

@pytest.mark.asyncio
async def test_redis_v2_health_check(redis_manager):
    """Test Redis health check."""
    health = await redis_manager.health_check()
    
    assert health["status"] == "healthy"
    assert "memory_used" in health
    assert "connected_clients" in health
    assert "uptime" in health
    assert "timestamp" in health

@pytest.mark.asyncio
async def test_redis_v2_memory_optimization(redis_manager):
    """Test Redis memory optimization."""
    # Fill Redis with test data
    for i in range(100):
        key = f"test:key:{i}"
        value = {"data": "x" * 1000}  # Large value
        await redis_manager.set_data(key, value)
    
    # Run optimization
    result = await redis_manager.optimize_memory()
    
    assert result["status"] == "optimized"
    assert "memory_reduced" in result
    assert "timestamp" in result

@pytest.mark.asyncio
async def test_redis_v2_error_handling(redis_manager):
    """Test Redis error handling."""
    # Test invalid key
    result = await redis_manager.get_data(None)
    assert result is None
    
    # Test invalid value
    with pytest.raises(Exception):
        await redis_manager.set_data("test:key", object())
    
    # Test invalid channel
    with pytest.raises(Exception):
        await redis_manager.publish(None, {"test": "data"})

@pytest.mark.asyncio
async def test_redis_v2_concurrent_operations(redis_manager):
    """Test Redis concurrent operations."""
    key_prefix = "test:concurrent:"
    tasks = []
    
    # Create multiple concurrent operations
    for i in range(10):
        key = f"{key_prefix}{i}"
        value = {"index": i, "timestamp": datetime.now(UTC).isoformat()}
        
        # Mix of set and get operations
        if i % 2 == 0:
            tasks.append(redis_manager.set_data(key, value))
        else:
            tasks.append(redis_manager.get_data(key))
    
    # Execute all operations concurrently
    results = await asyncio.gather(*tasks)
    
    # Verify results
    assert len(results) == 10
    for i, result in enumerate(results):
        if i % 2 == 0:
            assert result is True  # Set operation result
        else:
            assert result is not None  # Get operation result

@pytest.mark.asyncio
async def test_redis_v2_connection_cleanup(redis_manager):
    """Test Redis connection cleanup."""
    # Create multiple connections
    clients = []
    for _ in range(3):
        client = redis_manager.get_client()
        clients.append(client)
    
    # Close manager
    await redis_manager.close()
    
    # Verify cleanup
    for client in clients:
        try:
            client.ping()
        except Exception:
            pass  # Expected to fail as connection is closed 