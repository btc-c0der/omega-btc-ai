#!/usr/bin/env python3
"""
Redis Quick Cleanup

This script performs a quick cleanup of Redis job queues
without scanning all keys, which is too slow with millions of keys.
"""

import redis
import sys
import time

# ANSI colors for output
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
RESET = "\033[0m"

def main():
    """Main execution function."""
    print(f"\n{CYAN}===== REDIS QUICK CLEANUP ====={RESET}")
    
    try:
        # Connect to Redis
        print(f"Connecting to Redis...")
        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        r.ping()
        print(f"{GREEN}✓ Connected to Redis{RESET}")
        
        # First check how many keys we have
        key_count = r.dbsize()
        print(f"{GREEN}Database contains {key_count} keys{RESET}")
        
        # Get all rq: keys using scan instead of keys
        print(f"Scanning for job queue keys...")
        deleted = 0
        job_scan_count = 0
        
        # Use scan_iter which is more efficient than keys for large DBs
        cursor = 0
        pattern = 'rq:job:*'
        
        start_time = time.time()
        batch = []
        batch_size = 1000
        
        print(f"Deleting job keys in batches of {batch_size}...")
        
        # First pass: Delete job keys (these are usually the majority)
        cursor = 0
        while cursor != 0:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=batch_size)
            if keys:
                job_scan_count += len(keys)
                batch.extend(keys)
            
            # Delete in batches to improve performance
            if len(batch) >= batch_size or (cursor == 0 and batch):
                result = r.delete(*batch)
                deleted += result
                print(f"  Deleted batch of {result} keys, total: {deleted}")
                batch = []
        
        print(f"{GREEN}Successfully deleted {deleted} rq:job: keys{RESET}")
        
        # Second pass: Delete other RQ related keys
        other_patterns = [
            'rq:worker:*',
            'rq:workers*',
            'rq:queue:*',
            'rq:failed:*',
            'rq:clean-registries*'
        ]
        
        for pattern in other_patterns:
            batch = []
            cursor = 0
            pattern_deleted = 0
            
            print(f"Cleaning up pattern: {pattern}")
            
            while cursor != 0:
                cursor, keys = r.scan(cursor=cursor, match=pattern, count=batch_size)
                if keys:
                    pattern_deleted += len(keys)
                    batch.extend(keys)
                
                # Delete in batches to improve performance
                if len(batch) >= batch_size or (cursor == 0 and batch):
                    result = r.delete(*batch)
                    deleted += result
                    print(f"  Deleted {result} {pattern} keys")
                    batch = []
            
            print(f"  Cleaned up {pattern_deleted} {pattern} keys")
        
        elapsed = time.time() - start_time
        print(f"\n{GREEN}Cleanup completed in {elapsed:.2f} seconds{RESET}")
        print(f"{GREEN}Successfully deleted {deleted} total keys{RESET}")
        
        # Check final count
        final_count = r.dbsize()
        reduction = key_count - final_count
        percent = (reduction / key_count) * 100 if key_count > 0 else 0
        print(f"{GREEN}Database now contains {final_count} keys ({percent:.1f}% reduction){RESET}")
        
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 