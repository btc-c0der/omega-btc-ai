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
OMEGA BTC AI - Redis Manager
===========================

Utility module for managing Redis operations in the Trinity Brinks Matrix.
"""

import logging
from typing import Any, Optional
import json
from redis.asyncio import Redis
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Redis-Manager")

class RedisManager:
    """Manager for Redis operations in the Trinity Brinks Matrix."""
    
    def __init__(self):
        self.redis: Optional[Redis] = None
        self.redis_url = "redis://localhost:6379"
        
    async def connect(self) -> None:
        """Connect to Redis server."""
        try:
            if not self.redis:
                self.redis = Redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                await self.redis.ping()
                logger.info("✨ Connected to Redis server")
                
        except Exception as e:
            logger.error(f"❌ Error connecting to Redis: {e}")
            raise
            
    async def disconnect(self) -> None:
        """Disconnect from Redis server."""
        try:
            if self.redis:
                await self.redis.close()
                self.redis = None
                logger.info("✨ Disconnected from Redis server")
                
        except Exception as e:
            logger.error(f"❌ Error disconnecting from Redis: {e}")
            raise
            
    async def get_cached(self, key: str, default: Any = None) -> Any:
        """
        Get cached value from Redis.
        
        Args:
            key: Redis key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        try:
            if not self.redis:
                await self.connect()
                
            if not self.redis:
                return default
                
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return default
            
        except Exception as e:
            logger.error(f"❌ Error getting cached value: {e}")
            return default
            
    async def set_cached(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None
    ) -> None:
        """
        Set cached value in Redis.
        
        Args:
            key: Redis key
            value: Value to cache
            expire_seconds: Optional expiration time in seconds
        """
        try:
            if not self.redis:
                await self.connect()
                
            if not self.redis:
                return
                
            await self.redis.set(
                key,
                json.dumps(value),
                ex=expire_seconds
            )
            
        except Exception as e:
            logger.error(f"❌ Error setting cached value: {e}")
            raise
            
    async def delete_cached(self, key: str) -> None:
        """
        Delete cached value from Redis.
        
        Args:
            key: Redis key
        """
        try:
            if not self.redis:
                await self.connect()
                
            if not self.redis:
                return
                
            await self.redis.delete(key)
            
        except Exception as e:
            logger.error(f"❌ Error deleting cached value: {e}")
            raise
            
    async def clear_cache(self) -> None:
        """Clear all cached values from Redis."""
        try:
            if not self.redis:
                await self.connect()
                
            if not self.redis:
                return
                
            await self.redis.flushdb()
            logger.info("✨ Redis cache cleared")
            
        except Exception as e:
            logger.error(f"❌ Error clearing Redis cache: {e}")
            raise
