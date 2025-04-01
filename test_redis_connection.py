#!/usr/bin/env python3

"""
Test script to verify Redis connection works properly with cloud Redis
"""

import redis
import os
import ssl
from datetime import datetime

# Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
BLUE_RASTA = "\033[94m"
RESET = "\033[0m"

# Redis connection parameters from environment
redis_host = os.getenv('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com')
redis_port = int(os.getenv('REDIS_PORT', '19332'))
redis_username = os.getenv('REDIS_USERNAME', 'omega')
redis_password = os.getenv('REDIS_PASSWORD', 'VuKJU8Z.Z2V8Qn_')
redis_cert = os.getenv('REDIS_CERT', 'SSL_redis-btc-omega-redis.pem')

print(f"{BLUE_RASTA}=== Testing Redis Cloud Connection ==={RESET}")
print(f"Connecting to Redis at {redis_host}:{redis_port}")
print(f"Username: {redis_username}")
print(f"SSL Certificate: {redis_cert}")

# Create Redis connection with SSL
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    username=redis_username,
    password=redis_password,
    ssl=True,
    ssl_cert_reqs=None,  # Skip certificate verification for testing
    decode_responses=True
)

try:
    # Test connection
    print("\nTesting connection to Redis...")
    redis_client.ping()
    print(f"{GREEN_RASTA}✅ Successfully connected to Redis!{RESET}")
    
    # Test write
    test_key = f"test:connection:{datetime.now().timestamp()}"
    test_value = "Hello Redis Cloud!"
    redis_client.set(test_key, test_value)
    print(f"{GREEN_RASTA}✅ Successfully wrote test key: {test_key}{RESET}")
    
    # Test read
    value = redis_client.get(test_key)
    print(f"{GREEN_RASTA}✅ Successfully read test key: {value}{RESET}")
    
    # Test BTC live feed keys
    btc_keys = ["btc_price", "btc_price_changes", "btc_movement_history"]
    print("\nChecking BTC live feed keys:")
    for key in btc_keys:
        value = redis_client.get(key)
        if value:
            print(f"{GREEN_RASTA}✅ {key}: {value}{RESET}")
        else:
            print(f"{YELLOW_RASTA}⚠️ {key} not found{RESET}")
    
    # Cleanup test key
    redis_client.delete(test_key)
    print(f"\n{GREEN_RASTA}✅ Successfully cleaned up test key{RESET}")
    
except Exception as e:
    print(f"{RED_RASTA}❌ Error connecting to Redis: {e}{RESET}") 