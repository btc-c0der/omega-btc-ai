#!/usr/bin/env python3
"""
Redis Cleanup Utility

This script helps clean up Redis by:
1. Identifying key patterns and distributions
2. Safely removing temporary/queue keys
3. Preserving important data
"""

import redis
import sys
import time
import re
from collections import Counter
import argparse

# ANSI colors for output
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Patterns of keys that are safe to delete (regex)
SAFE_CLEANUP_PATTERNS = [
    r"^rq:job:.*",           # RQ job queues
    r"^rq:worker:.*",        # RQ worker registry
    r"^rq:workers.*",        # RQ worker lists
    r"^rq:failed:.*",        # Failed jobs
    r"^temporary:.*",        # Temporary data
    r"^cache:.*",            # Cache entries
    r".*:temp:.*",           # Temporary namespaced keys
]

# Keys that should always be preserved (exact matches)
PRESERVE_KEYS = [
    "current_trap_probability",
    "current_position",
    "last_btc_price",
    "btc_price",
]

def connect_to_redis():
    """Connect to Redis."""
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        # Test connection
        client.ping()
        print(f"{GREEN}✓ Connected to Redis{RESET}")
        return client
    except Exception as e:
        print(f"{RED}✗ Failed to connect to Redis: {e}{RESET}")
        return None

def analyze_keys(client):
    """Analyze Redis keys by patterns and types."""
    all_keys = list(client.keys("*"))
    if not all_keys:
        print(f"{YELLOW}No keys found in Redis{RESET}")
        return [], {}
    
    print(f"{GREEN}Found {len(all_keys)} keys in Redis{RESET}")
    
    # Analyze key types
    key_types = {}
    for key in all_keys:
        try:
            key_types[key] = client.type(key)
        except Exception:
            key_types[key] = "unknown"
    
    # Group by type
    type_counts = Counter(key_types.values())
    print(f"\n{CYAN}{BOLD}Key Types:{RESET}")
    for key_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {key_type}: {count} keys")
    
    # Look for patterns
    prefixes = []
    for key in all_keys:
        parts = key.split(":")
        if len(parts) > 1:
            prefixes.append(parts[0])
        else:
            prefixes.append("(no prefix)")
    
    prefix_counts = Counter(prefixes)
    print(f"\n{CYAN}{BOLD}Key Prefixes:{RESET}")
    for prefix, count in sorted(prefix_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {prefix}: {count} keys")
    
    return all_keys, key_types

def identify_cleanup_candidates(all_keys, key_types):
    """Identify keys that are candidates for cleanup."""
    # Match keys against cleanup patterns
    cleanup_candidates = set()
    for pattern in SAFE_CLEANUP_PATTERNS:
        for key in all_keys:
            if re.match(pattern, key) and key not in PRESERVE_KEYS:
                cleanup_candidates.add(key)
    
    # Categorize by type
    candidates_by_type = {}
    for key in cleanup_candidates:
        key_type = key_types.get(key, "unknown")
        if key_type not in candidates_by_type:
            candidates_by_type[key_type] = []
        candidates_by_type[key_type].append(key)
    
    # Print summary
    total = len(cleanup_candidates)
    if total > 0:
        print(f"\n{YELLOW}{BOLD}Found {total} keys that are candidates for cleanup:{RESET}")
        for key_type, keys in candidates_by_type.items():
            print(f"  • {key_type}: {len(keys)} keys")
        
        # Sample keys
        print(f"\n{CYAN}Sample cleanup candidates:{RESET}")
        for pattern in SAFE_CLEANUP_PATTERNS:
            matches = [k for k in cleanup_candidates if re.match(pattern, k)]
            if matches:
                print(f"  • Pattern '{pattern}': {min(len(matches), 3)} of {len(matches)} keys")
                for key in matches[:3]:
                    print(f"      - {key}")
    else:
        print(f"\n{GREEN}No cleanup candidates found{RESET}")
    
    return cleanup_candidates

def clean_keys(client, keys_to_clean, dry_run=True):
    """Clean up the specified keys."""
    if not keys_to_clean:
        print(f"{YELLOW}No keys to clean{RESET}")
        return 0
    
    total = len(keys_to_clean)
    
    if dry_run:
        print(f"\n{YELLOW}{BOLD}DRY RUN: Would delete {total} keys{RESET}")
        return 0
    
    # Group keys into batches for efficient deletion
    batch_size = 100
    batches = [list(keys_to_clean)[i:i+batch_size] for i in range(0, total, batch_size)]
    
    deleted = 0
    start_time = time.time()
    print(f"\n{MAGENTA}Deleting {total} keys in {len(batches)} batches...{RESET}")
    
    for i, batch in enumerate(batches, 1):
        try:
            result = client.delete(*batch)
            deleted += result
            if i % 10 == 0 or i == len(batches):
                print(f"  • Batch {i}/{len(batches)}: deleted {result} keys")
        except Exception as e:
            print(f"{RED}Error deleting batch {i}: {e}{RESET}")
    
    elapsed = time.time() - start_time
    print(f"\n{GREEN}Successfully deleted {deleted}/{total} keys in {elapsed:.2f} seconds{RESET}")
    return deleted

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Redis Cleanup Utility")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (don't actually delete)")
    parser.add_argument("--force", action="store_true", help="Force cleanup without asking for confirmation")
    args = parser.parse_args()
    
    print(f"\n{CYAN}{BOLD}===== REDIS CLEANUP UTILITY ====={RESET}")
    
    # Connect to Redis
    client = connect_to_redis()
    if not client:
        sys.exit(1)
    
    # Analyze keys
    all_keys, key_types = analyze_keys(client)
    if not all_keys:
        print(f"{YELLOW}No cleanup needed{RESET}")
        sys.exit(0)
    
    # Identify cleanup candidates
    cleanup_candidates = identify_cleanup_candidates(all_keys, key_types)
    
    # Confirm cleanup
    if cleanup_candidates and not args.dry_run and not args.force:
        confirm = input(f"\n{YELLOW}Confirm deletion of {len(cleanup_candidates)} keys? (y/N): {RESET}")
        if confirm.lower() != 'y':
            print(f"{YELLOW}Cleanup aborted{RESET}")
            sys.exit(0)
    
    # Clean keys
    cleaned = clean_keys(client, cleanup_candidates, args.dry_run)
    
    # Show final stats
    print(f"\n{CYAN}{BOLD}Cleanup Summary:{RESET}")
    print(f"  • Total Redis keys: {len(all_keys)}")
    print(f"  • Keys marked for cleanup: {len(cleanup_candidates)}")
    if args.dry_run:
        print(f"  • Keys cleaned: 0 (dry run)")
    else:
        print(f"  • Keys cleaned: {cleaned}")
        
        # Get final count
        final_count = len(client.keys("*"))
        print(f"  • Remaining keys: {final_count}")
    
    print(f"\n{GREEN}{BOLD}Cleanup finished!{RESET}")

if __name__ == "__main__":
    main() 