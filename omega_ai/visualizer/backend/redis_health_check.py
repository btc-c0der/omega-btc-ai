#!/usr/bin/env python3

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
Quick Redis health check utility
"""

import redis
import json
import sys
import time

# ANSI colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
RESET = "\033[0m"

def check_redis():
    """Check Redis connection and get basic stats"""
    try:
        # Connect to Redis
        print(f"{CYAN}Connecting to Redis...{RESET}")
        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        
        # Test connection
        if r.ping():
            print(f"{GREEN}✓ Redis connection successful{RESET}")
        else:
            print(f"{RED}✗ Redis ping failed{RESET}")
            return False
        
        # Get key count
        start_time = time.time()
        key_count = len(r.keys("*"))
        elapsed = time.time() - start_time
        print(f"{GREEN}✓ Found {key_count} keys in {elapsed:.2f} seconds{RESET}")
        
        # If too many keys, this could be the issue
        if key_count > 10000:
            print(f"{YELLOW}⚠️ Large number of keys detected! This may cause performance issues{RESET}")
        
        # Get sample keys
        print(f"{CYAN}Sample keys:{RESET}")
        for key in list(r.keys("*"))[:5]:
            key_type = r.type(key)
            if key_type == "string":
                value = r.get(key)
                if value is not None:
                    if len(value) > 50:
                        value = value[:50] + "..."
                else:
                    value = "(None)"
                print(f"  - {key} ({key_type}): {value}")
            elif key_type == "list":
                print(f"  - {key} ({key_type}): {r.llen(key)} items")
            elif key_type == "hash":
                print(f"  - {key} ({key_type}): {len(r.hkeys(key))} fields")
            else:
                print(f"  - {key} ({key_type})")
        
        # Test if test: keys exist
        test_keys = [k for k in r.keys("*") if k.startswith("test:")]
        if test_keys:
            print(f"{GREEN}✓ Found {len(test_keys)} test: keys{RESET}")
            for key in test_keys[:3]:
                print(f"  - {key}")
        else:
            print(f"{YELLOW}⚠️ No test: keys found{RESET}")
        
        return True
    
    except redis.ConnectionError as e:
        print(f"{RED}✗ Redis connection error: {e}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}✗ Error checking Redis: {e}{RESET}")
        return False

if __name__ == "__main__":
    print(f"\n{CYAN}===== Redis Health Check ====={RESET}")
    success = check_redis()
    if success:
        print(f"\n{GREEN}Redis check completed successfully{RESET}")
    else:
        print(f"\n{RED}Redis check failed{RESET}")
        sys.exit(1) 