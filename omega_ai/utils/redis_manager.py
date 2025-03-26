"""
🔱 OMEGA BTC AI - Redis Connection Manager 🔱
Sacred Redis connection management with divine error handling and retries.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""
import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
import signal
import sys
from typing import Optional, Dict, Any, List, Union, Tuple, Mapping
import json
import time
import os
from .redis_config import get_redis_config

class RedisManager:
    """Redis connection manager with error handling and retries."""
    
    def __init__(self, **kwargs):
        """Initialize Redis connection with configuration."""
        # Get default config and update with any overrides
        config = get_redis_config()
        config.update(kwargs)
        
        # Add retry strategy for better connection handling
        retry_strategy = Retry(
            ExponentialBackoff(),
            retries=3
        )
        
        # Ensure proper configuration
        config.setdefault('retry_on_timeout', True)
        config.setdefault('retry_on_error', [redis.ConnectionError])
        config.setdefault('retry', retry_strategy)
        
        try:
            self.redis = redis.Redis(**config)
            self._test_connection()
        except redis.AuthenticationError as e:
            raise ConnectionError(f"Redis authentication failed: {str(e)}")
        except redis.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error connecting to Redis: {str(e)}")
        
        self._cache = {}
        self._cache_ttl = {}
        self.CACHE_DURATION = 5  # seconds
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def _test_connection(self):
        """Test Redis connection."""
        try:
            self.redis.ping()
        except redis.AuthenticationError as e:
            raise ConnectionError(f"Redis authentication failed: {str(e)}")
        except redis.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Unexpected error testing Redis connection: {str(e)}")
    
    def connect(self):
        """Get a blessed Redis connection."""
        if not self.redis:
            self.redis = redis.Redis(
                host=self.redis.connection_pool.connection_kwargs['host'],
                port=self.redis.connection_pool.connection_kwargs['port'],
                db=self.redis.connection_pool.connection_kwargs['db'],
                decode_responses=True
            )
        return self.redis
    
    def get_cached(self, key: str, default: Any = None) -> Optional[Any]:
        """Get value from cache or Redis with TTL-based caching"""
        now = time.time()
        
        # Check cache first
        if key in self._cache and now < self._cache_ttl[key]:
            return self._cache[key]
            
        # Get from Redis
        try:
            value = self.redis.get(key)
            if value:
                self._cache[key] = value
                self._cache_ttl[key] = now + self.CACHE_DURATION
                return value
            return default
        except redis.exceptions.ResponseError as e:
            print(f"Redis error on get: {e}")
            # Check if this is a WRONGTYPE error
            if "WRONGTYPE" in str(e):
                # Try to identify the actual type and get it appropriately
                return self.get_key_with_type_detection(key, default)
            return default
        except redis.RedisError as e:
            print(f"Redis error on get: {e}")
            return default
    
    def get_key_with_type_detection(self, key: str, default: Any = None) -> Any:
        """
        Get a key's value from Redis with automatic type detection.
        Handles cases where a key exists but is of a different type than expected.
        """
        try:
            # Check the type of the key
            key_type = self.redis.type(key).decode('utf-8')
            
            if key_type == 'string':
                return self.redis.get(key)
            elif key_type == 'list':
                return self.redis.lrange(key, 0, -1)
            elif key_type == 'hash':
                return self.redis.hgetall(key)
            elif key_type == 'set':
                return list(self.redis.smembers(key))
            elif key_type == 'zset':
                return self.redis.zrange(key, 0, -1, withscores=True)
            else:
                print(f"Unknown Redis type for key '{key}': {key_type}")
                return default
        except redis.RedisError as e:
            print(f"Error detecting type for key '{key}': {e}")
            return default
    
    def fix_key_type(self, key: str, expected_type: str) -> bool:
        """
        Fix a key that has the wrong type by getting its value,
        deleting it, and recreating it with the correct type.
        
        Args:
            key: The Redis key to fix
            expected_type: The expected type ('string', 'list', 'hash', etc.)
            
        Returns:
            bool: True if fixed successfully, False otherwise
        """
        try:
            # Get current value with type detection
            current_value = self.get_key_with_type_detection(key)
            if current_value is None:
                return False
                
            # Delete the key
            self.redis.delete(key)
            
            # Recreate with proper type
            if expected_type == 'string':
                # For a string, we need to convert other types to string
                if isinstance(current_value, list):
                    if len(current_value) > 0:
                        value = current_value[0] if isinstance(current_value[0], str) else json.dumps(current_value[0])
                    else:
                        value = ""
                elif isinstance(current_value, dict):
                    value = json.dumps(current_value)
                else:
                    value = str(current_value)
                return self.set_cached(key, value)
                
            elif expected_type == 'list':
                # Convert to list if not already
                if not isinstance(current_value, list):
                    current_value = [current_value]
                
                # Add each item to the list
                for item in current_value:
                    self.lpush(key, item)
                return True
                
            elif expected_type == 'hash':
                # Convert to dict if not already
                if not isinstance(current_value, dict):
                    if isinstance(current_value, list) and len(current_value) > 0:
                        # Try to convert list to dict
                        try:
                            current_value = json.loads(current_value[0])
                            if not isinstance(current_value, dict):
                                current_value = {"value": current_value}
                        except:
                            current_value = {"value": str(current_value)}
                    else:
                        current_value = {"value": str(current_value)}
                
                # Add hash fields with proper type hints
                mapping: Mapping[str, str] = {str(k): str(v) for k, v in current_value.items()}
                return bool(self.redis.hset(key, mapping=mapping))
                
            else:
                print(f"Conversion to type '{expected_type}' not implemented")
                return False
                
        except Exception as e:
            print(f"Error fixing key type: {e}")
            return False
    
    def safe_get(self, key: str, default: Any = None) -> Optional[Any]:
        """Get a value from Redis, handling any type errors safely."""
        try:
            return self.get_cached(key, default)
        except redis.exceptions.ResponseError:
            # Try to get with type detection
            return self.get_key_with_type_detection(key, default)
        except Exception as e:
            print(f"Error retrieving key '{key}': {e}")
            return default
    
    def safe_lrange(self, key: str, start: int, end: int) -> List:
        """Safely get a range from a Redis list, handling type errors."""
        try:
            return self.lrange(key, start, end) or []
        except redis.exceptions.ResponseError as e:
            if "WRONGTYPE" in str(e):
                # Try to fix the key
                self.fix_key_type(key, 'list')
                # Try lrange again
                try:
                    return self.lrange(key, start, end) or []
                except:
                    return []
            return []
        except Exception:
            return []
    
    def check_key_exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            print(f"Error checking key existence: {e}")
            return False
    
    def get_key_type(self, key: str) -> Optional[str]:
        """Get the type of a Redis key."""
        try:
            key_type = self.redis.type(key)
            if isinstance(key_type, bytes):
                return key_type.decode('utf-8')
            return key_type
        except Exception as e:
            print(f"Error getting key type: {e}")
            return None
    
    def set_cached(self, key: str, value: Any) -> bool:
        """Set a value in Redis with divine energy."""
        try:
            self.redis.set(key, value)
            self._cache[key] = value
            self._cache_ttl[key] = time.time() + self.CACHE_DURATION
            return True
        except redis.RedisError as e:
            print(f"Redis error on set: {e}")
            return False
    
    def lpush(self, key: str, value: Any) -> bool:
        """Push to a list in Redis with Rastafarian rhythm."""
        try:
            self.redis.lpush(key, value)
            return True
        except redis.RedisError as e:
            print(f"Redis error on lpush: {e}")
            return False
    
    def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim a list in Redis with cosmic precision."""
        try:
            self.redis.ltrim(key, start, end)
            return True
        except redis.RedisError as e:
            print(f"Redis error on ltrim: {e}")
            return False
    
    def lrange(self, key: str, start: int, end: int) -> Optional[list]:
        """Get a range from a list in Redis with divine harmony."""
        try:
            return self.redis.lrange(key, start, end)
        except redis.RedisError as e:
            print(f"Redis error on lrange: {e}")
            return None
    
    def ping(self) -> bool:
        """Check Redis connection with JAH blessing."""
        try:
            return self.redis.ping()
        except redis.RedisError as e:
            print(f"Redis error on ping: {e}")
            return False
    
    def set_with_validation(self, key: str, data: Dict) -> bool:
        """Set data with type validation"""
        try:
            # Validate data structure
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary")
                
            # Validate specific fields based on key
            if "omega:live_trader_data" in key:
                self._validate_trader_data(data)
            elif "omega:live_battle_state" in key:
                self._validate_battle_state(data)
            
            # Store in Redis
            self.redis.set(key, json.dumps(data))
            
            # Update cache
            self._cache[key] = data
            self._cache_ttl[key] = time.time() + self.CACHE_DURATION
            
            return True
            
        except (redis.RedisError, ValueError) as e:
            print(f"Error storing data: {e}")
            return False
    
    def _validate_trader_data(self, data: Dict):
        """Validate trader data structure"""
        required_fields = {
            "name": str,
            "capital": (int, float),
            "pnl": (int, float),
            "win_rate": float,
            "trades": int,
            "emotional_state": str,
            "confidence": float,
            "risk_level": float
        }
        
        for profile_data in data.values():
            for field, field_type in required_fields.items():
                if field not in profile_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(profile_data[field], field_type):
                    raise ValueError(f"Invalid type for {field}")
    
    def _validate_battle_state(self, data: Dict):
        """Validate battle state structure"""
        required_fields = {
            "day": int,
            "session": int,
            "btc_price": (int, float),
            "battle_active": bool,
            "start_time": str
        }
        
        for field, field_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise ValueError(f"Invalid type for {field}")
    
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown."""
        if hasattr(self, 'redis') and self.redis:
            self.redis.close()
        sys.exit(0)

    def zcard(self, name: str) -> int:
        """Return the number of elements in the sorted set at key `name`."""
        return self.redis.zcard(name)

    def zadd(self, name: str, mapping: dict) -> int:
        """Add all the specified members with the specified scores to the sorted set stored at key `name`."""
        return self.redis.zadd(name, mapping)

    def zrange(self, name: str, start: int, end: int, desc: bool = False, withscores: bool = False) -> list:
        """Return a range of elements from the sorted set at key `name`."""
        return self.redis.zrange(name, start, end, desc=desc, withscores=withscores)

    def zremrangebyrank(self, name: str, start: int, end: int) -> int:
        """Remove all elements in the sorted set stored at key `name` with rank between `start` and `end`."""
        return self.redis.zremrangebyrank(name, start, end)

    def delete(self, *names: str) -> int:
        """Delete a key from the Redis database."""
        return self.redis.delete(*names)
