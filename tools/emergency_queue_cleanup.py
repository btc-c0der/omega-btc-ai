#!/usr/bin/env python3

"""Emergency Redis Queue Cleanup
Dramatically reduces queue sizes that are causing memory issues
"""

import redis
import sys
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def emergency_cleanup():
    # Target the massive zset queue first
    zset_name = "rq:queue:mm_trap_queue:zset"
    current_size = r.zcard(zset_name)
    print(f"Cleaning {zset_name}: {current_size:,} items → 10,000 items")
    
    # Keep only the newest 10,000 items (highest scores)
    if current_size > 10000:
        to_remove = current_size - 10000
        # Remove in batches to avoid blocking Redis
        batch_size = 100000
        removed = 0
        
        start_time = time.time()
        while removed < to_remove:
            batch = min(batch_size, to_remove - removed)
            count = r.zremrangebyrank(zset_name, 0, batch - 1)
            removed += count
            percent = removed / to_remove * 100
            print(f"Progress: {percent:.1f}% - Removed {removed:,}/{to_remove:,}")
            time.sleep(0.1)  # Small pause to allow other Redis operations
            
        print(f"Finished in {time.time() - start_time:.1f}s")
        print(f"New size: {r.zcard(zset_name):,}")
    
    # Clean other zset
    zset_name = "mm_trap_queue:zset"
    current_size = r.zcard(zset_name)
    if current_size > 10000:
        print(f"Cleaning {zset_name}: {current_size:,} → 10,000 items")
        r.zremrangebyrank(zset_name, 0, current_size - 10001)
        print(f"New size: {r.zcard(zset_name):,}")
    
    # Clean list-based queues
    for queue_name in ["rq:queue:mm_trap_queue", "mm_trap_queue"]:
        current_size = r.llen(queue_name)
        if current_size > 5000:
            print(f"Cleaning {queue_name}: {current_size:,} → 5,000 items")
            r.ltrim(queue_name, -5000, -1)
            print(f"New size: {r.llen(queue_name):,}")
    
    print("\nFreeing memory...")
    r.config_set("maxmemory-policy", "allkeys-lru")
    r.memory_purge()  # Release memory back to OS
    
    # Get Redis memory info after cleanup
    info = r.info(section="memory")
    print(f"Redis memory now: {info.get('used_memory_human', 'unknown')}")

if __name__ == "__main__":
    print("WARNING: This will delete millions of queue items!")
    print("Press Ctrl+C within 5 seconds to cancel...")
    
    try:
        for i in range(5, 0, -1):
            sys.stdout.write(f"\rStarting in {i}...")
            sys.stdout.flush()
            time.sleep(1)
        print("\rExecuting cleanup...    ")
        
        emergency_cleanup()
        print("\n✅ Emergency cleanup complete")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)