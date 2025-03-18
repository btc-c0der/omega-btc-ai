#!/usr/bin/env python3

"""
Redis Queue Optimization Tool
- Analyzes and optimizes your Redis queue structures
"""

import redis
import json
import sys

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def optimize_queue_keys():
    """Analyze and optimize queue structures."""
    # Find all list-based queue keys
    queue_keys = [k.decode('utf-8') for k in r.keys("*queue*") if r.type(k).decode('utf-8') == 'list']
    
    print(f"Found {len(queue_keys)} list-based queue keys")
    
    for queue in queue_keys:
        # Get queue length
        length = r.llen(queue)
        
        # Analyze memory usage
        mem_usage = r.memory_usage(queue)
        
        print(f"\nQueue: {queue}")
        print(f"  Length: {length}")
        print(f"  Memory: {mem_usage/1024/1024:.2f} MB")
        
        # Check for large items
        if length > 0:
            # Sample a few items to check size
            samples = min(5, length)
            total_size = 0
            largest_item = (0, None)
            
            for i in range(samples):
                item = r.lindex(queue, -i-1)
                item_size = len(item) if item else 0
                total_size += item_size
                
                if item_size > largest_item[0]:
                    largest_item = (item_size, item)
            
            avg_size = total_size / samples
            print(f"  Avg item size: {avg_size:.2f} bytes")
            
            if avg_size > 10000:  # 10KB
                print(f"  ⚠️ Large item detected: {largest_item[0]} bytes")
                print("  Recommendation: Consider compressing queue items")
            
            # Check if sorted set would be more efficient
            if length > 100 and r.llen(queue) > 100:
                print("  Recommendation: Consider using sorted set instead of list for better performance")

if __name__ == "__main__":
    optimize_queue_keys()