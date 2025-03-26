#!/usr/bin/env python3
"""
redis_manager_cloud.py - Redis Manager for Cloud Deployment
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This module provides a Redis manager for Scaleway cloud deployment with TLS support.
It also supports local testing without TLS.
"""

import os
import json
import time
import redis
import logging
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('redis_manager')

class RedisManager:
    """
    Redis Manager for cloud deployment with TLS support.
    Provides a common interface for TLS and non-TLS Redis connections.
    """
    
    def __init__(self, 
                 host: str = 'localhost', 
                 port: int = 6379, 
                 username: Optional[str] = None, 
                 password: Optional[str] = None,
                 ssl: bool = False,
                 ssl_ca_certs: Optional[str] = None,
                 db: int = 0,
                 max_retries: int = 5,
                 retry_delay: int = 3):
        """
        Initialize the Redis Manager.
        
        Args:
            host: Redis host
            port: Redis port
            username: Redis username (if authentication is enabled)
            password: Redis password (if authentication is enabled)
            ssl: Whether to use SSL/TLS
            ssl_ca_certs: Path to SSL CA certificate file
            db: Redis database number
            max_retries: Maximum number of connection retries
            retry_delay: Delay in seconds between retries
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl
        self.ssl_ca_certs = ssl_ca_certs
        self.db = db
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.conn: Optional[redis.Redis] = None
        
        # Display connection details (without password)
        conn_str = f"Redis connection: {host}:{port}"
        if username:
            conn_str += f" (with auth)"
        if ssl:
            conn_str += f" (SSL: {ssl_ca_certs})"
        logger.info(conn_str)
        
        # Connect to Redis
        self.connect()
    
    def connect(self) -> None:
        """Connect to Redis with automatic retry."""
        retries = 0
        while retries < self.max_retries:
            try:
                # Connection parameters
                params = {
                    'host': self.host,
                    'port': self.port,
                    'db': self.db,
                    'socket_timeout': 5,
                    'decode_responses': True
                }
                
                # Add authentication if provided
                if self.username:
                    params['username'] = self.username
                if self.password:
                    params['password'] = self.password
                
                # Add SSL/TLS if enabled
                if self.ssl:
                    params['ssl'] = True
                    if self.ssl_ca_certs:
                        params['ssl_ca_certs'] = self.ssl_ca_certs
                    logger.info("Using SSL for Redis connection")
                
                # Create connection
                self.conn = redis.Redis(**params)
                
                # Test connection
                if not self.conn.ping():
                    raise redis.exceptions.ConnectionError("Ping failed")
                    
                logger.info("Successfully connected to Redis")
                return
                
            except redis.exceptions.RedisError as e:
                retries += 1
                logger.error(f"Redis connection error (attempt {retries}/{self.max_retries}): {e}")
                
                if retries >= self.max_retries:
                    logger.error("Failed to connect to Redis after multiple attempts")
                    # Reset connection to None
                    self.conn = None
                    raise
                    
                time.sleep(self.retry_delay)
    
    def ping(self) -> bool:
        """
        Check Redis connection.
        
        Returns:
            True if connection is active, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                    
            return bool(self.conn.ping())
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis ping error: {e}")
            return False
    
    def get(self, key: str) -> Optional[str]:
        """
        Get a value from Redis.
        
        Args:
            key: The key to get
            
        Returns:
            The value for the key, or None if it doesn't exist
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return None
                    
            return self.conn.get(key)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis get error for key '{key}': {e}")
            return None
    
    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        Set a value in Redis.
        
        Args:
            key: The key to set
            value: The value to set (will be converted to string if not already)
            ex: Expiration time in seconds (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                
            # Convert value to string if it's not already
            if not isinstance(value, str):
                value = str(value)
                
            result = self.conn.set(key, value, ex=ex)
            return bool(result)  # Convert None to False
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis set error for key '{key}': {e}")
            return False
    
    def set_cached(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Alias for set() for backward compatibility."""
        return self.set(key, value, ex)
    
    def get_cached(self, key: str) -> Optional[str]:
        """Alias for get() for backward compatibility."""
        return self.get(key)
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.
        
        Args:
            key: The key to delete
            
        Returns:
            True if key was deleted, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                    
            result = self.conn.delete(key)
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis delete error for key '{key}': {e}")
            return False
    
    def lpush(self, key: str, value: Any) -> bool:
        """
        Push a value to a Redis list (left push).
        
        Args:
            key: The list key
            value: The value to push
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                
            # Convert value to string if it's not already
            if not isinstance(value, str):
                value = str(value)
                
            result = self.conn.lpush(key, value)
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis lpush error for key '{key}': {e}")
            return False
    
    def rpush(self, key: str, value: Any) -> bool:
        """
        Push a value to a Redis list (right push).
        
        Args:
            key: The list key
            value: The value to push
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                
            # Convert value to string if it's not already
            if not isinstance(value, str):
                value = str(value)
                
            result = self.conn.rpush(key, value)
            return bool(result)
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis rpush error for key '{key}': {e}")
            return False
    
    def ltrim(self, key: str, start: int, end: int) -> bool:
        """
        Trim a Redis list to the specified range.
        
        Args:
            key: The list key
            start: The start index
            end: The end index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return False
                    
            result = self.conn.ltrim(key, start, end)
            return result is True  # Redis returns True for ltrim
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis ltrim error for key '{key}': {e}")
            return False
    
    def lrange(self, key: str, start: int, end: int) -> List[str]:
        """
        Get a range of elements from a Redis list.
        
        Args:
            key: The list key
            start: The start index
            end: The end index
            
        Returns:
            List of elements, or empty list if key doesn't exist
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return []
                    
            result = self.conn.lrange(key, start, end)
            return result if result else []
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis lrange error for key '{key}': {e}")
            return []
            
    def keys(self, pattern: str) -> List[str]:
        """
        Find keys matching a pattern.
        
        Args:
            pattern: Pattern to match keys against
            
        Returns:
            List of matching keys, or empty list on error
        """
        try:
            if self.conn is None:
                self.connect()
                if self.conn is None:  # If connect failed
                    return []
                    
            result = self.conn.keys(pattern)
            return result if result else []
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis keys error for pattern '{pattern}': {e}")
            return []

# Example usage
if __name__ == "__main__":
    # This code only runs when you execute this file directly
    # It will not run when imported as a module
    
    # Get Redis connection details from environment variables or use defaults
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))
    redis_username = os.environ.get('REDIS_USERNAME')
    redis_password = os.environ.get('REDIS_PASSWORD')
    redis_ssl = os.environ.get('REDIS_USE_TLS', 'false').lower() == 'true'
    redis_cert = os.environ.get('REDIS_CERT')
    
    logger.info(f"Testing Redis connection to {redis_host}:{redis_port}")
    
    # Create Redis manager
    try:
        redis_mgr = RedisManager(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            ssl=redis_ssl,
            ssl_ca_certs=redis_cert if redis_ssl else None
        )
        
        # Test ping
        if redis_mgr.ping():
            logger.info("Redis ping successful!")
            
            # Set a test value
            test_key = "test:redis_manager"
            test_value = f"Connection test at {time.time()}"
            if redis_mgr.set(test_key, test_value):
                logger.info(f"Set test key: {test_key}")
                
                # Get the test value
                retrieved = redis_mgr.get(test_key)
                if retrieved == test_value:
                    logger.info(f"Retrieved test key successfully: {retrieved}")
                else:
                    logger.error(f"Retrieved value doesn't match: {retrieved}")
                
                # Clean up
                if redis_mgr.delete(test_key):
                    logger.info(f"Deleted test key: {test_key}")
                else:
                    logger.error(f"Failed to delete test key: {test_key}")
            else:
                logger.error("Failed to set test key")
        else:
            logger.error("Redis ping failed")
    except Exception as e:
        logger.error(f"Error testing Redis connection: {e}") 