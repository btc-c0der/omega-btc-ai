"""
🌌 OMEGA RASTA REDIS INTEGRATION TESTS 🌌
=======================================

Tests for the divine Redis integration functionality.
May the golden ratio be with you! 🚀
"""

import pytest
import json
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

class TestRedisIntegration:
    """Test suite for Redis integration."""
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_save_fibonacci_data(self, mock_redis, detector):
        """Test saving Fibonacci data to Redis."""
        # Set up test data
        test_data = {
            'levels': {0.618: 41236.0, 0.786: 41528.0},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'swing_high': 42000.0,
            'swing_low': 40000.0
        }
        
        # Save data
        detector.save_fibonacci_data(test_data)
        
        # Verify Redis calls
        mock_redis.set.assert_called_once()
        key, value = mock_redis.set.call_args[0]
        assert key == f"fibonacci_data:{detector.symbol}", "Should use correct Redis key"
        assert json.loads(value) == test_data, "Should save correct data"
        
        print(f"{GREEN}✓ Fibonacci data saving verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_get_fibonacci_data(self, mock_redis, detector):
        """Test retrieving Fibonacci data from Redis."""
        # Set up test data
        test_data = {
            'levels': {0.618: 41236.0, 0.786: 41528.0},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'swing_high': 42000.0,
            'swing_low': 40000.0
        }
        
        # Mock Redis response
        mock_redis.get.return_value = json.dumps(test_data)
        
        # Get data
        result = detector.get_fibonacci_data()
        
        # Verify result
        assert result == test_data, "Should retrieve correct data"
        mock_redis.get.assert_called_once_with(f"fibonacci_data:{detector.symbol}")
        
        print(f"{GREEN}✓ Fibonacci data retrieval verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_update_fibonacci_data(self, mock_redis, detector):
        """Test updating Fibonacci data in Redis."""
        # Set up initial data
        initial_data = {
            'levels': {0.618: 41236.0, 0.786: 41528.0},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'swing_high': 42000.0,
            'swing_low': 40000.0
        }
        
        # Set up update data
        update_data = {
            'levels': {0.618: 41250.0, 0.786: 41550.0},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'swing_high': 42100.0,
            'swing_low': 40100.0
        }
        
        # Mock Redis responses
        mock_redis.get.side_effect = [
            json.dumps(initial_data),
            json.dumps(update_data)
        ]
        
        # Get initial data
        initial_result = detector.get_fibonacci_data()
        assert initial_result == initial_data, "Should get initial data"
        
        # Update data
        detector.save_fibonacci_data(update_data)
        
        # Get updated data
        updated_result = detector.get_fibonacci_data()
        assert updated_result == update_data, "Should get updated data"
        
        print(f"{GREEN}✓ Fibonacci data update verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_connection_retry(self, mock_redis, detector):
        """Test Redis connection retry mechanism."""
        # Simulate Redis connection failure and recovery
        mock_redis.get.side_effect = [
            Exception("Connection failed"),
            Exception("Connection failed"),
            json.dumps({'levels': {0.618: 41236.0}})
        ]
        
        # Test with retries
        result = detector.get_fibonacci_data(max_retries=3)
        assert result is not None, "Should recover after retries"
        assert mock_redis.get.call_count == 3, "Should attempt correct number of retries"
        
        print(f"{GREEN}✓ Redis connection retry verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_data_expiration(self, mock_redis, detector):
        """Test Redis data expiration handling."""
        # Set up test data with expiration
        test_data = {
            'levels': {0.618: 41236.0, 0.786: 41528.0},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'swing_high': 42000.0,
            'swing_low': 40000.0
        }
        
        # Save data with expiration
        detector.save_fibonacci_data(test_data, expire_seconds=3600)
        
        # Verify Redis calls
        mock_redis.set.assert_called_once()
        mock_redis.expire.assert_called_once_with(
            f"fibonacci_data:{detector.symbol}",
            3600
        )
        
        print(f"{GREEN}✓ Redis data expiration verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_data_validation(self, mock_redis, detector):
        """Test Redis data validation."""
        # Set up invalid data
        invalid_data = {
            'levels': {'invalid': 'data'},
            'timestamp': 'invalid_timestamp',
            'swing_high': 'not_a_number',
            'swing_low': 'not_a_number'
        }
        
        # Test saving invalid data
        with pytest.raises(ValueError, match="Invalid Fibonacci data format"):
            detector.save_fibonacci_data(invalid_data)
        
        # Test retrieving invalid data
        mock_redis.get.return_value = json.dumps(invalid_data)
        result = detector.get_fibonacci_data()
        assert result is None, "Should handle invalid data gracefully"
        
        print(f"{GREEN}✓ Redis data validation verified!{RESET}")
    
    @patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn')
    def test_redis_batch_operations(self, mock_redis, detector):
        """Test Redis batch operations."""
        # Set up multiple test data entries
        test_data_list = [
            {
                'levels': {0.618: 41236.0 + i, 0.786: 41528.0 + i},
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'swing_high': 42000.0 + i,
                'swing_low': 40000.0 + i
            }
            for i in range(3)
        ]
        
        # Save multiple entries
        for i, data in enumerate(test_data_list):
            detector.save_fibonacci_data(data, key_suffix=f"_{i}")
        
        # Verify Redis calls
        assert mock_redis.set.call_count == 3, "Should save all entries"
        
        # Retrieve multiple entries
        results = []
        for i in range(3):
            mock_redis.get.return_value = json.dumps(test_data_list[i])
            result = detector.get_fibonacci_data(key_suffix=f"_{i}")
            results.append(result)
        
        # Verify results
        assert results == test_data_list, "Should retrieve all entries correctly"
        
        print(f"{GREEN}✓ Redis batch operations verified!{RESET}") 