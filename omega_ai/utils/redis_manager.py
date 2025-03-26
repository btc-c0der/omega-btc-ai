import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
import signal
import sys
from typing import Optional, Dict, Any
import json
import time
import os

class RedisManager:
    def __init__(self, host=None, port=None, db=0, 
                 username=None, password=None, ssl=False, ssl_ca_certs=None):
        """
        Initialize Redis connection manager with optional SSL support
        
        Args:
            host: Redis host (default: from env or localhost)
            port: Redis port (default: from env or 6379)
            db: Redis database number (default: 0)
            username: Redis username for auth (default: None)
            password: Redis password for auth (default: None)
            ssl: Whether to use SSL/TLS (default: False)
            ssl_ca_certs: Path to CA certificate file (default: None)
        """
        # Get Redis connection details from environment variables or use defaults
        host = host or os.getenv('REDIS_HOST', 'localhost')
        port = port or int(os.getenv('REDIS_PORT', '6379'))
        
        # Initialize Redis connection with flexible parameters
        connection_params = {
            "host": host,
            "port": port,
            "db": db,
            "decode_responses": True
        }
        
        # Add optional authentication if provided and not in development mode
        if not os.environ.get('OMEGA_DEV_MODE', 'true').lower() == 'true':
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
            self.redis = redis.Redis(**connection_params)
            print(f"Redis Manager initialized - Host: {host}, Port: {port}, SSL: {ssl}")
            # Test connection
            self.redis.ping()
            print("✅ Redis connection successful")
        except Exception as e:
            print(f"Error initializing Redis connection: {e}")
            raise
        
        self._cache = {}
        self._cache_ttl = {}
        self.CACHE_DURATION = 5  # seconds
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def connect(self):
        """Get a blessed Redis connection."""
        if not self.redis:
            self.redis = redis.Redis(
                host=self.redis.connection_pool.connection_kwargs['host'],
                port=self.redis.connection_pool.connection_kwargs['port'],
                db=self.redis.connection_pool.connection_kwargs['db'],
                decode_responses=True
            )
        return self.redis
    
    def get_cached(self, key: str, default: Any = None) -> Optional[Any]:
        """Get value from cache or Redis with TTL-based caching"""
        now = time.time()
        
        # Check cache first
        if key in self._cache and now < self._cache_ttl[key]:
            return self._cache[key]
            
        # Get from Redis
        try:
            value = self.redis.get(key)
            if value:
                self._cache[key] = value
                self._cache_ttl[key] = now + self.CACHE_DURATION
                return value
            return default
        except redis.RedisError as e:
            print(f"Redis error on get: {e}")
            return default
    
    def set_cached(self, key: str, value: Any) -> bool:
        """Set a value in Redis with divine energy."""
        try:
            self.redis.set(key, value)
            self._cache[key] = value
            self._cache_ttl[key] = time.time() + self.CACHE_DURATION
            return True
        except redis.RedisError as e:
            print(f"Redis error on set: {e}")
            return False
    
    def lpush(self, key: str, value: Any) -> bool:
        """Push to a list in Redis with Rastafarian rhythm."""
        try:
            self.redis.lpush(key, value)
            return True
        except redis.RedisError as e:
            print(f"Redis error on lpush: {e}")
            return False
    
    def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim a list in Redis with cosmic precision."""
        try:
            self.redis.ltrim(key, start, end)
            return True
        except redis.RedisError as e:
            print(f"Redis error on ltrim: {e}")
            return False
    
    def lrange(self, key: str, start: int, end: int) -> Optional[list]:
        """Get a range from a list in Redis with divine harmony."""
        try:
            return self.redis.lrange(key, start, end)
        except redis.RedisError as e:
            print(f"Redis error on lrange: {e}")
            return None
    
    def ping(self) -> bool:
        """Check Redis connection with JAH blessing."""
        try:
            return self.redis.ping()
        except redis.RedisError as e:
            print(f"Redis error on ping: {e}")
            return False
    
    def set_with_validation(self, key: str, data: Dict) -> bool:
        """Set data with type validation"""
        try:
            # Validate data structure
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary")
                
            # Validate specific fields based on key
            if "omega:live_trader_data" in key:
                self._validate_trader_data(data)
            elif "omega:live_battle_state" in key:
                self._validate_battle_state(data)
            
            # Store in Redis
            self.redis.set(key, json.dumps(data))
            
            # Update cache
            self._cache[key] = data
            self._cache_ttl[key] = time.time() + self.CACHE_DURATION
            
            return True
            
        except (redis.RedisError, ValueError) as e:
            print(f"Error storing data: {e}")
            return False
    
    def _validate_trader_data(self, data: Dict):
        """Validate trader data structure"""
        required_fields = {
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
            for field, field_type in required_fields.items():
                if field not in profile_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(profile_data[field], field_type):
                    raise ValueError(f"Invalid type for {field}")
    
    def _validate_battle_state(self, data: Dict):
        """Validate battle state structure"""
        required_fields = {
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
    
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        print("\n⚠️ Shutdown signal received. Saving state...")
        
        try:
            # Save final state
            final_state = {
                "shutdown_time": time.time(),
                "clean_shutdown": True
            }
            
            try:
                # Use a new Redis connection for shutdown to avoid issues
                shutdown_params = {
                    "host": self.redis.connection_pool.connection_kwargs['host'],
                    "port": self.redis.connection_pool.connection_kwargs['port'],
                    "db": self.redis.connection_pool.connection_kwargs['db'],
                    "decode_responses": True
                }
                
                # Add username/password if in original connection
                if 'username' in self.redis.connection_pool.connection_kwargs:
                    shutdown_params["username"] = self.redis.connection_pool.connection_kwargs['username']
                if 'password' in self.redis.connection_pool.connection_kwargs:
                    shutdown_params["password"] = self.redis.connection_pool.connection_kwargs['password']
                    
                # Add SSL if in original connection
                if 'ssl' in self.redis.connection_pool.connection_kwargs and self.redis.connection_pool.connection_kwargs['ssl']:
                    shutdown_params["ssl"] = True
                    if 'ssl_ca_certs' in self.redis.connection_pool.connection_kwargs:
                        shutdown_params["ssl_ca_certs"] = self.redis.connection_pool.connection_kwargs['ssl_ca_certs']
                
                shutdown_redis = redis.Redis(**shutdown_params)
                shutdown_redis.set("omega:shutdown_state", json.dumps(final_state))
                print("✅ State saved successfully")
            except Exception as e:
                print(f"⚠️ Could not save shutdown state: {e}")
            
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Error saving shutdown state: {e}")
            sys.exit(1)

    def zcard(self, name: str) -> int:
        """Return the number of elements in the sorted set at key `name`."""
        return self.redis.zcard(name)

    def zadd(self, name: str, mapping: dict) -> int:
        """Add all the specified members with the specified scores to the sorted set stored at key `name`."""
        return self.redis.zadd(name, mapping)

    def zrange(self, name: str, start: int, end: int, desc: bool = False, withscores: bool = False) -> list:
        """Return a range of elements from the sorted set at key `name`."""
        return self.redis.zrange(name, start, end, desc=desc, withscores=withscores)

    def zremrangebyrank(self, name: str, start: int, end: int) -> int:
        """Remove all elements in the sorted set stored at key `name` with rank between `start` and `end`."""
        return self.redis.zremrangebyrank(name, start, end)

    def delete(self, *names: str) -> int:
        """Delete a key from the Redis database."""
        return self.redis.delete(*names)

# Create a default config loader
def get_redis_config():
    """
    Get Redis configuration from environment variables with fallback to defaults
    
    Returns:
        dict: Redis connection parameters
    """
    # Check for environment variable to determine if we use cloud or local Redis
    use_cloud = os.environ.get('OMEGA_USE_CLOUD_REDIS', 'false').lower() == 'true'
    
    if use_cloud:
        # Cloud Redis configuration
        return {
            'host': os.environ.get('REDIS_HOST', '172.16.8.2'),
            'port': int(os.environ.get('REDIS_PORT', '6379')),
            'username': os.environ.get('REDIS_USERNAME', 'btc-omega-redis'),
            'password': os.environ.get('REDIS_PASSWORD', ''),
            'ssl': True,
            'ssl_ca_certs': os.environ.get('REDIS_CA_CERT', 'SSL_redis-btc-omega-redis.pem')
        }
    else:
        # Local Redis configuration
        return {
            'host': os.environ.get('REDIS_HOST', 'localhost'),
            'port': int(os.environ.get('REDIS_PORT', '6379')),
            'db': int(os.environ.get('REDIS_DB', '0')),
            'username': os.environ.get('REDIS_USERNAME', None),
            'password': os.environ.get('REDIS_PASSWORD', None),
            'ssl': False
        }