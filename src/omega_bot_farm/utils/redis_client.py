#!/usr/bin/env python3

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


"""
Redis client wrapper for Omega Bot Farm

This module provides a Redis client wrapper for containerized bot operations.
"""

import json
import redis
import logging
import os
from typing import Dict, Any, Optional, Union

logger = logging.getLogger("redis_client")

class RedisClient:
    """Redis client wrapper for bot farm operations."""
    
    def __init__(self, host: str = None, port: int = None, db: int = 0):
        """Initialize Redis client with containerized environment support."""
        # Allow environment variable configuration for containerized deployment
        self.host = host or os.environ.get("REDIS_HOST", "localhost")
        self.port = port or int(os.environ.get("REDIS_PORT", "6379"))
        self.db = db
        
        self._client = None
        self._connect()
        
    def _connect(self):
        """Connect to Redis server."""
        try:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True
            )
            # Test connection
            self._client.ping()
            logger.info(f"Connected to Redis at {self.host}:{self.port}")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            # Provide a basic fallback for development/testing
            self._client = None
            
    def get(self, key: str) -> Optional[Dict]:
        """Get value from Redis and parse JSON."""
        if not self._client:
            logger.warning("Redis not connected, returning None")
            return None
            
        try:
            value = self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
            
    def set(self, key: str, value: Union[Dict, list, str]) -> bool:
        """Set value in Redis with JSON serialization."""
        if not self._client:
            logger.warning("Redis not connected, data not saved")
            return False
            
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self._client.set(key, value)
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
            
    def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        if not self._client:
            logger.warning("Redis not connected, key not deleted")
            return False
            
        try:
            return bool(self._client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False
            
    def publish(self, channel: str, message: Union[Dict, str]) -> int:
        """Publish message to Redis channel."""
        if not self._client:
            logger.warning("Redis not connected, message not published")
            return 0
            
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            return self._client.publish(channel, message)
        except Exception as e:
            logger.error(f"Error publishing to channel {channel}: {e}")
            return 0
            
    def keys(self, pattern: str) -> list:
        """Get keys matching pattern."""
        if not self._client:
            logger.warning("Redis not connected, returning empty list")
            return []
            
        try:
            return self._client.keys(pattern)
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []
            
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self._client:
            logger.warning("Redis not connected, returning False")
            return False
            
        try:
            return bool(self._client.exists(key))
        except Exception as e:
            logger.error(f"Error checking existence of key {key}: {e}")
            return False 