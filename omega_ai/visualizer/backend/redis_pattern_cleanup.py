#!/usr/bin/env python

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

import redis
import sys
import time
import argparse
from datetime import datetime

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def connect_to_redis():
    """Connect to Redis and verify connection"""
    try:
        client = redis.Redis(host="localhost", port=6379, db=0, socket_timeout=10)
        client.ping()  # Test connection
        return client
    except redis.ConnectionError:
        print(f"{RED}✗ Could not connect to Redis{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}✗ Error connecting to Redis: {e}{RESET}")
        sys.exit(1)

def clean_patterns(client, patterns, batch_size=1000, dry_run=False):
    """Clean keys matching specific patterns"""
    total_deleted = 0
    start_time = time.time()
    initial_key_count = client.dbsize()

    print(f"{BOLD}===== REDIS PATTERN CLEANUP ====={RESET}")
    print(f"Connecting to Redis...")
    print(f"{GREEN}✓ Connected to Redis{RESET}")
    print(f"Database contains {BOLD}{initial_key_count}{RESET} keys")
    
    if dry_run:
        print(f"{YELLOW}Running in DRY RUN mode - no keys will be deleted{RESET}")
    
    for pattern in patterns:
        pattern_start = time.time()
        pattern_count = 0
        cursor = "0"
        
        print(f"Cleaning up pattern: {YELLOW}{pattern}{RESET}")
        
        # Use scan for efficient iteration
        while cursor != 0:
            cursor, keys = client.scan(cursor=int(cursor), match=pattern, count=batch_size)
            if keys:
                pattern_count += len(keys)
                if not dry_run:
                    client.delete(*keys)
                
                # Progress update for large deletions
                if pattern_count % 10000 == 0:
                    print(f"  Deleted {pattern_count} keys so far...")
            
            # Break if we've iterated through all keys
            if cursor == 0 or cursor == "0":
                break
        
        pattern_time = time.time() - pattern_start
        print(f"  {GREEN}Cleaned up {pattern_count} {pattern} keys in {pattern_time:.2f} seconds{RESET}")
        total_deleted += pattern_count
    
    # Calculate stats
    end_time = time.time()
    final_key_count = client.dbsize()
    elapsed_time = end_time - start_time
    
    if not dry_run:
        reduction = ((initial_key_count - final_key_count) / initial_key_count * 100) if initial_key_count > 0 else 0
        print(f"\nCleanup completed in {elapsed_time:.2f} seconds")
        print(f"{GREEN}Successfully deleted {total_deleted} total keys{RESET}")
        print(f"Database now contains {final_key_count} keys ({reduction:.1f}% reduction)")
    else:
        print(f"\n{YELLOW}DRY RUN completed - {total_deleted} keys would have been deleted{RESET}")
        print(f"Database contains {final_key_count} keys")

def main():
    parser = argparse.ArgumentParser(description="Clean Redis by removing keys matching specific patterns")
    parser.add_argument("--dry-run", action="store_true", help="Simulate cleanup without deleting keys")
    parser.add_argument("--patterns", nargs="+", help="Specific patterns to clean")
    args = parser.parse_args()
    
    # Connect to Redis
    client = connect_to_redis()
    
    # Define patterns to clean - these are common patterns that can accumulate
    default_patterns = [
        "rq:job:*",            # Redis Queue jobs
        "rq:worker:*",         # Redis Queue workers
        "rq:queue:*",          # Redis Queue queues
        "rq:failed:*",         # Redis Queue failed jobs
        "tmp:*",               # Temporary data
        "cache:*",             # Cache data
        "sess:*",              # Session data
        "task:*",              # Task data
        "log:*",               # Log data
        "stat:*",              # Statistics data
        "*:temp:*",            # Temporary data with namespace
        "*:cache:*",           # Cache data with namespace
        "*:job:*",             # Job data with namespace
        "celery-task-meta-*",  # Celery task metadata
        "celery-task-*",       # Celery tasks
        "_kombu.binding.*",    # Kombu bindings
        "unacked:*",           # Unacknowledged messages
        "*:device:*:feed:*",   # Device feed data
        "*:stream:*",          # Stream data
        "*:lock:*",            # Lock data
        "*:mutex:*",           # Mutex data
        "*:semaphore:*",       # Semaphore data
        "*:counter:*",         # Counter data
        "*:queue:*",           # Queue data
        "*:set:*",             # Set data
        "*:list:*",            # List data
        "*:hash:*",            # Hash data
        "*:string:*",          # String data
        "*:zset:*",            # Sorted set data
        "*:pubsub:*",          # PubSub data
        "*:channel:*",         # Channel data
        "*:event:*",           # Event data
        "*:notification:*",    # Notification data
        "*:message:*",         # Message data
    ]
    
    # Use provided patterns if specified, otherwise use defaults
    patterns_to_clean = args.patterns if args.patterns else default_patterns
    
    # Clean the patterns
    clean_patterns(client, patterns_to_clean, dry_run=args.dry_run)
    
if __name__ == "__main__":
    main() 