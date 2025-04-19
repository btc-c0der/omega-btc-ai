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
Redis Organic Move Cleanup

This script cleans up the organic_move:* keys in Redis which can accumulate
and impact Redis performance over time. By default, it runs in dry-run mode.
"""

import redis
import logging
import argparse
import time
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("redis-cleanup")

def connect_to_redis():
    """Connect to Redis server."""
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        client.ping()
        logger.info("✅ Connected to Redis")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {e}")
        return None

def count_organic_move_keys(client):
    """Count the total number of organic_move keys."""
    cursor = 0
    count = 0
    
    logger.info("Counting organic_move keys...")
    start_time = time.time()
    
    while True:
        cursor, keys = client.scan(cursor=cursor, match="organic_move:*", count=1000)
        count += len(keys)
        
        if cursor == 0:
            break
            
        # Progress update every 10,000 keys
        if count % 10000 == 0:
            logger.info(f"Found {count} keys so far...")
            
    elapsed = time.time() - start_time
    logger.info(f"Found {count} organic_move keys in {elapsed:.2f} seconds")
    return count

def clean_organic_move_keys(client, keep=1000, batch_size=1000, dry_run=True):
    """
    Clean organic_move keys, keeping only the most recent ones.
    
    Args:
        client: Redis client
        keep: Number of most recent keys to keep
        batch_size: Number of keys to delete in each batch
        dry_run: If True, don't actually delete anything
    
    Returns:
        Number of keys that were or would be deleted
    """
    # Get all organic_move keys
    all_keys = []
    cursor = 0
    
    logger.info("Scanning for organic_move keys...")
    while True:
        cursor, keys = client.scan(cursor=cursor, match="organic_move:*", count=batch_size)
        all_keys.extend(keys)
        
        if cursor == 0:
            break
            
        # Progress update for large datasets
        if len(all_keys) % 10000 == 0:
            logger.info(f"Scanned {len(all_keys)} keys so far...")
    
    logger.info(f"Found {len(all_keys)} organic_move keys")
    
    # If we want to keep all keys or there are fewer keys than the keep limit
    if keep >= len(all_keys):
        logger.info(f"No keys need to be deleted - {len(all_keys)} keys is below the keep threshold of {keep}")
        return 0
    
    # Sort keys by timestamp (assuming timestamp is part of the key after the colon)
    sorted_keys = sorted(all_keys, key=lambda k: int(k.split(':')[1]), reverse=True)
    
    # Keep the most recent ones
    keys_to_keep = sorted_keys[:keep]
    keys_to_delete = sorted_keys[keep:]
    
    logger.info(f"Keeping {len(keys_to_keep)} most recent keys")
    logger.info(f"Preparing to delete {len(keys_to_delete)} older keys")
    
    if dry_run:
        logger.warning("DRY RUN - No keys will be deleted")
        if len(keys_to_delete) > 0:
            logger.info(f"Would delete keys from {keys_to_delete[-1]} to {keys_to_delete[0]}")
        return len(keys_to_delete)
    
    # Delete keys in batches
    total_deleted = 0
    for i in range(0, len(keys_to_delete), batch_size):
        batch = keys_to_delete[i:i+batch_size]
        if batch:
            deleted = client.delete(*batch)
            total_deleted += deleted
            logger.info(f"Deleted batch of {deleted} keys ({total_deleted}/{len(keys_to_delete)} total)")
            
            # Small delay to reduce impact on Redis
            time.sleep(0.1)
    
    logger.info(f"✅ Cleanup complete - deleted {total_deleted} keys")
    return total_deleted

def main():
    parser = argparse.ArgumentParser(description="Clean up organic_move keys in Redis")
    parser.add_argument("--keep", type=int, default=1000, 
                        help="Number of most recent keys to keep (default: 1000)")
    parser.add_argument("--batch-size", type=int, default=1000, 
                        help="Number of keys to delete in each batch (default: 1000)")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Don't actually delete anything, just report what would be deleted")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    logger.info("Redis Organic Move Cleanup")
    logger.info(f"Keep: {args.keep} keys, Batch size: {args.batch_size}, Dry run: {args.dry_run}")
    
    # Connect to Redis
    client = connect_to_redis()
    if not client:
        logger.error("Failed to connect to Redis. Exiting.")
        return 1
    
    # Get the total number of organic_move keys
    total_keys = count_organic_move_keys(client)
    
    # If we don't need to delete anything
    if total_keys <= args.keep:
        logger.info(f"No cleanup needed. Found {total_keys} keys, keeping {args.keep}.")
        return 0
    
    # If not dry run and not force, ask for confirmation
    if not args.dry_run and not args.force:
        to_delete = total_keys - args.keep
        confirm = input(f"Will delete {to_delete} keys out of {total_keys}. Continue? [y/N] ")
        if confirm.lower() != 'y':
            logger.info("Aborted by user.")
            return 0
    
    # Perform the cleanup
    deleted = clean_organic_move_keys(
        client, 
        keep=args.keep, 
        batch_size=args.batch_size, 
        dry_run=args.dry_run
    )
    
    if args.dry_run:
        logger.info(f"DRY RUN - Would delete {deleted} keys, keeping {args.keep}")
    else:
        logger.info(f"Deleted {deleted} keys, kept {args.keep}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 