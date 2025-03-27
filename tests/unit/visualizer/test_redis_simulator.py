import pytest
import json
from unittest.mock import patch, MagicMock
import redis
import os
from datetime import datetime

from omega_ai.visualizer.backend.redis_simulator import RedisSimulator, TRAP_TYPES

class TestRedisSimulator:
    """Test suite for RedisSimulator"""
    
    def test_initialization(self):
        """Test initialization with mock Redis"""
        with patch('redis.Redis') as mock_redis:
            # Setup mock
            mock_instance = mock_redis.return_value
            mock_instance.ping.return_value = True
            
            # Create simulator
            simulator = RedisSimulator()
            
            # Verify Redis client was created
            assert simulator.redis is not None
            assert simulator.redis_host == "localhost"
            assert simulator.redis_port == 6379
    
    def test_initialization_failure(self):
        """Test initialization when Redis connection fails"""
        with patch('redis.Redis') as mock_redis:
            # Setup mock to raise exception
            mock_instance = mock_redis.return_value
            mock_instance.ping.side_effect = redis.ConnectionError("Connection failed")
            
            # Create simulator
            simulator = RedisSimulator()
            
            # Verify Redis client is None
            assert simulator.redis is None
    
    def test_generate_trap_probability(self):
        """Test trap probability generation"""
        with patch('redis.Redis') as mock_redis:
            # Setup mock
            mock_instance = mock_redis.return_value
            mock_instance.ping.return_value = True
            
            # Create simulator
            simulator = RedisSimulator()
            simulator.redis = mock_instance
            
            # Generate trap probability
            data = simulator.generate_trap_probability()
            
            # Verify data structure
            assert "probability" in data
            assert "trap_type" in data
            assert "timestamp" in data
            assert "source" in data
            assert 0 <= data["probability"] <= 1
            assert data["trap_type"] in TRAP_TYPES
            assert data["source"] == "simulator"
            
            # Verify Redis set was called
            mock_instance.set.assert_called_once()
            assert "current_trap_probability" in mock_instance.set.call_args[0]
            
            # Verify the JSON data can be parsed
            json_data = mock_instance.set.call_args[0][1]
            parsed = json.loads(json_data)
            assert "probability" in parsed
    
    def test_generate_position_data_with_position(self):
        """Test position data generation with a position"""
        with patch('redis.Redis') as mock_redis, patch('random.random', return_value=0.5):
            # Setup mock
            mock_instance = mock_redis.return_value
            mock_instance.ping.return_value = True
            
            # Create simulator
            simulator = RedisSimulator()
            simulator.redis = mock_instance
            
            # Generate position data (random.random > 0.2, so will create position)
            data = simulator.generate_position_data()
            
            # Verify data structure for position
            assert data["has_position"] is True
            assert "position_side" in data
            assert "entry_price" in data
            assert "current_price" in data
            assert "position_size" in data
            assert "pnl_percent" in data
            assert "pnl_usd" in data
            assert "timestamp" in data
            
            # Verify Redis set was called
            mock_instance.set.assert_called_once()
            assert "current_position" in mock_instance.set.call_args[0]
    
    def test_generate_position_data_without_position(self):
        """Test position data generation without a position"""
        with patch('redis.Redis') as mock_redis, patch('random.random', return_value=0.1):
            # Setup mock
            mock_instance = mock_redis.return_value
            mock_instance.ping.return_value = True
            
            # Create simulator
            simulator = RedisSimulator()
            simulator.redis = mock_instance
            
            # Generate position data (random.random < 0.2, so no position)
            data = simulator.generate_position_data()
            
            # Verify data structure for no position
            assert data["has_position"] is False
            assert "timestamp" in data
            assert "source" in data
            
            # Verify Redis set was called
            mock_instance.set.assert_called_once()
            assert "current_position" in mock_instance.set.call_args[0]
    
    def test_run_method_catches_keyboard_interrupt(self):
        """Test that run method handles KeyboardInterrupt gracefully"""
        with patch('redis.Redis') as mock_redis, \
             patch('time.sleep', side_effect=KeyboardInterrupt), \
             patch('omega_ai.visualizer.backend.redis_simulator.logger') as mock_logger:
            
            # Setup mock
            mock_instance = mock_redis.return_value
            mock_instance.ping.return_value = True
            
            # Create simulator
            simulator = RedisSimulator()
            simulator.redis = mock_instance
            
            # Run simulator (should catch KeyboardInterrupt)
            simulator.run()
            
            # Verify logger was called
            mock_logger.info.assert_called_with("Simulator stopped by user") 