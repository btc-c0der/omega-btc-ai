#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""AIXBT Interface Redis Manager.

Enhanced Redis management for AIXBT Interface with features:
1. Connection pooling and failover
2. Advanced data serialization
3. Real-time market data handling
4. Health monitoring
5. Memory optimization
6. Performance tracking
"""

import os
import json
import logging
import asyncio
from typing import Optional, Dict, List, Any, Union
from datetime import datetime, UTC
from dataclasses import dataclass
from redis import Redis, ConnectionPool, ResponseError
from redis.asyncio import Redis as AsyncRedis
from redis.asyncio.connection import ConnectionPool as AsyncConnectionPool
from redis.exceptions import RedisError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt-redis")

@dataclass
class RedisConfig:
    """Redis configuration for AIXBT interface."""
    host: str = os.getenv('REDIS_HOST', 'localhost')
    port: int = int(os.getenv('REDIS_PORT', '6379'))
    db: int = int(os.getenv('REDIS_DB', '0'))
    password: Optional[str] = os.getenv('REDIS_PASSWORD')
    ssl: bool = os.getenv('REDIS_SSL', 'false').lower() == 'true'
    pool_size: int = int(os.getenv('REDIS_POOL_SIZE', '10'))
    pool_timeout: int = int(os.getenv('REDIS_POOL_TIMEOUT', '20'))
    decode_responses: bool = True
    max_connections: int = int(os.getenv('REDIS_MAX_CONNECTIONS', '50'))

class AIXBTRedisManager:
    """Enhanced Redis Manager for AIXBT Interface."""
    
    def __init__(self, config: Optional[RedisConfig] = None, use_fallback: bool = True):
        """Initialize Redis manager with optional fallback to local instance."""
        self.config = config or RedisConfig()
        self.use_fallback = use_fallback
        self.pool = None
        self.async_pool = None
        self.is_fallback = False
        self._initialize_pools()

    def _initialize_pools(self) -> None:
        """Initialize Redis connection pools with fallback support."""
        try:
            # Try primary configuration
            self._create_pools(
                self.config.host,
                self.config.port,
                self.config.password,
                self.config.ssl
            )
            logger.info(f"Connected to Redis at {self.config.host}:{self.config.port}")
            
        except Exception as e:
            logger.warning(f"Failed to connect to primary Redis: {str(e)}")
            if self.use_fallback:
                try:
                    # Fallback to localhost
                    self._create_pools("localhost", 6379, None, False)
                    self.is_fallback = True
                    logger.info("Connected to fallback local Redis instance")
                except Exception as fallback_error:
                    logger.error(f"Fallback Redis connection failed: {str(fallback_error)}")
                    raise

    def _create_pools(self, host: str, port: int, password: Optional[str], ssl: bool) -> None:
        """Create Redis connection pools."""
        self.pool = ConnectionPool(
            host=host,
            port=port,
            db=self.config.db,
            password=password,
            ssl=ssl,
            max_connections=self.config.max_connections,
            decode_responses=self.config.decode_responses
        )
        
        self.async_pool = AsyncConnectionPool(
            host=host,
            port=port,
            db=self.config.db,
            password=password,
            ssl=ssl,
            max_connections=self.config.max_connections,
            decode_responses=self.config.decode_responses
        )

    def get_client(self) -> Redis:
        """Get a synchronous Redis client."""
        return Redis(connection_pool=self.pool)

    async def get_async_client(self) -> AsyncRedis:
        """Get an asynchronous Redis client."""
        return AsyncRedis(connection_pool=self.async_pool)

    async def set_market_data(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set market data with optional expiration."""
        try:
            async with await self.get_async_client() as client:
                serialized = json.dumps(value)
                await client.set(key, serialized)
                if expire:
                    await client.expire(key, expire)
                return True
        except RedisError as e:
            logger.error(f"Failed to set market data: {str(e)}")
            return False

    async def get_market_data(self, key: str) -> Optional[Any]:
        """Get market data with deserialization."""
        try:
            async with await self.get_async_client() as client:
                value = await client.get(key)
                return json.loads(value) if value else None
        except RedisError as e:
            logger.error(f"Failed to get market data: {str(e)}")
            return None

    async def publish_price_update(self, data: Dict[str, Any]) -> bool:
        """Publish price update to AIXBT channel."""
        try:
            async with await self.get_async_client() as client:
                channel = "aixbt:price_updates"
                await client.publish(channel, json.dumps(data))
                return True
        except RedisError as e:
            logger.error(f"Failed to publish price update: {str(e)}")
            return False

    async def subscribe_to_updates(self, callback) -> None:
        """Subscribe to AIXBT price updates."""
        try:
            async with await self.get_async_client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe("aixbt:price_updates")
                
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:
                        try:
                            data = json.loads(message['data'])
                            await callback(data)
                        except Exception as e:
                            logger.error(f"Failed to process update: {str(e)}")
                    await asyncio.sleep(0.1)
                    
        except RedisError as e:
            logger.error(f"Subscription error: {str(e)}")
            raise

    async def get_system_status(self) -> Dict[str, Any]:
        """Get AIXBT system status including Redis health."""
        try:
            async with await self.get_async_client() as client:
                # Check Redis health
                await client.ping()
                info = await client.info()
                
                return {
                    "status": "operational",
                    "redis_connected": True,
                    "using_fallback": self.is_fallback,
                    "connected_clients": info.get('connected_clients', 0),
                    "memory_usage": info.get('used_memory_human', '0B'),
                    "uptime_seconds": info.get('uptime_in_seconds', 0),
                    "timestamp": datetime.now(UTC).isoformat()
                }
        except RedisError as e:
            return {
                "status": "degraded",
                "redis_connected": False,
                "error": str(e),
                "using_fallback": self.is_fallback,
                "timestamp": datetime.now(UTC).isoformat()
            }

    async def optimize_storage(self) -> Dict[str, Any]:
        """Optimize Redis storage for AIXBT data."""
        try:
            async with await self.get_async_client() as client:
                before = await client.info(section='memory')
                
                # Clean up expired keys
                await client.execute_command('MEMORY PURGE')
                
                # Get post-optimization stats
                after = await client.info(section='memory')
                
                return {
                    "status": "optimized",
                    "memory_before": before.get('used_memory_human', '0B'),
                    "memory_after": after.get('used_memory_human', '0B'),
                    "timestamp": datetime.now(UTC).isoformat()
                }
        except RedisError as e:
            logger.error(f"Storage optimization failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat()
            }

    async def close(self) -> None:
        """Close Redis connections."""
        try:
            if self.pool:
                self.pool.disconnect()
            if self.async_pool:
                await self.async_pool.disconnect()
            logger.info("Redis connections closed")
        except Exception as e:
            logger.error(f"Failed to close Redis connections: {str(e)}")
            raise

# Global Redis manager instance
aixbt_redis = AIXBTRedisManager()