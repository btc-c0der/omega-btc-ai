
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
Async Redis Manager for OMEGA BTC AI
=================================

Provides an asynchronous Redis connection manager with features like:
- Connection pooling
- Local caching with TTL
- Data validation
- Graceful shutdown
- Automatic reconnection
- SSL/TLS support
"""

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
import signal
import sys
from typing import Optional, Dict, Any, Union, Tuple, Type
import json
import time
import logging
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)

def retry_on_connection_error(max_retries: int = 3, delay: float = 1.0):
    """Decorator for async Redis operations with retry logic."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (redis.ConnectionError, redis.TimeoutError) as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))
            logger.error(f"Redis operation failed after {max_retries} attempts: {last_error}")
            if last_error:
                raise last_error
            raise redis.ConnectionError("Max retries exceeded")
        return wrapper
    return decorator

class AsyncRedisManager:
    """Enhanced Async Redis Manager with support for managed Redis instances."""
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        password: Optional[str] = None,
        db: int = 0,
        ssl: bool = False,
        ssl_cert_reqs: Optional[str] = None,
        max_connections: int = 10,
        socket_timeout: float = 5.0,
        cache_ttl: int = 5  # seconds
    ):
        """Initialize Async Redis Manager with connection pooling."""
        self.pool = ConnectionPool(
            host=host,
            port=port,
            password=password,
            db=db,
            ssl=ssl,
            ssl_cert_reqs=ssl_cert_reqs,
            max_connections=max_connections,
            socket_timeout=socket_timeout,
            decode_responses=True
        )
        
        self.redis = redis.Redis(connection_pool=self.pool)
        self._cache: Dict[str, Any] = {}
        self._cache_ttl: Dict[str, float] = {}
        self.CACHE_DURATION = cache_ttl
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        
        logger.info(f"Async Redis Manager initialized - Host: {host}, Port: {port}, SSL: {ssl}")
    
    @retry_on_connection_error()
    async def get_cached(self, key: str) -> Optional[Any]:
        """Get value from cache or Redis with TTL-based caching."""
        now = time.time()
        
        # Check cache first
        if key in self._cache and now < self._cache_ttl.get(key, 0):
            return self._cache[key]
        
        # Get from Redis
        try:
            value = await self.redis.get(key)
            if value is not None:
                try:
                    # Handle bytes or string response
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    # Attempt to parse as JSON
                    parsed_value = json.loads(value)
                    self._cache[key] = parsed_value
                except json.JSONDecodeError:
                    # If not JSON, store as is
                    self._cache[key] = value
                self._cache_ttl[key] = now + self.CACHE_DURATION
                return self._cache[key]
        except redis.RedisError as e:
            logger.error(f"Redis error on get: {e}")
        return None
    
    @retry_on_connection_error()
    async def set_with_validation(self, key: str, data: Union[Dict, str]) -> bool:
        """Set data with type validation and automatic JSON serialization."""
        try:
            # Convert dict to JSON string
            if isinstance(data, dict):
                # Validate data structure based on key prefix
                if key.startswith("omega:live_trader"):
                    self._validate_trader_data(data)
                elif key.startswith("omega:battle_state"):
                    self._validate_battle_state(data)
                
                value = json.dumps(data)
            else:
                value = str(data)
            
            # Store in Redis
            await self.redis.set(key, value)
            
            # Update cache
            self._cache[key] = data
            self._cache_ttl[key] = time.time() + self.CACHE_DURATION
            
            return True
            
        except (redis.RedisError, ValueError) as e:
            logger.error(f"Error storing data: {e}")
            return False
    
    def _validate_trader_data(self, data: Dict) -> None:
        """Validate trader data structure."""
        required_fields: Dict[str, Union[Type, Tuple[Type, ...]]] = {
            "name": str,
            "capital": (int, float),
            "pnl": (int, float),
            "win_rate": float,
            "trades": int,
            "emotional_state": str,
            "confidence": float,
            "risk_level": float
        }
        
        for profile_data in data.values():
            if not isinstance(profile_data, dict):
                raise ValueError("Invalid trader profile data structure")
            
            for field, field_type in required_fields.items():
                if field not in profile_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(profile_data[field], field_type):
                    raise ValueError(f"Invalid type for {field}")
    
    def _validate_battle_state(self, data: Dict) -> None:
        """Validate battle state structure."""
        required_fields: Dict[str, Union[Type, Tuple[Type, ...]]] = {
            "day": int,
            "session": int,
            "btc_price": (int, float),
            "battle_active": bool,
            "start_time": str
        }
        
        for field, field_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise ValueError(f"Invalid type for {field}")
    
    def _handle_shutdown(self, signum: int, frame: Any) -> None:
        """Handle graceful shutdown."""
        logger.warning("Shutdown signal received. Saving state...")
        
        async def _save_state():
            try:
                # Save final state
                final_state = {
                    "shutdown_time": time.time(),
                    "clean_shutdown": True,
                    "cache_size": len(self._cache)
                }
                await self.redis.set("omega:shutdown_state", json.dumps(final_state))
                
                # Close Redis connections
                await self.pool.disconnect()
                
                logger.info("State saved successfully")
                sys.exit(0)
                
            except Exception as e:
                logger.error(f"Error saving shutdown state: {e}")
                sys.exit(1)
        
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_save_state())
    
    def clear_cache(self) -> None:
        """Clear the local cache."""
        self._cache.clear()
        self._cache_ttl.clear()
    
    @retry_on_connection_error()
    async def health_check(self) -> Tuple[bool, str]:
        """Perform a health check on the Redis connection."""
        try:
            if await self.redis.ping():
                info = await self.redis.info()
                if isinstance(info, dict):
                    version = info.get('redis_version', 'unknown')
                    return True, f"Connected - Redis v{version}"
                return True, "Connected - Version unknown"
            return False, "Ping failed"
        except redis.RedisError as e:
            return False, str(e)
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        try:
            await self.pool.disconnect()
        except Exception:
            pass 