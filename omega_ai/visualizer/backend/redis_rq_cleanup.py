#!/usr/bin/env python
import redis
import sys
import time
import argparse

# ANSI colors for console output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def connect_to_redis():
    """Connect to Redis and check connection."""
    try:
        client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        client.ping()  # Check if connection is alive
        print(f"{GREEN}✓ Connected to Redis{RESET}")
        return client
    except redis.exceptions.ConnectionError:
        print(f"{RED}✘ Redis connection failed{RESET}")
        sys.exit(1)

def cleanup_rq_jobs(client, dry_run=True, batch_size=5000):
    """Clean up Redis Queue job keys efficiently."""
    print(f"\n{BLUE}Cleaning up Redis Queue job keys...{RESET}")
    
    initial_count = client.dbsize()
    print(f"Initial key count: {initial_count}")
    
    # Pattern for RQ jobs
    pattern = "rq:job:*"
    
    # Counters
    deleted = 0
    total_scanned = 0
    batch = []
    
    if dry_run:
        print(f"{YELLOW}Running in DRY RUN mode - no keys will be deleted{RESET}")
    
    print(f"Scanning for Redis Queue job keys (pattern: {pattern})...")
    start_time = time.time()
    
    # First scan to count job keys
    job_count = 0
    cursor = 0
    while cursor != 0 or job_count == 0:
        cursor, keys = client.scan(cursor=cursor, match=pattern, count=1000)
        job_count += len(keys)
        total_scanned += len(keys)
        
        if total_scanned % 10000 == 0:
            print(f"  Scanned {total_scanned} keys so far, found {job_count} job keys...")
            
        # Limit scan to protect performance
        if total_scanned >= 100000 and job_count > 0:
            print(f"{YELLOW}Limiting scan to {total_scanned} keys for performance reasons{RESET}")
            break
    
    print(f"Found approximately {job_count} job keys")
    
    if job_count == 0:
        print(f"{GREEN}No job keys to clean up!{RESET}")
        return
    
    # Reset for actual cleanup
    cursor = 0
    total_scanned = 0
    
    # Ask for confirmation if not in dry run mode
    if not dry_run:
        confirmation = input(f"{YELLOW}About to delete approximately {job_count} Redis job keys. Proceed? (y/n) {RESET}")
        if confirmation.lower() != 'y':
            print("Cleanup cancelled.")
            return
    
    # Perform cleanup
    print(f"{'Simulating' if dry_run else 'Performing'} deletion of job keys in batches of {batch_size}...")
    
    while cursor != 0 or total_scanned == 0:
        cursor, keys = client.scan(cursor=cursor, match=pattern, count=batch_size)
        if keys:
            batch.extend(keys)
            total_scanned += len(keys)
        
        # Delete in batches to improve performance
        if len(batch) >= batch_size or (cursor == 0 and batch):
            if not dry_run:
                result = client.delete(*batch)
                deleted += result
                print(f"  Deleted batch of {result} keys, total: {deleted}")
            else:
                print(f"  [DRY RUN] Would delete batch of {len(batch)} keys")
                deleted += len(batch)
            
            batch = []
        
        # Progress update
        if total_scanned % 50000 == 0:
            elapsed = time.time() - start_time
            rate = total_scanned / elapsed if elapsed > 0 else 0
            print(f"  Progress: {total_scanned} keys processed in {elapsed:.2f}s ({rate:.2f} keys/sec)")
            
            # Calculate ETA
            if job_count > total_scanned and rate > 0:
                eta = (job_count - total_scanned) / rate
                print(f"  ETA: {eta:.2f} seconds remaining")
    
    elapsed = time.time() - start_time
    
    print(f"\n{GREEN}{'Simulated' if dry_run else 'Completed'} cleanup in {elapsed:.2f} seconds{RESET}")
    print(f"{'Would have deleted' if dry_run else 'Deleted'} {deleted} RQ job keys")
    
    if not dry_run:
        final_count = client.dbsize()
        reduction = initial_count - final_count
        reduction_percent = (reduction / initial_count) * 100 if initial_count > 0 else 0
        
        print(f"Initial key count: {initial_count}")
        print(f"Final key count: {final_count}")
        print(f"Reduction: {reduction} keys ({reduction_percent:.2f}%)")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Clean up Redis Queue job keys")
    parser.add_argument("--dry-run", action="store_true", help="Simulate cleanup without deleting keys")
    parser.add_argument("--batch-size", type=int, default=5000, help="Batch size for deletion")
    args = parser.parse_args()
    
    print(f"{BLUE}===== REDIS RQ JOB CLEANUP ====={RESET}")
    
    client = connect_to_redis()
    cleanup_rq_jobs(client, dry_run=args.dry_run, batch_size=args.batch_size)

if __name__ == "__main__":
    main() 