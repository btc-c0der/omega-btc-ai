import redis
import json
import logging
from typing import Any, Optional, Union
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError

class RedisConnectionManager:
    """Manages Redis connections with retries and error handling"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, 
                 db: int = 0, retry_count: int = 3):
        self.retry_strategy = Retry(
            ExponentialBackoff(),
            retries=retry_count
        )
        
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            retry_on_timeout=True,
            retry_on_error=[ConnectionError, TimeoutError],
            retry=self.retry_strategy
        )
    
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