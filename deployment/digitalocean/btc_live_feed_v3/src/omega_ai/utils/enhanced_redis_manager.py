#!/usr/bin/env python3
"""
OMEGA BTC AI - Enhanced Redis Manager
=====================================

Redis manager with automatic failover between remote and local Redis instances.
Provides connection management, error recovery, and data synchronization.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.
"""

import os
import time
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Union, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhanced-redis-manager")

# Try importing Redis, providing informative error if not available
try:
    import redis.asyncio as redis
except ImportError:
    logger.error("Redis not found. Install with 'pip install redis'")
    raise

# Constants
LOG_PREFIX = "🔱 REDIS MANAGER"
DEFAULT_REDIS_PORT = 6379
DEFAULT_RETRY_INTERVAL = 60  # seconds
DEFAULT_BATCH_SIZE = 100  # keys to sync at once

class EnhancedRedisManager:
    """
    Enhanced Redis Manager with automatic failover between remote and local instances.
    
    Provides resilient Redis operations with configurable failover behavior and 
    data synchronization strategies. Can operate in various modes:
    - Remote only: Uses only the remote Redis connection
    - Local only: Uses only the local Redis connection
    - Auto-failover: Uses remote Redis by default, but fails over to local Redis if remote is unavailable
    - Dual-write: Writes to both remote and local Redis for critical data
    
    Features:
    - Automatic connection management
    - Seamless failover between remote and local Redis
    - Data synchronization when connections are restored
    - Comprehensive health monitoring and statistics
    """
    
    def __init__(
        self,
        use_failover: bool = True,
        sync_on_reconnect: bool = True,
        retry_interval: int = DEFAULT_RETRY_INTERVAL,
        priority_keys: Optional[List[str]] = None
    ):
        """
        Initialize the Enhanced Redis Manager.
        
        Args:
            use_failover: Whether to use failover to local Redis if remote fails
            sync_on_reconnect: Whether to sync data when reconnecting to remote Redis
            retry_interval: Seconds to wait between reconnection attempts
            priority_keys: List of keys to prioritize during sync operations
        """
        # Configuration
        self.use_failover = use_failover
        self.sync_on_reconnect = sync_on_reconnect
        self.retry_interval = retry_interval
        self.priority_keys = priority_keys or []
        
        # Redis clients
        self.primary_redis = None   # Remote Redis client
        self.failover_redis = None  # Local Redis client
        self.current_redis = None   # Currently active Redis client
        
        # Connection state
        self.primary_connected = False
        self.failover_connected = False
        self.using_failover = False
        self.last_failover_time = None
        self.reconnection_attempts = 0
        
        # Logging prefix for this instance
        self.log_prefix = f"{LOG_PREFIX}"
        
        # Get connection parameters from environment
        self.primary_host = os.getenv("REDIS_HOST")
        self.primary_port = int(os.getenv("REDIS_PORT", DEFAULT_REDIS_PORT))
        self.primary_password = os.getenv("REDIS_PASSWORD")
        self.primary_username = os.getenv("REDIS_USERNAME")
        self.primary_use_ssl = os.getenv("REDIS_USE_TLS", "false").lower() in ("true", "1", "yes")
        self.primary_ssl_cert_reqs = os.getenv("REDIS_SSL_CERT_REQS", "none")
        
        # Failover (local) connection parameters
        self.failover_host = os.getenv("FAILOVER_REDIS_HOST", "localhost")
        self.failover_port = int(os.getenv("FAILOVER_REDIS_PORT", DEFAULT_REDIS_PORT))
        self.failover_password = os.getenv("FAILOVER_REDIS_PASSWORD")
        self.failover_username = os.getenv("FAILOVER_REDIS_USERNAME")
        
        # Log configuration
        logger.info(f"{self.log_prefix} - Initializing Enhanced Redis Manager")
        logger.info(f"{self.log_prefix} - Primary Redis: {self.primary_host}:{self.primary_port}")
        logger.info(f"{self.log_prefix} - Failover Redis: {self.failover_host}:{self.failover_port}")
        logger.info(f"{self.log_prefix} - Failover Enabled: {self.use_failover}")
        logger.info(f"{self.log_prefix} - Sync on Reconnect: {self.sync_on_reconnect}")
    
    async def connect(self) -> bool:
        """
        Connect to primary and failover Redis instances.
        
        Returns:
            bool: True if connected to at least one Redis instance
        """
        # Connect to primary Redis
        primary_connected = await self._connect_primary()
        
        # If failover is enabled, connect to failover Redis
        failover_connected = False
        if self.use_failover:
            failover_connected = await self._connect_failover()
        
        # Determine which Redis to use
        if primary_connected:
            self.current_redis = self.primary_redis
            self.using_failover = False
            logger.info(f"{self.log_prefix} - Using primary Redis")
        elif failover_connected and self.use_failover:
            self.current_redis = self.failover_redis
            self.using_failover = True
            self.last_failover_time = time.time()
            logger.info(f"{self.log_prefix} - Using failover Redis")
        else:
            self.current_redis = None
            logger.error(f"{self.log_prefix} - Failed to connect to any Redis instance")
            return False
        
        return True
    
    async def _connect_primary(self) -> bool:
        """
        Connect to primary (remote) Redis instance.
        
        Returns:
            bool: True if connected successfully
        """
        if not self.primary_host:
            logger.warning(f"{self.log_prefix} - Primary Redis host not configured, skipping connection")
            return False
        
        try:
            # Close existing connection if any
            if self.primary_redis:
                await self.primary_redis.close()
            
            # Create new connection
            logger.info(f"{self.log_prefix} - Connecting to primary Redis at {self.primary_host}:{self.primary_port}")
            logger.info(f"{self.log_prefix} - SSL enabled: {self.primary_use_ssl}, SSL cert reqs: {self.primary_ssl_cert_reqs}")
            
            # Prepare connection parameters
            redis_kwargs = {
                "host": self.primary_host,
                "port": self.primary_port,
                "decode_responses": True,
                "socket_timeout": 10.0,  # Increased timeout for debugging
                "socket_connect_timeout": 10.0  # Increased timeout for debugging
            }
            
            # Add optional parameters
            if self.primary_password:
                redis_kwargs["password"] = self.primary_password
                logger.info(f"{self.log_prefix} - Using password authentication")
            
            if self.primary_username:
                redis_kwargs["username"] = self.primary_username
                logger.info(f"{self.log_prefix} - Using username: {self.primary_username}")
                
            if self.primary_use_ssl:
                redis_kwargs["ssl"] = True
                
                # Set SSL certificate requirements based on configuration
                if self.primary_ssl_cert_reqs == "none":
                    redis_kwargs["ssl_cert_reqs"] = None
                    logger.info(f"{self.log_prefix} - SSL cert_reqs set to None")
                elif self.primary_ssl_cert_reqs == "optional":
                    redis_kwargs["ssl_cert_reqs"] = "optional"
                    logger.info(f"{self.log_prefix} - SSL cert_reqs set to optional")
                elif self.primary_ssl_cert_reqs == "required":
                    redis_kwargs["ssl_cert_reqs"] = "required"
                    logger.info(f"{self.log_prefix} - SSL cert_reqs set to required")
                else:
                    # Default to None for DigitalOcean Redis
                    redis_kwargs["ssl_cert_reqs"] = None
                    logger.info(f"{self.log_prefix} - SSL cert_reqs defaulting to None")
            
            # Create Redis client
            logger.info(f"{self.log_prefix} - Creating Redis client with parameters: host={self.primary_host}, port={self.primary_port}, ssl={self.primary_use_ssl}")
            self.primary_redis = redis.Redis(**redis_kwargs)
            
            # Test connection
            logger.info(f"{self.log_prefix} - Testing connection with PING command")
            ping_result = await self.primary_redis.ping()
            self.primary_connected = (ping_result == True)
            
            if self.primary_connected:
                logger.info(f"{self.log_prefix} - Successfully connected to primary Redis")
            else:
                logger.warning(f"{self.log_prefix} - Primary Redis ping failed")
            
            return self.primary_connected
            
        except Exception as e:
            logger.error(f"{self.log_prefix} - Failed to connect to primary Redis: {str(e)}")
            logger.error(f"{self.log_prefix} - Connection details: host={self.primary_host}, port={self.primary_port}, username={self.primary_username}, SSL={self.primary_use_ssl}")
            logger.error(f"{self.log_prefix} - Error type: {type(e).__name__}")
            self.primary_connected = False
            self.primary_redis = None
            return False
    
    async def _connect_failover(self) -> bool:
        """
        Connect to failover (local) Redis instance.
        
        Returns:
            bool: True if connected successfully
        """
        try:
            # Close existing connection if any
            if self.failover_redis:
                await self.failover_redis.close()
            
            # Create new connection
            logger.info(f"{self.log_prefix} - Connecting to failover Redis at {self.failover_host}:{self.failover_port}")
            
            # Prepare connection parameters
            redis_kwargs = {
                "host": self.failover_host,
                "port": self.failover_port,
                "decode_responses": True,
                "socket_timeout": 3.0,
                "socket_connect_timeout": 3.0
            }
            
            # Add optional parameters
            if self.failover_password:
                redis_kwargs["password"] = self.failover_password
            
            if self.failover_username:
                redis_kwargs["username"] = self.failover_username
            
            # Create Redis client
            self.failover_redis = redis.Redis(**redis_kwargs)
            
            # Test connection
            ping_result = await self.failover_redis.ping()
            self.failover_connected = (ping_result == True)
            
            if self.failover_connected:
                logger.info(f"{self.log_prefix} - Successfully connected to failover Redis")
            else:
                logger.warning(f"{self.log_prefix} - Failover Redis ping failed")
            
            return self.failover_connected
            
        except Exception as e:
            logger.error(f"{self.log_prefix} - Failed to connect to failover Redis: {str(e)}")
            self.failover_connected = False
            self.failover_redis = None
            return False
    
    async def try_reconnect_primary(self) -> bool:
        """
        Attempt to reconnect to primary Redis if disconnected.
        
        Returns:
            bool: True if reconnected successfully
        """
        if self.primary_connected:
            return True
        
        # Increment reconnection attempts
        self.reconnection_attempts += 1
        
        # Reconnect to primary
        reconnected = await self._connect_primary()
        
        if reconnected:
            logger.info(f"{self.log_prefix} - Reconnected to primary Redis")
            
            # If currently using failover, switch back to primary
            if self.using_failover and self.current_redis != self.primary_redis:
                logger.info(f"{self.log_prefix} - Switching from failover to primary Redis")
                self.current_redis = self.primary_redis
                self.using_failover = False
                
                # Sync data if configured
                if self.sync_on_reconnect and self.failover_connected:
                    await self._sync_data_to_primary()
        
        return reconnected
    
    async def _sync_data_to_primary(self) -> None:
        """Synchronize data from failover Redis to primary Redis."""
        if not self.primary_connected or not self.failover_connected:
            logger.warning(f"{self.log_prefix} - Cannot sync: not connected to both Redis instances")
            return
        
        try:
            logger.info(f"{self.log_prefix} - Starting data synchronization from failover to primary")
            
            # First, sync priority keys
            for key in self.priority_keys:
                await self._sync_key(key)
            
            # Then sync all other keys
            cursor = "0"
            while cursor != 0:
                cursor, keys = await self.failover_redis.scan(cursor=cursor, count=DEFAULT_BATCH_SIZE)
                for key in keys:
                    # Skip keys already synced
                    if key in self.priority_keys:
                        continue
                    await self._sync_key(key)
            
            logger.info(f"{self.log_prefix} - Data synchronization completed")
            
        except Exception as e:
            logger.error(f"{self.log_prefix} - Data synchronization failed: {str(e)}")
    
    async def _sync_key(self, key: str) -> None:
        """
        Synchronize a single key from failover to primary Redis.
        
        Args:
            key: The key to synchronize
        """
        try:
            # Check if key exists in failover Redis
            if not await self.failover_redis.exists(key):
                return
            
            # Get key type
            key_type = await self.failover_redis.type(key)
            
            # Handle different data types
            if key_type == "string":
                value = await self.failover_redis.get(key)
                if value:
                    await self.primary_redis.set(key, value)
            
            elif key_type == "list":
                values = await self.failover_redis.lrange(key, 0, -1)
                if values:
                    # Delete existing list and recreate
                    await self.primary_redis.delete(key)
                    await self.primary_redis.rpush(key, *values)
            
            elif key_type == "hash":
                values = await self.failover_redis.hgetall(key)
                if values:
                    await self.primary_redis.hmset(key, values)
            
            elif key_type == "set":
                members = await self.failover_redis.smembers(key)
                if members:
                    # Delete existing set and recreate
                    await self.primary_redis.delete(key)
                    await self.primary_redis.sadd(key, *members)
            
            elif key_type == "zset":
                # Get all members with scores
                members_with_scores = await self.failover_redis.zrange(key, 0, -1, withscores=True)
                if members_with_scores:
                    # Delete existing sorted set and recreate
                    await self.primary_redis.delete(key)
                    for member, score in members_with_scores:
                        await self.primary_redis.zadd(key, {member: score})
            
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Failed to sync key {key}: {str(e)}")
    
    async def ping(self) -> bool:
        """
        Ping the current Redis instance and handle failover if needed.
        
        Returns:
            bool: True if ping successful
        """
        # If no Redis is connected, try to connect
        if not self.current_redis:
            return await self.connect()
        
        try:
            # Try to ping current Redis
            result = await self.current_redis.ping()
            
            # If using primary and ping fails, try failover
            if not result and self.current_redis == self.primary_redis and self.use_failover:
                logger.warning(f"{self.log_prefix} - Primary Redis ping failed, switching to failover")
                self.primary_connected = False
                
                # Try to connect to failover if not already connected
                if not self.failover_connected:
                    await self._connect_failover()
                
                # If failover is connected, use it
                if self.failover_connected:
                    self.current_redis = self.failover_redis
                    self.using_failover = True
                    self.last_failover_time = time.time()
                    logger.info(f"{self.log_prefix} - Switched to failover Redis")
                    return True
                else:
                    self.current_redis = None
                    logger.error(f"{self.log_prefix} - Both primary and failover Redis are unavailable")
                    return False
            
            return result
            
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Ping failed: {str(e)}")
            
            # If using primary and it fails, try failover
            if self.current_redis == self.primary_redis and self.use_failover:
                self.primary_connected = False
                
                # Try to connect to failover if not already connected
                if not self.failover_connected:
                    await self._connect_failover()
                
                # If failover is connected, use it
                if self.failover_connected:
                    self.current_redis = self.failover_redis
                    self.using_failover = True
                    self.last_failover_time = time.time()
                    logger.info(f"{self.log_prefix} - Switched to failover Redis after error")
                    return True
            
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about Redis connections.
        
        Returns:
            Dict containing Redis connection statistics
        """
        # Check connection status
        if self.primary_redis:
            try:
                self.primary_connected = await self.primary_redis.ping()
            except:
                self.primary_connected = False
        
        if self.failover_redis:
            try:
                self.failover_connected = await self.failover_redis.ping()
            except:
                self.failover_connected = False
        
        # Return stats
        return {
            "primary_available": self.primary_connected,
            "failover_available": self.failover_connected,
            "using_failover": self.using_failover,
            "last_failover_time": self.last_failover_time,
            "reconnection_attempts": self.reconnection_attempts,
            "failover_enabled": self.use_failover,
            "sync_on_reconnect": self.sync_on_reconnect
        }
    
    # Redis wrapper methods with automatic failover
    
    async def get_cached(self, key: str) -> Optional[str]:
        """
        Get a cached value with automatic failover.
        
        Args:
            key: Redis key to retrieve
            
        Returns:
            The cached value, or None if not found or error
        """
        # Ensure we have a Redis connection
        if not await self.ping():
            logger.warning(f"{self.log_prefix} - Cannot get {key}: No Redis connection")
            return None
        
        try:
            return await self.current_redis.get(key)
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Error getting {key}: {str(e)}")
            return None
    
    async def set_cached(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """
        Set a cached value with automatic failover.
        
        Args:
            key: Redis key to set
            value: Value to cache
            ex: Optional expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        # Ensure we have a Redis connection
        if not await self.ping():
            logger.warning(f"{self.log_prefix} - Cannot set {key}: No Redis connection")
            return False
        
        try:
            return await self.current_redis.set(key, value, ex=ex)
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Error setting {key}: {str(e)}")
            return False
    
    async def publish(self, channel: str, message: str) -> int:
        """
        Publish a message to a Redis channel with automatic failover.
        
        Args:
            channel: Redis channel to publish to
            message: Message to publish
            
        Returns:
            Number of clients that received the message, or 0 on error
        """
        # Ensure we have a Redis connection
        if not await self.ping():
            logger.warning(f"{self.log_prefix} - Cannot publish to {channel}: No Redis connection")
            return 0
        
        try:
            return await self.current_redis.publish(channel, message)
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Error publishing to {channel}: {str(e)}")
            return 0
    
    async def lpush(self, key: str, value: str) -> int:
        """
        Push a value to the left of a list with automatic failover.
        
        Args:
            key: Redis list key
            value: Value to push
            
        Returns:
            Length of the list after the push, or 0 on error
        """
        # Ensure we have a Redis connection
        if not await self.ping():
            logger.warning(f"{self.log_prefix} - Cannot lpush to {key}: No Redis connection")
            return 0
        
        try:
            return await self.current_redis.lpush(key, value)
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Error pushing to {key}: {str(e)}")
            return 0
    
    async def ltrim(self, key: str, start: int, end: int) -> bool:
        """
        Trim a list to the specified range with automatic failover.
        
        Args:
            key: Redis list key
            start: Start index
            end: End index
            
        Returns:
            True if successful, False otherwise
        """
        # Ensure we have a Redis connection
        if not await self.ping():
            logger.warning(f"{self.log_prefix} - Cannot trim {key}: No Redis connection")
            return False
        
        try:
            return await self.current_redis.ltrim(key, start, end)
        except Exception as e:
            logger.warning(f"{self.log_prefix} - Error trimming {key}: {str(e)}")
            return False
    
    async def close(self) -> None:
        """Close all Redis connections."""
        if self.primary_redis:
            try:
                await self.primary_redis.close()
                logger.info(f"{self.log_prefix} - Closed primary Redis connection")
            except Exception as e:
                logger.warning(f"{self.log_prefix} - Error closing primary Redis: {str(e)}")
        
        if self.failover_redis:
            try:
                await self.failover_redis.close()
                logger.info(f"{self.log_prefix} - Closed failover Redis connection")
            except Exception as e:
                logger.warning(f"{self.log_prefix} - Error closing failover Redis: {str(e)}")
        
        self.primary_redis = None
        self.failover_redis = None
        self.current_redis = None
        self.primary_connected = False
        self.failover_connected = False 