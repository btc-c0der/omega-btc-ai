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
Queue Migration Tool - Convert list-based queues to more efficient sorted sets
"""

import redis
import time
import sys

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def migrate_list_to_zset(queue_name):
    """Migrate a list-based queue to a sorted set for better performance"""
    print(f"Starting migration of {queue_name} to sorted set...")
    
    # Create new sorted set name
    new_queue_name = f"{queue_name}:zset"
    
    # Check if queue exists and is a list
    if r.type(queue_name).decode('utf-8') != 'list':
        print(f"Error: {queue_name} is not a list")
        return False
    
    # Get queue length
    length = r.llen(queue_name)
    print(f"Found {length} items to migrate")
    
    # For very large queues, process in batches
    batch_size = 10000
    batches = (length // batch_size) + (1 if length % batch_size else 0)
    
    # Set up counters
    migrated = 0
    errors = 0
    start_time = time.time()
    
    # Process in batches
    for batch in range(batches):
        start = batch * batch_size
        end = min((batch + 1) * batch_size - 1, length - 1)
        
        # Get batch of items
        items = r.lrange(queue_name, start, end)
        
        # Add to sorted set with scores being timestamps
        pipe = r.pipeline()
        current_time = time.time()
        
        for i, item in enumerate(items):
            # Use incrementing time to maintain order
            score = current_time + (i / 1000000)
            try:
                pipe.zadd(new_queue_name, {item: score})
                migrated += 1
            except Exception as e:
                errors += 1
                print(f"Error migrating item: {e}")
        
        # Execute batch
        pipe.execute()
        
        # Update progress
        percent = (batch + 1) / batches * 100
        elapsed = time.time() - start_time
        remaining = (elapsed / (batch + 1)) * (batches - batch - 1)
        print(f"Progress: {percent:.1f}% - {migrated} items - ETA: {remaining:.1f}s")
    
    print(f"\nMigration complete!")
    print(f"- Original queue: {length} items")
    print(f"- New sorted set: {r.zcard(new_queue_name)} items")
    print(f"- Time taken: {time.time() - start_time:.2f}s")
    print(f"- Success rate: {migrated}/{length} ({migrated/length*100:.1f}%)")
    
    return True

def truncate_large_queue(queue_name, keep_count=100000):
    """Truncate a large queue while keeping the newest entries"""
    if r.type(queue_name).decode('utf-8') == 'list':
        length = r.llen(queue_name)
        if length > keep_count:
            # Keep the newest items (right side of the list)
            trim_count = length - keep_count
            print(f"Trimming {trim_count} old entries from {queue_name}")
            r.ltrim(queue_name, trim_count, -1)
            print(f"Queue now has {r.llen(queue_name)} items")
    elif r.type(queue_name).decode('utf-8') == 'zset':
        length = r.zcard(queue_name)
        if length > keep_count:
            # Remove oldest entries (lowest scores)
            trim_count = length - keep_count
            print(f"Trimming {trim_count} old entries from {queue_name}")
            r.zremrangebyrank(queue_name, 0, trim_count - 1)
            print(f"Queue now has {r.zcard(queue_name)} items")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--truncate":
        # Just truncate the large queues
        truncate_large_queue("rq:queue:mm_trap_queue", 50000)
        truncate_large_queue("mm_trap_queue", 50000)
        sys.exit(0)
    
    # Migrate and optimize queues
    migrate_list_to_zset("rq:queue:mm_trap_queue")
    migrate_list_to_zset("mm_trap_queue")