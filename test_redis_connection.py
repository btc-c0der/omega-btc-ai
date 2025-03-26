#!/usr/bin/env python3

"""
Test script to verify Redis connections work properly
"""

import sys
import json
import time
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.utils.redis_connection import RedisConnectionManager

def test_redis_manager():
    """Test RedisManager class"""
    print("Testing RedisManager...")
    try:
        # Initialize RedisManager
        redis_mgr = RedisManager(host='localhost', port=6379, db=0)
        
        # Test basic set/get
        test_key = f"test:manager:{int(time.time())}"
        test_data = {"test": True, "timestamp": time.time()}
        
        # Set with validation
        success = redis_mgr.set_with_validation(test_key, test_data)
        print(f"  - Set with validation: {'Success' if success else 'Failed'}")
        
        # Get from cache
        result = redis_mgr.get_cached(test_key)
        print(f"  - Get cached: {'Success' if result else 'Failed'}")
        
        # Test direct Redis access
        redis_mgr.redis.delete(test_key)
        print(f"  - Direct Redis access: Success")
        
        print("✅ RedisManager test completed successfully")
        return True
    except Exception as e:
        print(f"❌ RedisManager test failed: {e}")
        return False

def test_redis_connection_manager():
    """Test RedisConnectionManager class"""
    print("\nTesting RedisConnectionManager...")
    try:
        # Initialize RedisConnectionManager
        redis_conn = RedisConnectionManager(host='localhost', port=6379, db=0)
        
        # Test basic set/get
        test_key = f"test:connection:{int(time.time())}"
        test_data = {"test": True, "timestamp": time.time()}
        
        # Set data
        success = redis_conn.set(test_key, test_data)
        print(f"  - Set data: {'Success' if success else 'Failed'}")
        
        # Get data
        result = redis_conn.get(test_key)
        print(f"  - Get data: {'Success' if result else 'Failed'}")
        
        # Test direct Redis access
        redis_conn.client.delete(test_key)
        print(f"  - Direct Redis access: Success")
        
        print("✅ RedisConnectionManager test completed successfully")
        return True
    except Exception as e:
        print(f"❌ RedisConnectionManager test failed: {e}")
        return False

if __name__ == "__main__":
    print("Redis Connection Test Script")
    print("===========================")
    
    manager_success = test_redis_manager()
    connection_success = test_redis_connection_manager()
    
    if manager_success and connection_success:
        print("\n✅ All Redis connection tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Redis connection tests failed!")
        sys.exit(1) 