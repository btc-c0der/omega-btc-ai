#!/usr/bin/env python3

"""
Queue Health Check Script
Monitors and reports on Redis queue health
"""

import redis
import time
import datetime
import psutil
import os
import argparse

# Colors for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def check_queue_health():
    """Check the health of all Redis queues"""
    # Get system memory stats
    mem = psutil.virtual_memory()
    
    print(f"{BLUE}=== Redis Queue Health Check ==={RESET}")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System Memory: {mem.percent}% used ({mem.used / 1024 / 1024 / 1024:.1f} GB of {mem.total / 1024 / 1024 / 1024:.1f} GB)")
    
    # Get Redis memory usage
    info = r.info(section="memory")
    redis_mem = info.get("used_memory", 0)
    redis_mem_human = info.get("used_memory_human", "0B")
    redis_peak = info.get("used_memory_peak_human", "0B")
    
    print(f"Redis Memory: {redis_mem_human} (Peak: {redis_peak})")
    
    # Check for list-based queues
    list_queues = [k.decode('utf-8') for k in r.keys("*queue*") if r.type(k).decode('utf-8') == 'list']
    if list_queues:
        print(f"\n{YELLOW}List-based Queues:{RESET}")
        for queue in list_queues:
            length = r.llen(queue)
            status = f"{GREEN}OK{RESET}" if length < 1000 else f"{YELLOW}WARNING{RESET}" if length < 10000 else f"{RED}CRITICAL{RESET}"
            print(f"  {queue}: {length} items - Status: {status}")
    
    # Check for sorted set queues
    zset_queues = [k.decode('utf-8') for k in r.keys("*queue*:zset") if r.type(k).decode('utf-8') == 'zset']
    if zset_queues:
        print(f"\n{BLUE}Sorted Set Queues:{RESET}")
        for queue in zset_queues:
            length = r.zcard(queue)
            status = f"{GREEN}OK{RESET}" if length < 10000 else f"{YELLOW}WARNING{RESET}" if length < 100000 else f"{RED}CRITICAL{RESET}"
            print(f"  {queue}: {length} items - Status: {status}")
            
            # For very large queues, show age of oldest item
            if length > 10000:
                oldest = r.zrange(queue, 0, 0, withscores=True)
                if oldest:
                    oldest_score = oldest[0][1]
                    age_seconds = time.time() - oldest_score
                    age_hours = age_seconds / 3600
                    age_status = f"{GREEN}OK{RESET}" if age_hours < 1 else f"{YELLOW}WARNING{RESET}" if age_hours < 24 else f"{RED}CRITICAL{RESET}"
                    print(f"    Oldest item: {age_hours:.1f} hours old - Status: {age_status}")
    
    # Check for other potential queue systems
    rq_queues = [k.decode('utf-8') for k in r.keys("rq:queue:*") if r.type(k).decode('utf-8') == 'list']
    if rq_queues:
        print(f"\n{BLUE}RQ Queues:{RESET}")
        for queue in rq_queues:
            length = r.llen(queue)
            status = f"{GREEN}OK{RESET}" if length < 1000 else f"{YELLOW}WARNING{RESET}" if length < 10000 else f"{RED}CRITICAL{RESET}"
            print(f"  {queue}: {length} items - Status: {status}")
    
    # Check for Redis workers
    workers = r.smembers("rq:workers")
    if workers:
        print(f"\n{BLUE}RQ Workers ({len(workers)}):{RESET}")
        for worker in workers:
            worker_name = worker.decode('utf-8')
            state = r.get(f"rq:worker:{worker_name}")
            state_str = state.decode('utf-8') if state else "Unknown"
            print(f"  {worker_name}: {state_str}")
    
    # Check Redis client connections
    clients = r.client_list()
    print(f"\n{BLUE}Redis Clients ({len(clients)}):{RESET}")
    print(f"  Active connections: {len(clients)}")
    
    # Redis server load
    ops = info.get("instantaneous_ops_per_sec", 0)
    print(f"  Operations per second: {ops}")
    
    # Recommendations
    print(f"\n{YELLOW}Recommendations:{RESET}")
    if len(list_queues) > 0:
        print(f"  - Migrate list-based queues to sorted sets for better performance")
    
    large_queues = sum(1 for q in list_queues if r.llen(q) > 10000) + sum(1 for q in zset_queues if r.zcard(q) > 100000)
    if large_queues > 0:
        print(f"  - {large_queues} queues have excessive items. Run cleanup script.")
    
    if mem.percent > 80:
        print(f"  - {RED}System memory usage critical ({mem.percent}%){RESET}. Free up memory.")
    
    if float(redis_mem) / mem.total > 0.5:
        print(f"  - {RED}Redis using over 50% of system memory{RESET}. Adjust maxmemory setting.")

def clean_old_queue_items():
    """Clean up old items from queues"""
    # Find zset queues
    zset_queues = [k.decode('utf-8') for k in r.keys("*queue*:zset") if r.type(k).decode('utf-8') == 'zset']
    
    for queue in zset_queues:
        length = r.zcard(queue)
        if length > 50000:
            # Keep only newest 50000 items
            print(f"Cleaning {queue}: {length} items -> 50000 items")
            r.zremrangebyrank(queue, 0, length - 50001)
    
    # Find list queues that are too large
    list_queues = [k.decode('utf-8') for k in r.keys("*queue*") if r.type(k).decode('utf-8') == 'list']
    
    for queue in list_queues:
        length = r.llen(queue)
        if length > 10000:
            # Keep only newest 10000 items
            print(f"Cleaning {queue}: {length} items -> 10000 items")
            r.ltrim(queue, -10000, -1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redis Queue Health Check")
    parser.add_argument("--clean", action="store_true", help="Clean old items from queues")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_old_queue_items()
    else:
        check_queue_health()