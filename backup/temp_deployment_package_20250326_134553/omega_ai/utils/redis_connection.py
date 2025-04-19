
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

import redis
import json
import logging
from typing import Any, Optional, Union, List
from redis.exceptions import ConnectionError, TimeoutError, RedisError

logger = logging.getLogger(__name__)

class RedisConnectionManager:
    """Manages Redis connections with retries and error handling"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, 
                 db: int = 0, retry_count: int = 3):
        # Define connection parameters explicitly
        connection_params = {
            "host": host,
            "port": port,
            "db": db,
            "decode_responses": True,
            "retry_on_timeout": True
        }
        
        self.client = redis.Redis(**connection_params)
    
    def get(self, key: str, default: Any = None) -> Optional[str]:
        """Get value from Redis with error handling"""
        try:
            value = self.client.get(key)
            return value if value is not None else default
        except redis.RedisError as e:
            logging.error(f"Redis get error for key {key}: {e}")
            return default
            
    def set(self, key: str, value: Union[str, dict, list], 
            expiry: Optional[int] = None) -> bool:
        """Set value in Redis with error handling"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return bool(self.client.set(key, value, ex=expiry))
        except redis.RedisError as e:
            logging.error(f"Redis set error for key {key}: {e}")
            return False
    
    def lrange(self, key: str, start: int, end: int) -> List[str]:
        """
        Get a range of elements from a Redis list.
        
        Args:
            key: Redis key
            start: Start index
            end: End index
            
        Returns:
            List of elements
        """
        try:
            return self.client.lrange(key, start, end)
        except RedisError as e:
            logger.error(f"Error getting range from list {key}: {e}")
            return []
    
    def hgetall(self, key: str) -> dict:
        """
        Get all fields and values from a Redis hash.
        
        Args:
            key: Redis key
            
        Returns:
            Dictionary of field-value pairs
        """
        try:
            return self.client.hgetall(key)
        except RedisError as e:
            logger.error(f"Error getting hash {key}: {e}")
            return {}
    
    def hset(self, key: str, mapping: dict) -> bool:
        """
        Set multiple fields in a Redis hash.
        
        Args:
            key: Redis key
            mapping: Dictionary of field-value pairs
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.hset(key, mapping=mapping)
            return bool(result)
        except RedisError as e:
            logger.error(f"Error setting hash {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        try:
            result = self.client.delete(key)
            return bool(result)
        except Exception as e:
            logging.error(f"Error deleting key {key}: {e}")
            return False
            
    def rpush(self, key: str, value: str) -> bool:
        """Append a value to a Redis list."""
        try:
            result = self.client.rpush(key, value)
            return bool(result)
        except Exception as e:
            logging.error(f"Error appending to list {key}: {e}")
            return False