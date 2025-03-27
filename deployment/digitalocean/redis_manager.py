import os
import redis
import logging
from typing import Optional, Union
from redis.exceptions import ConnectionError, TimeoutError
import time
from datetime import datetime, UTC

class DigitalOceanRedisManager:
    """Redis manager with SSL support for DigitalOcean deployment."""
    
    def __init__(self, max_retries: int = 5, retry_delay: int = 5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.redis_client: Optional[redis.Redis] = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to Redis with retry logic."""
        retries = 0
        while retries < self.max_retries:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    password=os.getenv('REDIS_PASSWORD'),
                    ssl=True,  # Enable SSL for secure connection
                    ssl_cert_reqs=None,  # Skip certificate verification for now
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
                # Test connection
                self.redis_client.ping()
                logging.info(f"Successfully connected to Redis at {os.getenv('REDIS_HOST')}")
                return
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Failed to connect to Redis after {self.max_retries} attempts: {str(e)}")
                    raise
                logging.warning(f"Redis connection attempt {retries} failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
    
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis with retry logic."""
        if not self.redis_client:
            return None
            
        retries = 0
        while retries < self.max_retries:
            try:
                return self.redis_client.get(key)
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Failed to get key {key} after {self.max_retries} attempts: {str(e)}")
                    return None
                logging.warning(f"Redis get attempt {retries} failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                self._connect()  # Try to reconnect
        return None
    
    def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """Set value in Redis with retry logic."""
        if not self.redis_client:
            return False
            
        retries = 0
        while retries < self.max_retries:
            try:
                result = self.redis_client.set(key, value, ex=expire)
                return bool(result)
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Failed to set key {key} after {self.max_retries} attempts: {str(e)}")
                    return False
                logging.warning(f"Redis set attempt {retries} failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                self._connect()  # Try to reconnect
        return False
    
    def publish(self, channel: str, message: str) -> bool:
        """Publish message to Redis channel with retry logic."""
        if not self.redis_client:
            return False
            
        retries = 0
        while retries < self.max_retries:
            try:
                result = self.redis_client.publish(channel, message)
                return bool(result)
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Failed to publish to channel {channel} after {self.max_retries} attempts: {str(e)}")
                    return False
                logging.warning(f"Redis publish attempt {retries} failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                self._connect()  # Try to reconnect
        return False
    
    def subscribe(self, channel: str) -> Optional[redis.client.PubSub]:
        """Subscribe to Redis channel with retry logic."""
        if not self.redis_client:
            return None
            
        retries = 0
        while retries < self.max_retries:
            try:
                pubsub = self.redis_client.pubsub()
                pubsub.subscribe(channel)
                return pubsub
            except (ConnectionError, TimeoutError) as e:
                retries += 1
                if retries == self.max_retries:
                    logging.error(f"Failed to subscribe to channel {channel} after {self.max_retries} attempts: {str(e)}")
                    return None
                logging.warning(f"Redis subscribe attempt {retries} failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                self._connect()  # Try to reconnect
        return None
    
    def close(self) -> None:
        """Close Redis connection."""
        if self.redis_client:
            try:
                self.redis_client.close()
            except Exception as e:
                logging.error(f"Error closing Redis connection: {str(e)}") 