#!/usr/bin/env python3
"""
Redis Key Fixer Utility

This script scans through Redis to find and fix any keys with WRONGTYPE errors
by deleting problematic keys or converting them to the correct type.
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

# Add the project root to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import RedisManager
from omega_ai.utils.redis_manager import RedisManager

# ANSI color codes for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"

def print_colored(message: str, color: str = GREEN) -> None:
    """Print a colored message."""
    print(f"{color}{message}{RESET}")

def scan_and_fix_redis_keys() -> None:
    """Scan through Redis and fix any keys with type issues."""
    # Initialize RedisManager
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_manager = RedisManager(host=redis_host, port=redis_port)
    
    print_colored(f"Connected to Redis at {redis_host}:{redis_port}", BLUE)
    
    # Get all keys
    try:
        keys = redis_manager.redis.keys("*")
        print_colored(f"Found {len(keys)} keys in Redis", BLUE)
    except Exception as e:
        print_colored(f"Error getting keys: {e}", RED)
        return
    
    # Check each key
    fixed_keys = 0
    deleted_keys = 0
    error_keys = 0
    
    for key in keys:
        try:
            # Try to get the key type
            key_type = redis_manager.get_key_type(key)
            print(f"Key: {key}, Type: {key_type}")
            
            # Try to get the value
            try:
                if key_type == 'string':
                    value = redis_manager.redis.get(key)
                elif key_type == 'list':
                    value = redis_manager.redis.lrange(key, 0, 0)
                elif key_type == 'hash':
                    value = redis_manager.redis.hgetall(key)
                elif key_type == 'set':
                    value = redis_manager.redis.smembers(key)
                elif key_type == 'zset':
                    value = redis_manager.redis.zrange(key, 0, -1, withscores=True)
                else:
                    print_colored(f"Unknown key type: {key_type} for key: {key}", YELLOW)
                    continue
            except Exception as e:
                # Error indicates a WRONGTYPE issue
                print_colored(f"Error on key '{key}': {e}", YELLOW)
                
                # Get the expected type from key name
                expected_type = get_expected_type_from_key(key)
                
                # Fix the key
                if expected_type:
                    print_colored(f"Attempting to fix key '{key}' to type '{expected_type}'", YELLOW)
                    if redis_manager.fix_key_type(key, expected_type):
                        print_colored(f"Successfully fixed key: {key}", GREEN)
                        fixed_keys += 1
                    else:
                        print_colored(f"Failed to fix key: {key}, deleting it", RED)
                        redis_manager.redis.delete(key)
                        deleted_keys += 1
                else:
                    print_colored(f"Cannot determine expected type for key: {key}, deleting it", RED)
                    redis_manager.redis.delete(key)
                    deleted_keys += 1
                
                error_keys += 1
                
        except Exception as e:
            print_colored(f"Unexpected error with key '{key}': {e}", RED)
            error_keys += 1
    
    print_colored(f"\nScan complete!", GREEN)
    print_colored(f"Total keys: {len(keys)}", BLUE)
    print_colored(f"Fixed keys: {fixed_keys}", GREEN)
    print_colored(f"Deleted keys: {deleted_keys}", YELLOW)
    print_colored(f"Error keys: {error_keys}", RED)

def get_expected_type_from_key(key: str) -> Optional[str]:
    """
    Determine the expected Redis type based on key naming conventions.
    
    Args:
        key: The Redis key name
        
    Returns:
        The expected Redis type or None if undetermined
    """
    # Keys for lists
    list_keywords = ['history', 'queue', 'list', 'movements', 'candles']
    # Keys for hashes
    hash_keywords = ['config', 'settings', 'state', 'data']
    # Keys for strings
    string_keywords = ['price', 'level', 'time', 'value', 'count', 'last', 'high', 'low']
    
    key_lower = key.lower()
    
    # Check if this key matches any list naming pattern
    for keyword in list_keywords:
        if keyword in key_lower:
            return 'list'
    
    # Check if this key matches any hash naming pattern
    for keyword in hash_keywords:
        if keyword in key_lower:
            return 'hash'
    
    # Check if this key matches any string naming pattern
    for keyword in string_keywords:
        if keyword in key_lower:
            return 'string'
    
    # Default to string for unknown keys
    return 'string'

if __name__ == "__main__":
    print_colored("Redis Key Fixer Utility", BLUE)
    print_colored("-------------------------", BLUE)
    scan_and_fix_redis_keys() 