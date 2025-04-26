#!/usr/bin/env python3

import redis
import sys
import os
import json
from dotenv import load_dotenv
import time

def test_redis_connection(use_docker_redis=True):
    """Test connection to Redis and perform basic operations"""
    print("Testing Redis connection...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Use local Docker Redis container
    if use_docker_redis:
        host = "localhost"
        port = 6379
        username = None
        password = None
        ssl = False
        print(f"Using Docker Redis container: {host}:{port}")
    else:
        # Get Redis connection parameters from environment
        host = os.environ.get('REDIS_HOST', 'localhost')
        port = int(os.environ.get('REDIS_PORT', 6379))
        username = os.environ.get('REDIS_USERNAME')
        password = os.environ.get('REDIS_PASSWORD')
        ssl = os.environ.get('REDIS_SSL', 'false').lower() == 'true'
        print(f"Using configured Redis: {host}:{port}")
    
    try:
        # Create Redis client
        r = redis.Redis(
            host=host, 
            port=port, 
            username=username,
            password=password,
            decode_responses=True,
            ssl=ssl,
            socket_timeout=5.0  # Add timeout to avoid long waits
        )
        
        # Test connection with ping
        response = r.ping()
        print(f"Ping successful: {response}")
        
        # Get server info
        info = r.info()
        print("\nRedis server info:")
        print(f"Redis version: {info.get('redis_version', 'Unknown')}")
        print(f"Uptime: {info.get('uptime_in_seconds', 'Unknown')} seconds")
        print(f"Connected clients: {info.get('connected_clients', 'Unknown')}")
        print(f"Total memory used: {info.get('used_memory_human', 'Unknown')}")
        
        # Add some test data to verify read/write operations
        print("\nAdding test data...")
        test_timestamp = time.time()
        r.set("test_key", f"Test value at {test_timestamp}")
        r.set("btc_test_price", "48751.25")
        
        # Set a trap probability test value
        trap_data = {
            "probability": 0.625,
            "trap_type": "Bull Trap",
            "confidence": 0.75,
            "components": {
                "price_pattern": 0.8,
                "volume_spike": 0.6,
                "fib_level": 0.7,
                "historical_match": 0.5,
                "order_book": 0.4,
                "market_regime": 0.45
            },
            "timestamp": time.time()
        }
        r.set("latest_trap_prediction", json.dumps(trap_data))
        
        # Try to access the data we just added
        print("\nRetrieving test data:")
        print(f"test_key: {r.get('test_key')}")
        print(f"btc_test_price: {r.get('btc_test_price')}")
        
        # Try to access keys starting with "trap"
        print("\nLooking for keys related to trap probability meter:")
        keys = r.keys("*trap*")
        for key in keys:
            print(f"Found key: {key}")
            # Get the value of the key if it's a string
            try:
                value_type = r.type(key)
                if value_type == "string":
                    value = r.get(key)
                    value_data = json.loads(value)
                    print(f"  Type: {value_data.get('trap_type')}")
                    print(f"  Probability: {value_data.get('probability')}")
                    print(f"  Confidence: {value_data.get('confidence')}")
            except:
                pass
        
        # Try to list all keys
        print("\nListing all keys in the database:")
        all_keys = r.keys("*")
        for i, key in enumerate(all_keys):
            print(f"{i+1}. {key}")
        
        print("\nRedis connection test completed successfully!")
        return True
        
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        print("Is the Redis server running?")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)