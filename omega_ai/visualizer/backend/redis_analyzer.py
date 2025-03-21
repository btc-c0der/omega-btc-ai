#!/usr/bin/env python
import redis
import sys
import time
import re
from collections import Counter, defaultdict

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
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

def analyze_key_patterns(client, sample_size=1000):
    """Analyze key patterns to find common prefixes and structures"""
    print(f"{BOLD}===== REDIS KEY PATTERN ANALYZER ====={RESET}")
    print(f"Connecting to Redis...")
    print(f"{GREEN}✓ Connected to Redis{RESET}")
    
    # Get total key count
    total_keys = client.dbsize()
    print(f"Database contains {BOLD}{total_keys}{RESET} keys")
    
    # Sample keys for pattern analysis
    cursor = "0"
    keys = []
    
    print(f"Sampling keys for pattern analysis...")
    while cursor != 0 and len(keys) < sample_size:
        cursor, batch = client.scan(cursor=int(cursor), count=sample_size)
        keys.extend(batch[:sample_size - len(keys)])  # Limit to sample size
        
        # Break if we've iterated through all keys
        if cursor == 0 or cursor == "0":
            break
    
    print(f"Collected {len(keys)} keys for analysis")
    
    # Analyze patterns
    prefixes = Counter()
    type_counts = Counter()
    key_lengths = []
    pattern_groups = defaultdict(list)
    namespaces = Counter()
    
    print(f"Analyzing key patterns...")
    
    # Extract prefixes and count types
    for key in keys:
        key_str = key.decode('utf-8', errors='replace')
        
        # Get type and size
        key_type = client.type(key).decode('utf-8')
        type_counts[key_type] += 1
        
        # Add key length
        key_lengths.append(len(key_str))
        
        # Extract prefix (characters before first :)
        prefix = key_str.split(':', 1)[0] if ':' in key_str else key_str
        prefixes[prefix] += 1
        
        # Extract namespace (first two components if : separated)
        namespace_parts = key_str.split(':')
        if len(namespace_parts) >= 2:
            namespace = ':'.join(namespace_parts[:2])
            namespaces[namespace] += 1
        
        # Group by pattern (replace digits with #, letters with ?)
        pattern = re.sub(r'[0-9]+', '#', key_str)
        pattern = re.sub(r'[a-zA-Z]+', '?', pattern)
        pattern_groups[pattern].append(key_str)
    
    # Print analysis results
    print(f"\n{BOLD}{BLUE}=== Key Type Distribution ==={RESET}")
    for type_name, count in type_counts.most_common():
        percentage = (count / len(keys)) * 100
        print(f"{type_name}: {count} keys ({percentage:.1f}%)")
    
    print(f"\n{BOLD}{BLUE}=== Top Key Prefixes ==={RESET}")
    for prefix, count in prefixes.most_common(10):
        percentage = (count / len(keys)) * 100
        print(f"{prefix}: {count} keys ({percentage:.1f}%)")
    
    print(f"\n{BOLD}{BLUE}=== Top Namespaces ==={RESET}")
    for namespace, count in namespaces.most_common(10):
        percentage = (count / len(keys)) * 100
        print(f"{namespace}: {count} keys ({percentage:.1f}%)")
    
    print(f"\n{BOLD}{BLUE}=== Key Length Statistics ==={RESET}")
    avg_length = sum(key_lengths) / len(key_lengths) if key_lengths else 0
    print(f"Average key length: {avg_length:.1f} characters")
    print(f"Min key length: {min(key_lengths) if key_lengths else 0} characters")
    print(f"Max key length: {max(key_lengths) if key_lengths else 0} characters")
    
    print(f"\n{BOLD}{BLUE}=== Most Common Key Patterns ==={RESET}")
    for i, (pattern, keys_with_pattern) in enumerate(sorted(pattern_groups.items(), key=lambda x: len(x[1]), reverse=True)[:10]):
        percentage = (len(keys_with_pattern) / len(keys)) * 100
        print(f"{i+1}. Pattern: {pattern}")
        print(f"   Count: {len(keys_with_pattern)} keys ({percentage:.1f}%)")
        print(f"   Example: {keys_with_pattern[0]}")
    
    # Suggest cleanup patterns
    print(f"\n{BOLD}{MAGENTA}=== Suggested Cleanup Patterns ==={RESET}")
    for prefix, count in prefixes.most_common(5):
        if count > len(keys) * 0.05:  # If prefix represents over 5% of keys
            print(f"{prefix}:* - {count} keys ({(count / len(keys)) * 100:.1f}%)")
    
    for namespace, count in namespaces.most_common(5):
        if count > len(keys) * 0.05 and namespace not in [p + ':*' for p in prefixes]:
            print(f"{namespace}:* - {count} keys ({(count / len(keys)) * 100:.1f}%)")

def main():
    # Connect to Redis
    client = connect_to_redis()
    
    # Analyze Redis keys
    analyze_key_patterns(client)
    
if __name__ == "__main__":
    main() 