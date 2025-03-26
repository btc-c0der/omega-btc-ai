import os
from typing import Dict, Any, Optional, List
from .redis_manager import RedisManager

class TestRedisManager(RedisManager):
    """Test-specific Redis manager that uses separate test keys and connections."""
    
    def __init__(self, **kwargs):
        """Initialize test Redis connection with test-specific configuration."""
        # Get default config and update with test-specific settings
        config = self._get_test_config()
        config.update(kwargs)
        
        super().__init__(**config)
        
        # Test-specific key prefix
        self.test_prefix = "test:"
        
        # Clear any existing test data on initialization
        self._clear_test_data()
    
    def _get_test_config(self) -> Dict[str, Any]:
        """Get test-specific Redis configuration."""
        # Check if we should use local Redis for testing
        use_local = os.getenv('OMEGA_TEST_USE_LOCAL_REDIS', 'true').lower() == 'true'
        
        if use_local:
            # Local test Redis configuration
            return {
                'host': os.getenv('TEST_REDIS_HOST', 'localhost'),
                'port': int(os.getenv('TEST_REDIS_PORT', '6379')),
                'db': int(os.getenv('TEST_REDIS_DB', '1')),  # Use different DB for tests
                'decode_responses': True
            }
        else:
            # Remote Redis configuration
            return {
                'host': os.getenv('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
                'port': int(os.getenv('REDIS_PORT', '19332')),
                'username': os.getenv('REDIS_USERNAME', 'omega'),
                'password': os.getenv('REDIS_PASSWORD', 'VuKJU8Z.Z2V8Qn_'),
                'ssl': os.getenv('REDIS_USE_TLS', 'true').lower() == 'true',
                'ssl_ca_certs': os.getenv('REDIS_CERT', 'SSL_redis-btc-omega-redis.pem'),
                'decode_responses': True
            }
    
    def _clear_test_data(self) -> None:
        """Clear all test data from Redis."""
        try:
            # Get all keys with test prefix
            keys = self.redis.keys(f"{self.test_prefix}*")
            if keys:
                self.redis.delete(*keys)
            
            # Also clear unprefixed keys
            keys = self.redis.keys("btc_trend_*")
            if keys:
                self.redis.delete(*keys)
            keys = self.redis.keys("last_btc_*")
            if keys:
                self.redis.delete(*keys)
            keys = self.redis.keys("btc_candle_*")
            if keys:
                self.redis.delete(*keys)
            keys = self.redis.keys("btc_movement_*")
            if keys:
                self.redis.delete(*keys)
            keys = self.redis.keys("fibonacci:*")
            if keys:
                self.redis.delete(*keys)
        except Exception as e:
            print(f"Warning: Could not clear test data: {e}")
    
    def get_cached(self, key: str, default: Any = None) -> Optional[Any]:
        """Get value from cache or Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        value = super().get_cached(test_key, default)
        if value is None:
            value = super().get_cached(key, default)
        return value
    
    def set_cached(self, key: str, value: Any) -> bool:
        """Set a value in Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        return super().set_cached(test_key, value)
    
    def lpush(self, key: str, value: Any) -> bool:
        """Push to a list in Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        return super().lpush(test_key, value)
    
    def lrange(self, key: str, start: int, end: int) -> Optional[list]:
        """Get a range from a list in Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        value = super().lrange(test_key, start, end)
        if value is None:
            value = super().lrange(key, start, end)
        return value
    
    def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim a list in Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        return super().ltrim(test_key, start, end)
    
    def delete(self, *names: str) -> int:
        """Delete keys from Redis with test prefix."""
        test_keys = [f"{self.test_prefix}{name}" for name in names]
        super().delete(*test_keys)
        return super().delete(*names)
    
    def check_key_exists(self, key: str) -> bool:
        """Check if a key exists in Redis with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        exists = super().check_key_exists(test_key)
        if not exists:
            exists = super().check_key_exists(key)
        return exists
    
    def get_key_type(self, key: str) -> Optional[str]:
        """Get the type of a Redis key with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        key_type = super().get_key_type(test_key)
        if key_type is None:
            key_type = super().get_key_type(key)
        return key_type
    
    def set_with_validation(self, key: str, data: Dict) -> bool:
        """Set data with validation and test prefix."""
        test_key = f"{self.test_prefix}{key}"
        return super().set_with_validation(test_key, data)
    
    def zadd(self, name: str, mapping: dict) -> int:
        """Add to sorted set with test prefix."""
        test_name = f"{self.test_prefix}{name}"
        return super().zadd(test_name, mapping)
    
    def zrange(self, name: str, start: int, end: int, desc: bool = False, withscores: bool = False) -> list:
        """Get range from sorted set with test prefix."""
        test_name = f"{self.test_prefix}{name}"
        value = super().zrange(test_name, start, end, desc, withscores)
        if not value:
            value = super().zrange(name, start, end, desc, withscores)
        return value
    
    def zremrangebyrank(self, name: str, start: int, end: int) -> int:
        """Remove range from sorted set with test prefix."""
        test_name = f"{self.test_prefix}{name}"
        return super().zremrangebyrank(test_name, start, end)
    
    def zcard(self, name: str) -> int:
        """Get cardinality of sorted set with test prefix."""
        test_name = f"{self.test_prefix}{name}"
        value = super().zcard(test_name)
        if value == 0:
            value = super().zcard(name)
        return value
    
    def get(self, key: str) -> Any:
        """Get value with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        value = super().get(test_key)
        if value is None:
            value = super().get(key)
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Set value with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        return super().set(test_key, value)
    
    def llen(self, key: str) -> int:
        """Get list length with test prefix."""
        test_key = f"{self.test_prefix}{key}"
        value = super().llen(test_key)
        if value == 0:
            value = super().llen(key)
        return value 