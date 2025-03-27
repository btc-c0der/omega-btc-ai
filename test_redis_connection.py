#!/usr/bin/env python3

"""
Test script to verify Redis connection works properly with localhost
"""

import redis
import os
from omega_ai.utils.redis_manager import RedisManager

# Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
BLUE_RASTA = "\033[94m"
RESET = "\033[0m"

def log_message(message, color=GREEN_RASTA, level="info"):
    """Log with color coding."""
    if level == "error":
        print(f"{RED_RASTA}❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}✅ {message}{RESET}")
    else:
        print(f"{color}ℹ️  {message}{RESET}")

def test_redis_manager():
    """Test direct Redis connection and RedisManager class."""
    print(f"{BLUE_RASTA}=== Testing Redis Connections ==={RESET}")
    
    # Test direct Redis connection first
    try:
        direct_redis = redis.Redis(
            host='localhost',
            port=int(os.getenv('REDIS_PORT', '6379')),
            db=0
        )
        if direct_redis.ping():
            log_message("Direct Redis connection successful (localhost)", level="success")
        else:
            log_message("Direct Redis ping failed", level="error")
    except Exception as e:
        log_message(f"Direct Redis connection failed: {e}", level="error")
    
    # Test RedisManager
    try:
        # Initialize RedisManager with explicit localhost
        redis_mgr = RedisManager(host='localhost', port=6379, db=0)
        if redis_mgr.ping():
            log_message("RedisManager connection successful", level="success")
            
            # Test basic set/get
            test_key = "test:btc:price"
            test_value = "50000.0"
            success = redis_mgr.set_cached(test_key, test_value)
            if success:
                log_message("Set test value successful", level="success")
            else:
                log_message("Set test value failed", level="error")
                
            # Test get
            value = redis_mgr.get_cached(test_key)
            if value == test_value:
                log_message(f"Get test value successful: {value}", level="success")
            else:
                log_message(f"Get test value inconsistent: {value}", level="warning")
                
            # Test list operations
            test_list_key = "test:btc:history"
            redis_mgr.lpush(test_list_key, "49000.0,0.1")
            redis_mgr.lpush(test_list_key, "49100.0,0.2")
            
            list_values = redis_mgr.lrange(test_list_key, 0, -1)
            if list_values and len(list_values) > 0:
                log_message(f"List operations successful: {list_values}", level="success")
            else:
                log_message("List operations failed", level="error")
                
            # Check btc_movement_history
            btc_history = redis_mgr.lrange("btc_movement_history", 0, 5)
            if btc_history:
                log_message(f"btc_movement_history exists with {len(btc_history)} entries", level="success")
                log_message(f"Sample entries: {btc_history[:3]}", color=BLUE_RASTA)
            else:
                log_message("btc_movement_history is empty", level="warning")
        else:
            log_message("RedisManager ping failed", level="error")
    except Exception as e:
        log_message(f"RedisManager test failed: {e}", level="error")

if __name__ == "__main__":
    test_redis_manager() 