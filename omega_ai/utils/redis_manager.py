import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
import signal
import sys
from typing import Optional, Dict, Any
import json
import time

class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        # Configure retry strategy
        retry_strategy = Retry(
            ExponentialBackoff(),
            retries=5
        )
        
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            retry_on_timeout=True,
            retry_on_error=[redis.exceptions.ConnectionError],
            retry_strategy=retry_strategy,
            decode_responses=True
        )
        
        self._cache = {}
        self._cache_ttl = {}
        self.CACHE_DURATION = 5  # seconds
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def get_cached(self, key: str) -> Optional[Any]:
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
        except redis.RedisError as e:
            print(f"Redis error on get: {e}")
        return None
    
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
            self.redis.set("omega:shutdown_state", json.dumps(final_state))
            
            print("✅ State saved successfully")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Error saving shutdown state: {e}")
            sys.exit(1)