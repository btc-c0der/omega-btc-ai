
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

import pytest
import redis
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
import asyncio
from omega_ai.tools.redis_mapping import connect_redis, safe_get_value, extract_mm_traps, save_trap_data

# =============== ERROR HANDLING TESTS ===============

def test_connect_redis_connection_error():
    """Test Redis connection failure handling."""
    with patch('redis.StrictRedis') as mock_redis:
        mock_redis.return_value.ping.side_effect = redis.ConnectionError("Connection refused")
        with pytest.raises(SystemExit) as exc_info:
            connect_redis()
        assert exc_info.value.code == 1

def test_safe_get_value_wrong_type():
    """Test handling of WRONGTYPE Redis errors."""
    mock_redis = MagicMock()
    mock_redis.type.return_value = "string"
    mock_redis.get.side_effect = redis.ResponseError("WRONGTYPE Operation against a key holding the wrong kind of value")
    
    result = safe_get_value(mock_redis, "test_key")
    assert result is None

def test_safe_get_value_connection_timeout():
    """Test handling of Redis connection timeouts."""
    mock_redis = MagicMock()
    mock_redis.type.side_effect = redis.TimeoutError("Connection timeout")
    
    result = safe_get_value(mock_redis, "test_key")
    assert result is None

# =============== PERFORMANCE TESTS ===============

@pytest.mark.performance
def test_large_dataset_handling():
    """Test handling of large datasets."""
    mock_redis = MagicMock()
    # Simulate 10,000 keys
    mock_redis.scan_iter.return_value = [f"mm_trap:{i}" for i in range(10000)]
    mock_redis.type.return_value = "hash"
    mock_redis.hgetall.return_value = {"type": "Liquidity Grab", "confidence": "0.9"}
    
    start_time = datetime.now()
    data = extract_mm_traps(mock_redis)
    end_time = datetime.now()
    
    processing_time = (end_time - start_time).total_seconds()
    assert processing_time < 5.0  # Should process within 5 seconds
    assert len(data["raw_data"]) == 10000

@pytest.mark.performance
def test_concurrent_operations():
    """Test handling multiple concurrent operations."""
    mock_redis = MagicMock()
    mock_redis.scan_iter.return_value = [f"mm_trap:{i}" for i in range(100)]
    
    async def simulate_concurrent_access():
        tasks = []
        for _ in range(10):  # Simulate 10 concurrent operations
            tasks.append(asyncio.create_task(asyncio.to_thread(extract_mm_traps, mock_redis)))
        await asyncio.gather(*tasks)
    
    asyncio.run(simulate_concurrent_access())
    # If we reach here without exceptions, the test passes

# =============== INTEGRATION TESTS ===============

@pytest.mark.integration
def test_real_redis_connection():
    """Test connection to actual Redis instance."""
    try:
        redis_conn = connect_redis()
        assert redis_conn.ping()
    except (redis.ConnectionError, redis.TimeoutError):
        pytest.skip("Skipping integration test - Redis not available")

@pytest.mark.integration
def test_data_persistence():
    """Test data persistence in Redis."""
    try:
        redis_conn = connect_redis()
        test_key = "test:mm_trap:persistence"
        test_data = {"type": "Test Trap", "timestamp": datetime.now().isoformat()}
        
        # Store test data
        redis_conn.hset(test_key, mapping=test_data)
        
        # Verify data was stored
        stored_data = redis_conn.hgetall(test_key)
        assert stored_data["type"] == test_data["type"]
        
        # Cleanup
        redis_conn.delete(test_key)
    except (redis.ConnectionError, redis.TimeoutError):
        pytest.skip("Skipping integration test - Redis not available")

# =============== EDGE CASES ===============

def test_empty_redis_instance():
    """Test behavior with empty Redis instance."""
    mock_redis = MagicMock()
    mock_redis.scan_iter.return_value = []
    
    data = extract_mm_traps(mock_redis)
    assert data["mm_traps"] == []
    assert data["trap_detections"] == []
    assert data["trap_metrics"] == {}

def test_malformed_json_data():
    """Test handling of malformed JSON data."""
    mock_redis = MagicMock()
    mock_redis.scan_iter.return_value = ["mm_trap:malformed"]
    mock_redis.type.return_value = "string"
    mock_redis.get.return_value = "{"  # Invalid JSON
    
    data = extract_mm_traps(mock_redis)
    assert len(data["mm_traps"]) == 1
    assert isinstance(data["mm_traps"][0]["data"], str)  # Should store raw string if JSON parsing fails

def test_mixed_data_types():
    """Test handling of mixed data types in Redis."""
    mock_redis = MagicMock()
    mock_redis.scan_iter.return_value = ["mm_trap:1", "mm_trap:2"]
    
    def mock_type(key):
        return "string" if key == "mm_trap:1" else "hash"
    
    def mock_get(key):
        return json.dumps({"type": "string_trap"}) if key == "mm_trap:1" else None
    
    def mock_hgetall(key):
        return {"type": "hash_trap"} if key == "mm_trap:2" else {}
    
    mock_redis.type.side_effect = mock_type
    mock_redis.get.side_effect = mock_get
    mock_redis.hgetall.side_effect = mock_hgetall
    
    data = extract_mm_traps(mock_redis)
    assert len(data["raw_data"]) == 2

def test_unicode_handling():
    """Test handling of Unicode characters in Redis data."""
    mock_redis = MagicMock()
    mock_redis.scan_iter.return_value = ["mm_trap:unicode"]
    mock_redis.type.return_value = "string"
    test_string = "Unicode Test 🚀✨"
    mock_redis.get.return_value = json.dumps({"type": test_string})
    
    data = extract_mm_traps(mock_redis)
    # Check that the raw data contains the escaped version of the emoji
    assert "\\ud83d\\ude80" in data["raw_data"]["mm_trap:unicode"]
    # Verify we can decode it back
    decoded = json.loads(data["raw_data"]["mm_trap:unicode"])
    assert decoded["type"] == test_string

def test_large_key_count():
    """Test handling of large number of keys."""
    mock_redis = MagicMock()
    # Generate 1 million keys
    mock_redis.scan_iter.return_value = (f"mm_trap:{i}" for i in range(1000000))
    mock_redis.type.return_value = "string"
    mock_redis.get.return_value = "{}"
    
    data = extract_mm_traps(mock_redis)
    assert len(data["raw_data"]) > 0  # Should handle large number of keys without crashing

def test_save_trap_data_disk_full():
    """Test handling of disk full scenario."""
    test_data = {"test": "data"}
    with patch('builtins.open') as mock_open:
        mock_open.side_effect = OSError("No space left on device")
        # The function prints error but doesn't raise exception
        save_trap_data(test_data)
        # Verify the error was handled gracefully
        mock_open.assert_called_once() 