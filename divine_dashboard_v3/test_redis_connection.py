#!/usr/bin/env python3
"""
Redis Connection Test for Divine Dashboard v3

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This CODE is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by OMEGA BTC AI.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import redis
import datetime
import os
import json

# Redis connection configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 25061))
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "AVNS_OXMpU0P0ByYEz337Fgi")

def test_redis_connection():
    """Test connection to Redis and perform basic operations"""
    try:
        print(f"🔄 Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
        
        # Initialize Redis client
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD,
            ssl=True,
            decode_responses=True
        )
        
        # Test connection with PING
        response = redis_client.ping()
        print(f"✅ Redis PING: {response}")
        
        # Store test data
        timestamp = datetime.datetime.now().isoformat()
        redis_client.set("test_timestamp", timestamp)
        print(f"✅ Set test_timestamp: {timestamp}")
        
        # Increment connection counter
        counter = redis_client.incr("connection_test_count")
        print(f"✅ Connection test count: {counter}")
        
        # Store more complex data
        test_data = {
            "timestamp": timestamp,
            "environment": os.environ.get("HF_COMPONENT", "local_test"),
            "test_run": counter
        }
        redis_client.hset("test_data", mapping=test_data)
        print(f"✅ Stored test data hash")
        
        # Retrieve the data
        retrieved_data = redis_client.hgetall("test_data")
        print(f"✅ Retrieved test data: {json.dumps(retrieved_data, indent=2)}")
        
        print("\n✨ Redis connection test successful! ✨")
        return True
        
    except Exception as e:
        print(f"❌ Redis connection error: {str(e)}")
        return False

if __name__ == "__main__":
    test_redis_connection() 