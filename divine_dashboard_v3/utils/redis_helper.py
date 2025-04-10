#!/usr/bin/env python3
"""
Redis Helper for Divine Dashboard v3

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This CODE is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by OMEGA BTC AI.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import redis
import json
import datetime
import os
import logging
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("redis_helper")

# Redis connection configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 25061))
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "AVNS_OXMpU0P0ByYEz337Fgi")
REDIS_SSL = True
REDIS_DECODE_RESPONSES = True

# Initialize module-level Redis client
redis_client = None

def get_redis_client() -> redis.Redis:
    """Get or initialize the Redis client"""
    global redis_client
    
    if redis_client is None:
        try:
            logger.info(f"Initializing Redis connection to {REDIS_HOST}:{REDIS_PORT}")
            redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                username=REDIS_USERNAME,
                password=REDIS_PASSWORD,
                ssl=REDIS_SSL,
                decode_responses=REDIS_DECODE_RESPONSES
            )
            # Test connection
            redis_client.ping()
            logger.info("Redis connection successful")
        except Exception as e:
            logger.error(f"Redis connection error: {str(e)}")
            raise
    
    return redis_client

# Key management
def get_namespaced_key(namespace: str, key: str) -> str:
    """Create a namespaced key for better organization"""
    return f"{namespace}:{key}"

# Basic operations
def set_value(key: str, value: str, expiration: Optional[int] = None) -> bool:
    """Set a string value in Redis with optional expiration in seconds"""
    try:
        client = get_redis_client()
        return client.set(key, value, ex=expiration)
    except Exception as e:
        logger.error(f"Error setting key {key}: {str(e)}")
        return False

def get_value(key: str) -> Optional[str]:
    """Get a string value from Redis"""
    try:
        client = get_redis_client()
        return client.get(key)
    except Exception as e:
        logger.error(f"Error getting key {key}: {str(e)}")
        return None

# JSON operations
def set_json(key: str, value: Dict[str, Any], expiration: Optional[int] = None) -> bool:
    """Store a JSON object in Redis"""
    try:
        json_str = json.dumps(value)
        return set_value(key, json_str, expiration)
    except Exception as e:
        logger.error(f"Error setting JSON for key {key}: {str(e)}")
        return False

def get_json(key: str) -> Optional[Dict[str, Any]]:
    """Get a JSON object from Redis"""
    try:
        value = get_value(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Error getting JSON for key {key}: {str(e)}")
        return None

# Hash operations
def hset_dict(key: str, mapping: Dict[str, Any]) -> bool:
    """Set multiple hash fields to multiple values"""
    try:
        client = get_redis_client()
        # Convert all values to strings for Redis compatibility
        string_mapping = {k: str(v) for k, v in mapping.items()}
        client.hset(key, mapping=string_mapping)
        return True
    except Exception as e:
        logger.error(f"Error setting hash for key {key}: {str(e)}")
        return False

def hget_dict(key: str) -> Dict[str, str]:
    """Get all fields and values in a hash"""
    try:
        client = get_redis_client()
        return client.hgetall(key) or {}
    except Exception as e:
        logger.error(f"Error getting hash for key {key}: {str(e)}")
        return {}

# Counters
def increment(key: str, amount: int = 1) -> int:
    """Increment a counter by the given amount"""
    try:
        client = get_redis_client()
        return client.incrby(key, amount)
    except Exception as e:
        logger.error(f"Error incrementing key {key}: {str(e)}")
        return 0

# Lists
def push_to_list(key: str, *values: str) -> int:
    """Push values onto the end of a list"""
    try:
        client = get_redis_client()
        return client.rpush(key, *values)
    except Exception as e:
        logger.error(f"Error pushing to list {key}: {str(e)}")
        return 0

def get_list(key: str, start: int = 0, end: int = -1) -> List[str]:
    """Get a range of elements from a list"""
    try:
        client = get_redis_client()
        return client.lrange(key, start, end)
    except Exception as e:
        logger.error(f"Error getting list {key}: {str(e)}")
        return []

# Logging and analytics
def log_event(event_type: str, data: Dict[str, Any]) -> bool:
    """Log an event to Redis for analytics"""
    try:
        # Add timestamp
        data["timestamp"] = datetime.datetime.now().isoformat()
        
        # Create namespaced key
        key = get_namespaced_key("events", f"{event_type}:{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Store event
        set_json(key, data)
        
        # Add to event list
        event_list_key = get_namespaced_key("events", f"{event_type}_list")
        push_to_list(event_list_key, key)
        
        # Increment event counter
        event_counter_key = get_namespaced_key("counters", f"event_{event_type}")
        increment(event_counter_key)
        
        return True
    except Exception as e:
        logger.error(f"Error logging event {event_type}: {str(e)}")
        return False

def record_metric(metric_name: str, value: Union[int, float, str]) -> bool:
    """Record a metric value with timestamp"""
    try:
        timestamp = datetime.datetime.now().isoformat()
        
        # Store in a hash
        key = get_namespaced_key("metrics", metric_name)
        hset_dict(key, {
            "value": value,
            "timestamp": timestamp
        })
        
        # Also store as time series
        series_key = get_namespaced_key("time_series", metric_name)
        ts_data = {
            "value": value,
            "timestamp": timestamp
        }
        push_to_list(series_key, json.dumps(ts_data))
        
        return True
    except Exception as e:
        logger.error(f"Error recording metric {metric_name}: {str(e)}")
        return False

# Testing
def test_connection() -> bool:
    """Test the Redis connection"""
    try:
        client = get_redis_client()
        result = client.ping()
        logging.info(f"Redis connection test: {result}")
        return bool(result)
    except Exception as e:
        logging.error(f"Redis connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Run connection test when the module is executed directly
    if test_connection():
        print("✅ Redis connection test successful!")
    else:
        print("❌ Redis connection test failed!") 