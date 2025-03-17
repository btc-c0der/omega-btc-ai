import redis
import json
import logging
import os
from typing import Any, Optional, Union
from redis.exceptions import ConnectionError, TimeoutError

class RedisConnectionManager:
    """Manages Redis connections with retries and error handling"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, 
                 db: int = 0, username: str = None, password: str = None,
                 ssl: bool = False, ssl_ca_certs: str = None):
        """
        Initialize Redis connection manager with SSL support
        
        Args:
            host: Redis host (default: localhost)
            port: Redis port (default: 6379)
            db: Redis database number (default: 0)
            username: Redis username for auth (default: None)
            password: Redis password for auth (default: None)
            ssl: Whether to use SSL/TLS (default: False)
            ssl_ca_certs: Path to CA certificate file (default: None)
        """
        # Define connection parameters explicitly
        connection_params = {
            "host": host,
            "port": port,
            "db": db,
            "decode_responses": True,
            "retry_on_timeout": True
        }
        
        # Add authentication if provided
        if username:
            connection_params["username"] = username
        if password:
            connection_params["password"] = password
            
        # Add SSL/TLS parameters if enabled
        if ssl:
            connection_params["ssl"] = True
            if ssl_ca_certs:
                connection_params["ssl_ca_certs"] = ssl_ca_certs
        
        try:
            self.client = redis.Redis(**connection_params)
            # Test connection
            self.client.ping()
            logging.info(f"Redis connection successful - Host: {host}, Port: {port}, SSL: {ssl}")
        except Exception as e:
            logging.error(f"Redis connection failed: {e}")
            raise
    
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

# Use configuration from redis_manager
def get_connection_from_env():
    """Create a RedisConnectionManager using environment variables"""
    from omega_ai.utils.redis_manager import get_redis_config
    
    config = get_redis_config()
    return RedisConnectionManager(**config)